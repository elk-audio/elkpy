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

import grpc
from . import sushierrors
from . import grpc_gen
from . import sushi_info_types as info_types

from . import audiographcontroller
from . import keyboardcontroller
from . import parametercontroller
from . import programcontroller
from . import timingcontroller
from . import transportcontroller

from typing import List

###############################
# Main sushi controller class #
###############################

class SushiController(object):
    '''
    A class to control sushi via gRPC.

    Attributes:
        _stub (SushiControllerStub): Connection stubs to the gRPC interface implemented in sushi.
    '''
    def __init__(self,
                 address = 'localhost:51051',
                 sushi_proto_def = '/usr/share/sushi/sushi_rpc.proto'):
        '''
        The constructor for the SushiController class.

        Parameters:
            address (str): 'ip-addres:port' The ip-addres and port at which to connect to sushi.
            sushi_proto_def (str): path to .proto file with SUSHI's gRPC services definition
        '''
        self.audio_graph = audiographcontroller.AudioGraphController(address, sushi_proto_def)
        self.keyboard = keyboardcontroller.KeyboardController(address, sushi_proto_def)
        self.parameters = parametercontroller.ParameterController(address, sushi_proto_def)
        self.programs = programcontroller.ProgramController(address, sushi_proto_def)
        self.timings = timingcontroller.TimingController(address, sushi_proto_def)
        self.transport = transportcontroller.TransportController(address, sushi_proto_def)
