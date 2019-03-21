import os
from io import StringIO

import h5py
import numpy as np
from typing import List, Dict, Any


def get_file_attributes(filename):
    # type: (str) -> Dict[str, Any]
    """
    Get a list of the attributes of the file and their values. Will convert to str from bytes in python3
    :param filename:
    :return:
    """
    with h5py.File(filename, 'r') as infile:
        return {key: (value.decode('UTF-8') if isinstance(value, bytes) and str is not bytes else value)
                for key, value in infile.attrs.items()}


def get_file_attribute_dtypes(filename):
    # type: (str) -> Dict[str, str]
    """
    Get the dtypes of the attributes of the file
    :param filename:
    :return:
    """
    with h5py.File(filename, 'r') as infile:
        return {key: type(value).__name__ for key, value in infile.attrs.items()}


def get_collection_metadata(filename):
    # type: (str) -> Dict[str, Any]
    """
    Get attributes of a hdf5 file, its last modified date, and the sizes of its largest datasets
    :param filename:
    :return:
    """
    with h5py.File(filename, 'r') as infile:
        attrs = {key: (value.decode('UTF-8') if isinstance(value, bytes) and str is not bytes else value)
                 for key, value in infile.attrs.items()}
    attrs['date_modified'] = int(os.path.getmtime(filename))
    dims = approximate_dims(filename)
    attrs['max_row_count'] = dims[0]
    attrs['max_col_count'] = dims[1]
    return {key: (value.item() if hasattr(value, 'item') else value) for (key, value) in attrs.items()}


def get_collection_info(filename):
    # type: (str) -> Dict[str, Any]
    """
    Get the metadata and paths of an hdf5 file
    :param filename:
    :return:
    """
    with h5py.File(filename, 'r') as infile:
        collection_info = get_group_info(infile)
    collection_info.update(collection_info['attrs'])
    del collection_info['attrs']
    collection_info['date_modified'] = int(os.path.getmtime(filename))
    dims = approximate_dims(filename)
    collection_info['max_row_count'] = dims[0]
    collection_info['max_col_count'] = dims[1]
    return {key: (value.item() if hasattr(value, 'item') else value) for (key, value) in collection_info.items()}


def get_dataset_paths(filename):
    # type: (str) -> List[str]
    """
    Get all the paths pointing to objects of type h5py.Dataset in this file.
    :param filename:
    :return:
    """
    paths = []
    with h5py.File(filename, 'r') as infile:
        iterate_dataset_paths(infile, paths)
    return paths


#  Can raise exceptions!
def get_csv(filename, path):
    # type: (str, str) -> str
    """
    Get a string containing comma-separated values for a dataset
    :param filename:
    :param path:
    :return:
    """
    """Get a string containing comma-separated values for a dataset"""
    with h5py.File(filename, 'r') as infile:
        dataset = infile[str(path)].value
    s = StringIO()
    if dataset is not None:
        for row in dataset:
            s.write(convert_row(row))
            s.write('\n')
        csv = s.getvalue()
        return csv.encode('ascii') if str is bytes else csv
    raise ValueError('File or path not found')


def convert_row(row):
    # type: (np.array) -> str
    """
    Get a csv representation of a row of a dataset.
    :param row:
    :return:
    """
    if isinstance(row, bytes):
        return row.decode('ascii') if str is not bytes else row
    else:
        return ','.join([convert_cell(cell) for cell in row])


def convert_cell(cell):
    # type: (Any) -> str
    """
    Convert an array cell to utf-8 string on python3 or ascii bytes on python2
    :param cell:
    :return:
    """
    return cell.decode('ascii') if isinstance(cell, bytes) and str is not bytes else str(cell)


def iterate_dataset_paths(group, paths):
    # type: (h5py.Group, List) -> None
    """
    Recursively touch every path in the group.
    :param group:
    :param paths:
    :return:
    """
    [iterate_dataset_paths(group[key], paths) for key in group.keys() if isinstance(group[key], h5py.Group)]
    paths.extend([get_dataset_info(group[key]) for key in group.keys() if isinstance(group[key], h5py.Dataset)])


