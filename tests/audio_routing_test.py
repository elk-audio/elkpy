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
from tests.mockups import audiorouting_service_mock
from src.elkpy import audioroutingcontroller as arc
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

SUSHI_ADDRESS = "localhost:51052"

mock_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
service = audiorouting_service_mock.AudioRoutingControllerServiceMockup()
SUSHI_GRPC.add_AudioRoutingControllerServicer_to_server(service, mock_server)
mock_server.add_insecure_port(SUSHI_ADDRESS)
mock_server.start()


class TestAudioRoutingController(unittest.TestCase):
    def setUp(self):
        self._arc = arc.AudioRoutingController(SUSHI_ADDRESS, proto_file)

    def test_get_all_input_connections(self):
        self.assertEqual(
            self._arc.get_all_input_connections(),
            audiorouting_service_mock.expected_input_connections,
        )

    def test_get_all_output_connections(self):
        self.assertEqual(
            self._arc.get_all_output_connections(),
            audiorouting_service_mock.expected_output_connections,
        )

    def test_get_input_connections_for_track(self):
        self.assertEqual(
            self._arc.get_input_connections_for_track(
                audiorouting_service_mock.expected_input_connection.track
            ),
            audiorouting_service_mock.expected_input_connections,
        )

    def test_get_output_connections_for_track(self):
        self.assertEqual(
            self._arc.get_output_connections_for_track(
                audiorouting_service_mock.expected_output_connection.track
            ),
            audiorouting_service_mock.expected_output_connections,
        )

    def test_connect_input_channel_to_track(self):
        self._arc.connect_input_channel_to_track(
            audiorouting_service_mock.expected_input_connection.track,
            audiorouting_service_mock.expected_input_connection.track_channel,
            audiorouting_service_mock.expected_input_connection.engine_channel,
        )
        self.assertTrue(service.was_called())

    def test_connect_output_channel_from_track(self):
        self._arc.connect_output_channel_from_track(
            audiorouting_service_mock.expected_output_connection.track,
            audiorouting_service_mock.expected_output_connection.track_channel,
            audiorouting_service_mock.expected_output_connection.engine_channel,
        )
        self.assertTrue(service.was_called())

    def test_disconnect_input(self):
        self._arc.disconnect_input(
            audiorouting_service_mock.expected_input_connection.track,
            audiorouting_service_mock.expected_input_connection.track_channel,
            audiorouting_service_mock.expected_input_connection.engine_channel,
        )
        self.assertTrue(service.was_called())

    def test_disconnect_output(self):
        self._arc.disconnect_output(
            audiorouting_service_mock.expected_output_connection.track,
            audiorouting_service_mock.expected_output_connection.track_channel,
            audiorouting_service_mock.expected_output_connection.engine_channel,
        )
        self.assertTrue(service.was_called())

    def test_disconnect_all_inputs_from_track(self):
        self._arc.disconnect_all_inputs_from_track(
            audiorouting_service_mock.expected_input_connection.track
        )
        self.assertTrue(service.was_called())

    def test_disconnect_all_outputs_from_track(self):
        self._arc.disconnect_all_outputs_from_track(
            audiorouting_service_mock.expected_output_connection.track
        )
        self.assertTrue(service.was_called())
