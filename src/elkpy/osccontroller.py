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

import grpc

from . import sushierrors
from . import sushi_info_types as info_types
from . import grpc_gen
from typing import List

##################################
#   Sushi OSC Controller class   #
##################################


class OscController(object):
    """
    Class to manage OSC communication features in Sushi. It can change the OSC port and enable/disable
    OSC output for particular parameters
    """
    def __init__(self,
                 address: str = 'localhost:51051',
                 sushi_proto_def: str = '/usr/share/sushi/sushi_rpc.proto') -> None:
        """
        The constructor for the MidiController class setting up the gRPC connection with sushi.

        Parameters:
            address (str): IP address to Sushi in the uri form : 'ip-addr:port'
            sushi_proto_def (str): path to the .proto file with SUSHI gRPC services definitions
        """
        try:
            channel = grpc.insecure_channel(address)
        except AttributeError as e:
            raise TypeError(f"Parameter address = {address}. Should be a string containing the ip-address and port "
                            f"to Sushi") from e

        self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(sushi_proto_def)
        self._stub = self._sushi_grpc.OscControllerStub(channel)

    def get_send_port(self) -> int:
        """
        The the current port that OSC is transmitting to

        Returns:
            int: The port number
        """
        try:
            response = self._stub.GetSendPort(self._sushi_proto.GenericVoidValue())
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
            response = self._stub.GetReceivePort(self._sushi_proto.GenericVoidValue())
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
            response = self._stub.GetEnabledParameterOutputs(self._sushi_proto.GenericVoidValue())
            return [path for path in response.path]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def enable_output_for_parameter(self, processor_id: int, parameter_id: int) -> None:
        """
        Enable OSC for a parameter

        Parameters:
            processor_id (int): The id of the processor the parameter belongs to
            parameter_id (int): The id of the parameter to enable OSC for
        """
        try:
            self._stub.EnableOutputForParameter(self._sushi_proto.ParameterIdentifier(processor_id=processor_id, parameter_id=parameter_id))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disable_output_for_parameter(self, processor_id: int, parameter_id: int) -> None:
        """
        Disable OSC for a parameter

        Parameters:
            processor_id (int): The id of the processor the parameter belongs to
            parameter_id (int): The id of the parameter to disble OSC for
        """
        try:
            self._stub.DisableOutputForParameter(self._sushi_proto.ParameterIdentifier(processor_id=processor_id, parameter_id=parameter_id))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def enable_all_output(self):
        """
        Enable OSC output for all parameters
        """
        try:
            self._stub.EnableAllOutput(self._sushi_proto.GenericVoidValue())
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disable_all_output(self):
        """
        Disable OSC output for all parameters
        """
        try:
            self._stub.DisableAllOutput(self._sushi_proto.GenericVoidValue())
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)
