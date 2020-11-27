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
from tests.mockups import transport_service_mock
from elkpy import transportcontroller as tc
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
service = transport_service_mock.TransportControllerServiceMockup()
SUSHI_GRPC.add_TransportControllerServicer_to_server(service, mock_server)
mock_server.add_insecure_port(SUSHI_ADDRESS)
mock_server.start()

class TestTransportController(unittest.TestCase):
    def setUp(self):
        self._tc = tc.TransportController(SUSHI_ADDRESS, proto_file)

    def test_get_samplerate(self):
        self.assertEqual(self._tc.get_samplerate(), transport_service_mock.expected_sample_rate)

    def test_get_playing_mode(self):
        self.assertEqual(self._tc.get_playing_mode(), transport_service_mock.expected_playing_mode)

    def test_get_sync_mode(self):
        self.assertEqual(self._tc.get_sync_mode(), transport_service_mock.expected_sync_mode)

    def test_get_tempo(self):
        self.assertEqual(self._tc.get_tempo(), transport_service_mock.expected_tempo)

    def test_get_time_signature(self):
        self.assertEqual(self._tc.get_time_signature(), transport_service_mock.expected_time_signature)

    def test_set_playing_mode_positive(self):
        self._tc.set_playing_mode(transport_service_mock.expected_playing_mode)
        self.assertTrue(service.was_called())
        expected_result = SUSHI_PROTO.PlayingMode(mode = transport_service_mock.expected_playing_mode)
        self.assertEqual(expected_result, service.get_recent_request())

    def test_set_sync_mode(self):
        self._tc.set_sync_mode(transport_service_mock.expected_sync_mode)
        self.assertTrue(service.was_called())
        expected_result = SUSHI_PROTO.SyncMode(mode = transport_service_mock.expected_sync_mode)
        self.assertEqual(expected_result, service.get_recent_request())

    def test_set_tempo(self):
        self._tc.set_tempo(transport_service_mock.expected_tempo)
        self.assertTrue(service.was_called())
        expected_result = SUSHI_PROTO.GenericFloatValue(value = transport_service_mock.expected_tempo)
        self.assertEqual(expected_result, service.get_recent_request())

    def test_set_time_signature(self):
        self._tc.set_time_signature(transport_service_mock.expected_time_signature[0],
                                    transport_service_mock.expected_time_signature[1])
        self.assertTrue(service.was_called())
        expected_result = SUSHI_PROTO.TimeSignature(
            numerator = transport_service_mock.expected_time_signature[0],
            denominator = transport_service_mock.expected_time_signature[1]
        )
        self.assertEqual(service.get_recent_request(), expected_result)
