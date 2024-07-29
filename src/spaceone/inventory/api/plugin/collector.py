from spaceone.api.inventory.plugin import collector_pb2_grpc, collector_pb2
from spaceone.core.pygrpc import BaseAPI

from spaceone.inventory.service.metric_service import MetricService


class Collector(BaseAPI, collector_pb2_grpc.CollectorServicer):
    pb2 = collector_pb2
    pb2_grpc = collector_pb2_grpc

    def collect(self, request, context):
        params, metadata = self.parse_request(request, context)
        metric_svc: MetricService = self.locator.get_service('MetricService', params)

        with metric_svc:
            # 성능 수집 서비스 호출
            result_data = metric_svc.metric(params)

            for result in result_data:
                yield self.locator.get_info('ResourceInfo', result)
