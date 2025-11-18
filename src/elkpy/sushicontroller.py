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

from pathlib import Path
from typing import Any
import re
import sys

from .events import SushiCommandResponse

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
from . import grpc_gen

from .sushi_info_types import CommandResponseStatus
from . import sushierrors


sushi_proto = Path(__file__).parent / "rpc" / "sushi_rpc.proto"


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
        sushi_proto_def=sushi_proto,
        auto_update_async_command_responses: bool = True,
    ):
        """
        The constructor for the SushiController class setting up the gRPC connection with sushi.

        Parameters:
            - address (str): 'ip-addres:port' The ip-addres and port at which to connect to sushi.
            - sushi_proto_def (str): path to .proto file with SUSHI's gRPC services definition
            - auto_update_async_command_responses (bool): controls whether the notificaton controller
                    listens to async command response notifications and manages pending command
                    responses.
        """
        self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(
            str(sushi_proto_def)
        )

        self.audio_graph = audiographcontroller.AudioGraphController(
            self, address, str(sushi_proto_def), self._sushi_proto, self._sushi_grpc
        )
        self.keyboard = keyboardcontroller.KeyboardController(
            self, address, str(sushi_proto_def), self._sushi_proto, self._sushi_grpc
        )
        self.parameters = parametercontroller.ParameterController(
            self, address, str(sushi_proto_def), self._sushi_proto, self._sushi_grpc
        )
        self.programs = programcontroller.ProgramController(
            self, address, str(sushi_proto_def)
        )
        self.timings = timingcontroller.TimingController(
            self, address, str(sushi_proto_def), self._sushi_proto, self._sushi_grpc
        )
        self.transport = transportcontroller.TransportController(
            self, address, str(sushi_proto_def), self._sushi_proto, self._sushi_grpc
        )
        self.audio_routing = audioroutingcontroller.AudioRoutingController(
            self, address, str(sushi_proto_def), self._sushi_proto, self._sushi_grpc
        )
        self.midi_controller = midicontroller.MidiController(
            self, address, str(sushi_proto_def), self._sushi_proto, self._sushi_grpc
        )
        self.cv_gate_controller = cvgatecontroller.CvGateController(
            self, address, str(sushi_proto_def), self._sushi_proto, self._sushi_grpc
        )
        self.osc_controller = osccontroller.OscController(
            self, address, str(sushi_proto_def), self._sushi_proto, self._sushi_grpc
        )
        self.system = systemcontroller.SystemController(address, str(sushi_proto_def))
        self.session = sessioncontroller.SessionController(
            self, address, str(sushi_proto_def), self._sushi_proto, self._sushi_grpc
        )

        if not self.check_sushi_api_compatibility():
            sys.exit()

        self.notifications = notificationcontroller.NotificationController(
            self,
            address,
            str(sushi_proto_def),
            self._sushi_proto,
            self._sushi_grpc,
            auto_update_async_command_responses,
        )

        self.command_responses: dict[int, SushiCommandResponse] = {}

    def check_sushi_api_compatibility(self) -> bool:
        """Verifies that the version of the api used by elkpy matches the one build in Sushi"""

        api_proto_file = Path(__file__).parent / "rpc" / "api_version.proto"

        with open(api_proto_file, 'r') as f:
            content = f.read()
        
        # Find: [default = "something"]
        match = re.search(r'\[default\s*=\s*"([^"]+)"\]', content)
        
        if match:
            api_version = match.group(1)
            sushi_version = self.system.get_sushi_api_version() 
            if api_version == sushi_version:
                print("API match!")
                return True
            else:
                print(f"API version mismatch! Sushi = {sushi_version} <-> Elkpy = {api_version}")
                sys.exit()
        
        raise ValueError("No default api version found")


    def validate_command_response(self, cr, context_info: str = "") -> Any:
        match CommandResponseStatus(cr.status.status):
            case CommandResponseStatus.SUCCESS:
                return cr
            case CommandResponseStatus.ERROR:
                raise sushierrors.SushiUnkownError(context_info)
            case CommandResponseStatus.UNSUPPORTED_OPERATION:
                raise sushierrors.SushiUnsupportedOperationError(context_info)
            case CommandResponseStatus.NOT_FOUND:
                raise sushierrors.SushiNotFoundError(context_info)
            case CommandResponseStatus.OUT_OF_RANGE:
                raise sushierrors.SushiOutOfRangeError(context_info)
            case CommandResponseStatus.INVALID_ARGUMENTS:
                raise sushierrors.SushiInvalidArgumentError(context_info)
            case CommandResponseStatus.ASYNC_RESPONSE:
                event = SushiCommandResponse(id=cr.id)
                self.command_responses[cr.id] = event
                return event

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
