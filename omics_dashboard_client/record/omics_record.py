from typing import Dict, Any, Union

from omics_dashboard_client.record.record import Record


class OmicsRecord(Record):
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
        super(OmicsRecord, self).__init__(res_data, base_url)
        self._name = res_data['name']
        self._description = res_data['description']
        self._creator_id = res_data['creator_id']
        self._owner_id = res_data['owner_id']
        self._last_editor_id = res_data['last_editor_id']
        self._group_can_read = res_data['group_can_read']
        self._group_can_write = res_data['group_can_write']
        self._all_can_read = res_data['all_can_read']
        self._all_can_write = res_data['all_can_write']
        self._user_group_id = res_data['user_group_id']
        self.__is_write_permitted = True if self.id is None or session_user_is_admin else res_data['is_write_permitted'] if 'is_write_permitted' in res_data else False
        self.__session_user_is_admin = session_user_is_admin

    @property
    def id(self):
        # type: () -> Union[int, str]
        """
        The id of this record on the Omics Dashboard service.
        :return:
        """
        return self._id

    @id.setter
    def id(self, value):
        # type: (Union[int, str]) -> None
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
            self._id = value
            if value is None:
                # setting value to None is equivalent to making a copy
                self.__is_write_permitted = True
                self._update_url = None

    @property
    def name(self):
        # type: () -> str
        """
        The name field of the record.
        :return:
        """
        return self._name

    @name.setter
    def name(self, value):
        # type: (str) -> None
        if not self.valid:
            raise RuntimeError('Record has been invalidated!')
        if self.__is_write_permitted:
            self._name = value
        else:
            raise RuntimeError('Current user cannot edit this field.')

    @name.deleter
    def name(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def description(self):
        # type: () -> str
        """
        The description field of the record.
        :return:
        """
        return self._description

    @description.setter
    def description(self, value):
        # type: (str) -> None
        if not self.valid:
            raise RuntimeError('Record has been invalidated!')
        if self.__is_write_permitted:
            self._description = value
        else:
            raise RuntimeError('Current user cannot edit this field.')

    @description.deleter
    def description(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def creator_id(self):
        # type: () -> int
        """
        The user id of the creator of the record.
        :return:
        """
        return self._creator_id

    @creator_id.setter
    def creator_id(self, value):
        # type: (str) -> None
        if self.__session_user_is_admin:
            self._creator_id = value
        else:
            raise RuntimeError('Only admins can edit this record.')

    @creator_id.deleter
    def creator_id(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def owner_id(self):
        # type: () -> int
        """
        The user id of the owner of the record.
        :return:
        """
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        # type: (int) -> None
        if self.__session_user_is_admin:
            self._owner_id = value
        else:
            raise RuntimeError('Only admins can edit this record.')

    @owner_id.deleter
    def owner_id(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def last_editor_id(self):
        # type: () -> int
        """
        The user id of the last user to edit this record.
        :return:
        """
        return self._last_editor_id

    @last_editor_id.setter
    def last_editor_id(self, value):
        # type: (int) -> None
        if self.__session_user_is_admin:
            self._last_editor_id = value
        else:
            raise RuntimeError('Only admins can edit this record.')

    @last_editor_id.deleter
    def last_editor_id(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def group_can_read(self):
        # type: () -> bool
        """
        Whether members of the user group with id user_group_id can read this record.
        :return:
        """
        return self._group_can_read

    @group_can_read.setter
    def group_can_read(self, value):
        # type: (bool) -> None
        if self.__is_write_permitted:
            self._group_can_read = value
        else:
            raise RuntimeError('Current user cannot edit this field.')

    @group_can_read.deleter
    def group_can_read(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def group_can_write(self):
        # type: () -> bool
        """
        Whether members of the user group with id user_group_id can write this record.
        :return:
        """
        return self._group_can_write

    @group_can_write.setter
    def group_can_write(self, value):
        # type: (bool) -> None
        if self.__is_write_permitted:
            self._group_can_write = value
        else:
            raise RuntimeError('Current user cannot edit this field.')

    @group_can_write.deleter
    def group_can_write(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def all_can_read(self):
        # type: () -> bool
        """
        Whether any user can read this record.
        :return:
        """
        return self._all_can_read

    @all_can_read.setter
    def all_can_read(self, value):
        # type: (bool) -> None
        if self.__is_write_permitted:
            self._all_can_read = value
        else:
            raise RuntimeError('Current user cannot edit this field.')

    @all_can_read.deleter
    def all_can_read(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def all_can_write(self):
        # type: () -> bool
        """
        Whether any user can write this record.
        :return:
        """
        return self._all_can_write

    @all_can_write.setter
    def all_can_write(self, value):
        # type: (bool) -> None
        if self.__is_write_permitted:
            self._all_can_write = value
        else:
            raise RuntimeError('Current user cannot edit this field.')

    @all_can_write.deleter
    def all_can_write(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def user_group_id(self):
        # type: () -> int
        """
        The id of the User Group this record is attached to.
        :return:
        """
        return self._user_group_id

    @user_group_id.setter
    def user_group_id(self, value):
        # type: (int) -> None
        if self.__is_write_permitted:
            self._user_group_id = value
        else:
            raise RuntimeError('Current user cannot edit this field.')

    @user_group_id.deleter
    def user_group_id(self):
        raise RuntimeError('Fields cannot be deleted.')

    def serialize(self):
        # type: () -> Dict[str, Any]
        """
        Get a dictionary representation of this record's fields.
        :return:
        """
        return {
            'id': self.id,
            'name': self._name,
            'description': self._description,
            'creator_id': self._creator_id,
            'owner_id': self._owner_id,
            'group_can_read': self._group_can_read,
            'group_can_write': self._group_can_write,
            'all_can_read': self._all_can_read,
            'all_can_write': self._all_can_write,
            'user_group_id': self._user_group_id,
        }

    def update(self, new_data, base_url):
        super(OmicsRecord, self).update(new_data, base_url)
        self._name = new_data['name']
        self._description = new_data['description']
        self._creator_id = new_data['creator_id']
        self._owner_id = new_data['owner_id']
        self._last_editor_id = new_data['last_editor_id']
        self._group_can_read = new_data['group_can_read']
        self._group_can_write = new_data['group_can_write']
        self._all_can_read = new_data['all_can_read']
        self._all_can_write = new_data['all_can_write']
        self._user_group_id = new_data['user_group_id']
        self.__is_write_permitted = True if self.id is None or self.__session_user_is_admin else new_data[
            'is_write_permitted'] if 'is_write_permitted' in new_data else False
