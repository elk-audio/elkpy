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

expected_timings_set = False
expected_cpu_timings = proto.CpuTimings(
    main=proto.Timings(
        max=1.0,
        min=0.8,
        average=22.8,
    ),
    threads=[
        proto.Timings(
            max=10.5,
            min=5.0,
            average=28.5,
        ),
        proto.Timings(
            max=1.88,
            min=0.9,
            average=2.5,
        ),
    ],
)
expected_processor_timings = proto.Timings(
    max=1.88,
    min=0.9,
    average=2.5,
)

expected_id = 2
success_command_response = proto.CommandResponse(
    status=proto.CommandStatus(status=1), id=42
)


class TimingControllerServiceMockup(sushi_rpc_pb2_grpc.TimingControllerServicer):
    def __init__(self):
        super().__init__()
        self.called = False
        self.recent_request = None

    def GetTimingsEnabled(self, request, context):
        return proto.GenericBoolValue(value=expected_timings_set)

    def SetTimingsEnabled(self, request, context):
        self.called = True
        self.recent_request = request
        return success_command_response

    def GetEngineTimings(self, request, context):
        return expected_cpu_timings

    def GetTrackTimings(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.TimingResponse(
            status=proto.CommandStatus(status=1),
            timings=proto.Timings(
                max=1.88,
                min=0.9,
                average=2.5,
            ),
        )

    def GetProcessorTimings(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.TimingResponse(
            status=proto.CommandStatus(status=1),
            timings=proto.Timings(
                max=1.88,
                min=0.9,
                average=2.5,
            ),
        )

    def ResetAllTimings(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def ResetTrackTimings(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def ResetProcessorTimings(self, request, context):
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
