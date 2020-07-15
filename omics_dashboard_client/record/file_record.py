import os
import shutil
import tempfile
import warnings
from typing import Dict, Any

import h5py

from omics_dashboard_client.record.omics_record import OmicsRecord


class FileRecord(OmicsRecord):
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
        super(FileRecord, self).__init__(res_data, base_url, session_user_is_admin)
        self._local_filename = None  # if not None, then the file is downloaded
        self._upload_url = '{}/upload'.format(base_url)
        self._update_url = '{}/{}'.format(base_url, self.id) if self.id is not None else None
        self._create_url = base_url
        self._download_url = '{}/download/{}'.format(base_url, self.id)
        self._filename = res_data['filename']
        self._file_type = res_data['file_type']
        self._file_info = res_data['file_info']
        self._temp_dir = None

    def __del__(self):
        if self._temp_dir is not None and os.path.isdir(self._temp_dir):
            shutil.rmtree(self._temp_dir)

    @property
    def temp_dir(self):
        # type: () -> str
        """
        Where the file(s) are saved to.
        :return:
        """
        return self._temp_dir

    @temp_dir.setter
    def temp_dir(self, value):
        # type: (str) -> None
        raise RuntimeError('temp_dir cannot be changed.')

    @temp_dir.deleter
    def temp_dir(self):
        raise RuntimeError('Fields cannot be deleted.')


    @property
    def upload_url(self):
        # type: () -> str
        """
        The URL used to upload this as a new record.
        :return:
        """
        return self._upload_url

    @upload_url.setter
    def upload_url(self, value):
        # type: (str) -> None
        raise ValueError('Upload url cannot be changed.')

    @upload_url.deleter
    def upload_url(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def download_url(self):
        # type: () -> str
        """
        The URL used to get the file associated with this record.
        :return:
        """
        return self._download_url

    @download_url.setter
    def download_url(self, value):
        # type: (str) -> None
        raise ValueError('Download url cannot be changed.')

    @download_url.deleter
    def download_url(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def local_filename(self):
        # type: () -> str
        """
        The filename of the downloaded file on disk. None if file not downloaded.
        :return:
        """
        return self._local_filename

    @local_filename.setter
    def local_filename(self, value):
        # type: (str) -> None
        raise ValueError('Filename cannot be changed. Change _local_filename cautiously if you know what you\'re doing')

    @local_filename.deleter
    def local_filename(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def filename(self):
        # type: () -> str
        """
        The filename of the file on the omics server.
        :return:
        """
        return self._filename

    @filename.setter
    def filename(self, value):
        # type: (str) -> None
        raise ValueError('Filename is set by the Omics Dashboard service and cannot be changed.')

    @filename.deleter
    def filename(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def file_type(self):
        # type: () -> str
        """
        The type of the file.
        :return:
        """
        return self._file_type

    @file_type.setter
    def file_type(self, value):
        # type: (str) -> None
        raise ValueError('File type is determined by the Omics Dashboard service and cannot be changed.')

    @file_type.deleter
    def file_type(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def file_info(self):
        # type: () -> Dict[str, Any]
        """
        A dictionary containing some information about the file on the omics server.
        :return:
        """
        return self._file_info

    @file_info.setter
    def file_info(self, value):
        # type: (Dict[str, Any]) -> None
        raise RuntimeError('File info is determined by the Omics Dashboard service and cannot be changed.')

    @file_info.deleter
    def file_info(self):
        raise RuntimeError('Fields cannot be deleted.')

    def download_file(self, content):
        # type: (bytes) -> None
        """
        Associate this record with a file on disk.
        :return: The filename
        """
        if self._temp_dir is None or not os.path.isdir(self._temp_dir):
            self._temp_dir = tempfile.mkdtemp()
        if self._local_filename is not None and os.path.isfile(self._local_filename):  # delete existing file
            os.remove(self._local_filename)
        self._local_filename = os.path.join(self._temp_dir, os.path.basename(self._filename))
        with open(self._local_filename, 'wb') as fp:
            fp.write(content)

    def update(self, new_data, base_url):
        # type: (Dict[str, Any], str) -> None
        super(FileRecord, self).update(new_data, base_url)
        self._upload_url = '{}/upload'.format(base_url)
        self._update_url = '{}/{}'.format(base_url, self.id) if self.id is not None else None
        self._create_url = '{}/create'.format(base_url)
        self._download_url = '{}/download/{}'.format(base_url, self.id)
        self._filename = new_data['filename']
        self._file_type = new_data['file_type']
        self._file_info = new_data['file_info']

    def select_local_file(self, path, force=False):
        # type: (str, bool) -> None
        """
        Set the local_filename field to an existing file. If the file does not exist or is not a valid HDF5 file, then
        this will raise ValueError. With force=True, this will not raise.
        :param path:
        :param force: If true, filename will be set with errors ignored.
        :return:
        """
        if os.path.isfile(path):
            if h5py.is_hdf5(path):
                self._local_filename = path
            else:
                msg = '{} is not a valid HDF5 file.'.format(path)
                if force:
                    warnings.warn(msg, RuntimeWarning)
                    self._local_filename = path
                else:
                    raise ValueError(msg)
        else:
            msg = 'No file with path {} exists!'.format(path)
            if force:
                warnings.warn(msg, RuntimeWarning)
                self._local_filename = path
            else:
                raise ValueError(msg)
