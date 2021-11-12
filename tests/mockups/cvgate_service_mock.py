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

expected_cv_input_channel_count = 5
expected_cv_output_channel_count = 7

expected_input_cv_connection = info.CvConnection()
expected_input_cv_connection.cv_port_id = 2
expected_input_cv_connection.processor_id = 7
expected_input_cv_connection.parameter_id = 12

expected_input_cv_connections = [expected_input_cv_connection, expected_input_cv_connection]

grpc_input_cv_connection = proto.CvConnection(cv_port_id=expected_input_cv_connection.cv_port_id,
                                              parameter=proto.ParameterIdentifier(
                                                  parameter_id=expected_input_cv_connection.parameter_id,
                                                  processor_id=expected_input_cv_connection.processor_id
                                              ))

grpc_input_cv_connections = proto.CvConnectionList(connections=[grpc_input_cv_connection, grpc_input_cv_connection])

expected_output_cv_connection = info.CvConnection()
expected_output_cv_connection.cv_port_id = 4
expected_output_cv_connection.parameter_id = 8
expected_output_cv_connection.processor_id = 13

expected_output_cv_connections = [expected_output_cv_connection, expected_output_cv_connection]

grpc_output_cv_connection = proto.CvConnection(cv_port_id=expected_output_cv_connection.cv_port_id,
                                               parameter=proto.ParameterIdentifier(
                                                   parameter_id=expected_output_cv_connection.parameter_id,
                                                   processor_id=expected_output_cv_connection.processor_id
                                               ))

grpc_output_cv_connections = proto.CvConnectionList(connections=[grpc_output_cv_connection, grpc_output_cv_connection])

expected_input_gate_connection = info.GateConnection()
expected_input_gate_connection.channel = 3
expected_input_gate_connection.gate_port_id = 2
expected_input_gate_connection.note_no = 64
expected_input_gate_connection.processor_id = 34

expected_input_gate_connections = [expected_input_gate_connection, expected_input_gate_connection]

grpc_input_gate_connection = proto.GateConnection(channel=expected_input_gate_connection.channel,
                                                  gate_port_id=expected_input_gate_connection.gate_port_id,
                                                  note_no=expected_input_gate_connection.note_no,
                                                  processor=proto.ProcessorIdentifier(id=expected_input_gate_connection.processor_id)
                                                 )

grpc_input_gate_connections = proto.GateConnectionList(connections=[grpc_input_gate_connection, grpc_input_gate_connection])

expected_output_gate_connection = info.GateConnection()
expected_output_gate_connection.channel = 9
expected_output_gate_connection.gate_port_id = 7
expected_output_gate_connection.note_no = 62
expected_output_gate_connection.processor_id = 29

expected_output_gate_connections = [expected_output_gate_connection, expected_output_gate_connection]

grpc_output_gate_connection = proto.GateConnection(channel=expected_output_gate_connection.channel,
                                                   gate_port_id=expected_output_gate_connection.gate_port_id,
                                                   note_no=expected_output_gate_connection.note_no,
                                                   processor=proto.ProcessorIdentifier(id=expected_output_gate_connection.processor_id)
                                                   )

grpc_output_gate_connections = proto.GateConnectionList(connections=[grpc_output_gate_connection, grpc_output_gate_connection])

