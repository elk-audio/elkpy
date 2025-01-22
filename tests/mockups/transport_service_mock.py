__author__ = "Ruben Svensson"
__copyright__ = """

    Copyright 2017-2019 Modern Ancient Instruments Networked AB, dba Elk

    elkpy is free software: you can redistribute it and/or modify it under the terms of the
    GNU General Public License as published by the Free Software Foundation, either version 3
    of the License, or (at your option) any later version.

    elkpy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
    even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with elkpy.  If
    not, see <http://www.gnu.org/licenses/>.
"""
__license__ = "GPL-3.0"

import grpc
import sushi_rpc_pb2 as proto
import sushi_rpc_pb2_grpc
from src.elkpy import sushi_info_types as info

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
