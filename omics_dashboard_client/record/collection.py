from typing import Dict, Any, List

from omics_dashboard_client.record.numeric_file_record import NumericFileRecord


class Collection(NumericFileRecord):
    url_suffix = 'collections'

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
        super(Collection, self).__init__(res_data,
                                         '{}/{}'.format(base_url, Collection.url_suffix),
                                         session_user_is_admin)
        self._analysis_ids = res_data['analysis_ids']
        self._parent_id = res_data['parent_id']

    @property
    def id(self):
        # type: () -> int
        """
        The id of this record on the Omics Dashboard service.
        :return:
        """
        return self._id

    @id.setter
    def id(self, value):
        # type: (int) -> None
        """
        If you set the id to something else, then the record will be moved. If the id already exists, an error will be
        thrown. If you set the record id to none, the record will be marked as writable ("id" is always ignored on
        create routes).
        :param value:
        :return:
        """
        """
        """
        if self.valid:
            if value is None:
                # setting value to None is equivalent to making a copy
                self.__is_write_permitted = True
                self._update_url = None
                self._parent_id = self._id
            self._id = value
        else:
            raise RuntimeError('Record is invalid')

    @id.deleter
    def id(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def analysis_ids(self):
        # type: () -> List[int]
        """
        The analyses this collection belongs to.
        :return:
        """
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

    @property
    def parent_id(self):
        # type () -> int
        """
        The id of the collection this collection is derived from.
        :return:
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value):
        # type: (int) -> None
        if self.valid:
            if self.__is_write_permitted:
                self._parent_id = value
            else:
                raise RuntimeError('Current user cannot edit this record.')
        else:
            raise RuntimeError('Record is invalid.')

    @parent_id.deleter
    def parent_id(self):
        raise RuntimeError('Fields cannot be deleted.')

    def serialize(self):
        # type: () -> Dict[str, Any]
        """
        Get a dictionary representation of this record's fields.
        :return:
        """
        out = super(Collection, self).serialize()
        out.update({
            'analysis_ids': self._analysis_ids
        })
        return out
