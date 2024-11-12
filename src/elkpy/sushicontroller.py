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

from .events import ElkpyEvent

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
from . import sessioncontroller
from . import notificationcontroller


############################
# Error handling functions #
############################
class SushiUnkownError(Exception):
    """
    Error thrown when the source of the error can't be determined
    """

    pass


class SushiUnsupportedOperationError(Exception):
    """
    Error thrown when the operation attempted is not currently supported in sushi
    """

    pass


class SushiNotFoundError(Exception):
    """
    Error thrown if the requested entity is not found in sushi
    """

    pass


class SushiOutOfRangeError(Exception):
    """
    Error thrown if one or more of the passed arguments are out of their allowed range
    """

    pass


class SushiInvalidArgumentError(Exception):
    """
    Error thrown if one or more of the passed arguments are invalid
    """

    pass


class SushiInternalError(Exception):
    """
    Error thrown if sushi encountered an internal error
    """

    pass


def grpc_error_handling(e, context_info=""):
    """
    Maps a gRPC exception to the corresponding sushi error. If the exception doesn't have a mapping
    the context info will be printed and the same exception will be re-raised
    """
    if e.code().name == "UNKNOWN":
        raise SushiUnkownError(e.details(), context_info) from e
    elif e.code().name == "FAILED_PRECONDITION":
        raise SushiUnsupportedOperationError(e.details(), context_info) from e
    elif e.code().name == "NOT_FOUND":
        raise SushiNotFoundError(e.details(), context_info) from e
    elif e.code().name == "OUT_OF_RANGE":
        raise SushiOutOfRangeError(e.details(), context_info) from e
    elif e.code().name == "INVALID_ARGUMENT":
        raise SushiInvalidArgumentError(e.details(), context_info) from e
    elif e.code().name == "INTERNAL":
        raise SushiInternalError(e.details(), context_info) from e
    else:
        print("Grpc error: " + str(e.code().name) + ", " + e.details())
        raise e


###############################
# Main sushi controller class #
###############################


class SushiController:
    """
    A class to control sushi via gRPC.
    This class creates one instance of each different controller type and makes
    these sub-controllers available as member variables. See the documentation
    of the separate sub-controllers for their usage.

    Attributes:
        _stub (SushiControllerStub): Connection stubs to the gRPC interface implemented in sushi.

    Notes:
        close() should ALWAYS be called as part of an application housekeeping/cleanup-before-shutdown routine as it
        ensure proper releasing of resources and clean joining of concurrent threads.
    """

    def __init__(
        self,
        address="localhost:51051",
        sushi_proto_def="/usr/share/sushi/sushi_rpc.proto",
    ):
        """
        The constructor for the SushiController class setting up the gRPC connection with sushi.

        Parameters:
            address (str): 'ip-addres:port' The ip-addres and port at which to connect to sushi.
            sushi_proto_def (str): path to .proto file with SUSHI's gRPC services definition
        """
        self.audio_graph = audiographcontroller.AudioGraphController(
            self, address, sushi_proto_def
        )
        self.keyboard = keyboardcontroller.KeyboardController(
            address, sushi_proto_def)
        self.parameters = parametercontroller.ParameterController(
            address, sushi_proto_def
        )
        self.programs = programcontroller.ProgramController(
            address, sushi_proto_def)
        self.timings = timingcontroller.TimingController(
            address, sushi_proto_def)
        self.transport = transportcontroller.TransportController(
            address, sushi_proto_def
        )
        self.audio_routing = audioroutingcontroller.AudioRoutingController(
            address, sushi_proto_def
        )
        self.midi_controller = midicontroller.MidiController(
            address, sushi_proto_def)
        self.cv_gate_controller = cvgatecontroller.CvGateController(
            address, sushi_proto_def
        )
        self.osc_controller = osccontroller.OscController(
            address, sushi_proto_def)
        self.system = systemcontroller.SystemController(
            address, sushi_proto_def)
        self.session = sessioncontroller.SessionController(
            address, sushi_proto_def)
        self.notifications = notificationcontroller.NotificationController(
            self, address, sushi_proto_def
        )

        self.audiograph_event_queue: list[ElkpyEvent] = []
        self.processor_event_queue = []
        self.parameter_event_queue = []

    def close(self):
        """
        This method should be called at app close.
        It should call any sub-controller close routines whenever they exist.
        i.e.: NotificationController has an infinite event loop running in its own thread, which has to be stopped and joined
        to ensure clean closing and proper releasing of any resources.
        """
        self.notifications.close()

    def __del__(self):
        self.notifications.close()
