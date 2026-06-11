#!/usr/bin/python3

__author__ = "Gustav Andersson"
__copyright__ = """

    Copyright 2017-2026 Elk Audio AB
    elkpy is free software: you can redistribute it and/or modify it under the terms of the
    GNU General Public License as published by the Free Software Foundation, either version 3
    of the License, or (at your option) any later version.

    elkpy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
    even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with elkpy. If
    not, see <http://www.gnu.org/licenses/>.
"""
__license__ = "GPL-3.0"

""" 
    An example passive monitor app using elkpy.
    It connects to a sushi instance, subscribes to notifications and displays all the
    parameter, transport and audio graph changes that Sushi broadcasts.
"""

import os
import sys
import time
import argparse

# This is needed to run sushi_monitor.py from within the examples folder without also copying elkpy to it.
sys.path.append("../elkpy/")

from elkpy.sushicontroller import SushiController
from elkpy.sushicontroller import DEFAULT_SUSHI_RPC_PORT, DEFAULT_SUSHI_IPC_PORT, DEFAULT_SUSHI_IPC_SUB_PORT

SYNC_MODES = ['Dummy', 'Internal', 'Midi', 'Link']
PLAYING_MODES = ['Dummy', 'Stopped', 'Playing']

def read_args():
    parser = argparse.ArgumentParser(description="Sushi notification monitor",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--ipc", action="store_true", help="Use ZMQ-based IPC transport")
    parser.add_argument("-r", "--rpc", action="store_true", help="Use gRPC-based RPC transport (default)")
    parser.add_argument("-a", "--address", action="store", help="Port for transport")
    parser.add_argument("-s", "--sub_address", action="store", help="Port for notifications (IPC only)")
    args = parser.parse_args()
    config = vars(args)
    return config

def _process_transport_notification(notif):
    try:
        if notif.HasField('tempo'):
            print(f"Tempo set to {notif.tempo} bpm")

        elif notif.HasField('playing_mode'):
            print(f"Playing mode set to {PLAYING_MODES[notif.playing_mode.mode]}")

        elif notif.HasField('sync_mode'):
            print(f"tempo sync mode set to {SYNC_MODES[notif.sync_mode.mode]}")

        elif notif.HasField('time_signature'):
            print(
                f"Time time_signature set to {notif.time_signature.denominator} / {notif.time_signature.numerator}")

    except Exception as e:
        print(e)


def _process_timing_notification(notif):
    try:
        print(f"Cpu load: avg: {notif.main.average * 100:.1f}%, min: {notif.main.min * 100:.1f}%, max: {notif.main.max * 100:.1f}%")

    except Exception as e:
        print(e)

def _process_async_notification(notif):
    try:
        print(f"Async notification, req: {notif.request_id} completed with {notif.status}".strip("\n"))

    except Exception as e:
        print(e)


class Listener(SushiController):

    def __init__(self, transport, address, sub_address):
        super().__init__(transport=transport, address=address, sub_address=sub_address,
                         auto_update_async_command_responses=False)
        self._print_system_info()
        self._read_audio_graph()

        self.notifications.subscribe_to_track_changes(self._process_track_notification)
        self.notifications.subscribe_to_processor_changes(self._process_processor_notification)
        self.notifications.subscribe_to_parameter_updates(self._process_parameter_notification)
        self.notifications.subscribe_to_property_updates(self._process_property_notification)
        self.notifications.subscribe_to_transport_changes(_process_transport_notification)
        self.notifications.subscribe_to_timing_updates(_process_timing_notification)
        self.notifications.subscribe_to_async_command_response(_process_async_notification)

    def _print_system_info(self):
        info = self.system.get_build_info()
        print(f"Connected to Sushi! \n"
              f"Version: {info.version}, built: {info.build_date} from commit: {info.commit_hash}")

    def _read_audio_graph(self):
        self._processors = {}
        processors = self.audio_graph.get_all_processors()
        tracks = self.audio_graph.get_all_tracks()
        for p in processors:
            self._add_processor(p)

        print(f"A total of {len(processors)} processors on {len(tracks)} tracks")

    def _add_processor(self, info):
        processor = {'info': info,
                     'parameters': {param.id: param for param in self.parameters.get_processor_parameters(info.id)},
                     'properties': {prop.id: prop for prop in self.parameters.get_processor_properties(info.id)}}
        self._processors[info.id] = processor

    def _process_track_notification(self, notif):
        if notif.action == 1:  # TRACK_ADDED
            info = self.audio_graph.get_processor_info(notif.track.id)
            self._add_processor(info)
            print(f"Track \"{info.name}\" ({info.id}) added")

        elif notif.action == 2:  # TRACK_DELETED
            info = self._processors[notif.track.id]['info']
            print(f"Track \"{info.name}\" ({info.id}) deleted")

    def _process_processor_notification(self, notif):
        track = self._processors[notif.parent_track.id]['info']

        if notif.action == 1:  # PROCESSOR_ADDED
            info = self.audio_graph.get_processor_info(notif.processor.id)
            self._add_processor(info)
            print(f"Processor \"{info.name}\" ({info.id}) added to track \"{track.name}\" ({track.id})")

        elif notif.action == 2:  # PROCESSOR_DELETED
            info = self._processors[notif.processor.id]['info']
            print(f"Processor \"{info.name}\" ({info.id}) was deleted from track \"{track.name}\" ({track.id})")

    def _process_parameter_notification(self, notif):
        try:
            processor = self._processors[notif.parameter.processor_id]
            info = processor['parameters'][notif.parameter.parameter_id]
            print(f"Parameter {info.name} on {processor['info'].name} "
                  f"set to {notif.formatted_value} {info.unit.strip()} ({notif.normalized_value:.3f})")

        except Exception as e:
            print(e)

    def _process_property_notification(self, notif):
        try:
            processor = self._processors[notif.property.processor_id]
            info = processor['properties'][notif.property.property_id]
            print(f"Property {info.name} on {processor['info'].name} set to {notif.value}")

        except Exception as e:
            print(e)


def main():
    config = read_args()
    transport = "IPC" if (config["ipc"]) else "RPC"
    address = config["address"] if config["address"] else (DEFAULT_SUSHI_IPC_PORT if (config["ipc"]) else DEFAULT_SUSHI_RPC_PORT)
    sub_address = config["sub_address"] if config["sub_address"] else DEFAULT_SUSHI_IPC_SUB_PORT

    listener = Listener(transport=transport, address=address, sub_address=sub_address)

    while True:
        try:
            time.sleep(1)

        except KeyboardInterrupt:
            # The close() method is inherited from SushiController
            listener.close()
            sys.exit(0)

    listener.close()


if __name__ == '__main__':
    main()
