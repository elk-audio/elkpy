import grpc
import sushi_rpc_pb2 as proto
import sushi_rpc_pb2_grpc
from elkpy import sushi_info_types as info

expected_timings_set = False
expected_cpu_timings = (2.5,2,3)
expected_id = 2
class TimingControllerServiceMockup(sushi_rpc_pb2_grpc.TimingControllerServicer):

    def __init__(self):
        super().__init__()
        self.called = False
        self.recent_request = None

    def GetTimingsEnabled(self, request, context):
        return proto.GenericBoolValue(value = expected_timings_set)

    def SetTimingsEnabled(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def GetEngineTimings(self, request, context):
        return proto.CpuTimings(min = expected_cpu_timings[1],
                                max = expected_cpu_timings[2],
                                average = expected_cpu_timings[0])

    def GetTrackTimings(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.CpuTimings(min = expected_cpu_timings[1],
                                max = expected_cpu_timings[2],
                                average = expected_cpu_timings[0])

    def GetProcessorTimings(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.CpuTimings(min = expected_cpu_timings[1],
                                max = expected_cpu_timings[2],
                                average = expected_cpu_timings[0])

    def ResetAllTimings(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def ResetTrackTimings(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def ResetProcessorTimings(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def was_called(self):
        temp = self.called
        self.called = False
        return temp

    def get_recent_request(self):
        temp = self.recent_request
        self.recent_request = None
        return temp
