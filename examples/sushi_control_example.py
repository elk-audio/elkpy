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

import sys

from elkpy.sushi_info_types import PluginType

# This is needed to run sushi_monitor.py from within the examples folder without also copying elkpy to it.
sys.path.append("../elkpy/")

from elkpy import sushicontroller as sc
from elkpy import sushiprocessor as sp

PROCESSOR_NAME = 'OB-Xd'
SEQUENCER_NAME = 'sequencer_obxd'
EFFECT_NAME = 'ADelay'

SUSHI_PROCESSORS = ['main', SEQUENCER_NAME, PROCESSOR_NAME, EFFECT_NAME]

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
                "path": "/Users/iliaselk/repos/sushi/cmake-build-debug/VST3/Debug/adelay.vst3",
                "name": "ADelay",
                "type": PluginType.VST3X,
                "uid": "ADelay"
            }]

class StrangerFish(object):
    """ 
    This example takes an existing setup of
    """

    def __init__(self):
        self._sushi_controller = sc.SushiController()

        track_name = 'main'
        track_id = self._sushi_controller.audio_graph.get_track_id(track_name)

        for plugin_spec in PLUGINS:
            self._add_plugin(track_id, plugin_spec)

        self._processors = self._create_processor_controllers(SUSHI_PROCESSORS)

        self._processors[PROCESSOR_NAME].set_parameter_value("VoiceCount", 8)

        self._processors[PROCESSOR_NAME].set_parameter_value("Cutoff", 0.5)

        # TODO: Really? Try!
    #    self.sushi.set_tempo(200)

        # Arpeggio
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_0", 0.4166666666666667)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_1", 0.5)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_2", 0.5625)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_3", 0.6458333333333334)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_4", 0.6666666666666666)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_5", 0.6458333333333334)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_6", 0.5625)
        self._processors[SEQUENCER_NAME].set_parameter_value("pitch_7", 0.5)

    def _add_plugin(self, track_id, plugin_spec):
        path = plugin_spec['path']
        name = plugin_spec['name']
        p_type = plugin_spec['type']
        uid = plugin_spec['uid']

        try:
            self._sushi_controller.audio_graph.create_processor_on_track(name, uid, path, p_type, track_id, 0, True)
        except Exception as e:
            print('Error creating plugin: {}'.format(e))

    def _create_processor_controllers(self, list_of_processors):
        processors = {}
        for processor in list_of_processors:
            processors[processor] = sp.SushiProcessor(processor, self._sushi_controller)
        return processors

    def close(self):
        self._sushi_controller.close()

if __name__ == '__main__':
    bridge = StrangerFish()

    bridge.close()


