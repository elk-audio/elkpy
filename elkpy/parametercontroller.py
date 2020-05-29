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
from typing import List

####################################
# Sushi parameter controller class #
####################################

class ParameterController(object):
    '''
    A class to control the parameter in sushi via gRPC.

    Attributes:
        _stub (ParameterControllerStub): Connection stubs to the gRPC parameter interface implemented in sushi.
    '''
    def __init__(self,
                 address = 'localhost:51051',
                 sushi_proto_def = '/usr/share/sushi/sushi_rpc.proto'):
        '''
        The constructor for the ParameterController class.

        Parameters:
            address (str): 'ip-addres:port' The ip-addres and port at which to connect to sushi.
            sushi_proto_def (str): path to .proto file with SUSHI's gRPC services definition
        '''
        try:
            channel = grpc.insecure_channel(address)
        except AttributeError as e:
            raise TypeError("Parameter address = {}. Should be a string containing the ip-address and port of sushi ('ip-address:port')".format(address)) from e

        self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(sushi_proto_def)
        self._stub = self._sushi_grpc.ParameterControllerStub(channel)


    def get_track_parameters(self, track_identifier: int) -> List[info_types.ParameterInfo]:
        '''
        Get a list of parameters available on the specified track.

        Parameters:
            track_identifier (int): The id of the track to get the parameter list from.

        Returns:
            List[info_types.ParameterInfo]: A list of the info of the parameters assigned to the track matching the id.
        '''
        try:
            response = self._stub.GetTrackParameters(self._sushi_proto.TrackIdentifier(
                id = track_identifier
            ))

            parameter_info_list = []
            for parameter_info in response.parameters:
                parameter_info_list.append(info_types.ParameterInfo(parameter_info))

            return parameter_info_list

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With track id: {}".format(track_identifier))

    def get_processor_parameters(self, processor_identifier: int) -> List[info_types.ParameterInfo]:
        '''
        Get a list of the parameters available to the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameters from.

        Returns:
            List[info_types.ParameterInfo]: A list of the parameters available to the processor matching the id.
        '''
        try:
            response = self._stub.GetProcessorParameters(self._sushi_proto.ProcessorIdentifier(
                id = processor_identifier
            ))

            parameter_info_list = []
            for parameter_info in response.parameters:
                parameter_info_list.append(info_types.ParameterInfo(parameter_info))

            return parameter_info_list

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}".format(processor_identifier))

    def get_parameter_id(self, processor_identifier: int, parameter_name: str) -> int:
        '''
        Get the id of the parameter of the specified processor corresponding to the specified parameter name.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameter id from.
            parameter_name (str): The name of the parameter to get the id from.

        Returns:
            int: The id of the parameter matching the parameter name.
        '''
        try:
            response = self._stub.GetParameterId(self._sushi_proto.ParameterIdRequest(
                processor = self._sushi_proto.ProcessorIdentifier(id = processor_identifier),
                ParameterName = parameter_name
            ))
            return response.parameter_id

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter name: {}".format(processor_identifier, parameter_name))

    def get_parameter_info(self, processor_identifier: int, parameter_identifier: int) -> info_types.ParameterInfo:
        '''
        Get info about the specified parameter on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameter info from.
            parameter_identifier (int): The id of the parameter to get the info from.

        Returns:
            info_types.ParameterInfo: Info of the parameter matching the id.
        '''
        try:
            response = self._stub.GetParameterInfo(self._sushi_proto.ParameterIdentifier(
                processor_id = processor_identifier,
                parameter_id = parameter_identifier
            ))
            return info_types.ParameterInfo(response)

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter id: {}".format(processor_identifier, parameter_identifier))

    def get_parameter_value(self, processor_identifier: int, parameter_identifier: int) -> float:
        '''
        Get the value of the parameter matching the specified parameter on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameter value from.
            parameter_identifier (int): The id of the parameter to get the value from.

        Returns:
            float: The value of the parameter matching the id.
        '''
        try:
            response = self._stub.GetParameterValue(self._sushi_proto.ParameterIdentifier(
                processor_id = processor_identifier,
                parameter_id = parameter_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter id: {}".format(processor_identifier, parameter_identifier))

    def get_parameter_value_in_domain(self, processor_identifier: int, parameter_identifier: int) -> float:
        '''
        Get the normalised value of the parameter matching the specified parameter on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the normalised parameter value from.
            parameter_identifier (int): The id of the parameter to get the normalised value from.

        Returns:
            float: The normalised value of the parameter matching the id.
        '''
        try:
            response = self._stub.GetParameterValueInDomain(self._sushi_proto.ParameterIdentifier(
                processor_id = processor_identifier,
                parameter_id = parameter_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter id: {}".format(processor_identifier,parameter_identifier))

    def get_parameter_value_as_string(self, processor_identifier: int, parameter_identifier: int) -> str:
        '''
        Get the value of the parameter matching the specified parameter on the specified processor as a string.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameter value string from.
            parameter_identifier (int): The id of the parameter to get value string from.

        Returns:
            str: The value as a string of the parameter matching the id.
        '''
        try:
            response = self._stub.GetParameterValueAsString(self._sushi_proto.ParameterIdentifier(
                processor_id = processor_identifier,
                parameter_id = parameter_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter id: {}".format(processor_identifier, parameter_identifier))

    def set_parameter_value(self, processor_identifier: int, parameter_identifier: int, value: float) -> None:
        '''
        Set the value of the specified parameter on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor that has the parameter to be changed.
            parameter_identifier (int): The id of the parameter to set the value of.
        '''
        try:
            self._stub.SetParameterValue(self._sushi_proto.ParameterValue(
                parameter = self._sushi_proto.ParameterIdentifier(
                    processor_id = processor_identifier,
                    parameter_id = parameter_identifier
                    ),
                value = value
            ))

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter id: {}, value: {}".format(processor_identifier, parameter_identifier, value))
