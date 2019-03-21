from datetime import datetime

from typing import Dict, Any, Union


class Record(object):
    def __init__(self, res_data, base_url):
        # type: (Dict[str, Any], str) -> None
        """
        :param res_data: The dictionary received as JSON from the server.
        :param base_url: The url of the record_type's list
        """
        self._original_id = res_data['id'] if 'id' in res_data else None
        self._id = res_data['id'] if 'id' in res_data else None
        self._created_on = datetime.strptime(res_data['created_on'], '%Y-%m-%dT%H:%M:%S')
        self._updated_on = datetime.strptime(res_data['updated_on'], '%Y-%m-%dT%H:%M:%S')
        self._base_url = base_url
        self._update_url = '{}/{}'.format(base_url, self.id) if self.id is not None else None
        self._create_url = '{}/create'.format(base_url)
        self._valid = True

    @property
    def original_id(self):
        """
        The id of this record when it was retrieved from the service.
        :return:
        """
        return self._original_id

    @original_id.setter
    def original_id(self, value):
        raise RuntimeError('Original id cannot be changed.')

    @property
    def id(self):
        """
        The id of this record.
        :return:
        """
        return self._id

    @id.setter
    def id(self, value):
        # type: (Union[int, str]) -> None
        self._id = value
        self._update_url = '{}/{}'.format(self._base_url, self._id) if self._id is not None else None

    @id.deleter
    def id(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def update_url(self):
        # type: () -> str
        """
        The url used to update the metadata of this record on the Omics Dashboard service.
        :return:
        """
        return self._update_url

    @update_url.setter
    def update_url(self, value):
        # type: (str) -> None
        raise ValueError('Update url cannot be changed')

    @update_url.deleter
    def update_url(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def create_url(self):
        # type: () -> str
        """
        The url used to create a new record of this type on the Omics Dashboard service.
        :return:
        """
        return self._create_url

    @create_url.setter
    def create_url(self, value):
        # type: (str) -> None
        raise ValueError('Create url cannot be changed')

    @create_url.deleter
    def create_url(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def created_on(self):
        # type: () -> datetime
        """
        The date this record was created on the Omics Dashboard service.
        :return:
        """
        return self._created_on

    @created_on.setter
    def created_on(self, value):
        # type: (datetime) -> None
        raise ValueError('created_on is set by the Omics Dashboard service and cannot be changed!')

    @created_on.deleter
    def created_on(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def updated_on(self):
        # type: () -> datetime
        """
        The date this record was last changed on the Omics Dashboard service.
        :return:
        """
        return self._updated_on

    @updated_on.setter
    def updated_on(self, value):
        # type: (datetime) -> None
        raise ValueError('updated_on is set by the Omics Dashboard service and cannot be changed!')

    @updated_on.deleter
    def updated_on(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def valid(self):
        # type: () -> bool
        """
        Whether this file is valid. Invalid files are "dead" and cannot be edited, and the session will not do anything
        with them. The session will set any deleted record to be invalid. You should delete invalid records.
        :return:
        """
        return self._valid

    @valid.setter
    def valid(self, value):
        # type: (bool) -> None
        if not self._valid and value:
            raise ValueError("Invalid records cannot be made valid. Please instantiate or get a new record.")
        else:
            self._valid = value

    @valid.deleter
    def valid(self):
        raise RuntimeError('Fields cannot be deleted.')

    def serialize(self):
        # type: () -> Dict[str, Any]
        """
        Get a dictionary representation of this record's fields.
        :return:
        """
        raise NotImplementedError()  # should be overloaded to fit established payload for record type

    def update(self, new_data, base_url):
        # type: (Dict[str, Any], str) -> None
        """
        Take an object from the server and update fields of this object
        :param new_data:
        :param base_url: Base url of the application.
        :return:
        """
        self.__init__(new_data, base_url)

    def invalidate(self):
        """
        Make the object invalid. This makes the record "dead" so that no fields may be edited and the session will not
        interact with the record at all.
        :return:
        """
        self._valid = False
