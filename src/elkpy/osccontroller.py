__author__ = "Maxime Gendebien"
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

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from elkpy.sushicontroller import SushiController
from .events import SushiCommandResponse
import grpc
from . import sushierrors
from .rpc import sushi_rpc_pb2

##################################
#   Sushi OSC Controller class   #
##################################


class OscController:
    """
    Class to manage OSC communication features in Sushi. It can change the OSC port and enable/disable
    OSC output for particular parameters
    """

    def __init__(self, parent: "SushiController", stub) -> None:
        self._stub = stub
        self._parent = parent

    def get_send_port(self) -> int:
        """
        The the current port that OSC is transmitting to

        Returns:
            int: The port number
        """
        try:
            response = self._stub.GetSendPort(sushi_rpc_pb2.GenericVoidValue())
            return response.value
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_receive_port(self) -> int:
        """
        The the current port that OSC is receiving on

        Returns:
            int: The port number
        """
        try:
            response = self._stub.GetReceivePort(sushi_rpc_pb2.GenericVoidValue())
            return response.value
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_enabled_parameter_outputs(self) -> List[str]:
        """
        Get which parameters have OSC output enabled

        Returns:
            List[str]: List of names of the parameters for which OSC is enabled
        """
        try:
            response = self._stub.GetEnabledParameterOutputs(
                sushi_rpc_pb2.GenericVoidValue()
            )
            return [path for path in response.path]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def enable_output_for_parameter(
        self, processor_id: int, parameter_id: int
    ) -> SushiCommandResponse:
        """
        Enable OSC for a parameter

        Parameters:
            processor_id (int): The id of the processor the parameter belongs to
            parameter_id (int): The id of the parameter to enable OSC for

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.EnableOutputForParameter(
                sushi_rpc_pb2.ParameterIdentifier(
                    processor_id=processor_id, parameter_id=parameter_id
                )
            )
            return self._parent.validate_command_response(
                cr, f"Enable output for parameter {parameter_id}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disable_output_for_parameter(
        self, processor_id: int, parameter_id: int
    ) -> SushiCommandResponse:
        """
        Disable OSC for a parameter

        Parameters:
            processor_id (int): The id of the processor the parameter belongs to
            parameter_id (int): The id of the parameter to disble OSC for

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DisableOutputForParameter(
                sushi_rpc_pb2.ParameterIdentifier(
                    processor_id=processor_id, parameter_id=parameter_id
                )
            )
            return self._parent.validate_command_response(
                cr, f"Disable output for parameter {parameter_id}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def enable_all_output(self) -> SushiCommandResponse:
        """
        Enable OSC output for all parameters

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.EnableAllOutput(sushi_rpc_pb2.GenericVoidValue())
            return self._parent.validate_command_response(cr, "Enable all outputs")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disable_all_output(self) -> SushiCommandResponse:
        """
        Disable OSC output for all parameters

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DisableAllOutput(sushi_rpc_pb2.GenericVoidValue())
            return self._parent.validate_command_response(cr, "Disable all outputs")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)
