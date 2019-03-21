from typing import Dict, List, Any

from omics_dashboard_client.record.file_record import FileRecord


class Workflow(FileRecord):
    """
    A workflow on the Omics Dashboard service.
    """
    url_suffix = 'workflows'

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
        super(Workflow, self).__init__(res_data,
                                       '{}/{}'.format(base_url, Workflow.url_suffix),
                                       session_user_is_admin)
        self._workflow_language = res_data['workflow_language']
        self._workflow_definition = res_data['workflow_definition']
        self._analysis_ids = res_data['analysis_ids']

    @property
    def workflow_language(self):
        # type: () -> str
        return self._workflow_language

    @workflow_language.setter
    def workflow_language(self, value):
        # type: (str) -> None
        if self.__session_user_is_admin:
            self._workflow_language = value
        else:
            raise RuntimeError('Only admins can set this field.')

    @workflow_language.deleter
    def workflow_language(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def workflow_definition(self):
        # type: () -> str
        return self._workflow_definition

    @workflow_definition.setter
    def workflow_definition(self, value):
        if self.__is_write_permitted:
            self._workflow_definition = value
        else:
            raise RuntimeError('Current user cannot edit this field.')

    @workflow_definition.deleter
    def workflow_definition(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def analysis_ids(self):
        # type: () -> List[int]
        return self._analysis_ids

    @analysis_ids.setter
    def analysis_ids(self, value):
        # type: (List[int]) -> None
        if self.__is_write_permitted:
            self._analysis_ids = value
        else:
            raise RuntimeError('Current user cannot edit this field.')

    @analysis_ids.deleter
    def analysis_ids(self):
        raise RuntimeError('Fields cannot be deleted.')

    def serialize(self):
        # type: () -> Dict[str, Any]
        """
        Get a dictionary representation of this record's fields.
        :return:
        """
        out = super(Workflow, self).serialize()
        out.update({
            'workflow_language': self._workflow_language,
            'workflow_definition': self._workflow_definition,
            'analysis_ids': self.analysis_ids
        })
        return out

    def update(self, new_data, base_url):
        super(Workflow, self).update(new_data, '{}/{}'.format(base_url, Workflow.url_suffix))
        self._workflow_language = new_data['workflow_language']
        self._workflow_definition = new_data['workflow_definition']
        self._analysis_ids = new_data['analysis_ids']
