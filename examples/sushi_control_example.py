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
import argparse
import asyncio

from elkpy.sushi_info_types import PluginType
from elkpy import grpc_gen

# This is needed to run sushi_monitor.py from within the examples folder without also copying elkpy to it.
sys.path.append("../elkpy/")

from elkpy.sushicontroller import SushiController
from elkpy import sushiprocessor as sp

TRACK_NAME = 'main'
SYNTH_NAME = 'mda JX10'
SEQUENCER_NAME = 'step_sequencer'
EFFECT_NAME = 'mda DubDelay'

SUSHI_PROCESSORS = [TRACK_NAME, SEQUENCER_NAME, SYNTH_NAME, EFFECT_NAME]

PLUGINS = [
    {
        "path": "",
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


def read_args() -> dict:
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

    if not config['protofile']:
        print("No proto file is found, probably the environment variable SUSHI_GRPC_ELKPY_PROTO is not defined.")
        sys.exit(-1)

    return config


class ArpeggiatedSynthExample(SushiController):
    """ 
    This example takes an existing setup of Sushi, with a single main track connected to MIDI input,
    adds a sequencer, a synth, and an effect, and sets their values to play back an arpeggio.
    """

    def __init__(self, address: str, proto_file: str):
        super().__init__(address, proto_file)
        self._print_system_info()
        self._processors: dict = {}

        # Fetching the track ID from the name defined in the Sushi config file:
        self.track_id = self.audio_graph.get_track_id(TRACK_NAME)

    async def set_state(self) -> None:
        """
        This example shows off the way Elkpy is meant to handle Sushi's asynchronous processing of audio graph altering commands.
        Because _load_plugin_on_track blocks and waits for each Sushi event to be set, we can start setting parameters right 
        after calling it. The command is guaranteed to have completed.

        If the .wait() call in _load_plugin_on_track had been missing, _set_parameters_for_theme_tune might fail as there is no
        guarantee that the target processor exists yet.
        """
        for plugin_spec in PLUGINS:
            await self._load_plugin_on_track(self.track_id, plugin_spec)
            self._processors[plugin_spec['name']] = sp.SushiProcessor(plugin_spec['name'], self)

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

    async def _load_plugin_on_track(self, track_id: int, plugin_spec: dict):
        path = plugin_spec['path']
        name = plugin_spec['name']
        p_type = plugin_spec['type']
        uid = plugin_spec['uid']

        try:
            ev = self.audio_graph.create_processor_on_track(name, uid, path, p_type, track_id, 0, True)
            # The following call to ev.wait() is crucial to guarantee that the processor actually exists in Sushi when the method returns.
            # Other asyncio strategies are possible, like gathering all events and waiting for them as a separate track for instance.
            await ev.wait()
        except Exception as e:
            print('Error loading plugin: {}'.format(e))

    def _print_system_info(self):
        info = self.system.get_build_info()
        print(f"Connected to Sushi! \n"
              f"Version: {info.version}, built: {info.build_date} from commit: {info.commit_hash}")

async def main():
    """
    Having a main function is not necessary per se BUT it is a convenient way to make sure that an asyncio.Event is running when we 
    start running coroutines. Programmers should not forget that elkpy starts some coroutines as soon as a SushiController is
    created.
    """
    bridge = ArpeggiatedSynthExample(f"{config['ip']}:{config['port']}", config['protofile'])
    await bridge.set_state()


if __name__ == '__main__':
    config = read_args()
    sushi_grpc_types, _ = grpc_gen.modules_from_proto(config['protofile'])

    asyncio.run(main())
