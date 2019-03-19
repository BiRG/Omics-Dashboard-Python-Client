from omics_dashboard_client.record.file_record import FileRecord
from typing import Dict, Any


class NumericFileRecord(FileRecord):
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
        super(NumericFileRecord, self).__init__(res_data, base_url, session_user_is_admin)
