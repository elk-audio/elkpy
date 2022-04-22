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

import os
import sys
import unittest
import time
import grpc

from concurrent import futures
from tests.mockups import session_service_mock
from elkpy import sessioncontroller as sc
from elkpy import sushi_info_types as info_types

from elkpy import grpc_gen
from elkpy import sushierrors

proto_file = os.environ.get('SUSHI_GRPC_ELKPY_PROTO')
if proto_file is None:
    print("Environment variable SUSHI_GRPC_ELKPY_PROTO not defined, set it to point the .proto definition")
    sys.exit(-1)

SUSHI_PROTO, SUSHI_GRPC = grpc_gen.modules_from_proto(proto_file)

SUSHI_ADDRESS = ('localhost:51060')

mock_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
service = system_service_mock.SessionControllerServiceMockup()
SUSHI_GRPC.add_SessionControllerServicer_to_server(service, mock_server)
mock_server.add_insecure_port(SUSHI_ADDRESS)
mock_server.start()

class TestSessionController(unittest.TestCase):
    def setUp(self):
        self._sc = sc.SessionController(SUSHI_ADDRESS, proto_file)

    def test_save_session(self):
        self.assertEqual(self._sc.save_binary_session(),
                         session_service_mock.expected_binary_session)

    def test_restore_state(self):
        self.assertEqual(self._sc.restore_binary_session(session_service_mock.expected_binary_session),
                         0)

