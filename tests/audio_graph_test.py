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
import grpc
from src.elkpy import grpc_gen
from src.elkpy import sushierrors

proto_file = os.environ.get("SUSHI_GRPC_ELKPY_PROTO")
if proto_file is None:
    print(
        "Environment variable SUSHI_GRPC_ELKPY_PROTO not defined, set it to point the .proto definition"
    )
    sys.exit(-1)

SUSHI_PROTO, SUSHI_GRPC = grpc_gen.modules_from_proto(proto_file)

from concurrent import futures
from tests.mockups import audiograph_service_mock
from src.elkpy import audiographcontroller as agc
from src.elkpy import sushi_info_types as info_types


SUSHI_ADDRESS = "localhost:51051"

mock_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
service = audiograph_service_mock.AudioGraphControllerServiceMockup()
SUSHI_GRPC.add_AudioGraphControllerServicer_to_server(service, mock_server)
mock_server.add_insecure_port(SUSHI_ADDRESS)
mock_server.start()


class TestAudioGraphController(unittest.TestCase):
    def setUp(self):
        print("in setUp")
        self._agc = agc.AudioGraphController(self, SUSHI_ADDRESS, proto_file)

    def test_get_all_processors(self):
        self.assertEqual(
            self._agc.get_all_processors(),
            [
                audiograph_service_mock.expected_processor_1,
                audiograph_service_mock.expected_processor_2,
            ],
        )

    def test_get_all_tracks(self):
        self.assertEqual(
            self._agc.get_all_tracks(),
            [
                audiograph_service_mock.expected_track_1,
                audiograph_service_mock.expected_track_2,
            ],
        )

    def test_get_track_id(self):
        self.assertEqual(
            self._agc.get_track_id(audiograph_service_mock.expected_track_1.name),
            audiograph_service_mock.expected_track_1.id,
        )
        self.assertEqual(
            self._agc.get_track_id(audiograph_service_mock.expected_track_2.name),
            audiograph_service_mock.expected_track_2.id,
        )
        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._agc.get_track_id("invalid_name")

    def test_get_track_info(self):
        self.assertEqual(
            self._agc.get_track_info(audiograph_service_mock.expected_track_1.id),
            audiograph_service_mock.expected_track_1,
        )
        self.assertEqual(
            self._agc.get_track_info(audiograph_service_mock.expected_track_2.id),
            audiograph_service_mock.expected_track_2,
        )
        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._agc.get_track_info(-1)

    def test_get_track_processors(self):
        self.assertEqual(
            self._agc.get_track_processors(audiograph_service_mock.expected_track_1.id),
            [
                audiograph_service_mock.expected_processor_1,
                audiograph_service_mock.expected_processor_2,
            ],
        )
        self.assertEqual(
            self._agc.get_track_processors(audiograph_service_mock.expected_track_2.id),
            [
                audiograph_service_mock.expected_processor_1,
                audiograph_service_mock.expected_processor_2,
            ],
        )
        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._agc.get_track_processors(-1)

    def test_get_processor_id(self):
        self.assertEqual(
            self._agc.get_processor_id(
                audiograph_service_mock.expected_processor_1.name
            ),
            audiograph_service_mock.expected_processor_1.id,
        )
        self.assertEqual(
            self._agc.get_processor_id(
                audiograph_service_mock.expected_processor_2.name
            ),
            audiograph_service_mock.expected_processor_2.id,
        )
        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._agc.get_processor_id("invalid_name")

    def test_get_processor_info(self):
        self.assertEqual(
            self._agc.get_processor_info(
                audiograph_service_mock.expected_processor_1.id
            ),
            audiograph_service_mock.expected_processor_1,
        )
        self.assertEqual(
            self._agc.get_processor_info(
                audiograph_service_mock.expected_processor_2.id
            ),
            audiograph_service_mock.expected_processor_2,
        )
        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._agc.get_processor_info(-1)

    def test_get_processor_bypass_state(self):
        self.assertEqual(
            self._agc.get_processor_bypass_state(
                audiograph_service_mock.expected_processor_1.id
            ),
            audiograph_service_mock.expected_processor_1_bypass,
        )
        self.assertEqual(
            self._agc.get_processor_bypass_state(
                audiograph_service_mock.expected_processor_2.id
            ),
            audiograph_service_mock.expected_processor_2_bypass,
        )
        with self.assertRaises(sushierrors.SushiInvalidArgumentError):
            self._agc.get_processor_bypass_state(-1)

    def test_get_processor_state(self):
        self.assertEqual(
            self._agc.get_processor_state(
                audiograph_service_mock.expected_processor_1.id
            ),
            audiograph_service_mock.expected_processor_state,
        )
        self.assertEqual(
            self._agc.get_processor_state(
                audiograph_service_mock.expected_processor_2.id
            ),
            audiograph_service_mock.expected_processor_state,
        )

    def test_set_processor_state(self):
        self._agc.set_processor_state(
            audiograph_service_mock.expected_processor_1.id,
            audiograph_service_mock.expected_processor_state,
        )
        self.assertTrue(service.called)

    def test_create_track(self):
        self._agc.create_track(
            audiograph_service_mock.expected_create_track_request.name,
            audiograph_service_mock.expected_create_track_request.channels,
        )
        self.assertTrue(service.was_called())
        self.assertEqual(
            service.get_recent_request(),
            audiograph_service_mock.expected_create_track_request,
        )

    def test_create_multibus_track(self):
        self._agc.create_multibus_track(
            audiograph_service_mock.expected_create_multibus_request.name,
            audiograph_service_mock.expected_create_multibus_request.buses,
        )
        self.assertTrue(service.was_called())
        self.assertEqual(
            service.get_recent_request(),
            audiograph_service_mock.expected_create_multibus_request,
        )

    def test_create_pre_track(self):
        self._agc.create_pre_track(
            audiograph_service_mock.expected_create_pre_track_request.name
        )
        self.assertTrue(service.was_called())
        self.assertEqual(
            service.get_recent_request(),
            audiograph_service_mock.expected_create_pre_track_request,
        )

    def test_create_post_track(self):
        self._agc.create_post_track(
            audiograph_service_mock.expected_create_post_track_request.name
        )
        self.assertTrue(service.was_called())
        self.assertEqual(
            service.get_recent_request(),
            audiograph_service_mock.expected_create_post_track_request,
        )

    def test_create_processor_on_track(self):
        self._agc.create_processor_on_track(
            audiograph_service_mock.expected_create_processor_request.name,
            audiograph_service_mock.expected_create_processor_request.uid,
            audiograph_service_mock.expected_create_processor_request.path,
            audiograph_service_mock.expected_create_processor_request.type.type,
            audiograph_service_mock.expected_create_processor_request.track.id,
            audiograph_service_mock.expected_create_processor_request.position.before_processor.id,
            audiograph_service_mock.expected_create_processor_request.position.add_to_back,
        )
        self.assertTrue(service.was_called())
        self.assertEqual(
            service.get_recent_request(),
            audiograph_service_mock.expected_create_processor_request,
        )

    def test_move_processor_on_track(self):
        self._agc.move_processor_on_track(
            audiograph_service_mock.expected_move_processor_request.processor.id,
            audiograph_service_mock.expected_move_processor_request.source_track.id,
            audiograph_service_mock.expected_move_processor_request.dest_track.id,
            audiograph_service_mock.expected_move_processor_request.position.before_processor.id,
            audiograph_service_mock.expected_move_processor_request.position.add_to_back,
        )
        self.assertTrue(service.was_called())
        self.assertEqual(
            service.get_recent_request(),
            audiograph_service_mock.expected_move_processor_request,
        )

    def test_delete_processor_from_track(self):
        self._agc.delete_processor_from_track(
            audiograph_service_mock.expected_delete_processor_request.processor.id,
            audiograph_service_mock.expected_delete_processor_request.track.id,
        )
        self.assertTrue(service.was_called())
        self.assertEqual(
            service.get_recent_request(),
            audiograph_service_mock.expected_delete_processor_request,
        )

    def test_delete_track(self):
        self._agc.delete_track(audiograph_service_mock.expected_track_1.id)
        self.assertTrue(service.was_called())
        self.assertEqual(
            service.get_recent_request(),
            SUSHI_PROTO.TrackIdentifier(id=audiograph_service_mock.expected_track_1.id),
        )
