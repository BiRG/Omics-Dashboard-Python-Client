from omics_dashboard_client.record.omics_record import OmicsRecord
from typing import Dict, Any, List


class Analysis(OmicsRecord):
    url_suffix = 'analyses'

    def __init__(self,
                 res_data,
                 base_url,
                 session_user_is_admin):
        # type: (Dict[str, Any], str, bool) -> None
        """
        :param res_data: The dictionary received as JSON from the server.
        :param base_url: The url of service
        :param session_user_is_admin:
        """
        super(Analysis, self).__init__(res_data,
                                       '{}/{}'.format(base_url, Analysis.url_suffix),
                                       session_user_is_admin)
        self._workflow_ids = [workflow['id'] for workflow in res_data['workflows']]
        self._collection_ids = [collection['id'] for collection in res_data['collections']]
        self._external_file_ids = [external_file['id'] for external_file in res_data['external_files']]

    @property
    def workflow_ids(self):
        # type: () -> List[int]
        return self._workflow_ids

    @workflow_ids.setter
    def workflow_ids(self, value):
        # type: (List[int]) -> None
        if self.__is_write_permitted:
            self._workflow_ids = value
        else:
            raise PermissionError('Current user cannot edit this field.')

    @workflow_ids.deleter
    def workflow_ids(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def collection_ids(self):
        # type: () -> List[int]
        return self._collection_ids

    @collection_ids.setter
    def collection_ids(self, value):
        # type: (List[int]) -> None
        if self.__is_write_permitted:
            self._collection_ids = value
        else:
            raise PermissionError('Current user cannot edit this field.')

    @collection_ids.deleter
    def collection_ids(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def external_file_ids(self):
        # type: () -> List[int]
        return self._external_file_ids

    @external_file_ids.setter
    def external_file_ids(self, value):
        # type: (List[int]) -> None
        if self.__is_write_permitted:
            self._external_file_ids = value
        else:
            raise PermissionError('Current user cannot edit this field.')

    @external_file_ids.deleter
    def external_file_ids(self):
        raise RuntimeError('Fields cannot be deleted.')

    def serialize(self):
        # type: () -> Dict[str, Any]
        return {
            **super().serialize(),
            'collection_ids': self._collection_ids,
            'workflow_ids': self._workflow_ids,
            'external_file_ids': self._external_file_ids
        }
