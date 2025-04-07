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

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from elkpy.sushicontroller import SushiController

from .events import SushiCommandResponse
import grpc

from . import sushierrors
from . import grpc_gen
from . import sushi_info_types as info_types
from typing import List

####################################
# Sushi parameter controller class #
####################################

class ParameterController:
    """
    A class to control the parameter in sushi via gRPC. It manages the parameters of sushi. Enabling
    getting and setting of values as well as getting info about what parameters are availble and their
    ranges, types, etc.

    Attributes:
        _stub (ParameterControllerStub): Connection stubs to the gRPC parameter interface implemented in sushi.
    """
    def __init__(self,
                 parent: 'SushiController',
                 address = 'localhost:51051',
                 sushi_proto_def = '/usr/share/sushi/sushi_rpc.proto',
                 sushi_proto = None, sushi_grpc = None):
        """
        The constructor for the ParameterController class setting up the gRPC connection with sushi.

        Parameters:
            address (str): 'ip-addres:port' The ip-addres and port at which to connect to sushi.
            sushi_proto_def (str): path to .proto file with SUSHI's gRPC services definition
        """
        try:
            channel = grpc.insecure_channel(address)
        except AttributeError as e:
            raise TypeError("Parameter address = {}. Should be a string containing the ip-address and port of sushi ('ip-address:port')".format(address)) from e

        if sushi_proto and sushi_grpc:
            self._sushi_proto = sushi_proto
            self._sushi_grpc = sushi_grpc
        else:
            self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(sushi_proto_def)

        self._stub = self._sushi_grpc.ParameterControllerStub(channel)
        self._parent = parent

    def get_track_parameters(self, track_identifier: int) -> List[info_types.ParameterInfo]:
        """
        Get a list of parameters available on the specified track.

        Parameters:
            track_identifier (int): The id of the track to get the parameter list from.

        Returns:
            List[info_types.ParameterInfo]: A list of the info of the parameters assigned to the track matching the id.
        """
        try:
            cr = self._stub.GetTrackParameters(self._sushi_proto.TrackIdentifier(
                id = track_identifier
            ))

            response = self._parent.validate_command_response(cr, f"Get parameters for track {track_identifier}")
            parameter_info_list = []
            for parameter_info in response.parameters:
                parameter_info_list.append(info_types.ParameterInfo(parameter_info))

            return parameter_info_list

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With track id: {}".format(track_identifier))

    def get_processor_parameters(self, processor_identifier: int) -> List[info_types.ParameterInfo]:
        """
        Get a list of the parameters available to the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameters from.

        Returns:
            List[info_types.ParameterInfo]: A list of the parameters available to the processor matching the id.
        """
        try:
            cr = self._stub.GetProcessorParameters(self._sushi_proto.ProcessorIdentifier(
                id = processor_identifier
            ))
            response = self._parent.validate_command_response(cr, f"Get parameters for processor {processor_identifier}")

            parameter_info_list = []
            for parameter_info in response.parameters:
                parameter_info_list.append(info_types.ParameterInfo(parameter_info))

            return parameter_info_list

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}".format(processor_identifier))

    def get_parameter_id(self, processor_identifier: int, parameter_name: str) -> int:
        """
        Get the id of the parameter of the specified processor corresponding to the specified parameter name.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameter id from.
            parameter_name (str): The name of the parameter to get the id from.

        Returns:
            int: The id of the parameter matching the parameter name.
        """
        try:
            cr = self._stub.GetParameterId(self._sushi_proto.ParameterIdRequest(
                processor = self._sushi_proto.ProcessorIdentifier(id = processor_identifier),
                ParameterName = parameter_name
            ))
            response = self._parent.validate_command_response(cr, f"Get parameters for processor {processor_identifier}")
            return response.id.parameter_id

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter name: {}".format(processor_identifier, parameter_name))

    def get_parameter_info(self, processor_identifier: int, parameter_identifier: int) -> info_types.ParameterInfo:
        """
        Get info about the specified parameter on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameter info from.
            parameter_identifier (int): The id of the parameter to get the info from.

        Returns:
            info_types.ParameterInfo: Info of the parameter matching the id.
        """
        try:
            cr = self._stub.GetParameterInfo(self._sushi_proto.ParameterIdentifier(
                processor_id = processor_identifier,
                parameter_id = parameter_identifier
            ))
            response = self._parent.validate_command_response(cr, f"Get info for parameter {parameter_identifier}")
            return info_types.ParameterInfo(response.info)

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter id: {}".format(processor_identifier, parameter_identifier))

    def get_parameter_value(self, processor_identifier: int, parameter_identifier: int) -> float:
        """
        Get the value of the parameter matching the specified parameter on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameter value from.
            parameter_identifier (int): The id of the parameter to get the value from.

        Returns:
            float: The value of the parameter matching the id.
        """
        try:
            cr = self._stub.GetParameterValue(self._sushi_proto.ParameterIdentifier(
                processor_id = processor_identifier,
                parameter_id = parameter_identifier
            ))
            response = self._parent.validate_command_response(cr, f"Get value of parameter {parameter_identifier}")
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter id: {}".format(processor_identifier, parameter_identifier))

    def get_parameter_value_in_domain(self, processor_identifier: int, parameter_identifier: int) -> float:
        """
        Get the normalised value of the parameter matching the specified parameter on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the normalised parameter value from.
            parameter_identifier (int): The id of the parameter to get the normalised value from.

        Returns:
            float: The normalised value of the parameter matching the id.
        """
        try:
            cr = self._stub.GetParameterValueInDomain(self._sushi_proto.ParameterIdentifier(
                processor_id = processor_identifier,
                parameter_id = parameter_identifier
            ))
            response = self._parent.validate_command_response(cr, f"Get value of parameter {parameter_identifier} in domain")
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter id: {}".format(processor_identifier,parameter_identifier))

    def get_parameter_value_as_string(self, processor_identifier: int, parameter_identifier: int) -> str:
        """
        Get the value of the parameter matching the specified parameter on the specified processor as a string.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameter value string from.
            parameter_identifier (int): The id of the parameter to get value string from.

        Returns:
            str: The value as a string of the parameter matching the id.
        """
        try:
            cr = self._stub.GetParameterValueAsString(self._sushi_proto.ParameterIdentifier(
                processor_id = processor_identifier,
                parameter_id = parameter_identifier
            ))
            response = self._parent.validate_command_response(cr, f"Get value of parameter {parameter_identifier} as string")
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter id: {}".format(processor_identifier, parameter_identifier))

    def set_parameter_value(self, processor_identifier: int, parameter_identifier: int, value: float) -> SushiCommandResponse:
        """
        Set the value of the specified parameter on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor that has the parameter to be changed.
            parameter_identifier (int): The id of the property to set the value of.

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.SetParameterValue(self._sushi_proto.ParameterValue(
                parameter = self._sushi_proto.ParameterIdentifier(
                    processor_id = processor_identifier,
                    parameter_id = parameter_identifier
                    ),
                value = value
            ))
            return self._parent.validate_command_response(cr, f"Get value of parameter {parameter_identifier} as string")

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, property id: {}, value: {}".format(processor_identifier, parameter_identifier, value))

    def get_track_properties(self, track_identifier: int) -> List[info_types.PropertyInfo]:
        """
        Get a list of string properties available on the specified track.

        Parameters:
            track_identifier (int): The id of the track to get the property list from.

        Returns:
            List[info_types.PropertyInfo]: A list of the info of the properties assigned to the track matching the id.
        """
        try:
            cr = self._stub.GetTrackProperties(self._sushi_proto.TrackIdentifier(
                id = track_identifier
            ))
            response = self._parent.validate_command_response(cr, f"Get properties for track {track_identifier}")

            property_info_list = []
            for property_info in response.properties:
                property_info_list.append(info_types.PropertyInfo(property_info))

            return property_info_list

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With track id: {}".format(track_identifier))

    def get_processor_properties(self, processor_identifier: int) -> List[info_types.PropertyInfo]:
        """
        Get a list of the string properties available to the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the properties from.

        Returns:
            List[info_types.PropertyInfo]: A list of the properties available to the processor matching the id.
        """
        try:
            cr = self._stub.GetProcessorProperties(self._sushi_proto.ProcessorIdentifier(
                id = processor_identifier
            ))
            response = self._parent.validate_command_response(cr, f"Get properties for processor {processor_identifier}")

            property_info_list = []
            for property_info in response.properties:
                property_info_list.append(info_types.PropertyInfo(property_info))

            return property_info_list

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}".format(processor_identifier))

    def get_property_id(self, processor_identifier: int, property_name: str) -> int:
        """
        Get the id of the property of the specified processor corresponding to the specified property name.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameter id from.
            property_name (str): The name of the property to get the id from.

        Returns:
            int: The id of the property matching the property name.
        """
        try:
            cr = self._stub.GetPropertyId(self._sushi_proto.PropertyIdRequest(
                processor = self._sushi_proto.ProcessorIdentifier(id = processor_identifier),
                property_name = property_name
            ))
            response = self._parent.validate_command_response(cr, f"Get id for property {property_name}")
            return response.id.property_id

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, string property name: {}".format(processor_identifier, property_name))

    def get_property_info(self, processor_identifier: int, property_identifier: int) -> info_types.PropertyInfo:
        """
        Get info about the specified property on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameter info from.
            property_identifier (int): The id of the string property to get the info from.

        Returns:
            info_types.PropertyInfo: Info of the property matching the id.
        """
        try:
            cr = self._stub.GetPropertyInfo(self._sushi_proto.PropertyIdentifier(
                processor_id = processor_identifier,
                property_id = property_identifier
            ))
            response = self._parent.validate_command_response(cr, f"Get info for property {processor_identifier}")
            return info_types.PropertyInfo(response.info)

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, property id: {}".format(processor_identifier, property_identifier))

    def get_property_value(self, processor_identifier: int, property_identifier: int) -> str:
        """
        Get the value of the property matching the specified property on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameter value string from.
            property_identifier (int): The id of the string property to get value string from.

        Returns:
            str: The value of the property matching the id.
        """
        try:
            cr = self._stub.GetPropertyValue(self._sushi_proto.PropertyIdentifier(
                processor_id = processor_identifier,
                property_id = property_identifier
            ))
            response = self._parent.validate_command_response(cr, f"Get value of property {property_identifier}")
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, property id: {}".format(processor_identifier, property_identifier))

    def set_property_value(self, processor_identifier: int, property_identifier: int, value: float) -> SushiCommandResponse:
        """
        Set the value of the specified property on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor that has the property to be changed.
            property_identifier (int): The id of the property to set the value of.
            value (string) : The new value to assign to the property

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.SetPropertyValue(self._sushi_proto.PropertyValue(
                property = self._sushi_proto.PropertyIdentifier(
                    processor_id = processor_identifier,
                    property_id = property_identifier
                    ),
                value = value
            ))
            return self._parent.validate_command_response(cr, f"Set value of property {property_identifier}")

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, property id: {}, value: {}".format(processor_identifier, property_identifier, value))
