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
