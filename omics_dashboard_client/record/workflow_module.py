from typing import Dict, Any

from omics_dashboard_client.record.record import Record


class WorkflowModule(Record):
    url_suffix = 'workflows/workflow_modules'

    def __init__(self, res_data, base_url):
        # type: (Dict[str, Any], str) -> None
        """
        :param res_data: The dictionary received as JSON from the server.
        :param base_url: The url of service
        """
        super(WorkflowModule, self).__init__(res_data, '{}/{}'.format(base_url, WorkflowModule.url_suffix))
        self._path = res_data['path']
        self._label = res_data['label']
        self._description = res_data['description']
        self._package = res_data['package']
        self._package_description = res_data['package_description']
        self._subpackage = res_data['subpackage']
        self._subpackage_description = res_data['subpackage_description']
        self._tool_definition = res_data['tool_definition']

    @property
    def path(self):
        # type: () -> str
        return self._path

    @path.setter
    def path(self, value):
        raise RuntimeError('Workflow modules are not editable.')

    @path.deleter
    def path(self):
        raise RuntimeError('Workflow modules are not editable.')

    @property
    def label(self):
        # type: () -> str
        return self._label

    @label.setter
    def label(self, value):
        raise RuntimeError('Workflow modules are not editable.')

    @label.deleter
    def label(self):
        raise RuntimeError('Workflow modules are not editable.')

    @property
    def description(self):
        # type: () -> str
        return self._description

    @description.setter
    def description(self, value):
        raise RuntimeError('Workflow modules are not editable.')

    @description.deleter
    def description(self):
        raise RuntimeError('Workflow modules are not editable.')

    @property
    def package(self):
        # type: () -> str
        return self._package

    @package.setter
    def package(self, value):
        raise RuntimeError('Workflow modules are not editable.')

    @package.deleter
    def package(self):
        raise RuntimeError('Workflow modules are not editable')

    @property
    def package_description(self):
        # type: () -> str
        return self._package_description

    @package_description.setter
    def package_description(self, value):
        raise RuntimeError('Workflow modules are not editable.')

    @package_description.deleter
    def package_description(self):
        raise RuntimeError('Workflow modules are not editable.')

    @property
    def subpackage(self):
        # type: () -> str
        return self._subpackage

    @subpackage.setter
    def subpackage(self, value):
        raise RuntimeError('Workflow modules are not editable.')

    @subpackage.deleter
    def subpackage(self):
        raise RuntimeError('Workflow modules are not editable.')

    @property
    def subpackage_description(self):
        # type: () -> str
        return self.subpackage_description

    @subpackage_description.setter
    def subpackage_description(self, value):
        raise RuntimeError('Workflow modules are not editable.')

    @subpackage_description.deleter
    def subpackage_description(self):
        raise RuntimeError('Workflow modules are not editable.')

    @property
    def tool_definition(self):
        # type: () -> Dict[str, Any]
        return self._tool_definition

    @tool_definition.setter
    def tool_definition(self, value):
        raise RuntimeError('Workflow modules are not editable.')

    @tool_definition.deleter
    def tool_definition(self):
        raise RuntimeError('Workflow modules are not editable.')

    def serialize(self):
        # type: () -> Dict[str, Any]
        """
        Get a dictionary representation of this record's fields.
        :return:
        """
        out = super(WorkflowModule, self).serialize()
        out.update({
            'path': self._path,
            'label': self._label,
            'description': self._description,
            'package': self._package,
            'package_description': self._package_description,
            'subpackage': self._subpackage,
            'subpackage_description': self._subpackage_description,
            'tool_definition': self._tool_definition
        })
        return out

    def update(self, new_data, base_url):
        super(WorkflowModule, self).update(new_data, base_url)
        self._path = new_data['path']
        self._label = new_data['label']
        self._description = new_data['description']
        self._package = new_data['package']
        self._package_description = new_data['package_description']
        self._subpackage = new_data['subpackage']
        self._subpackage_description = new_data['subpackage_description']
        self._tool_definition = new_data['tool_definition']
