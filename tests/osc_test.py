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
from tests.mockups import osc_service_mock
from src.elkpy import osccontroller as oc
from src.elkpy import sushi_info_types as info_types

from src.elkpy import grpc_gen
from src.elkpy import sushierrors

proto_file = os.environ.get("SUSHI_GRPC_ELKPY_PROTO")
if proto_file is None:
    print(
        "Environment variable SUSHI_GRPC_ELKPY_PROTO not defined, set it to point the .proto definition"
    )
    sys.exit(-1)

SUSHI_PROTO, SUSHI_GRPC = grpc_gen.modules_from_proto(proto_file)

SUSHI_ADDRESS = "localhost:51057"

mock_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
service = osc_service_mock.OscControllerServiceMockup()
SUSHI_GRPC.add_OscControllerServicer_to_server(service, mock_server)
mock_server.add_insecure_port(SUSHI_ADDRESS)
mock_server.start()


class TestOscController(unittest.TestCase):
    def setUp(self):
        self._oc = oc.OscController(SUSHI_ADDRESS, proto_file)

    def test_get_send_port(self):
        self.assertEqual(
            self._oc.get_send_port(), osc_service_mock.expected_osc_send_port
        )

    def test_get_receive_port(self):
        self.assertEqual(
            self._oc.get_receive_port(), osc_service_mock.expected_osc_receive_port
        )

    def test_get_enabled_parameter_outputs(self):
        self.assertEqual(
            self._oc.get_enabled_parameter_outputs(),
            osc_service_mock.expected_osc_parameter_outputs,
        )

    def test_enable_output_for_parameter(self):
        self._oc.enable_output_for_parameter(
            osc_service_mock.expected_processor_id,
            osc_service_mock.expected_parameter_id,
        )
        self.assertTrue(service.was_called())

    def test_disable_output_for_parameter(self):
        self._oc.enable_output_for_parameter(
            osc_service_mock.expected_processor_id,
            osc_service_mock.expected_parameter_id,
        )
        self.assertTrue(service.was_called())

    def test_enable_all_output(self):
        self._oc.enable_all_output()
        self.assertTrue(service.was_called())

    def test_disable_all_output(self):
        self._oc.enable_all_output()
        self.assertTrue(service.was_called())
