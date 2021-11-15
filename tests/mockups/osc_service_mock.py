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

expected_osc_send_port = 24024
expected_osc_receive_port = 24023

expected_osc_parameter_outputs = ["proc1/param1", "proc1/param2", "proc2/param1"]

expected_processor_id = 5
expected_parameter_id = 2

class OscControllerServiceMockup(sushi_rpc_pb2_grpc.OscControllerServicer):

    def __init__(self) -> None:
        super().__init__()
        self.called = False

    def GetSendPort(self, request, context):
        return proto.GenericIntValue(value=expected_osc_send_port)

    def GetReceivePort(self, request, context):
        return proto.GenericIntValue(value=expected_osc_receive_port)

    def GetEnabledParameterOutputs(self, request, context):
        return proto.OscParameterOutputList(path=expected_osc_parameter_outputs)

    def EnableOutputForParameter(self, request, context):
        if request.processor_id == expected_processor_id \
        and request.parameter_id == expected_parameter_id:
            self.called = True
        return proto.GenericVoidValue()

    def DisableOutputForParameter(self, request, context):
        if request.processor_id == expected_processor_id \
        and request.parameter_id == expected_parameter_id:
            self.called = True
        return proto.GenericVoidValue()

    def EnableAllOutput(self, request, context):
        self.called = True
        return proto.GenericVoidValue()

    def DisableAllOutput(self, request, context):
        self.called = True
        return proto.GenericVoidValue()

    def was_called(self):
        result = self.called
        self.called = False
        return result