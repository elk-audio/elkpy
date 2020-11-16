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

import threading
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
from . import audioroutingcontroller
from . import midicontroller
from . import cvgatecontroller
from . import osccontroller
from . import systemcontroller

from typing import List
from typing import List, Callable



############################
# Error handling functions #
############################
class SushiUnkownError(Exception):
    pass

class SushiUnsupportedOperationError(Exception):
    pass

class SushiNotFoundError(Exception):
    pass

class SushiOutOfRangeError(Exception):
    pass

class SushiInvalidArgumentError(Exception):
    pass

class SushiInternalError(Exception):
    pass

def grpc_error_handling(e, context_info = ''):
    if (e.code().name == 'UNKNOWN'):
        raise SushiUnkownError(e.details() , context_info) from e
    elif (e.code().name == 'FAILED_PRECONDITION'):
        raise SushiUnsupportedOperationError(e.details() , context_info) from e
    elif (e.code().name == 'NOT_FOUND'):
        raise SushiNotFoundError(e.details() , context_info) from e
    elif (e.code().name == 'OUT_OF_RANGE'):
        raise SushiOutOfRangeError(e.details() , context_info) from e
    elif (e.code().name == 'INVALID_ARGUMENT'):
        raise SushiInvalidArgumentError(e.details() , context_info) from e
    elif (e.code().name == 'INTERNAL'):
        raise SushiInternalError(e.details() , context_info) from e
    else:
        print(context_info)
        raise e
      #  print('Grpc error: ' + str e.code().name) + ', ' + e.details())

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
        self.audio_routing = audioroutingcontroller.AudioRoutingController(address, sushi_proto_def)
        self.midi_controller = midicontroller.MidiController(address, sushi_proto_def)
        self.cv_gate_controller = cvgatecontroller.CvGateController(address, sushi_proto_def)
        self.osc_controller = osccontroller.OscController(address, sushi_proto_def)
        self.system = systemcontroller.SystemController(address, sushi_proto_def)
