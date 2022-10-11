#!/usr/bin/env python3

__copyright__ = """

    Copyright 2017-2022 Modern Ancient Instruments Networked AB, dba Elk

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

import os
import sys
import time
import argparse

from elkpy.sushi_info_types import PluginType
from elkpy import grpc_gen, sushierrors

# This is needed to run sushi_monitor.py from within the examples folder without also copying elkpy to it.
sys.path.append("../elkpy/")

from elkpy.sushicontroller import SushiController
from elkpy import sushiprocessor as sp

TRACK_NAME = 'main'
PROCESSOR_NAME = 'OB-Xd'
SEQUENCER_NAME = 'sequencer_obxd'
EFFECT_NAME = 'mda DubDelay'

SUSHI_PROCESSORS = [TRACK_NAME, SEQUENCER_NAME, PROCESSOR_NAME, EFFECT_NAME]

PLUGINS = [{
                "path": "",
                "name": "sequencer_obxd",
                "uid": "sushi.testing.step_sequencer",
                "type": PluginType.INTERNAL
            },
            {
                "path": "/Library/Audio/Plug-Ins/VST3/OB-Xd.vst3",
                "name": "OB-Xd",
                "type": PluginType.VST3X,
                "uid": "OB-Xd"
            },
            {
                "path": "/Users/iliaselk/Library/Audio/Plug-Ins/VST3/mda-vst3.vst3",
                "name": "mda DubDelay",
                "type": PluginType.VST3X,
                "uid": "mda DubDelay"
            }]


def read_args():
    proto_file = os.environ.get('SUSHI_GRPC_ELKPY_PROTO')

    parser = argparse.ArgumentParser(description="Sushi grpc monitor",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--ip", action="store", help="Ip of sushi device", default="localhost")
    parser.add_argument("-p", "--port", action="store_true", help="Port of Sushi device", default="51051")
    parser.add_argument("-g", "--protofile", action="store",
                        help="Path to proto_file (Retrieved from the SUSHI_GRPC_ELKPY_PROTO env. variable)",
                        default=proto_file)
    args = parser.parse_args()
    config = vars(args)

    print(config)
    if not config['protofile']:
        print("No proto file is found, probably the environment variable SUSHI_GRPC_ELKPY_PROTO is not defined.")
        sys.exit(-1)

    return config


class ArpeggiatedSynthExample(SushiController):
    """ 
    This example takes an existing setup of Sushi, with a single main track connected to MIDI input,
    adds a sequencer, a synth, and an effect, and sets their values to play back an arpeggio.
    """

    def __init__(self, address, proto_file):
        super().__init__(address, proto_file)
        self._print_system_info()

        self._processor_notifications_received = 0
        self.notifications.subscribe_to_processor_changes(self._process_processor_notification)

        track_id = self.audio_graph.get_track_id(TRACK_NAME)

        for plugin_spec in PLUGINS:
            self._add_plugin(track_id, plugin_spec)

    def _process_processor_notification(self, notification):
        if notification.action == 1:   # PROCESSOR_ADDED
            print('Processor created with ID: {}'.format(notification.processor.id))
            self._processor_notifications_received += 1

        if self._processor_notifications_received == len(PLUGINS):
            self._processors = self._create_processor_controllers(SUSHI_PROCESSORS)
            self._set_parameters()

    def _set_parameters(self):
        # Synth parameters
        self._processors[PROCESSOR_NAME].set_parameter_value("VoiceCount", 8)
        self._processors[PROCESSOR_NAME].set_parameter_value("Cutoff", 0.5)

        # Arpeggio
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_0", 0.4166666666666667)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_1", 0.5)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_2", 0.5625)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_3", 0.6458333333333334)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_4", 0.6666666666666666)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_5", 0.6458333333333334)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_6", 0.5625)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_7", 0.5)

        self.transport.set_tempo(200)

    def _add_plugin(self, track_id, plugin_spec):
        path = plugin_spec['path']
        name = plugin_spec['name']
        p_type = plugin_spec['type']
        uid = plugin_spec['uid']

        try:
            self.audio_graph.create_processor_on_track(name, uid, path, p_type, track_id, 0, True)
        except Exception as e:
            print('Error creating plugin: {}'.format(e))

    def _create_processor_controllers(self, list_of_processors):
        processors = {}
        for processor in list_of_processors:
            processors[processor] = sp.SushiProcessor(processor, self)

        return processors

    def _print_system_info(self):
        info = self.system.get_build_info()
        print(f"Connected to Sushi! \nVersion: {info.version}, built: {info.build_date} from commit: {info.commit_hash}")


if __name__ == '__main__':
    config = read_args()
    sushi_grpc_types, _ = grpc_gen.modules_from_proto(config['protofile'])

    bridge = ArpeggiatedSynthExample(f"{config['ip']}:{config['port']}", config['protofile'])

    while True:
        try:
            time.sleep(1)

        except KeyboardInterrupt:
            # The close() method is inherited from SushiController
            bridge.close()
            sys.exit(0)
