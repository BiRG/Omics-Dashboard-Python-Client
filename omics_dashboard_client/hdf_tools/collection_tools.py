import h5py
import numpy as np
import pandas as pd
from typing import Any, List


def get_dataframe(filename, row_index_key='base_sample_id', keys=None):
    # type: (str, str, List[str]) -> pd.DataFrame
    """
    Get a Pandas DataFrame from an hdf5 file
    :param filename:
    :param row_index_key: Key of a label row to use as the row index
    :param keys: Keys to construct dataframe from. Should all have the same number of rows. If none, will use columns of '/Y'.
    :return:
    """
    with h5py.File(filename, 'r') as fp:
        if 'Y' not in fp and not keys:
            raise ValueError('No \'Y\' dataset in file and no other keys specified.')
        if keys:
            row_count = fp[keys[0]].shape[0]
        else:
            row_count = fp['Y'].shape[0]
            keys = [key for key in fp.keys() if (fp[key].shape[0] == row_count)]
        index = np.asarray(fp[row_index_key]).flatten() if row_index_key in fp else [i for i in range(0, row_count)]
        df = pd.DataFrame(index=index)
        for key in keys:
            if key in {'Y', '/Y'}:
                columns = ['Y_{}'.format(x_i) for x_i in np.asarray(fp['x']).flatten().tolist()] \
                    if 'x' in fp else [i + 1 for i in range(0, fp['Y'].shape[1])]
            else:
                column_count = fp[key].shape[1] if len(fp[key].shape) > 1 else 1
                columns = ['{}_{}'.format(key, i + 1) for i in range(0, fp[key].shape[1])] if column_count > 1 else [
                    key]
            new_df = pd.DataFrame(columns=columns, data=np.asarray(fp[key]), index=index)
            df = pd.concat((df, new_df), axis=1)
        df.index.name = row_index_key if row_index_key is not None else 'id'
        return df


def update_array(filename, path, i, j, val):
    # type: (str, str, int, int, Any) -> None
    """
    Change the value of the array in the file at (i, j)
    :param filename:
    :param path:
    :param i:
    :param j:
    :param val:
    :return:
    """
    i = 0 if i is None else i
    j = 0 if j is None else j
    with h5py.File(filename, 'r+') as file:
        print('file opened')
        val = file[path].dtype.type(val)
        print(val)
        if len(file[path].shape) == 1:
            file[path][int(i)] = val
        else:
            file[path][int(i), int(j)] = val


def validate_update(filename, path, i, j, val):
    # type: (str, str, int, int, Any) -> Any
    """
    Raise an exception if the types of val and the array at path do not agree, or if i or j are out of range.
    If this raises an exception, so will update_array.
    :param filename:
    :param path:
    :param i:
    :param j:
    :param val:
    :return:
    """
    i = 0 if i is None else i
    j = 0 if j is None else j
    with h5py.File(filename, 'r') as fp:
        fp[path].dtype.type(val)  # throw ValueError if can't convert to dtype, KeyError if path not in file
        if len(fp[path].shape) == 1:
            current_val = fp[path][int(i)]  # throw ValueError if i out of range
        else:
            current_val = fp[path][int(i), int(j)]  # throw ValueError if i or j out of range
    return current_val


def get_dataset(filename, path, convert_strings=False):
    # type: (str, str, bool) -> np.array
    """
    Get a dataset from the file as a numpy array.
    In python 3, you usually want convert_strings to be true.
    :param filename:
    :param path:
    :param convert_strings:
    :return:
    """
    with h5py.File(filename, 'r') as fp:
        # get shape and try to flatten if 1 row or 1 column
        if max(fp[path].shape) + 1 >= sum(fp[path].shape):
            val = np.asarray(fp[path]).flatten()
        else:
            val = np.asarray(fp[path])
        if convert_strings:
            return np.asarray([row.decode('ascii') if isinstance(row, bytes) else row for row in val])
        return val
