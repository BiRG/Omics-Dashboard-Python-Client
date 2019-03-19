from omics_dashboard_client.record.record import Record
from datetime import datetime
from typing import Dict, Any


class Job(Record):
    url_suffix = 'jobs'

    def __init__(self,
                 res_data,
                 base_url):
        # type: (Dict[str, Any], str) -> None
        """
        :param res_data: The dictionary received as JSON from the server.
        :param base_url: The url of service
        """
        res_data['created_on'] = res_data['submission'] if 'submission' in res_data else None
        res_data['updated_on'] = res_data['end'] if 'end' in res_data else None
        super(Job, self).__init__(res_data, '{}/{}'.format(base_url, Job.url_suffix))
        self._owner_id = res_data['owner_id']
        self._user_group_id = res_data['user_group_id']
        self._type = res_data['type']
        self._submission = datetime.fromisoformat(res_data['submission'])
        self._start = datetime.fromisoformat(res_data['start'])
        self._end = datetime.fromisoformat(res_data['end'])
        self._status = res_data['status']
        self._logs = res_data['logs']

    @property
    def owner_id(self):
        # type: () -> int
        """
        The id of the user that owns the record.
        :return:
        """
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        raise PermissionError('Job metadata is not editable.')

    @owner_id.deleter
    def owner_id(self):
        raise PermissionError('Job metadata is not editable.')

    @property
    def user_group_id(self):
        # type: () -> int
        """
        The id of the user group this record belongs to.
        :return:
        """
        return self._user_group_id

    @user_group_id.setter
    def user_group_id(self, value):
        raise PermissionError('Job metadata is not editable.')

    @user_group_id.deleter
    def user_group_id(self):
        raise PermissionError('Job metadata is not editable.')

    @property
    def type(self):
        # type: () -> str
        """
        The type of the job.
        :return:
        """
        return self._type

    @type.setter
    def type(self, value):
        raise PermissionError('Job metadata is not editable')

    @type.deleter
    def type(self):
        raise PermissionError('Job metadata is not editable.')

    @property
    def submission(self):
        # type: () -> datetime
        """
        The time when the job was submitted to the job server from the omics server.
        :return:
        """
        return self._submission

    @submission.setter
    def submission(self, value):
        raise PermissionError('Job metadata is not editable.')

    @submission.deleter
    def submission(self):
        raise PermissionError('Job metadata is not editable.')

    @property
    def start(self):
        # type: () -> datetime
        """
        The time when the job was started by the job server.
        :return:
        """
        return self._start

    @start.setter
    def start(self, value):
        raise PermissionError('Job metadata is not editable.')

    @start.deleter
    def start(self):
        raise PermissionError('Job metadata is not editable.')

    @property
    def end(self):
        # type: () -> datetime
        """
        The time when the job finished running on the jobserver.
        :return:
        """
        return self._end

    @end.setter
    def end(self, value):
        raise PermissionError('Job metadata is not editable.')

    @end.deleter
    def end(self):
        raise PermissionError('Job metadata is not editable.')

    @property
    def status(self):
        # type: () -> str
        """
        The status of the job on the job server (Succeeded/Failed/Running).
        :return:
        """
        return self._status

    @status.setter
    def status(self, value):
        raise PermissionError('Job metadata is not editable.')

    @status.deleter
    def status(self):
        raise PermissionError('Job metadata is not editable.')

    @property
    def logs(self):
        # type: () -> Dict[str, Dict[str, str]]
        """
        Get the logs (stdout and stderr) of the workflow steps.
        :return:
        """
        return self._logs

    @logs.setter
    def logs(self, value):
        raise PermissionError('Job metadata is not editable.')

    @logs.deleter
    def logs(self):
        raise PermissionError('Job metadata is not editable')

    def serialize(self):
        # type: () -> Dict[str, Any]
        """
        Get a dictionary representation of this record's fields.
        :return:
        """
        return {
            **super().serialize(),
            'owner_id': self._owner_id,
            'user_group_id': self._user_group_id,
            'type': self._type,
            'submission': self._submission,
            'start': self._start.isoformat(),
            'end': self._end.isoformat(),
            'status': self._status,
            'logs': self._logs
        }
