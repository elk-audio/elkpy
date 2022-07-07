#!/usr/bin/python3

__author__ = "Gustav Andersson"
__copyright__ = """

    Copyright 2017-2022 Modern Ancient Instruments Networked AB, dba Elk

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

""" 
    Example passive monitor app using elkpy
    Connects to a sushi instance, subscribes to notifications and displays all
    parameter, transport and audio graph changes that Sushi broadcasts
""" 

import os
import sys
import time
import argparse
from elkpy.sushicontroller import SushiController
from elkpy import sushi_info_types as sushi
from elkpy import grpc_gen
from enum import IntEnum
from pathlib import Path
import asyncio

SYNC_MODES = ['Dummy', 'Internal', 'Midi', 'Link']
PLAYING_MODES = ['Dummy', 'Stopped', 'Playing']

def read_args():
    proto_file = os.environ.get('SUSHI_GRPC_ELKPY_PROTO')
    
    parser = argparse.ArgumentParser(description="Sushi grpc monitor",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--ip", action="store", help="Ip of sushi device", default="localhost")
    parser.add_argument("-p", "--port", action="store_true", help="Port of Sushi device", default="51051")
    parser.add_argument("-g", "--protofile", action="store", help="Path to proto_file (Retrived from SUSHI_GRPC_ELKPY_PROTO env. variable)", default=proto_file)
    args = parser.parse_args()
    config = vars(args)

    print(config)
    if not config['protofile']:
        print("No proto file set or environment variable SUSHI_GRPC_ELKPY_PROTO not defined")
        sys.exit(-1)

    return config


class Listener(SushiController):

    def __init__(self, address, proto_file):
        super().__init__(address, proto_file)
        self._print_system_info()
        self._read_audio_graph()

        self.notifications.subscribe_to_track_changes(self._process_track_notification)
        self.notifications.subscribe_to_processor_changes(self._process_processor_notification)
        self.notifications.subscribe_to_parameter_updates(self._process_parameter_notification)
        self.notifications.subscribe_to_property_updates(self._process_property_notification)
        self.notifications.subscribe_to_transport_changes(self._process_transport_notification)

    def _print_system_info(self):
        info = self.system.get_build_info()
        print(f"Connected to Sushi! \nVersion: {info.version}, built: {info.build_date} from commit: {info.commit_hash}")

    def _read_audio_graph(self):
        self._processors = {}
        processors = self.audio_graph.get_all_processors()
        tracks = self.audio_graph.get_all_tracks()
        for p in processors:
            self._add_processor(p)

        print(f"A total of {len(processors)} processors on {len(tracks)} tracks")

    def _add_processor(self, info):
        processor = {}
        processor['info'] = info
        processor['parameters'] = {param.id : param for param in self.parameters.get_processor_parameters(info.id)}
        processor['properties'] = {prop.id : prop for prop in self.parameters.get_processor_properties(info.id)}
        self._processors[info.id] = processor

    def _process_track_notification(self, notif):
        if notif.action == 1:   # TRACK_ADDED
            info = self.audio_graph.get_processor_info(notif.track.id)
            self._add_processor(info)
            print(f"Track \"{info.name}\" ({info.id}) added") 

        elif notif.action == 2:  # TRACK_DELETED
            info = self._processors[notif.track.id]['info']
            print(f"Track \"{info.name}\" ({info.id}) deleted")

    def _process_processor_notification(self, notif):
        track = self._processors[notif.parent_track.id]['info']

        if notif.action == 1:   # PROCESSOR_ADDED
            self._add_processor(info)
            print(f"Processor \"{info.name}\" ({info.id}) added to track \"{track.name}\" ({track.id})") 

        elif notif.action == 2:  # PROCESSOR_DELETED
            info = self._processors[notif.processor.id]['info']
            print(f"Processor \"{info.name}\" ({info.id}) was deleted from track \"{track.name}\" ({track.id})")

    def _process_parameter_notification(self, notif):
        try:
            processor = self._processors[notif.parameter.processor_id]
            info = processor['parameters'][notif.parameter.parameter_id]
            print(f"Parameter {info.name} on {processor['info'].name} set to {notif.formatted_value} {info.unit.strip()} ({notif.normalized_value:.3f})")

        except Exception as e:
            print(e)

    def _process_property_notification(self, notif):
        try:
            processor = self._processors[notif.property.processor_id]
            info = processor['properties'][notif.property.property_id]
            print(f"Property {info.name} on {processor['info'].name} set to {notif.value}")
        
        except Exception as e:
            print(e)

    def _process_transport_notification(self, notif):
        try:
            if notif.HasField('tempo'):
                print(f"Tempo set to {notif.tempo} bpm")

            elif notif.HasField('playing_mode'):
                print(f"Playing mode set to {PLAYING_MODES[notif.playing_mode.mode]}")

            elif notif.HasField('sync_mode'):
                print(f"tempo sync mode set to {SYNC_MODES[notif.sync_mode.mode]}")

            elif notif.HasField('time_signature'):
                print(f"Time time_signature set to {notif.time_signature.denominator} / {notif.time_signature.numerator}")

        except Exception as e:
            print(e)

def main():
    config = read_args()
    sushi_grpc_types, _ = grpc_gen.modules_from_proto(config['protofile'])

    listener = Listener(f"{config['ip']}:{config['port']}", config['protofile'])

    while True:
        try:
            time.sleep(1)

        except KeyboardInterrupt:
            listener.close()
            sys.exit(0)

    listener.close()

if __name__ == '__main__':
    main()
