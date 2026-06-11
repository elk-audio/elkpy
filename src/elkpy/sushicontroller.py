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

from .sushi_info_types import CommandResponseStatus
from . import sushierrors

DEFAULT_SUSHI_RPC_PORT = "localhost:51051"
DEFAULT_SUSHI_IPC_PORT = "ipc:///tmp/sushi_ipc.sock"
DEFAULT_SUSHI_IPC_SUB_PORT = "ipc:///tmp/sushi_pub.sock"

###############################
# Main sushi controller class #
###############################

class SushiController:
    """
    A class to control sushi via gRPC or ZMQ/IPC.
    This class creates one instance of each different controller type and makes
    these sub-controllers available as member variables. See the documentation
    of the separate sub-controllers for their usage.

    Notes:
        close() should ALWAYS be called as part of an application housekeeping/cleanup-before-shutdown routine as it
        ensure proper releasing of resources and clean joining of concurrent threads.
    """

    def __init__(
        self,
        address: str = None,
        sub_address: str = None,
        transport: str = "RPC",
        auto_update_async_command_responses: bool = False,
    ):
        """
        The constructor for the SushiController class.

        Parameters:
            - address (str): Connection address. For RPC: 'ip-address:port' (default 'localhost:51051').
                             For IPC: ZMQ address (default 'ipc:///tmp/sushi_ipc.sock').
            - transport (str): 'RPC' for gRPC (default) or 'IPC' for ZMQ over a local socket.
            - auto_update_async_command_responses (bool): controls whether the notification controller
                    listens to async command response notifications and manages pending command
                    responses. Only applicable in RPC mode.
        """
        self.command_responses: dict[int, SushiCommandResponse] = {}

        if transport == "IPC":
            from .rpc.sushi_zmq_stub import SushiZmqStub
            addr = address or DEFAULT_SUSHI_IPC_PORT
            sub_addr = sub_address or DEFAULT_SUSHI_IPC_SUB_PORT
            stub = SushiZmqStub(addr)
            self.audio_graph = audiographcontroller.AudioGraphController(self, stub)
            self.keyboard = keyboardcontroller.KeyboardController(self, stub)
            self.parameters = parametercontroller.ParameterController(self, stub)
            self.programs = programcontroller.ProgramController(self, stub)
            self.timings = timingcontroller.TimingController(self, stub)
            self.transport = transportcontroller.TransportController(self, stub)
            self.audio_routing = audioroutingcontroller.AudioRoutingController(self, stub)
            self.midi_controller = midicontroller.MidiController(self, stub)
            self.cv_gate_controller = cvgatecontroller.CvGateController(self, stub)
            self.osc_controller = osccontroller.OscController(self, stub)
            self.system = systemcontroller.SystemController(stub)
            self.session = sessioncontroller.SessionController(self, stub)
            from .zmq_notificationcontroller import ZmqNotificationController
            self.notifications = ZmqNotificationController(self, stub, pub_address=sub_addr,
                auto_update_async_command_responses=auto_update_async_command_responses
            )
        else:
            import grpc
            from .rpc import sushi_rpc_pb2_grpc
            addr = address or DEFAULT_SUSHI_RPC_PORT
            channel = grpc.insecure_channel(addr)
            self.audio_graph = audiographcontroller.AudioGraphController(self, sushi_rpc_pb2_grpc.AudioGraphControllerStub(channel))
            self.keyboard = keyboardcontroller.KeyboardController(self, sushi_rpc_pb2_grpc.KeyboardControllerStub(channel))
            self.parameters = parametercontroller.ParameterController(self, sushi_rpc_pb2_grpc.ParameterControllerStub(channel))
            self.programs = programcontroller.ProgramController(self, sushi_rpc_pb2_grpc.ProgramControllerStub(channel))
            self.timings = timingcontroller.TimingController(self, sushi_rpc_pb2_grpc.TimingControllerStub(channel))
            self.transport = transportcontroller.TransportController(self, sushi_rpc_pb2_grpc.TransportControllerStub(channel))
            self.audio_routing = audioroutingcontroller.AudioRoutingController(self, sushi_rpc_pb2_grpc.AudioRoutingControllerStub(channel))
            self.midi_controller = midicontroller.MidiController(self, sushi_rpc_pb2_grpc.MidiControllerStub(channel))
            self.cv_gate_controller = cvgatecontroller.CvGateController(self, sushi_rpc_pb2_grpc.CvGateControllerStub(channel))
            self.osc_controller = osccontroller.OscController(self, sushi_rpc_pb2_grpc.OscControllerStub(channel))
            self.system = systemcontroller.SystemController(sushi_rpc_pb2_grpc.SystemControllerStub(channel))
            self.session = sessioncontroller.SessionController(self, sushi_rpc_pb2_grpc.SessionControllerStub(channel))
            self.notifications = notificationcontroller.NotificationController(
                self, addr, auto_update_async_command_responses
            )

        try:
            self.check_sushi_api_compatibility()
        except sushierrors.SushiNotFoundError:
            print(f"ELKPY: Could not find a running Sushi at {addr}")
        except sushierrors.SushiAPIMismatchError:
            pass

    def check_sushi_api_compatibility(self) -> bool:
        """Verifies that the version of the api used by elkpy matches the one build in Sushi"""

        api_proto_file = Path(__file__).parent / "rpc" / "api_version.proto"

        with open(api_proto_file, "r") as f:
            content = f.read()

        # Find: [default = "something"]
        match = re.search(r'\[default\s*=\s*"([^"]+)"\]', content)

        if match:
            api_version = match.group(1)
            try:
                sushi_version = self.system.get_sushi_api_version()
                if api_version == sushi_version:
                    print(f"ELKPY: Sushi API match! -> {api_version}")
                    return True
                else:
                    print(
                        f"ELKPY: API version mismatch! Sushi = {sushi_version} <-> Elkpy = {api_version}"
                    )
                    raise sushierrors.SushiAPIMismatchError()
            except Exception:
                raise sushierrors.SushiNotFoundError()

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
        if self.notifications is not None:
            self.notifications.close()

    def __del__(self):
        if self.notifications is not None:
            self.notifications.close()
