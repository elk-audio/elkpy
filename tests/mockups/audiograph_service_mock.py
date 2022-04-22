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
from elkpy import sushi_info_types as info

expected_processor_1 = info.ProcessorInfo()
expected_processor_1.id = 1
expected_processor_1.label = "Test plugin 1"
expected_processor_1.name = "test_plugin_1"
expected_processor_1.parameter_count = 1
expected_processor_1.program_count = 1

expected_processor_1_bypass = True

expected_processor_2 = info.ProcessorInfo()
expected_processor_2.id = 2
expected_processor_2.label = "Test plugin 2"
expected_processor_2.name = "test_plugin_2"
expected_processor_2.parameter_count = 2
expected_processor_2.program_count = 2

expected_processor_2_bypass = False

grpc_proc_1 = proto.ProcessorInfo(
    id = expected_processor_1.id,
    label = expected_processor_1.label,
    name = expected_processor_1.name,
    parameter_count = expected_processor_1.parameter_count,
    program_count = expected_processor_1.program_count
)

grpc_proc_2 = proto.ProcessorInfo(
    id = expected_processor_2.id,
    label = expected_processor_2.label,
    name = expected_processor_2.name,
    parameter_count = expected_processor_2.parameter_count,
    program_count = expected_processor_2.program_count
)

grpc_proc_list = proto.ProcessorInfoList(processors = [grpc_proc_1, grpc_proc_2])

expected_track_1 = info.TrackInfo()
expected_track_1.id = 1
expected_track_1.label = "Test track 1"
expected_track_1.name = "test_plugin_1"
expected_track_1.input_channels = 1
expected_track_1.input_busses = 1
expected_track_1.output_channels = 1
expected_track_1.output_busses = 1
expected_track_1.processors = [1, 2]

expected_track_2 = info.TrackInfo()
expected_track_2.id = 2
expected_track_2.label = "Test track 2"
expected_track_2.name = "test_plugin_2"
expected_track_2.input_channels = 2
expected_track_2.input_busses = 2
expected_track_2.output_channels = 2
expected_track_2.output_busses = 2
expected_track_2.processors = [1, 2]

grpc_track_1 = proto.TrackInfo(
    id = expected_track_1.id,
    label = expected_track_1.label,
    name = expected_track_1.name,
    input_channels = expected_track_1.input_channels,
    input_busses = expected_track_1.input_busses,
    output_channels = expected_track_1.output_channels,
    output_busses = expected_track_1.output_busses,
    processors = [proto.ProcessorIdentifier(id = expected_track_1.processors[0]),
                  proto.ProcessorIdentifier(id = expected_track_1.processors[1])]
)

grpc_track_2 = proto.TrackInfo(
    id = expected_track_2.id,
    label = expected_track_2.label,
    name = expected_track_2.name,
    input_channels = expected_track_2.input_channels,
    input_busses = expected_track_2.input_busses,
    output_channels = expected_track_2.output_channels,
    output_busses = expected_track_2.output_busses,
    processors = [proto.ProcessorIdentifier(id = expected_track_2.processors[0]),
                  proto.ProcessorIdentifier(id = expected_track_2.processors[1])]
)

grpc_track_list = proto.TrackInfoList(tracks = [grpc_track_1, grpc_track_2])

expected_proc_bypass_request = proto.ProcessorBypassStateSetRequest(
    processor = proto.ProcessorIdentifier(id = 1),
    value = True
)

expected_processor_state = info.ProcessorState
expected_processor_state.program_id = 5
expected_processor_state.bypassed = False
expected_processor_state.properties = []
expected_processor_state.parameters = [(0, 0.5), (1, 1.0)]
expected_processor_state.binary_data = bytes()

expected_create_track_request = proto.CreateTrackRequest(
    name = "test_track_3",
    channels = 3
)

expected_create_multibus_request = proto.CreateMultibusTrackRequest(
    name = "test_multibus",
    output_busses = 12,
    input_busses = 16
)

expected_create_processor_request = proto.CreateProcessorRequest(
    name = "test_processor_3",
    uid = "sushi.internal.test",
    path = "/test/path",
    type = proto.PluginType(type = 2),
    track = proto.TrackIdentifier(id = 1),
    position = proto.ProcessorPosition(add_to_back = False,
                                       before_processor = proto.ProcessorIdentifier(id = 1))
)

expected_move_processor_request = proto.MoveProcessorRequest(
    processor = proto.ProcessorIdentifier(id = 1),
    source_track = proto.TrackIdentifier(id = 1),
    dest_track = proto.TrackIdentifier(id = 2),
    position = proto.ProcessorPosition(add_to_back = True,
                                       before_processor = proto.ProcessorIdentifier(id = 1))
)

expected_delete_processor_request = proto.DeleteProcessorRequest(
    processor = proto.ProcessorIdentifier(id = 2),
    track = proto.TrackIdentifier(id = 1)
)

class AudioGraphControllerServiceMockup(sushi_rpc_pb2_grpc.AudioGraphControllerServicer):

    def __init__(self):
        super().__init__()
        self.called = False
        self.recent_request = None

    def GetAllProcessors(self, request, context):
        return grpc_proc_list

    def GetAllTracks(self, request, context):
        return grpc_track_list

    def GetTrackId(self, request, context):
        if request.value == expected_track_1.name:
            return proto.TrackIdentifier(id = grpc_track_1.id)
        elif request.value == expected_track_2.name:
            return proto.TrackIdentifier(id = grpc_track_2.id)
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "{} is not a track name".format(request.value))

    def GetTrackInfo(self, request, context):
        if request.id == expected_track_1.id:
            return grpc_track_1
        elif request.id == expected_track_2.id:
            return grpc_track_2
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "{} is not a track id".format(request.id))

    def GetTrackProcessors(self, request, context):
        if request.id == 1 or request.id == 2:
            return grpc_proc_list
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "{} is not a track id".format(request.id))

    def GetProcessorId(self, request, context):
        if request.value == expected_processor_1.name:
            return proto.ProcessorIdentifier(id = grpc_proc_1.id)
        elif request.value == expected_processor_2.name:
            return proto.ProcessorIdentifier(id = grpc_proc_2.id)
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "{} is not a processor name".format(request.value))

    def GetProcessorInfo(self, request, context):
        if request.id == expected_processor_1.id:
            return grpc_proc_1
        elif request.id == expected_processor_2.id:
            return grpc_proc_2
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "{} is not a processor id".format(request.id))

    def GetProcessorBypassState(self, request, context):
        if request.id == expected_processor_1.id:
            return proto.GenericBoolValue(value = expected_processor_1_bypass)
        elif request.id == expected_processor_2.id:
            return proto.GenericBoolValue(value = expected_processor_2_bypass)
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "{} is not a processor id".format(request.id))

    def GetProcessorState(self, request, context):
        if request.id == expected_processor_1.id or request.id == expected_processor_2.id:
            state = proto.ProcessorState()

            state.program_id.value = expected_processor_state.program_id
            state.program_id.has_value = True
            state.bypassed.value = expected_processor_state.bypassed
            state.bypassed.has_value = True
            for parameter in expected_processor_state.parameters:
                state_param = state.parameters.add()
                state_param.parameter.parameter_id = parameter[0]
                state_param.value = parameter[1]

            return state
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "{} is not a processor id".format(request.id))

    def SetProcessorBypassState(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def CreateTrack(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def CreateMultibusTrack(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def CreateProcessorOnTrack(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def MoveProcessorOnTrack(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def DeleteProcessorFromTrack(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def DeleteTrack(self, request, context):
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
