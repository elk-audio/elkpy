import grpc
import sushi_rpc_pb2 as proto
import sushi_rpc_pb2_grpc
from elkpy import sushi_info_types as info

expected_track_id = 2
expected_channel = 4
expected_note = 42
expected_velocity = 0.4
expected_value = 0.2

class KeyboardControllerServiceMockup(sushi_rpc_pb2_grpc.KeyboardControllerServicer):

    def __init__(self):
        super().__init__()
        self.called = False
        self.recent_request = None

    def SendNoteOn(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def SendNoteOff(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def SendNoteAftertouch(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def SendAftertouch(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def SendPitchBend(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def SendModulation(self, request, context):
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
