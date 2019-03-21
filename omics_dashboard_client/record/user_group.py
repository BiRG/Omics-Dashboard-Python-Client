from typing import Dict, Any, List

from omics_dashboard_client.record.record import Record


class UserGroup(Record):
    """
    A user group on the Omics Dashboard service.
    """
    url_suffix = 'user_groups'

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
        super(UserGroup, self).__init__(res_data, '{}/{}'.format(base_url, UserGroup.url_suffix))
        self._creator_id = res_data['creator_id']
        self._name = res_data['name']
        self._description = res_data['description']
        self._member_ids = [member['id'] for member in res_data['members']]
        self._admin_ids = [admin['id'] for admin in res_data['admins']]
        self.__is_write_permitted = True if self.id is None or session_user_is_admin else res_data['is_write_permitted'] if 'is_write_permitted' in res_data else False
        self.__session_user_is_admin = session_user_is_admin

    @property
    def name(self):
        # type: () -> str
        """
        The name field of this record.
        :return:
        """
        return self._name

    @name.setter
    def name(self, value):
        # type: (str) -> None
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
        The description field of this record.
        :return:
        """
        return self._description

    @description.setter
    def description(self, value):
        # type: (str) -> None
        if self.__is_write_permitted:
            self._description = value
        else:
            raise RuntimeError('Current user cannot edit this field.')

    @description.deleter
    def description(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def member_ids(self):
        # type: () -> List[int]
        """
        The user ids of the members of this group.
        :return:
        """
        return self._member_ids

    @member_ids.setter
    def member_ids(self, value):
        # type: (List[int]) -> None
        if self.__is_write_permitted:
            self._member_ids = value
        else:
            raise RuntimeError('Current user cannot edit this field.')

    @member_ids.deleter
    def member_ids(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def admin_ids(self):
        # type: () -> List[int]
        """
        The user ids of the admins of this group.
        :return:
        """
        return self._admin_ids

    @admin_ids.setter
    def admin_ids(self, value):
        if self.__is_write_permitted:
            self._admin_ids = value
        else:
            raise RuntimeError('Current user cannot edit this field.')

    @admin_ids.deleter
    def admin_ids(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def creator_id(self):
        # type: () -> int
        """
        The user id of the creator of this record.
        :return:
        """
        return self._creator_id

    @creator_id.setter
    def creator_id(self, value):
        # type: (int) -> None
        if self.__session_user_is_admin:
            self._creator_id = value
        else:
            raise RuntimeError('Only admins can modify creator_id or owner_id.')

    @creator_id.deleter
    def creator_id(self):
        raise RuntimeError('Fields cannot be deleted.')

    def serialize(self):
        # type: () -> Dict[str, Any]
        """
        Get a dictionary representation of this record's fields.
        :return:
        """
        return {
            'id': self.id,
            'creator_id': self._creator_id,
            'name': self._name,
            'description': self._description,
            'member_ids': self._member_ids,
            'admin_ids': self._admin_ids
        }

    def update(self, new_data, base_url):
        super(UserGroup, self).update(new_data, base_url)
        self._creator_id = new_data['creator_id']
        self._name = new_data['name']
        self._description = new_data['description']
        self._member_ids = [member['id'] for member in new_data['members']]
        self._admin_ids = [admin['id'] for admin in new_data['admins']]
