from typing import Dict, Any, List

from omics_dashboard_client.record.file_record import FileRecord


class ExternalFile(FileRecord):
    url_suffix = 'external_files'

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
        super(ExternalFile, self).__init__(res_data,
                                           '{}/{}'.format(base_url, ExternalFile.url_suffix),
                                           session_user_is_admin)
        self._analysis_ids = res_data['analysis_ids']

    @property
    def analysis_ids(self):
        return self._analysis_ids

    @analysis_ids.setter
    def analysis_ids(self, value):
        # type: (List[int]) -> None
        if self.__is_write_permitted:
            self._analysis_ids = value
        else:
            raise RuntimeError('Current user cannot edit this record.')

    @analysis_ids.deleter
    def analysis_ids(self):
        raise RuntimeError('Fields cannot be deleted.')

    def serialize(self):
        # type: () -> Dict[str, Any]
        """
        Get a dictionary representation of this record's fields.
        :return:
        """
        out = super(ExternalFile, self).serialize()
        out.update({'analysis_ids': self._analysis_ids})
        return out

    def update(self, new_data, base_url):
        super(ExternalFile, self).update(new_data, base_url)
        self._analysis_ids = new_data['analysis_ids']
