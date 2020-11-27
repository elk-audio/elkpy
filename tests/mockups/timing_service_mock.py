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

expected_timings_set = False
expected_cpu_timings = (2.5,2,3)
expected_id = 2
class TimingControllerServiceMockup(sushi_rpc_pb2_grpc.TimingControllerServicer):

    def __init__(self):
        super().__init__()
        self.called = False
        self.recent_request = None

    def GetTimingsEnabled(self, request, context):
        return proto.GenericBoolValue(value = expected_timings_set)

    def SetTimingsEnabled(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def GetEngineTimings(self, request, context):
        return proto.CpuTimings(min = expected_cpu_timings[1],
                                max = expected_cpu_timings[2],
                                average = expected_cpu_timings[0])

    def GetTrackTimings(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.CpuTimings(min = expected_cpu_timings[1],
                                max = expected_cpu_timings[2],
                                average = expected_cpu_timings[0])

    def GetProcessorTimings(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.CpuTimings(min = expected_cpu_timings[1],
                                max = expected_cpu_timings[2],
                                average = expected_cpu_timings[0])

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
