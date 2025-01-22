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
from tests.mockups import midi_service_mock
from src.elkpy import midicontroller as mc
from src.elkpy import sushi_info_types as info_types

from src.elkpy import grpc_gen
from src.elkpy import sushierrors

proto_file = os.environ.get('SUSHI_GRPC_ELKPY_PROTO')
if proto_file is None:
    print("Environment variable SUSHI_GRPC_ELKPY_PROTO not defined, set it to point the .proto definition")
    sys.exit(-1)

SUSHI_PROTO, SUSHI_GRPC = grpc_gen.modules_from_proto(proto_file)

SUSHI_ADDRESS = ('localhost:51055')

mock_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
service = midi_service_mock.MidiControllerServiceMockup()
SUSHI_GRPC.add_MidiControllerServicer_to_server(service, mock_server)
mock_server.add_insecure_port(SUSHI_ADDRESS)
mock_server.start()

class TestMidiController(unittest.TestCase):
    def setUp(self):
        self._mc = mc.MidiController(SUSHI_ADDRESS, proto_file)

    def test_get_input_ports(self):
        self.assertEqual(self._mc.get_input_ports(),
                         midi_service_mock.expected_input_ports)

    def test_get_output_ports(self):
        self.assertEqual(self._mc.get_output_ports(),
                         midi_service_mock.expected_output_ports)

    def test_get_all_kbd_input_connections(self):
        self.assertEqual(self._mc.get_all_kbd_input_connections(),
                         midi_service_mock.expected_input_kbd_connections)

    def test_get_all_kbd_output_connections(self):
        self.assertEqual(self._mc.get_all_kbd_output_connections(),
                         midi_service_mock.expected_output_kbd_connections)

    def test_get_all_cc_input_connections(self):
        self.assertEqual(self._mc.get_all_cc_input_connections(),
                         midi_service_mock.expected_input_cc_connections)

    def test_get_all_pc_input_connections(self):
        self.assertEqual(self._mc.get_all_pc_input_connections(),
                         midi_service_mock.expected_input_pc_connections)

    def test_get_cc_input_connections_for_processor(self):
        self.assertEqual(self._mc.get_cc_input_connections_for_processor(midi_service_mock.expected_input_cc_connection.processor_id),
                         midi_service_mock.expected_input_cc_connections)

    def test_get_pc_input_connections_for_processor(self):
        self.assertEqual(self._mc.get_pc_input_connections_for_processor(midi_service_mock.expected_input_pc_connection.processor),
                         midi_service_mock.expected_input_pc_connections)

    def test_get_midi_clock_output(self):
        self.assertTrue(self._mc.get_midi_clock_output_enabled(midi_service_mock.expected_midi_clock_port))

    def test_set_midi_clock_output(self):
        self._mc.set_midi_clock_output_enabled(midi_service_mock.expected_midi_clock_port, True)
        self.assertTrue(service.was_called())

    def test_connect_kbd_input_to_track(self):
        self._mc.connect_kbd_input_to_track(midi_service_mock.expected_input_kbd_connection.track,
                                            midi_service_mock.expected_input_kbd_connection.channel,
                                            midi_service_mock.expected_input_kbd_connection.port,
                                            midi_service_mock.expected_input_kbd_connection.raw_midi)
        self.assertTrue(service.was_called())

    def test_connect_kbd_output_from_track(self):
        self._mc.connect_kbd_output_from_track(midi_service_mock.expected_output_kbd_connection.track,
                                               midi_service_mock.expected_output_kbd_connection.channel,
                                               midi_service_mock.expected_output_kbd_connection.port,
                                               midi_service_mock.expected_output_kbd_connection.raw_midi)
        self.assertTrue(service.was_called())

    def test_connect_cc_to_parameter(self):
        self._mc.connect_cc_to_parameter(midi_service_mock.expected_input_cc_connection.processor_id,
                                         midi_service_mock.expected_input_cc_connection.parameter_id,
                                         midi_service_mock.expected_input_cc_connection.channel,
                                         midi_service_mock.expected_input_cc_connection.port,
                                         midi_service_mock.expected_input_cc_connection.cc_number,
                                         midi_service_mock.expected_input_cc_connection.min_range,
                                         midi_service_mock.expected_input_cc_connection.max_range,
                                         midi_service_mock.expected_input_cc_connection.relative_mode)
        self.assertTrue(service.was_called())

    def test_connect_pc_to_parameter(self):
        self._mc.connect_pc_to_processor(midi_service_mock.expected_input_pc_connection.processor,
                                         midi_service_mock.expected_input_pc_connection.channel,
                                         midi_service_mock.expected_input_pc_connection.port)
        self.assertTrue(service.was_called())

    def test_disconnect_kbd_input(self):
        self._mc.disconnect_kbd_input(midi_service_mock.expected_input_kbd_connection.track,
                                      midi_service_mock.expected_input_kbd_connection.channel,
                                      midi_service_mock.expected_input_kbd_connection.port,
                                      midi_service_mock.expected_input_kbd_connection.raw_midi)
        self.assertTrue(service.was_called())

    def test_disconnect_kbd_output(self):
        self._mc.disconnect_kbd_output(midi_service_mock.expected_output_kbd_connection.track,
                                       midi_service_mock.expected_output_kbd_connection.channel,
                                       midi_service_mock.expected_output_kbd_connection.port,
                                       midi_service_mock.expected_output_kbd_connection.raw_midi)
        self.assertTrue(service.was_called())

    def test_disconnect_cc(self):
        self._mc.disconnect_cc(midi_service_mock.expected_input_cc_connection.processor_id,
                               midi_service_mock.expected_input_cc_connection.parameter_id,
                               midi_service_mock.expected_input_cc_connection.channel,
                               midi_service_mock.expected_input_cc_connection.port,
                               midi_service_mock.expected_input_cc_connection.cc_number,
                               midi_service_mock.expected_input_cc_connection.min_range,
                               midi_service_mock.expected_input_cc_connection.max_range,
                               midi_service_mock.expected_input_cc_connection.relative_mode)
        self.assertTrue(service.was_called())

    def test_disconnect_pc(self):
        self._mc.disconnect_pc(midi_service_mock.expected_input_pc_connection.processor,
                               midi_service_mock.expected_input_pc_connection.channel,
                               midi_service_mock.expected_input_pc_connection.port)
        self.assertTrue(service.was_called())

    def test_disconnect_all_cc_from_processor(self):
        self._mc.disconnect_all_cc_from_processor(midi_service_mock.expected_input_cc_connection.processor_id)
        self.assertTrue(service.was_called())

    def test_disconnect_all_pc_from_processor(self):
        self._mc.disconnect_all_pc_from_processor(midi_service_mock.expected_input_pc_connection.processor)
        self.assertTrue(service.was_called())
