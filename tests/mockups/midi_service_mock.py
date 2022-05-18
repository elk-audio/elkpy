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

expected_input_ports = 16
expected_output_ports = 7
expected_midi_clock_port = 1

expected_input_kbd_connection = info.MidiKbdConnection()
expected_input_kbd_connection.channel = 2
expected_input_kbd_connection.port = 3
expected_input_kbd_connection.raw_midi = True
expected_input_kbd_connection.track = 12

expected_input_kbd_connections = [expected_input_kbd_connection, expected_input_kbd_connection]

grpc_input_kbd_connection = proto.MidiKbdConnection(channel=proto.MidiChannel(channel=expected_input_kbd_connection.channel),
                                                    port=expected_input_kbd_connection.port,
                                                    raw_midi=expected_input_kbd_connection.raw_midi,
                                                    track=proto.TrackIdentifier(id=expected_input_kbd_connection.track))

grpc_input_kbd_connections = proto.MidiKbdConnectionList(connections=[grpc_input_kbd_connection, grpc_input_kbd_connection])

expected_output_kbd_connection = info.MidiKbdConnection()
expected_output_kbd_connection.channel = 4
expected_output_kbd_connection.port = 7
expected_output_kbd_connection.raw_midi = False
expected_output_kbd_connection.track = 21

expected_output_kbd_connections = [expected_output_kbd_connection, expected_output_kbd_connection]

grpc_output_kbd_connection = proto.MidiKbdConnection(channel=proto.MidiChannel(channel=expected_output_kbd_connection.channel),
                                                     port=expected_output_kbd_connection.port,
                                                     raw_midi=expected_output_kbd_connection.raw_midi,
                                                     track=proto.TrackIdentifier(id=expected_output_kbd_connection.track))

grpc_output_kbd_connections = proto.MidiKbdConnectionList(connections=[grpc_output_kbd_connection, grpc_output_kbd_connection])

expected_input_cc_connection = info.MidiCCConnection()
expected_input_cc_connection.port = 2
expected_input_cc_connection.cc_number = 77
expected_input_cc_connection.channel = 5
expected_input_cc_connection.max_range = 100
expected_input_cc_connection.min_range = -21
expected_input_cc_connection.parameter_id = 4
expected_input_cc_connection.processor_id = 9

expected_input_cc_connections = [expected_input_cc_connection, expected_input_cc_connection]

grpc_input_cc_connection = proto.MidiCCConnection(port=expected_input_cc_connection.port,
                                                  cc_number=expected_input_cc_connection.cc_number,
                                                  channel=proto.MidiChannel(channel=expected_input_cc_connection.channel),
                                                  min_range=expected_input_cc_connection.min_range,
                                                  max_range=expected_input_cc_connection.max_range,
                                                  parameter=proto.ParameterIdentifier(processor_id=expected_input_cc_connection.processor_id,
                                                                                      parameter_id=expected_input_cc_connection.parameter_id))

grpc_input_cc_connections = proto.MidiCCConnectionList(connections=[grpc_input_cc_connection, grpc_input_cc_connection])

expected_input_pc_connection = info.MidiPCConnection()
expected_input_pc_connection.channel = 64
expected_input_pc_connection.port = 2
expected_input_pc_connection.processor = 92

expected_input_pc_connections = [expected_input_pc_connection, expected_input_pc_connection]

grpc_input_pc_connection = proto.MidiPCConnection(channel=proto.MidiChannel(channel=expected_input_pc_connection.channel),
                                                  port=expected_input_pc_connection.port,
                                                  processor=proto.ProcessorIdentifier(id=expected_input_pc_connection.processor))

grpc_input_pc_connections = proto.MidiPCConnectionList(connections=[grpc_input_pc_connection, grpc_input_pc_connection])

