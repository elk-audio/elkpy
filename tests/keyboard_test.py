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
from tests.mockups import keyboard_service_mock
from elkpy import keyboardcontroller as kc
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
service = keyboard_service_mock.KeyboardControllerServiceMockup()
SUSHI_GRPC.add_KeyboardControllerServicer_to_server(service, mock_server)
mock_server.add_insecure_port('localhost:51051')
mock_server.start()

class TestKeyboardController(unittest.TestCase):
    def setUp(self):
        self._kc = kc.KeyboardController(SUSHI_ADDRESS, proto_file)

    def test_send_note_on(self):
        self._kc.send_note_on(
            keyboard_service_mock.expected_track_id,
            keyboard_service_mock.expected_channel,
            keyboard_service_mock.expected_note,
            keyboard_service_mock.expected_velocity)

        self.assertTrue(service.was_called())

        expected_request = SUSHI_PROTO.NoteOnRequest(
            track = SUSHI_PROTO.TrackIdentifier(
                id = keyboard_service_mock.expected_track_id),
            channel = keyboard_service_mock.expected_channel,
            note = keyboard_service_mock.expected_note,
            velocity = keyboard_service_mock.expected_velocity)

        self.assertEqual(service.get_recent_request(), expected_request)

    def test_send_note_off(self):
        self._kc.send_note_off(
            keyboard_service_mock.expected_track_id,
            keyboard_service_mock.expected_channel,
            keyboard_service_mock.expected_note,
            keyboard_service_mock.expected_velocity)

        self.assertTrue(service.was_called())

        expected_request = SUSHI_PROTO.NoteOffRequest(
            track = SUSHI_PROTO.TrackIdentifier(
                id = keyboard_service_mock.expected_track_id),
            channel = keyboard_service_mock.expected_channel,
            note = keyboard_service_mock.expected_note,
            velocity = keyboard_service_mock.expected_velocity)

        self.assertEqual(service.get_recent_request(), expected_request)

    def test_send_note_aftertouch(self):
        self._kc.send_note_aftertouch(
            keyboard_service_mock.expected_track_id,
            keyboard_service_mock.expected_channel,
            keyboard_service_mock.expected_note,
            keyboard_service_mock.expected_value)

        self.assertTrue(service.was_called())

        expected_request = SUSHI_PROTO.NoteAftertouchRequest(
            track = SUSHI_PROTO.TrackIdentifier(
                id = keyboard_service_mock.expected_track_id),
            channel = keyboard_service_mock.expected_channel,
            note = keyboard_service_mock.expected_note,
            value = keyboard_service_mock.expected_value)

        self.assertEqual(service.get_recent_request(), expected_request)

    def test_send_aftertouch(self):
        self._kc.send_aftertouch(
            keyboard_service_mock.expected_track_id,
            keyboard_service_mock.expected_channel,
            keyboard_service_mock.expected_value)

        self.assertTrue(service.was_called())

        expected_request = SUSHI_PROTO.NoteModulationRequest(
            track = SUSHI_PROTO.TrackIdentifier(
                id = keyboard_service_mock.expected_track_id),
            channel = keyboard_service_mock.expected_channel,
            value = keyboard_service_mock.expected_value)

        self.assertEqual(service.get_recent_request(), expected_request)

    def test_send_pitch_bend(self):
        self._kc.send_pitch_bend(
            keyboard_service_mock.expected_track_id,
            keyboard_service_mock.expected_channel,
            keyboard_service_mock.expected_value)

        self.assertTrue(service.was_called())

        expected_request = SUSHI_PROTO.NoteModulationRequest(
            track = SUSHI_PROTO.TrackIdentifier(
                id = keyboard_service_mock.expected_track_id),
            channel = keyboard_service_mock.expected_channel,
            value = keyboard_service_mock.expected_value)

        self.assertEqual(service.get_recent_request(), expected_request)

    def test_send_modulation(self):
        self._kc.send_modulation(
            keyboard_service_mock.expected_track_id,
            keyboard_service_mock.expected_channel,
            keyboard_service_mock.expected_value)

        self.assertTrue(service.was_called())

        expected_request = SUSHI_PROTO.NoteModulationRequest(
            track = SUSHI_PROTO.TrackIdentifier(
                id = keyboard_service_mock.expected_track_id),
            channel = keyboard_service_mock.expected_channel,
            value = keyboard_service_mock.expected_value)

        self.assertEqual(service.get_recent_request(), expected_request)
