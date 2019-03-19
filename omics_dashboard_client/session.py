import requests
import json
from typing import Union, Dict, Type
from omics_dashboard_client.record.record import Record
from omics_dashboard_client.record.file_record import FileRecord

from omics_dashboard_client.record.analysis import Analysis
from omics_dashboard_client.record.collection import Collection
from omics_dashboard_client.record.external_file import ExternalFile
from omics_dashboard_client.record.job import Job
from omics_dashboard_client.record.sample import Sample
from omics_dashboard_client.record.sample_group import SampleGroup
from omics_dashboard_client.record.user import User
from omics_dashboard_client.record.user_group import UserGroup
from omics_dashboard_client.record.workflow import Workflow
from omics_dashboard_client.record.workflow_module import WorkflowModule

AnyRecordType = Type[Union[Analysis, Collection, ExternalFile, Job, Sample,
                           SampleGroup, User, UserGroup, Workflow, WorkflowModule]]


class Session:
    """
    Create one of these before doing anything else
    """
    def __init__(self, base_url, credentials):
        # type: (str, Union[str, Dict[str, str]]) -> None
        """
        :param base_url:  The base url of your Omics Dashboard service (ex: 'https://example.com/omics')
        :param credentials: Either a filename of a json file (which you should have 400 permissions or be similarly secure)
                            or a dictionary containing an email and password
        """
        self.__base_url = '{}/api'.format(base_url)
        if isinstance(credentials, str):
            # try to read json file
            self.credentials = json.load(open(credentials))
        else:
            self.credentials = credentials
        headers = {'Content-Type': 'application/json'}
        res = requests.post('{}/api/authenticate'.format(base_url), json=self.credentials, headers=headers)
        res.raise_for_status()
        self.__auth_token = res.json()['token']
        self.__current_user = None

    def authenticate(self):
        res = requests.post('{}/authenticate'.format(self.__base_url), json=self.credentials)
        try:
            res.raise_for_status()
            self.__auth_token = res.json()['token']
        except requests.HTTPError as e:
            message = 'Could not authenticate with provided credentials. Status code {}'.format(e.response.status_code)
            raise ValueError(message)

    def is_authenticated(self):
        if self.__auth_token is not None:
            try:
                res = requests.get('{}/current_user'.format(self.__base_url),
                                   headers={'Authorization': 'Bearer {}'.format(self.__auth_token)})
                res.raise_for_status()
                self.__current_user = User(res.json(), self.__base_url, False, False)
                return self.__current_user.active
            except requests.HTTPError:
                return False
        return False

    def get_auth_header(self):
        if self.is_authenticated():
            return {'Authorization': 'Bearer {}'.format(self.__auth_token)}
        else:
            self.authenticate()
            if self.is_authenticated():
                return {'Authorization': 'Bearer {}'.format(self.__auth_token)}
            raise RuntimeError('Could not authenticate with provided credentials!')

    def get(self, record_type, record_id):
        # type: (AnyRecordType, Union[str, int]) -> Record
        """
        Get a record
        :param record_type: The type of the record (i.e. Sample, Collection, Analysis)
        :param record_id: The id of the record (an int for everything but job, a string uuid for job)
        :return: The record with the specified id
        """
        url = '{}/{}/{}'.format(self.__base_url, record_type.url_suffix, record_id)
        res = requests.get(url, headers=self.get_auth_header())
        res.raise_for_status()
        return record_type(res.json(), self.__base_url, self.__current_user.admin)

    def delete(self, record):
        # type: (Record) -> Dict[str, str]
        """
        Delete a record. Record object will be set to invalid
        :param record:
        :return:
        """
        if record.valid:
            res = requests.delete(record.update_url, headers=self.get_auth_header())
            res.raise_for_status()
            record.invalidate()
            return res.json()
        else:
            raise ValueError('Record is not valid.')

    def update(self, record, upload_file=False):
        # type: (Record, bool) -> Record
        """
        Update the server with the values of the record
        :param record: The record to update on the server
        :param upload_file: Only applies when record is FileRecord
        :return:
        """
        if record.valid:
            if isinstance(record, FileRecord) and record.local_filename is not None and upload_file:
                res = requests.post(record.update_url,
                                    headers={**self.get_auth_header(), 'Content-Type': 'multipart/form-data'},
                                    data=record.serialize(),
                                    files={'file': open(record.local_filename, 'rb')})
            else:
                res = requests.post(record.update_url, headers=self.get_auth_header(), json=record.serialize())
                res.raise_for_status()
            res.raise_for_status()
            record.update(res.json())
            return record
        else:
            raise ValueError('Record is not valid.')

    def create(self, record):
        # type: (Record) -> Record
        """
        Create a new record. Record object will be populated with new id
        :param record: A record
        :return:
        """
        if record.valid:
            if isinstance(record, FileRecord) and record.local_filename is not None:
                res = requests.post(record.create_url,
                                    headers={**self.get_auth_header(), 'Content-Type': 'multipart/form-data'},
                                    data=record.serialize(),
                                    files={'file': open(record.local_filename, 'rb')})
            else:
                res = requests.post(record.create_url,
                                    headers=self.get_auth_header(),
                                    data=record.serialize())
            res.raise_for_status()
            record.update(res.json())
            return record
        else:
            raise ValueError('Record is not valid.')

    def download_file(self, record):
        # type: (FileRecord) -> FileRecord
        """
        Download the file associated with a FileRecord.
        :param record:
        :return:
        """
        res = requests.get(record.download_url, headers={self.get_auth_header()})
        record.download_file(res.content)
        return record
