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

expected_processor_identifier = proto.ProcessorIdentifier(
    id = 12
)

expected_program_1 = info.ProgramInfo({})
expected_program_1.name = "Test program 1"
expected_program_1.id = 1

grpc_program_1 = proto.ProgramInfo(
    name = expected_program_1.name,
    id = proto.ProgramIdentifier(program = expected_program_1.id)
)

expected_program_2 = info.ProgramInfo({})
expected_program_2.name = "Test program 2"
expected_program_2.id = 2

grpc_program_2 = proto.ProgramInfo(
    name = expected_program_2.name,
    id = proto.ProgramIdentifier(program = expected_program_2.id)
)

expected_program_set_request = proto.ProcessorProgramSetRequest(
    processor = proto.ProcessorIdentifier(id = 5),
    program = proto.ProgramIdentifier(program = 7)
)

class ProgramControllerServiceMockup(sushi_rpc_pb2_grpc.ProgramControllerServicer):

    def __init__(self):
        super().__init__()
        self.called = False
        self.recent_request = None

    def GetProcessorCurrentProgram(self, request, context):
        if request.id == expected_processor_identifier.id:
            return proto.GenericIntValue(value = expected_program_1.id)
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "No processor with id {}".format(request.id))

    def GetProcessorCurrentProgramName(self, request, context):
        if request.id == expected_processor_identifier.id:
            return proto.GenericStringValue(value = expected_program_1.name)
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "No processor with id {}".format(request.id))

    def GetProcessorProgramName(self, request, context):
        if request.processor.id == expected_processor_identifier.id:
            if request.program == expected_program_1.id:
                return proto.GenericStringValue(value = expected_program_1.name)
            elif request.program == expected_program_2.id:
                return proto.GenericStringValue(value = expected_program_2.name)
            else:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, "No program with id {}".format(request.program))
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "No processor with id {}".format(request.processor.id))

    def GetProcessorPrograms(self, request, context):
        if request.id == expected_processor_identifier.id:
            return proto.ProgramInfoList(programs = [grpc_program_1, grpc_program_2])
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "No processor with id {}".format(request.id))

    def SetProcessorProgram(self, request, context):
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
