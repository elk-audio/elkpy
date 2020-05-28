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
from tests.mockups import timing_service_mock
from elkpy import timingcontroller as tc
from elkpy import sushi_info_types as info_types

from elkpy import grpc_gen

proto_file = os.environ.get('SUSHI_GRPC_ELKPY_PROTO')
if proto_file is None:
    print("Environment variable SUSHI_GRPC_ELKPY_PROTO not defined, set it to point the .proto definition")
    sys.exit(-1)

SUSHI_PROTO, SUSHI_GRPC = grpc_gen.modules_from_proto(proto_file)

SUSHI_ADDRESS = ('localhost:51051')

# Run sushi with arguments: -j --connect-ports --timing-statistics -c ~/work/sushi/example_configs/config_temper.json
# The config file has andes followed by temper on a single stereo channel called main

mock_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
service = timing_service_mock.TimingControllerServiceMockup()
SUSHI_GRPC.add_TimingControllerServicer_to_server(service, mock_server)
mock_server.add_insecure_port(SUSHI_ADDRESS)
mock_server.start()

class TestTimingController(unittest.TestCase):
    def setUp(self):
        self._tc = tc.TimingController(SUSHI_ADDRESS, proto_file)

    def test_get_timings_enabled(self):
        self.assertEqual(self._tc.get_timings_enabled(), timing_service_mock.expected_timings_set)

    def test_set_timings_enabled(self):
        self._tc.set_timings_enabled(timing_service_mock.expected_timings_set)
        self.assertTrue(service.was_called())
        expected_request = SUSHI_PROTO.GenericBoolValue(value = timing_service_mock.expected_timings_set)
        self.assertEqual(service.get_recent_request(), expected_request)

    def test_get_engine_timings(self):
        self.assertEqual(self._tc.get_engine_timings(),
                         timing_service_mock.expected_cpu_timings)

    def test_get_track_timings(self):
        self.assertEqual(self._tc.get_track_timings(timing_service_mock.expected_id),
                         timing_service_mock.expected_cpu_timings)

        expected_request = SUSHI_PROTO.TrackIdentifier(id = timing_service_mock.expected_id)
        self.assertTrue(service.was_called())
        self.assertEqual(service.get_recent_request(), expected_request)

    def test_get_processor_timings(self):
        self.assertEqual(self._tc.get_processor_timings(timing_service_mock.expected_id),
                         timing_service_mock.expected_cpu_timings)

        expected_request = SUSHI_PROTO.ProcessorIdentifier(id = timing_service_mock.expected_id)
        self.assertTrue(service.was_called())
        self.assertEqual(service.get_recent_request(), expected_request)

    def test_reset_all_timings(self):
        self._tc.reset_all_timings()
        self.assertTrue(service.was_called())
        self.assertEqual(service.get_recent_request(), SUSHI_PROTO.GenericVoidValue())

    def test_reset_track_timings(self):
        self._tc.reset_track_timings(timing_service_mock.expected_id)
        self.assertTrue(service.was_called())

        expected_request = SUSHI_PROTO.TrackIdentifier(id = timing_service_mock.expected_id)
        self.assertEqual(service.get_recent_request(), expected_request)

    def test_reset_processor_timings(self):
        self._tc.reset_processor_timings(timing_service_mock.expected_id)
        self.assertTrue(service.was_called())

        expected_request = SUSHI_PROTO.ProcessorIdentifier(id = timing_service_mock.expected_id)
        self.assertEqual(service.get_recent_request(), expected_request)