class CvGateControllerServiceMockup(sushi_rpc_pb2_grpc.CvGateControllerServicer):

    def __init__(self) -> None:
        super().__init__()
        self.called = False

    def GetCvInputChannelCount(self, request, context):
        return proto.GenericIntValue(value=expected_cv_input_channel_count)

    def GetCvOutputChannelCount(self, request, context):
        return proto.GenericIntValue(value=expected_cv_output_channel_count)

    def GetAllCvInputConnections(self, request, context):
        return grpc_input_cv_connections

    def GetAllCvOutputConnections(self, request, context):
        return grpc_output_cv_connections

    def GetAllGateInputConnections(self, request, context):
        return grpc_input_gate_connections

    def GetAllGateOutputConnections(self, request, context):
        return grpc_output_gate_connections

    def GetCvInputConnectionsForProcessor(self, request, context):
        if request.id == expected_input_cv_connection.processor_id:
            return grpc_input_cv_connections

    def GetCvOutputConnectionsForProcessor(self, request, context):
        if request.id == expected_output_cv_connection.processor_id:
            return grpc_output_cv_connections

    def GetGateInputConnectionsForProcessor(self, request, context):
        if request.id == expected_input_gate_connection.processor_id:
            return grpc_input_gate_connections

    def GetGateOutputConnectionsForProcessor(self, request, context):
        if request.id == expected_output_gate_connection.processor_id:
            return grpc_output_gate_connections

    def ConnectCvInputToParameter(self, request, context):
        if request.parameter.processor_id == expected_input_cv_connection.processor_id \
        and request.parameter.parameter_id == expected_input_cv_connection.parameter_id \
        and request.cv_port_id == expected_input_cv_connection.cv_port_id:
            self.called = True
        return proto.GenericVoidValue()

    def ConnectCvOutputFromParameter(self, request, context):
        if request.parameter.processor_id == expected_output_cv_connection.processor_id \
        and request.parameter.parameter_id == expected_output_cv_connection.parameter_id \
        and request.cv_port_id == expected_output_cv_connection.cv_port_id:
            self.called = True
        return proto.GenericVoidValue()

    def ConnectGateInputToProcessor(self, request, context):
        if request.processor.id == expected_input_gate_connection.processor_id \
        and request.channel == expected_input_gate_connection.channel \
        and request.note_no == expected_input_gate_connection.note_no \
        and request.gate_port_id == expected_input_gate_connection.gate_port_id:
            self.called = True
        return proto.GenericVoidValue()

    def ConnectGateOutputFromProcessor(self, request, context):
        if request.processor.id == expected_output_gate_connection.processor_id \
        and request.channel == expected_output_gate_connection.channel \
        and request.note_no == expected_output_gate_connection.note_no \
        and request.gate_port_id == expected_output_gate_connection.gate_port_id:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectCvInput(self, request, context):
        if request.parameter.processor_id == expected_input_cv_connection.processor_id \
        and request.parameter.parameter_id == expected_input_cv_connection.parameter_id \
        and request.cv_port_id == expected_input_cv_connection.cv_port_id:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectCvOutput(self, request, context):
        if request.parameter.processor_id == expected_output_cv_connection.processor_id \
        and request.parameter.parameter_id == expected_output_cv_connection.parameter_id \
        and request.cv_port_id == expected_output_cv_connection.cv_port_id:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectGateInput(self, request, context):
        if request.processor.id == expected_input_gate_connection.processor_id \
        and request.channel == expected_input_gate_connection.channel \
        and request.note_no == expected_input_gate_connection.note_no \
        and request.gate_port_id == expected_input_gate_connection.gate_port_id:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectGateOutput(self, request, context):
        if request.processor.id == expected_output_gate_connection.processor_id \
        and request.channel == expected_output_gate_connection.channel \
        and request.note_no == expected_output_gate_connection.note_no \
        and request.gate_port_id == expected_output_gate_connection.gate_port_id:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectAllCvInputsFromProcessor(self, request, context):
        if request.id == expected_input_cv_connection.processor_id:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectAllCvOutputsFromProcessor(self, request, context):
        if request.id == expected_output_cv_connection.processor_id:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectAllGateInputsFromProcessor(self, request, context):
        if request.id == expected_input_gate_connection.processor_id:
            self.called = True
        return proto.GenericVoidValue()

    def DisconnectAllGateOutputsFromProcessor(self, request, context):
        if request.id == expected_output_gate_connection.processor_id:
            self.called = True
        return proto.GenericVoidValue()

    def was_called(self):
        result = self.called
        self.called = False
        return result