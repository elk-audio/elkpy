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

expected_input_connection = info.AudioConnection({})
expected_input_connection.track = 4
expected_input_connection.track_channel = 3
expected_input_connection.engine_channel = 2

expected_input_connections = [expected_input_connection, expected_input_connection]

grpc_input_connection = proto.AudioConnection(
    track=proto.TrackIdentifier(id=expected_input_connection.track),
    track_channel=expected_input_connection.track_channel,
    engine_channel=expected_input_connection.engine_channel
)

grpc_input_connections = proto.AudioConnectionList(connections = [grpc_input_connection, grpc_input_connection])

expected_output_connection = info.AudioConnection({})
expected_output_connection.track = 11
expected_output_connection.track_channel = 1
expected_output_connection.engine_channel = 0

expected_output_connections = [expected_output_connection, expected_output_connection]

grpc_output_connection = proto.AudioConnection(
    track=proto.TrackIdentifier(id=expected_output_connection.track),
    track_channel=expected_output_connection.track_channel,
    engine_channel=expected_output_connection.engine_channel
)

grpc_output_connections = proto.AudioConnectionList(connections = [grpc_output_connection, grpc_output_connection])

class AudioRoutingControllerServiceMockup(sushi_rpc_pb2_grpc.AudioRoutingControllerServicer):

    def __init__(self) -> None:
        super().__init__()
        self.called = False

    def GetAllInputConnections(self, request, context):
        return grpc_input_connections

    def GetAllOutputConnections(self, request, context):
        return grpc_output_connections

    def GetInputConnectionsForTrack(self, request, context):
        if request.id == expected_input_connection.track:
            return grpc_input_connections

    def GetOutputConnectionsForTrack(self, request, context):
        if request.id == expected_output_connection.track:
            return grpc_output_connections

    def ConnectInputChannelToTrack(self, request, context):
        if request == grpc_input_connection:
            self.called = True
        return proto.GenericVoidValue()

    def ConnectOutputChannelFromTrack(self, request, context):
        if request == grpc_output_connection:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectInput(self, request, context):
        if request == grpc_input_connection:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectOutput(self, request, context):
        if request == grpc_output_connection:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectAllInputsFromTrack(self, request, context):
        if request.id == expected_input_connection.track:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectAllOutputsFromTrack(self, request, context):
        if request.id == expected_output_connection.track:
            self.called = True
        return proto.GenericVoidValue()

    def was_called(self):
        result = self.called
        self.called = False
        return result