class MidiControllerServiceMockup(sushi_rpc_pb2_grpc.MidiControllerServicer):

    def __init__(self) -> None:
        super().__init__()
        self.called = False

    def GetInputPorts(self, request, context):
        return proto.GenericIntValue(value=expected_input_ports)

    def GetOutputPorts(self, request, context):
        return proto.GenericIntValue(value=expected_output_ports)

    def GetAllKbdInputConnections(self, request, context):
        return grpc_input_kbd_connections

    def GetAllKbdOutputConnections(self, request, context):
        return grpc_output_kbd_connections

    def GetAllCCInputConnections(self, request, context):
        return grpc_input_cc_connections

    def GetAllPCInputConnections(self, request, context):
        return grpc_input_pc_connections

    def GetCCInputConnectionsForProcessor(self, request, context):
        if request.id == expected_input_cc_connection.processor_id:
            return grpc_input_cc_connections

    def GetPCInputConnectionsForProcessor(self, request, context):
        if request.id == expected_input_pc_connection.processor:
            return grpc_input_pc_connections

    def GetMidiClockOutputEnabled(self, request, context):
        return proto.GenericBoolValue(value = (request.value == expected_midi_clock_port))

    def SetMidiClockOutputEnabled(self, request, context):
        if request.port == expected_midi_clock_port:
            self.called = True
        return proto.GenericVoidValue()

    def ConnectKbdInputToTrack(self, request, context):
        if request.track.id == expected_input_kbd_connection.track \
        and request.channel.channel == expected_input_kbd_connection.channel \
        and request.port == expected_input_kbd_connection.port \
        and request.raw_midi == expected_input_kbd_connection.raw_midi:
            self.called = True
        return proto.GenericVoidValue()

    def ConnectKbdOutputFromTrack(self, request, context):
        if request.track.id == expected_output_kbd_connection.track \
        and request.channel.channel == expected_output_kbd_connection.channel \
        and request.port == expected_output_kbd_connection.port \
        and request.raw_midi == expected_output_kbd_connection.raw_midi:
            self.called = True
        return proto.GenericVoidValue()

    def ConnectCCToParameter(self, request, context):
        if request.parameter.processor_id == expected_input_cc_connection.processor_id \
        and request.parameter.parameter_id == expected_input_cc_connection.parameter_id \
        and request.channel.channel == expected_input_cc_connection.channel \
        and request.port == expected_input_cc_connection.port \
        and request.cc_number == expected_input_cc_connection.cc_number \
        and request.min_range == expected_input_cc_connection.min_range \
        and request.max_range == expected_input_cc_connection.max_range \
        and request.relative_mode == expected_input_cc_connection.relative_mode:
            self.called = True
        return proto.GenericVoidValue()

    def ConnectPCToProcessor(self, request, context):
        if request.processor.id == expected_input_pc_connection.processor \
        and request.channel == expected_input_pc_connection.channel \
        and request.port == expected_input_pc_connection.port:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectKbdInput(self, request, context):
        if request.track == expected_input_kbd_connection.track \
        and request.channel == expected_input_kbd_connection.channel \
        and request.port == expected_input_kbd_connection.port \
        and request.raw_midi == expected_input_kbd_connection.raw_midi:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectKbdOutput(self, request, context):
        if request.track == expected_input_kbd_connection.track \
        and request.channel == expected_input_kbd_connection.channel \
        and request.port == expected_input_kbd_connection.port \
        and request.raw_midi == expected_input_kbd_connection.raw_midi:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectCC(self, request, context):
        if request.parameter.processor_id == expected_input_cc_connection.processor_id \
        and request.parameter.parameter_id == expected_input_cc_connection.parameter_id \
        and request.channel.channel == expected_input_cc_connection.channel \
        and request.port == expected_input_cc_connection.port \
        and request.cc_number == expected_input_cc_connection.cc_number \
        and request.min_range == expected_input_cc_connection.min_range \
        and request.max_range == expected_input_cc_connection.max_range \
        and request.relative_mode == expected_input_cc_connection.relative_mode:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectPC(self, request, context):
        if request.processor.id == expected_input_pc_connection.processor \
        and request.channel == expected_input_pc_connection.channel \
        and request.port == expected_input_pc_connection.port:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectAllCCFromProcessor(self, request, context):
        if request.id == expected_input_cc_connection.processor_id:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectAllPCFromProcessor(self, request, context):
        if request.id == expected_input_pc_connection.processor:
            self.called = True
        return proto.GenericVoidValue()

    def was_called(self):
        result = self.called
        self.called = True
        return result