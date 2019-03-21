from typing import Dict, Any, List

from omics_dashboard_client.record.numeric_file_record import NumericFileRecord


class Sample(NumericFileRecord):
    url_suffix = 'samples'

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
        super(Sample, self).__init__(res_data,
                                     '{}/{}'.format(base_url, Sample.url_suffix),
                                     session_user_is_admin)
        self._sample_group_ids = res_data['sample_group_ids']

    @property
    def sample_group_ids(self):
        # type: () -> List[int]
        """
        The ids of the sample groups that this sample belongs to.
        :return:
        """
        return self._sample_group_ids

    @sample_group_ids.setter
    def sample_group_ids(self, value):
        # type: (List[int]) -> None
        if self.__is_write_permitted:
            self._sample_group_ids = value
        else:
            raise RuntimeError('Current user cannot edit this field.')

    @sample_group_ids.deleter
    def sample_group_ids(self):
        raise RuntimeError('Fields cannot be deleted.')

    def serialize(self):
        # type: () -> Dict[str, Any]
        """
        Get a dictionary representation of this record's fields.
        :return:
        """
        out = super(Sample, self).serialize()
        out.update({
            'sample_group_ids': self._sample_group_ids
        })
        return out

    def update(self, new_data, base_url):
        super(Sample, self).update(new_data, base_url)
        self._sample_group_ids = new_data['sample_group_ids']