def get_group_info(group):
    # type: (h5py.Group) -> Dict[str, Any]
    """Get the path, attributes, child groups and child datasets of a group"""
    return {
        'path': group.name,
        'attrs': {key: (value.decode('UTF-8') if isinstance(value, bytes) and str is not bytes else value)
                  for key, value in group.attrs.items()},
        'groups': [get_group_info(group[key]) for key in group.keys() if isinstance(group[key], h5py.Group)],
        'datasets': [get_dataset_info(group[key]) for key in group.keys() if isinstance(group[key], h5py.Dataset)]
    }


def get_dataset_info(dataset):
    # type: (h5py.Dataset) -> Dict[str, Any]
    """
    Get the dimensions, data type and attributes of a dataset
    :param dataset:
    :return:
    """
    """Get the dimensions, data type and attributes of a dataset"""
    rows = 0
    cols = 0
    if len(dataset.shape) == 1:
        rows = dataset.shape[0]
        cols = 1
    if len(dataset.shape) > 1:
        rows = dataset.shape[0]
        cols = dataset.shape[1]
    return {
        'path': dataset.name,
        'attrs': {key: (value.decode('UTF-8') if isinstance(value, bytes) and str is not bytes else value)
                  for key, value in dataset.attrs.items()},
        'rows': rows,
        'cols': cols,
        'dtype': str(dataset.dtype)
    }


def get_all_dataset_info(filename):
    # type: (str) -> List[Dict[str, Any]]
    """
    Get the information for all the datasets in the file
    :param filename:
    :return:
    """
    with h5py.File(filename, 'r') as fp:
        return [get_dataset_info(dataset) for dataset in get_datasets(fp)]


def update_metadata(filename, new_data):
    # type: (str, Dict[str, Any]) -> Dict[str, Any]
    """
    Update the attributes of a file from a dictionary.
    :param filename:
    :param new_data:
    :return:
    """
    with h5py.File(filename, 'r+') as fp:
        fp.attrs.update(new_data)
    return get_collection_info(filename)


def create_empty_file(filename, new_data):
    # type: (str, Dict[str, Any]) -> Dict[str, Any]
    """
    Create an empty hdf5 file.
    :param filename:
    :param new_data:
    :return:
    """
    with h5py.File(filename, 'w') as fp:
        fp.attrs.update(new_data)
    return get_collection_info(filename)


def approximate_dims(filename):
    # type: (str) -> (int, int)
    """
    Return a (m, n) pair where m is the longest row count and n is longest col count of all datasets
    :param filename:
    :return:
    """
    with h5py.File(filename, 'r') as fp:
        try:
            m = max([dataset.shape[0] for dataset in get_datasets(fp)])
            n = max([dataset.shape[1] if len(dataset.shape) > 1 else 1 for dataset in get_datasets(fp)])
            return m, n
        except ValueError:
            return 0, 0


def get_datasets(fp):
    # type: (h5py.File) -> List[h5py.Dataset]
    """
    Get all the datasets in this file
    :param fp:
    :return:
    """
    return [fp[key] for key in fp.keys() if isinstance(fp[key], h5py.Dataset)]


def add_column(filename, name, data_type='string'):
    # type: (str, str, str) -> None
    """
    Add an empty column of data_type 'int' (numpy.int64), 'float' (numpy.float64) or 'string' (numpy.string_)
    to the file.
    :param filename:
    :param name:
    :param data_type:
    :return:
    """
    m, _ = approximate_dims(filename)
    with h5py.File(filename, 'r+') as fp:
        if data_type == 'integer':
            fp.create_dataset(name, shape=(m, 1), dtype=np.int64)
        elif data_type == 'float':
            fp.create_dataset(name, shape=(m, 1), dtype=np.float64)
        elif data_type == 'string':
            fp.create_dataset(name, shape=(m, 1), dtype=h5py.special_dtype(vlen=bytes))
        else:
            raise ValueError('Improper data_type {}'.format(data_type))
