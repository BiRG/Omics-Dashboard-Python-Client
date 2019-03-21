import os

import h5py
import numpy as np
import pandas as pd
from typing import Dict, Any, List

import omics_dashboard_client.hdf_tools as hdf_tools
from omics_dashboard_client.record.file_record import FileRecord


class NumericFileRecord(FileRecord):
    def __init__(self,
                 res_data,
                 base_url,
                 session_user_is_admin=False):
        # type: (Dict[str, Any], str, bool) -> None
        """
        :param res_data: The dictionary received as JSON from the server.
        :param base_url: The url of service
        :param session_user_is_admin:
        """
        super(NumericFileRecord, self).__init__(res_data, base_url, session_user_is_admin)

    def get_attr(self, key, path=None):
        # type: (str, str) -> Any
        """
        Get an attribute of the file or a path (Group or Dataset) inside the file.
        :param key: The key of the attribute to access.
        :param path: Optional. Get the attribute on a Group or Dataset of the file.
        :return:
        """
        if self.local_filename is not None and os.path.isfile(self.local_filename):
            with h5py.File(self.local_filename, 'r') as fp:
                if path is not None:
                    return fp[path].attrs[key]
                else:
                    return fp.attrs[key]
        else:
            raise RuntimeError('File has not been downloaded! Use Session.download_file to download the file for this '
                               'record')

    def set_attr(self, key, value, path=None):
        # type: (str, Any, str) -> None
        """
        Get an attribute of the file or a path (Group or Dataset) inside the file.
        :param key: The key of the attribute to set.
        :param value: The new value for the attribute.
        :param path: Optional. Set the attribute on a Group or Dataset of the file.
        :return:
        """
        if self.local_filename is not None and os.path.isfile(self.local_filename):
            with h5py.File(self.local_filename, 'r') as fp:
                if path is not None:
                    fp[path].attrs[key] = value
                else:
                    fp.attrs[key] = value
        else:
            raise RuntimeError('File has not been downloaded! Use Session.download_file to download the file for this '
                               'record')

    def get_dataset(self, path):
        # type: (str) -> np.array
        """
        Get a numpy array from the file.
        :param path:
        :return:
        """
        if self.local_filename is not None and os.path.isfile(self.local_filename):
            with h5py.File(self.local_filename, 'r') as fp:
                return np.asarray(fp[path])
        else:
            raise RuntimeError('File has not been downloaded! Use Session.download_file to download the file for this '
                               'record')

    def set_dataset(self, path, arr):
        # type: (str, np.array) -> None
        """
        Set the value of the dataset at path to arr
        :param arr: The numpy array.
        :param path: The path to the dataset.
        :return:
        """
        if self.local_filename is not None and os.path.isfile(self.local_filename):
            with h5py.File(self.local_filename, 'r+') as fp:
                if path in fp:
                    del fp[path]
                fp.create_dataset(path, data=arr)
        else:
            raise RuntimeError('File has not been downloaded! Use Session.download_file to download the file for this '
                               'record')

    def get_dataframe(self, row_index_key='base_sample_id', keys=None):
        # type: (str, List[str]) -> pd.DataFrame
        """
        Get a Pandas DataFrame containing the records in keys or the columns of 'Y'. The column names will be 'Y_{x_i}'
        for 'x_i' in 'x' for Y if 'x' exists with the same dimensions as Y. Otherwise, the column names for all datasets
        with multiple columns will be 'Key_{i}' for i in n columns. The column names for datasets with one column will
        be the key of the dataset.
        :param row_index_key: A key for a column with unique values to use as a row index.
        :param keys: An iterable of keys to use as data for the dataframe.
        :return:
        """
        """
        Get a Pandas DataFrame containing the records in keys. If keys is not specified or set to None, the index will
        be the values in "/x" and the names of the "label columns" (those columns with same number of rows as /Y).
        :param include_labels: Whether to include label columns alongside "/x" and "/Y". This will change the name of
        the indices associated with "/x" from "1" to "x_1"
        :return:
        """
        if self.local_filename is not None and os.path.isfile(self.local_filename):
            return hdf_tools.get_dataframe(self.local_filename, row_index_key, keys)
        else:
            raise RuntimeError('File has not been downloaded! Use Session.download_file to download the file for this '
                               'record')

    def get_dataset_csv(self, path):
        # type: (str) -> str
        """
        Get a string containing CSV of a dataset
        :param path:
        :return:
        """
        if self.local_filename is not None and os.path.isfile(self.local_filename):
            return hdf_tools.get_csv(self.local_filename, path)
        else:
            raise RuntimeError('File has not been downloaded! Use Session.download_file to download the file for this '
                               'record')

    def update_dataset(self, path, i, j, val):
        # type: (str, int, int, Any) -> None
        """
        Change the value of an array at (i, j)
        :param path:
        :param i:
        :param j:
        :param val:
        :return:
        """

        if self.local_filename is not None and os.path.isfile(self.local_filename):
            hdf_tools.update_array(self.local_filename, path, i, j, val)
        else:
            raise RuntimeError('File has not been downloaded! Use Session.download_file to download the file for this '
                               'record')
