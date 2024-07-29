import logging
import google.oauth2.service_account
import googleapiclient
import googleapiclient.discovery
from spaceone.core.connector import BaseConnector


class GoogleCloudConnector(BaseConnector):
    def __init__(self, *args, **kwargs):
        self.client = None
        self.project_id = None
        super().__init__(*args, **kwargs)

    def set_connect(self, secret_data: dict):
        """
        cred(dict)
            - type: ..
            - project_id: ...
            - token_uri: ...
            - ...
        """
        try:
            self.project_id = secret_data.get('project_id')
            credentials = google.oauth2.service_account.Credentials.from_service_account_info(secret_data)
            self.client = googleapiclient.discovery.build('monitoring', 'v3', credentials=credentials)

        except Exception as e:
            print(e)
            raise self.client(message='connection failed. Please check your authentication information.')

    def get_metric_data(self, request):
        return self.client.projects().timeSeries().list(**request).execute()
