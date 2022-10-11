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
SYNTH_NAME = 'mda JX10'
SEQUENCER_NAME = 'step_sequencer'
EFFECT_NAME = 'mda DubDelay'

SUSHI_PROCESSORS = [TRACK_NAME, SEQUENCER_NAME, SYNTH_NAME, EFFECT_NAME]

PLUGINS = [{
                "path": "",
                "name": SEQUENCER_NAME,
                "name": SEQUENCER_NAME,
                "uid": "sushi.testing.step_sequencer",
                "type": PluginType.INTERNAL
            },
            {
                "path": "mda-vst3.vst3",
                "name": SYNTH_NAME,
                "uid": SYNTH_NAME,
                "type": PluginType.VST3X
            },
            {
                "path": "mda-vst3.vst3",
                "name": EFFECT_NAME,
                "uid": EFFECT_NAME,
                "type": PluginType.VST3X
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

        # Subscribing to notifications for processor changes:
        self._processor_creation_notification_count = 0
        self.notifications.subscribe_to_processor_changes(self._process_processor_notification)

        # Fetching the track ID from the name defined in the Sushi config file:
        track_id = self.audio_graph.get_track_id(TRACK_NAME)

        # Adding the plugins to the track:
        for plugin_spec in PLUGINS:
            self._load_plugin_on_track(track_id, plugin_spec)

    def _process_processor_notification(self, notification):
        """
        A callback invoked by the elkpy notification controller, whenever a processor is added/removed.
        """

        if notification.action == 1:  # PROCESSOR_ADDED
            print('Processor created with ID: {}'.format(notification.processor.id))
            self._processor_creation_notification_count += 1

        # When all processors have been created, instantiate controllers for them, and set their parameters:
        if self._processor_creation_notification_count == len(PLUGINS):
            self._processors = self._create_processor_controllers(SUSHI_PROCESSORS)
            self._set_parameters_for_theme_tune()

    def _set_parameters_for_theme_tune(self):
        """
        Sets the parameters for the processors, to play a familiar theme tune.
        """

        # Synth parameters:
        self._processors[SYNTH_NAME].set_parameter_value("OSC Mix", 0.2)
        self._processors[SYNTH_NAME].set_parameter_value("ENV Rel", 0.3)
        self._processors[SYNTH_NAME].set_parameter_value("VCF Vel", 0.6)
        self._processors[SYNTH_NAME].set_parameter_value("VCF Freq", 0.5)
        self._processors[SYNTH_NAME].set_parameter_value("VCF Reso", 0.1)

        # Arpeggio:
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_0", 0.4166666666666667)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_1", 0.5)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_2", 0.5625)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_3", 0.6458333333333334)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_4", 0.6666666666666666)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_5", 0.6458333333333334)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_6", 0.5625)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_7", 0.5)

        self.transport.set_tempo(200)

    def _load_plugin_on_track(self, track_id, plugin_spec):
        path = plugin_spec['path']
        name = plugin_spec['name']
        p_type = plugin_spec['type']
        uid = plugin_spec['uid']

        try:
            self.audio_graph.create_processor_on_track(name, uid, path, p_type, track_id, 0, True)
        except Exception as e:
            print('Error loading plugin: {}'.format(e))

    def _create_processor_controllers(self, processor_names):
        """
        Instantiates elkpy controllers for the Sushi processors named in list argument.
        """
        processor_controllers = {}
        for processor_name in processor_names:
            processor_controllers[processor_name] = sp.SushiProcessor(processor_name, self)

        return processor_controllers

    def _print_system_info(self):
        info = self.system.get_build_info()
        print(f"Connected to Sushi! \n"
              f"Version: {info.version}, built: {info.build_date} from commit: {info.commit_hash}")


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
