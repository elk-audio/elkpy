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

import os
import sys
import unittest
import time
import grpc

from concurrent import futures
from tests.mockups import system_service_mock
from src.elkpy import systemcontroller as sc
from src.elkpy import sushi_info_types as info_types

from src.elkpy import grpc_gen
from src.elkpy import sushierrors

proto_file = os.environ.get('SUSHI_GRPC_ELKPY_PROTO')
if proto_file is None:
    print("Environment variable SUSHI_GRPC_ELKPY_PROTO not defined, set it to point the .proto definition")
    sys.exit(-1)

SUSHI_PROTO, SUSHI_GRPC = grpc_gen.modules_from_proto(proto_file)

SUSHI_ADDRESS = ('localhost:51060')

mock_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
service = system_service_mock.SystemControllerServiceMockup()
SUSHI_GRPC.add_SystemControllerServicer_to_server(service, mock_server)
mock_server.add_insecure_port(SUSHI_ADDRESS)
mock_server.start()

class TestSystemController(unittest.TestCase):
    def setUp(self):
        self._sc = sc.SystemController(SUSHI_ADDRESS, proto_file)

    def test_get_sushi_version(self):
        self.assertEqual(self._sc.get_sushi_version(),
                         system_service_mock.expected_build_info.version)

    def test_get_build_info(self):
        self.assertEqual(self._sc.get_build_info(),
                         system_service_mock.expected_build_info)

    def test_get_input_audio_channel_count(self):
        self.assertEqual(self._sc.get_input_audio_channel_count(),
                         system_service_mock.expected_input_channel_count)

    def test_get_output_audio_channel_count(self):
        self.assertEqual(self._sc.get_output_audio_channel_count(),
                         system_service_mock.expected_output_channel_count)

