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
from tests.mockups import parameter_service_mock
from elkpy import parametercontroller as pc
from elkpy import sushi_info_types as info_types

from elkpy import grpc_gen
from elkpy import sushierrors

proto_file = os.environ.get('SUSHI_GRPC_ELKPY_PROTO')
if proto_file is None:
    print("Environment variable SUSHI_GRPC_ELKPY_PROTO not defined, set it to point the .proto definition")
    sys.exit(-1)

SUSHI_PROTO, SUSHI_GRPC = grpc_gen.modules_from_proto(proto_file)

SUSHI_ADDRESS = ('localhost:51051')

mock_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
service = parameter_service_mock.ParameterControllerServiceMockup()
SUSHI_GRPC.add_ParameterControllerServicer_to_server(service, mock_server)
mock_server.add_insecure_port(SUSHI_ADDRESS)
mock_server.start()

class TestParameterController(unittest.TestCase):
    def setUp(self):
        self._pc = pc.ParameterController(SUSHI_ADDRESS, proto_file)

    def test_get_track_parameters(self):
        self.assertEqual(self._pc.get_track_parameters(
            parameter_service_mock.expected_track_identifier),
            [parameter_service_mock.expected_parameter_1,
            parameter_service_mock.expected_parameter_2])

        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._pc.get_track_parameters(-1)

    def test_get_processor_parameters(self):
        self.assertEqual(self._pc.get_processor_parameters(
            parameter_service_mock.expected_processor_identifier),
            [parameter_service_mock.expected_parameter_1,
            parameter_service_mock.expected_parameter_2])

        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._pc.get_processor_parameters(-1)

    def test_get_parameter_id(self):
        self.assertEqual(self._pc.get_parameter_id(
            parameter_service_mock.expected_processor_identifier,
            parameter_service_mock.expected_parameter_1.name),
            parameter_service_mock.expected_parameter_1.id)

        self.assertEqual(self._pc.get_parameter_id(
            parameter_service_mock.expected_processor_identifier,
            parameter_service_mock.expected_parameter_2.name),
            parameter_service_mock.expected_parameter_2.id)

        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._pc.get_parameter_id(-1, "invalid_name")

    def test_get_parameter_info(self):
        self.assertEqual(self._pc.get_parameter_info(
            parameter_service_mock.expected_processor_identifier,
            parameter_service_mock.expected_parameter_1.id),
            parameter_service_mock.expected_parameter_1)

        self.assertEqual(self._pc.get_parameter_info(
            parameter_service_mock.expected_processor_identifier,
            parameter_service_mock.expected_parameter_2.id),
            parameter_service_mock.expected_parameter_2)

        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._pc.get_parameter_info(-1,-1)

    def test_get_parameter_value(self):
        self.assertAlmostEqual(self._pc.get_parameter_value(
            parameter_service_mock.expected_processor_identifier,
            parameter_service_mock.expected_parameter_1.id),
            parameter_service_mock.expected_parameter_1_value)

        self.assertAlmostEqual(self._pc.get_parameter_value(
            parameter_service_mock.expected_processor_identifier,
            parameter_service_mock.expected_parameter_2.id),
            parameter_service_mock.expected_parameter_2_value)

        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._pc.get_parameter_value(-1, -1)

    def test_get_parameter_value_in_domain(self):
        self.assertEqual(self._pc.get_parameter_value_in_domain(
            parameter_service_mock.expected_processor_identifier,
            parameter_service_mock.expected_parameter_1.id),
            parameter_service_mock.expected_parameter_1_value_in_domain)

        self.assertEqual(self._pc.get_parameter_value_in_domain(
            parameter_service_mock.expected_processor_identifier,
            parameter_service_mock.expected_parameter_2.id),
            parameter_service_mock.expected_parameter_2_value_in_domain)

        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._pc.get_parameter_value_in_domain(-1, -1)

    def test_get_parameter_value_as_string(self):
        self.assertEqual(self._pc.get_parameter_value_as_string(
            parameter_service_mock.expected_processor_identifier,
            parameter_service_mock.expected_parameter_1.id),
            str(parameter_service_mock.expected_parameter_1_value))

        self.assertEqual(self._pc.get_parameter_value_as_string(
            parameter_service_mock.expected_processor_identifier,
            parameter_service_mock.expected_parameter_2.id),
            str(parameter_service_mock.expected_parameter_2_value))

        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._pc.get_parameter_value_as_string(-1, -1)

    def test_set_parameter_value(self):
        self._pc.set_parameter_value(
            parameter_service_mock.expected_parameter_value_request.parameter.processor_id,
            parameter_service_mock.expected_parameter_value_request.parameter.parameter_id,
            parameter_service_mock.expected_parameter_value_request.value
        )
        self.assertTrue(service.was_called())
        self.assertEqual(service.get_recent_request(), parameter_service_mock.expected_parameter_value_request)
