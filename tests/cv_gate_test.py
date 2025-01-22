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
from tests.mockups import cvgate_service_mock
from src.elkpy import cvgatecontroller as cgc
from src.elkpy import sushi_info_types as info_types

from src.elkpy import grpc_gen
from src.elkpy import sushierrors

proto_file = os.environ.get('SUSHI_GRPC_ELKPY_PROTO')
if proto_file is None:
    print("Environment variable SUSHI_GRPC_ELKPY_PROTO not defined, set it to point the .proto definition")
    sys.exit(-1)

SUSHI_PROTO, SUSHI_GRPC = grpc_gen.modules_from_proto(proto_file)

SUSHI_ADDRESS = ('localhost:51053')

mock_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
service = cvgate_service_mock.CvGateControllerServiceMockup()
SUSHI_GRPC.add_CvGateControllerServicer_to_server(service, mock_server)
mock_server.add_insecure_port(SUSHI_ADDRESS)
mock_server.start()

class TestCVGateController(unittest.TestCase):
    def setUp(self):
        self._cgc = cgc.CvGateController(SUSHI_ADDRESS, proto_file)

    def test_get_cv_input_channel_count(self):
        self.assertEqual(self._cgc.get_cv_input_channel_count(),
                        cvgate_service_mock.expected_cv_input_channel_count)

    def test_get_cv_input_channel_count(self):
        self.assertEqual(self._cgc.get_cv_output_channel_count(),
                         cvgate_service_mock.expected_cv_output_channel_count)

    def test_get_all_cv_input_connections(self):
        self.assertEqual(self._cgc.get_all_cv_input_connections(),
                         cvgate_service_mock.expected_input_cv_connections)

    def test_get_all_cv_output_connections(self):
        self.assertEqual(self._cgc.get_all_cv_input_connections(),
                         cvgate_service_mock.expected_input_cv_connections)

    def test_get_all_gate_input_connections(self):
        self.assertEqual(self._cgc.get_all_gate_input_connections(),
                         cvgate_service_mock.expected_input_gate_connections)

    def test_get_all_gate_output_connections(self):
        self.assertEqual(self._cgc.get_all_gate_input_connections(),
                         cvgate_service_mock.expected_input_gate_connections)

    def test_get_cv_input_connections_for_processor(self):
        self.assertEqual(self._cgc.get_cv_input_connections_for_processor(cvgate_service_mock.expected_input_cv_connection.processor_id),
                         cvgate_service_mock.expected_input_cv_connections)

    def test_get_cv_output_connections_for_processor(self):
        self.assertEqual(self._cgc.get_cv_output_connections_for_processor(cvgate_service_mock.expected_output_cv_connection.processor_id),
                         cvgate_service_mock.expected_output_cv_connections)

    def test_get_gate_input_connections_for_processor(self):
        self.assertEqual(self._cgc.get_gate_input_connections_for_processor(cvgate_service_mock.expected_input_gate_connection.processor_id),
                         cvgate_service_mock.expected_input_gate_connections)

    def test_get_gate_output_connections_for_processor(self):
        self.assertEqual(self._cgc.get_gate_output_connections_for_processor(cvgate_service_mock.expected_output_gate_connection.processor_id),
                         cvgate_service_mock.expected_output_gate_connections)

    def test_connect_cv_input_to_parameter(self):
        self._cgc.connect_cv_input_to_parameter(cvgate_service_mock.expected_input_cv_connection.processor_id,
                                                cvgate_service_mock.expected_input_cv_connection.parameter_id,
                                                cvgate_service_mock.expected_input_cv_connection.cv_port_id)
        self.assertTrue(service.was_called())

    def test_connect_cv_output_from_parameter(self):
        self._cgc.connect_cv_output_from_parameter(cvgate_service_mock.expected_output_cv_connection.processor_id,
                                                   cvgate_service_mock.expected_output_cv_connection.parameter_id,
                                                   cvgate_service_mock.expected_output_cv_connection.cv_port_id)
        self.assertTrue(service.was_called())

    def test_connect_gate_input_to_processor(self):
        self._cgc.connect_gate_input_to_processor(cvgate_service_mock.expected_input_gate_connection.processor_id,
                                                  cvgate_service_mock.expected_input_gate_connection.gate_port_id,
                                                  cvgate_service_mock.expected_input_gate_connection.channel,
                                                  cvgate_service_mock.expected_input_gate_connection.note_no)
        self.assertTrue(service.was_called())

    def test_connect_gate_output_from_processor(self):
        self._cgc.connect_gate_output_from_processor(cvgate_service_mock.expected_output_gate_connection.processor_id,
                                                  cvgate_service_mock.expected_output_gate_connection.gate_port_id,
                                                  cvgate_service_mock.expected_output_gate_connection.channel,
                                                  cvgate_service_mock.expected_output_gate_connection.note_no)
        self.assertTrue(service.was_called())

    def test_disconnect_cv_input(self):
        self._cgc.disconnect_cv_input(cvgate_service_mock.expected_input_cv_connection.processor_id,
                                      cvgate_service_mock.expected_input_cv_connection.parameter_id,
                                      cvgate_service_mock.expected_input_cv_connection.cv_port_id)
        self.assertTrue(service.was_called())

    def test_disconnect_cv_output(self):
        self._cgc.disconnect_cv_output(cvgate_service_mock.expected_output_cv_connection.processor_id,
                                       cvgate_service_mock.expected_output_cv_connection.parameter_id,
                                       cvgate_service_mock.expected_output_cv_connection.cv_port_id)
        self.assertTrue(service.was_called())

    def test_disconnect_gate_input(self):
        self._cgc.disconnect_gate_input(cvgate_service_mock.expected_input_gate_connection.processor_id,
                                        cvgate_service_mock.expected_input_gate_connection.gate_port_id,
                                        cvgate_service_mock.expected_input_gate_connection.channel,
                                        cvgate_service_mock.expected_input_gate_connection.note_no)
        self.assertTrue(service.was_called())

    def test_disconnect_gate_output(self):
        self._cgc.disconnect_gate_output(cvgate_service_mock.expected_output_gate_connection.processor_id,
                                         cvgate_service_mock.expected_output_gate_connection.gate_port_id,
                                         cvgate_service_mock.expected_output_gate_connection.channel,
                                         cvgate_service_mock.expected_output_gate_connection.note_no)
        self.assertTrue(service.was_called())

    def test_disconnect_all_cv_inputs_from_processor(self):
        self._cgc.disconnect_all_cv_inputs_from_processor(cvgate_service_mock.expected_input_cv_connection.processor_id)
        self.assertTrue(service.was_called())

    def test_disconnect_all_cv_outputs_from_processor(self):
        self._cgc.disconnect_all_cv_outputs_from_processor(cvgate_service_mock.expected_output_cv_connection.processor_id)
        self.assertTrue(service.was_called())

    def test_disconnect_all_gate_inputs_from_processor(self):
        self._cgc.disconnect_all_gate_inputs_from_processor(cvgate_service_mock.expected_input_gate_connection.processor_id)
        self.assertTrue(service.was_called())

    def test_disconnect_all_gate_outputs_from_processor(self):
        self._cgc.disconnect_all_gate_outputs_from_processor(cvgate_service_mock.expected_output_gate_connection.processor_id)
        self.assertTrue(service.was_called())
