import logging
import pandas as pd

from datetime import timedelta
from spaceone.core.manager import BaseManager
from spaceone.inventory.connector.google_cloud_connector import GoogleCloudConnector


_LOGGER = logging.getLogger(__name__)
provider = 'google_cloud'
perSeriesAligners = ['ALIGN_MEAN', 'ALIGN_MIN', 'ALIGN_MAX']
end = pd.Timestamp.now()
end = end.replace(second=0, microsecond=0)
start = end - timedelta(days=1)


class GoogleCloudManager(BaseManager):

    def metric_data_collect(self, secret_data, metric):
        #gcp connect
        GoogleCloudConnector.set_connect(self, secret_data)
        project_id = secret_data['project_id']

        data_list = {}
        for perSeriesAligner in perSeriesAligners:
            request = self._request_setting(project_id, metric, perSeriesAligner)  # 조회 조건

            # gcp connector 호출, data 수집
            data = GoogleCloudConnector.get_metric_data(self, request)

            if 'timeSeries' not in data:
                return

            data_list[perSeriesAligner] = data

        result = self._merge_data(data_list)

        return result

    #metric 조회 조건 설정
    def _request_setting(self, project_id, metric_type, perseries_aligner):
        startTime = self.date_time_to_iso(start)
        endTime = self.date_time_to_iso(end)

        request = {
            'name': 'projects/' + project_id,
            'filter': 'metric.type = "' + metric_type + '"',
            'aggregation_alignmentPeriod': '60s', # 24hour
            # 'aggregation_alignmentPeriod': '86400s', # 24hour
            'aggregation_perSeriesAligner': perseries_aligner,
            'interval_startTime': startTime,
            'interval_endTime': endTime,
            'view': 'FULL'
        }

        return request

    # interval 조회 date time 형식으로 변환
    @staticmethod
    def date_time_to_iso(date_time):
        date_format = date_time.isoformat()
        return date_format[0:date_format.find('+')] + 'Z' if '+' in date_format else date_format + 'Z'

    # MIN, MAX, AVG 병합
    def _merge_data(self, data_list):
        min_unit = data_list['ALIGN_MIN']['unit']
        max_unit = data_list['ALIGN_MAX']['unit']
        mean_unit = data_list['ALIGN_MEAN']['unit']

        result_list = []

        for min_data, max_data, avg_data in zip(data_list['ALIGN_MIN']['timeSeries'], data_list['ALIGN_MAX']['timeSeries'], data_list['ALIGN_MEAN']['timeSeries']):

            result = self._make_metric_data(min_data, max_data, avg_data, min_unit, max_unit, mean_unit)
            result_list.append(result)

        return result_list

    @staticmethod
    def _make_metric_data(min_data, max_data, avg_data, min_unit, max_unit, mean_unit):
        result = []

        labels = min_data['resource'].get('labels')
        instance_name = min_data.get('metric').get('labels').get('instance_name')
        resource_id = 'projects/' + labels.get('project_id') + '/zones/' + labels.get('zone') + '/instances/' + instance_name

        for min_point, max_point, avg_point in zip(min_data['points'], max_data['points'], avg_data['points']):
            min_point['unit'] = min_unit
            max_point['unit'] = max_unit
            avg_point['unit'] = mean_unit

            data_format = {
                'provider': 'google_cloud',
                'metric_name': min_data['metric']['type'],
                'resource_id': resource_id,
                'timestamp': min_point['interval']['startTime'],
                'data': {
                    'min': min_point,
                    'max': max_point,
                    'avg': avg_point
                },
                'meta_data': {
                    'metric': min_data['metric'],
                    'resource': min_data['resource']
                }
            }

            result.append(data_format)

        return result
