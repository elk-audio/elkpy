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
from tests.mockups import program_service_mock
from elkpy import programcontroller as pc
from elkpy import sushi_info_types as info_types

from elkpy import grpc_gen
from elkpy import sushierrors

proto_file = os.environ.get('SUSHI_GRPC_ELKPY_PROTO')
if proto_file is None:
    print("Environment variable SUSHI_GRPC_ELKPY_PROTO not defined, set it to point the .proto definition")
    sys.exit(-1)

SUSHI_PROTO, SUSHI_GRPC = grpc_gen.modules_from_proto(proto_file)

SUSHI_ADDRESS = ('localhost:51051')

# Run sushi with arguments: -j --connect-ports --timing-statistics -c ~/work/sushi/example_configs/config_temper.json
# The config file has andes followed by temper on a single stereo channel called main

mock_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
service = program_service_mock.ProgramControllerServiceMockup()
SUSHI_GRPC.add_ProgramControllerServicer_to_server(service, mock_server)
mock_server.add_insecure_port('localhost:51051')
mock_server.start()

class TestProgramController(unittest.TestCase):
    def setUp(self):
        self._pc = pc.ProgramController(SUSHI_ADDRESS, proto_file)

    def test_get_processor_current_program(self):
        self.assertEqual(self._pc.get_processor_current_program(program_service_mock.expected_processor_identifier.id),
                         program_service_mock.expected_program_1.id)

        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._pc.get_processor_current_program(-1)

    def test_get_processor_current_program_name(self):
        self.assertEqual(self._pc.get_processor_current_program_name(program_service_mock.expected_processor_identifier.id),
                         program_service_mock.expected_program_1.name)

        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._pc.get_processor_current_program_name(-1)

    def test_get_processor_program_name(self):
        self.assertEqual(self._pc.get_processor_program_name(
            program_service_mock.expected_processor_identifier.id,
            program_service_mock.expected_program_1.id),
            program_service_mock.expected_program_1.name)

        self.assertEqual(self._pc.get_processor_program_name(
            program_service_mock.expected_processor_identifier.id,
            program_service_mock.expected_program_2.id),
            program_service_mock.expected_program_2.name)

        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._pc.get_processor_program_name(-1, -1)

    def test_get_processor_programs(self):
        self.assertEqual(self._pc.get_processor_programs(program_service_mock.expected_processor_identifier.id),
                         [program_service_mock.expected_program_1, program_service_mock.expected_program_2])

        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._pc.get_processor_programs(-1)

    def test_set_processor_program(self):
        self._pc.set_processor_program(
            program_service_mock.expected_program_set_request.processor.id,
            program_service_mock.expected_program_set_request.program.program
        )

        self.assertTrue(service.was_called())
        self.assertEqual(service.get_recent_request(), program_service_mock.expected_program_set_request)
