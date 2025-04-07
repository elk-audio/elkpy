__author__ = "Gustav Andersson "
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

import grpc

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from elkpy.sushicontroller import SushiController

from .events import SushiCommandResponse
from . import sushierrors
from . import grpc_gen


##################################
# Sushi session controller class #
##################################


class SessionController:
    """
    A class to save and restore the full state of a sushi session.

    Attributes:
        _stub (SessionControllerStub): Connection stubs to the session interface implemented in sushi.
    """

    def __init__(
        self,
        parent: 'SushiController',
        address: str='localhost:51051',
        sushi_proto_def: str='/usr/share/sushi/sushi_rpc.proto',
        sushi_proto = None, sushi_grpc = None) -> None:
        """
        The constructor for the SessionController class setting up the gRPC connection with sushi.

        Parameters:
            address (str): 'ip-addres:port' The ip-addres and port at which to connect to sushi.
            sushi_proto_def (str): path to .proto file with SUSHI's gRPC services definition
        """
        try:
            channel = grpc.insecure_channel(address)
        except AttributeError as e:
            raise TypeError(
                "Parameter address = {}. Should be a string containing the ip-address and port of sushi ('ip-address:port')".format(
                    address
                )
            ) from e

        if sushi_proto and sushi_grpc:
            self._sushi_proto = sushi_proto
            self._sushi_grpc = sushi_grpc
        else:
            self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(sushi_proto_def)
        self._stub = self._sushi_grpc.SessionControllerStub(channel)
        self._parent = parent

    def save_binary_session(self) -> bytes | None:
        """
        Save the sushi session.

        Returns:
            bytes: A bytes object containing the complete state of the sushi session.
        """
        try:
            response = self._stub.SaveSession(
                self._sushi_proto.GenericVoidValue())
            return response.SerializeToString()

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def restore_binary_session(self, binary_session: bytes) -> SushiCommandResponse:
        """
        Restore the sushi session from a previously save session state. This will clear all track and loaded plugins

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            grpc_state = self._sushi_proto.SessionState()
            grpc_state.ParseFromString(binary_session)
            cr = self._stub.RestoreSession(grpc_state)
            return self._parent.validate_command_response(cr, "Restore session")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)
