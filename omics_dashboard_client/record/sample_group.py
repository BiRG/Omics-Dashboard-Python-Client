from typing import Dict, List, Any

from omics_dashboard_client.record.omics_record import OmicsRecord


class SampleGroup(OmicsRecord):
    url_suffix = "sample_groups"

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
        super(SampleGroup, self).__init__(res_data,
                                          '{}/{}'.format(base_url, SampleGroup.url_suffix),
                                          session_user_is_admin)
        self._sample_ids = [sample['id'] for sample in res_data['samples']]
        self._upload_job_id = res_data['upload_job_id']

    @property
    def sample_ids(self):
        # type: () -> List[int]
        """
        The ids of the samples that belong to this group.
        :return:
        """
        return self._sample_ids

    @sample_ids.setter
    def sample_ids(self, value):
        # type: (List[int]) -> None
        if self.__is_write_permitted:
            self._sample_ids = value
        else:
            raise RuntimeError('Current user cannot edit this field.')

    @sample_ids.deleter
    def sample_ids(self):
        raise RuntimeError('Fields cannot be deleted.')

    @property
    def upload_job_id(self):
        # type: () -> str
        """
        The id of the upload job for this sample group.
        :return:
        """
        return self._upload_job_id

    @upload_job_id.setter
    def upload_job_id(self, value):
        # type: (str) -> None
        if self.__session_user_is_admin:
            self._upload_job_id = value
        else:
            raise RuntimeError('Only admins can edit this field.')

    @upload_job_id.deleter
    def upload_job_id(self):
        raise RuntimeError('Fields cannot be deleted.')

    def serialize(self):
        # type: () -> Dict[str, Any]
        """
        Get a dictionary representation of this record's fields.
        :return:
        """
        out = super(SampleGroup, self).serialize()
        out.update({
            'sample_ids': self._sample_ids,
            'upload_job_id': self._upload_job_id
        })
        return out

    def update(self, new_data, base_url):
        super(SampleGroup, self).update(new_data, '{}/{}'.format(base_url, SampleGroup.url_suffix))
        self._sample_ids = [sample['id'] for sample in new_data['samples']]
        self._upload_job_id = new_data['upload_job_id']
