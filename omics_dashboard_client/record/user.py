from typing import Dict, Any, List

from omics_dashboard_client.record.record import Record


class User(Record):
    url_suffix = 'users'

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
        super(User, self).__init__(res_data, '{}/{}'.format(base_url, User.url_suffix))
        self._email = res_data['email']
        self._name = res_data['name']
        self._admin = res_data['admin']
        self._active = res_data['active']
        self._primary_user_group_id = res_data['primary_user_group_id']
        self._group_ids = res_data['group_ids']
        self._admin_group_ids = res_data['admin_group_ids']
        self.__is_write_permitted = True if self.id is None or session_user_is_admin else res_data['is_write_permitted'] if 'is_write_permitted' in res_data else False
        self.__session_user_is_admin = session_user_is_admin

    @property
    def email(self):
        # type: () -> str
        """
        The email address of the user.
        :return:
        """
        return self._email

    @email.setter
    def email(self, value):
        # type: (str) -> None
        if not self.valid:
            raise RuntimeError('Record has been invalidated!')
        if self.__is_write_permitted:
            self._email = value
        else:
            raise RuntimeError('Current user cannot edit this field.')

    @email.deleter
    def email(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def name(self):
        # type: () -> str
        """
        The name of the user.
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
    def admin(self):
        # type: () -> str
        """
        Whether or not the user is an administrator.
        :return:
        """
        return self._admin

    @admin.setter
    def admin(self, value):
        # type: (str) -> None
        if not self.valid:
            raise RuntimeError('Record has been invalidated!')
        if self.__session_user_is_admin:
            self._admin = value
        else:
            raise RuntimeError('Only admins can elevate or de-elevate other users to admin')

    @admin.deleter
    def admin(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def active(self):
        # type: () -> str
        """
        Whether or not this user is active in the system
        :return:
        """
        return self._active

    @active.setter
    def active(self, value):
        # type: (str) -> None
        if not self.valid:
            raise RuntimeError('Record has been invalidated!')
        if self.__session_user_is_admin:
            self._active = value
        else:
            raise RuntimeError('Only admins can activate or deactivate user accounts')

    @active.deleter
    def active(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def group_ids(self):
        # type: () -> str
        """
        The ids of the user groups this user belongs to.
        :return:
        """
        return self._group_ids

    @group_ids.setter
    def group_ids(self, value):
        # type: (str) -> None
        raise RuntimeError('User group membership should be changed by editing the user group.')

    @group_ids.deleter
    def group_ids(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def primary_user_group_id(self):
        # type: () -> int
        """
        The id of the user's primary user group.
        :return:
        """
        return self.primary_user_group_id

    @primary_user_group_id.setter
    def primary_user_group_id(self, value):
        # type: (int) -> None
        if not self.valid:
            raise RuntimeError('Record has been invalidated!')
        if self.__is_write_permitted:
            self._primary_user_group_id = value
        else:
            raise RuntimeError('Current user cannot edit this field.')

    @primary_user_group_id.deleter
    def primary_user_group_id(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def admin_group_ids(self):
        # type: () -> List[int]
        """
        The ids of the groups this user is an admin in.
        :return:
        """
        return self._admin_group_ids

    @admin_group_ids.setter
    def admin_group_ids(self, value):
        # type: (List[int]) -> None
        raise RuntimeError('User group admin status should be changed by editing the user group.')

    @admin_group_ids.deleter
    def admin_group_ids(self):
        raise RuntimeError('Fields cannot be deleted.')

    def serialize(self):
        # type: () -> Dict[str, Any]
        """
        Get a dictionary representation of this record's fields.
        :return:
        """
        return {
            'email': self.email,
            'name': self.name,
            'admin': self.admin,
            'active': self.active,
            'primary_user_group_id': self.primary_user_group_id,
            'group_ids': self.group_ids,
            'admin_group_ids': self.admin_group_ids
        }

    def update(self, new_data, base_url):
        super(User, self).update(new_data, base_url)
        self._email = new_data['email']
        self._name = new_data['name']
        self._admin = new_data['admin']
        self._active = new_data['active']
        self._primary_user_group_id = new_data['primary_user_group_id']
        self._group_ids = new_data['group_ids']
        self._admin_group_ids = new_data['admin_group_ids']
