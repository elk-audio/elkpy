__author__ = "Gustav Andersson"
__copyright__ = """

    Copyright 2017-2022 Modern Ancient Instruments Networked AB, dba Elk

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

expected_session = proto.SessionState()
expected_binary_session = expected_session.SerializeToString()

class SessionControllerServiceMockup(sushi_rpc_pb2_grpc.SessionControllerServicer):

    def __init__(self) -> None:
        super().__init__()

    def SaveSession(self, request, context):
        return proto.SessionState()

    def RestoreSession(self, request, context):
        return proto.GenericVoidValue()
