import logging

from spaceone.core.service import check_required
from spaceone.core.service import authentication_handler, BaseService
from spaceone.core.pygrpc.message_type import *
from spaceone.inventory.conf.metric_type_conf import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class MetricService(BaseService):

    #service main 로직
    @check_required(['secret_data'])
    def metric(self, params):
        # self._secret_data_chk(param.get('secret_data'))
        secret_data = params['secret_data']
        return self._metric_data_collect(secret_data)

    #metric 수집
    def _metric_data_collect(self, secret_data):
        gcp_mng = self.locator.get_manager('GoogleCloudManager')
        metric_list = self._metric_list_get()

        for metric in metric_list:
            result = gcp_mng.metric_data_collect(secret_data, metric)

            if result is None:
                continue

            if len(result) != 0:
                for metric_inst in result:
                    for metric_point in metric_inst:
                        yield self._convert_to_message(metric_point)

    #metric 조건 list
    @staticmethod
    def _metric_list_get() -> list:
        metric_type_groups = ['VM_Instance', 'Compute_Disk', 'SQL_Instance']

        metric_types = []
        for metric_type in metric_type_groups:
            if metric_type in METRIC_TYPE:
                metric_types.extend(item['value'] for item in METRIC_TYPE[metric_type])

        return metric_types

    @staticmethod
    def _convert_to_message(result_data):
        match_rules = {"1": ["metric_name", "provider", "resource_id", "timestamp"]}

        result = {
            # 'state': StringType(default="SUCCESS", choices=("SUCCESS", "FAILURE", "TIMEOUT")),
            # 'message': str(result_data),
            'resource_type': 'inventory.Metric',
            'match_rules': change_struct_type(match_rules),
            'resource': change_struct_type(result_data),
            # 'options': change_struct_type(resource.get('options', {}))
        }
        return result
