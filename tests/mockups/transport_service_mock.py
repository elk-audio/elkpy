import grpc
import sushi_rpc_pb2 as proto
import sushi_rpc_pb2_grpc
from elkpy import sushi_info_types as info

expected_sample_rate = 48000
expected_playing_mode = info.PlayingMode.PLAYING
expected_sync_mode = info.SyncMode.INTERNAL
expected_time_signature = (4, 4)
expected_tempo = 120.0

class TransportControllerServiceMockup(sushi_rpc_pb2_grpc.TransportControllerServicer):

    def __init__(self):
        super().__init__()
        self.called = False
        self.recent_request = None

    def GetSamplerate(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericFloatValue(value = expected_sample_rate)

    def GetPlayingMode(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.PlayingMode(mode = expected_playing_mode)

    def GetSyncMode(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.SyncMode(mode = expected_sync_mode)

    def GetTimeSignature(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.TimeSignature(
            numerator = expected_time_signature[0],
            denominator = expected_time_signature[1]
            )

    def GetTempo(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericFloatValue(value = expected_tempo)

    def SetTempo(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def SetPlayingMode(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def SetSyncMode(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def SetTimeSignature(self, request, context):
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
