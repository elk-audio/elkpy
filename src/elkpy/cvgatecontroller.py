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

######################################
#   Sushi CV-Gate Controller class   #
######################################


class CvGateController(object):
    """
    Class to manage CV/Gate connections in Sushi via gRPC. It creates, deletes and gets info about
    Cv/Gate connections on sushi tracks.

    Attributes:
        _stub (CvGateControllerStub): Connection stub to the gRPC CvGate interface.
    """
    def __init__(self,
                 address='localhost:51051',
                 sushi_proto_def='/usr/share/sushi/sushi_rpc.proto'):
        """
        The constructor for the CvGateController class setting up the gRPC connection with sushi.

        Args:
            address: IP address to Sushi in the uri form : 'ip-addr:port'
            sushi_proto_def: path to the .proto file with SUSHI gRPC services definitions
        """
        try:
            channel = grpc.insecure_channel(address)
        except AttributeError as e:
            raise TypeError(f"Parameter address = {address}. Should be a string with the IP address and port of Sushi") from e

        self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(sushi_proto_def)
        self._stub = self._sushi_grpc.CvGateControllerStub(channel)

    def get_cv_input_channel_count(self) -> int:
        """
        Gets a count of all CV input channels

        Returns:
            int: count
        """
        try:
            response = self._stub.GetCvInputChannelCount(self._sushi_proto.GenericVoidValue())
            return response.value
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_cv_output_channel_count(self) -> int:
        """
        Gets a count of all CV output channels

        Returns:
            int: count
        """
        try:
            response = self._stub.GetCvOutputChannelCount(self._sushi_proto.GenericVoidValue())
            return response.value
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_all_cv_input_connections(self) -> List[info_types.CvConnection]:
        """
        Gets all CV input connections

        Returns:
            List[info_types.CvConnection]: List of CvConnection objects
        """
        try:
            response = self._stub.GetAllCvInputConnections(self._sushi_proto.GenericVoidValue())
            return [info_types.CvConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_all_cv_output_connections(self) -> List[info_types.CvConnection]:
        """
        Gets all CV output connections

        Returns:
            List[info_types.CvConnection]: List of CvConnection objects
        """
        try:
            response = self._stub.GetAllCvOutputConnections(self._sushi_proto.GenericVoidValue())
            return [info_types.CvConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_all_gate_input_connections(self) -> List[info_types.GateConnection]:
        """
        Gets all Gate input connections

        Returns:
            List[info_types.GateConnection]: List of GateConnection objects
        """
        try:
            response = self._stub.GetAllGateInputConnections(self._sushi_proto.GenericVoidValue())
            return [info_types.GateConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_all_gate_output_connections(self) -> List[info_types.GateConnection]:
        """
        Gets all Gate output connections

        Returns:
            List[info_types.GateConnection]: List of GateConnection objects
        """
        try:
            response = self._stub.GetAllGateOutputConnections(self._sushi_proto.GenericVoidValue())
            return [info_types.GateConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_cv_input_connections_for_processor(self, processor_id: int) -> List[info_types.CvConnection]:
        """
        Gets a list of all CV input connections for specified processor.

        Returns:
            List[info_types.CvConnection]: List of CvConnection objects
        """
        try:
            response = self._stub.GetCvInputConnectionsForProcessor(self._sushi_proto.ProcessorIdentifier(id=processor_id))
            return [info_types.CvConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_cv_output_connections_for_processor(self, processor_id: int) -> List[info_types.CvConnection]:
        """
        Gets a list of all CV output connections for specified processor.

        Returns:
            List[info_types.CvConnection]: List of CvConnection objects
        """
        try:
            response = self._stub.GetCvOutputConnectionsForProcessor(self._sushi_proto.ProcessorIdentifier(id=processor_id))
            return [info_types.CvConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_gate_input_connections_for_processor(self, processor_id: int) -> List[info_types.GateConnection]:
        """
        Gets a list of all Gate input connections for specified processor.

        Returns:
            List[info_types.GateConnection]: List of GateConnection objects
        """
        try:
            response = self._stub.GetGateInputConnectionsForProcessor(self._sushi_proto.ProcessorIdentifier(id=processor_id))
            return [info_types.GateConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_gate_output_connections_for_processor(self, processor_id: int) -> List[info_types.GateConnection]:
        """
        Gets a list of all Gate output connections for specified processor.

        Returns:
            List[info_types.GateConnection]: List of GateConnection objects
        """
        try:
            response = self._stub.GetGateOutputConnectionsForProcessor(self._sushi_proto.ProcessorIdentifier(id=processor_id))
            return [info_types.GateConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def connect_cv_input_to_parameter(self, processor_id: int, parameter_id: int, cv_port_id: int) -> None:
        """
        Connects a CV input to a parameter

        Parameters:
            processor_id (int): The id of the processor to parameter belongs to
            parameter_id (int): The id of parameter to connect to
            cv_port_id (int): The id of the CV port to connect to
        """
        try:
            self._stub.ConnectCvInputToParameter(self._sushi_proto.CvConnection(parameter=self._sushi_proto.ParameterIdentifier(processor_id=processor_id, parameter_id=parameter_id),
                                                                                cv_port_id=cv_port_id))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def connect_cv_output_from_parameter(self, processor_id: int, parameter_id: int, cv_port_id: int) -> None:
        """
        Connects a CV output to a parameter

        Parameters:
            processor_id (int): The id of the processor to parameter belongs to
            parameter_id (int): The id of parameter to connect to
            cv_port_id (int): The id of the CV port to connect to
        """
        try:
            self._stub.ConnectCvOutputFromParameter(self._sushi_proto.CvConnection(parameter=self._sushi_proto.ParameterIdentifier(processor_id=processor_id, parameter_id=parameter_id),
                                                                                   cv_port_id=cv_port_id))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def connect_gate_input_to_processor(self, processor: int, gate_port_id: int, channel: int, note_no: int) -> None:
        """
        Connects a Gate input to a processor

        Parameters:
            processor (int): The id of the processor to connect to
            gate_port_id (int): The id of the gate port being connected
            channel (int): The midi channel number
            note_no (int): The note number to trigger
        """
        try:
            self._stub.ConnectGateInputToProcessor(self._sushi_proto.GateConnection(processor=self._sushi_proto.ProcessorIdentifier(id=processor),
                                                                                    gate_port_id=gate_port_id,
                                                                                    channel=channel,
                                                                                    note_no=note_no))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def connect_gate_output_from_processor(self, processor: int, gate_port_id: int, channel: int, note_no: int) -> None:
        """
        Connects a Gate output from a processor

        Parameters:
            processor (int): The id of the processor to connect to
            gate_port_id (int): The id of the gate port being connected
            channel (int): The midi channel number
            note_no (int): The note number to trigger
        """
        try:
            self._stub.ConnectGateOutputFromProcessor(self._sushi_proto.GateConnection(processor=self._sushi_proto.ProcessorIdentifier(id=processor),
                                                                                       gate_port_id=gate_port_id,
                                                                                       channel=channel,
                                                                                       note_no=note_no))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disconnect_cv_input(self, processor_id: int, parameter_id: int, cv_port_id: int) -> None:
        """
        Disconnects a CV input from a parameter

        Parameters:
            procsessor_id (int): The id of the processor the parameter belongs to
            parameter_id (int): The id of the parameter to disconnect
            cv_port_id (int): The id of the CV port to disconnect
        """
        try:
            self._stub.DisconnectCvInput(self._sushi_proto.CvConnection(parameter=self._sushi_proto.ParameterIdentifier(processor_id=processor_id, parameter_id=parameter_id),
                                                                        cv_port_id=cv_port_id))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disconnect_cv_output(self, processor_id: int, parameter_id: int, cv_port_id: int) -> None:
        """
        Disconnects a CV output from a parameter

        Parameters:
            procsessor_id (int): The id of the processor the parameter belongs to
            parameter_id (int): The id of the parameter to disconnect
            cv_port_id (int): The id of the CV port to disconnect
        """
        try:
            self._stub.DisconnectCvOutput(self._sushi_proto.CvConnection(parameter=self._sushi_proto.ParameterIdentifier(processor_id=processor_id, parameter_id=parameter_id),
                                                                         cv_port_id=cv_port_id))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disconnect_gate_input(self, processor: int, gate_port_id: int, channel: int, note_no: int) -> None:
        """
        Disconnects a Gate input from a processor

        Parameters:
            processor (int): The id of the processor to connect to
            gate_port_id (int): The id of the gate port being connected
            channel (int): The midi channel number
            note_no (int): The note number to trigger
        """
        try:
            self._stub.DisconnectGateInput(self._sushi_proto.GateConnection(processor=self._sushi_proto.ProcessorIdentifier(id=processor),
                                                                            gate_port_id=gate_port_id,
                                                                            channel=channel,
                                                                            note_no=note_no))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disconnect_gate_output(self, processor: int, gate_port_id: int, channel: int, note_no: int) -> None:
        """
        Disconnects a Gate output from a processor

        Parameters:
            processor (int): The id of the processor to connect to
            gate_port_id (int): The id of the gate port being connected
            channel (int): The midi channel number
            note_no (int): The note number to trigger
        """
        try:
            self._stub.DisconnectGateOutput(self._sushi_proto.GateConnection(processor=self._sushi_proto.ProcessorIdentifier(id=processor),
                                                                             gate_port_id=gate_port_id,
                                                                             channel=channel,
                                                                             note_no=note_no))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disconnect_all_cv_inputs_from_processor(self, processor: int) -> None:
        """
        Disconnects all CV inputs from a processor.

        Parameters:
            processor (int): the processor ID from which to disconnect CV inputs
        """
        try:
            self._stub.DisconnectAllCvInputsFromProcessor(self._sushi_proto.ProcessorIdentifier(id=processor))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disconnect_all_cv_outputs_from_processor(self, processor: int) -> None:
        """
        Disconnects all CV outputs from a processor.

        Parameters:
            processor (int): the processor ID from which to disconnect CV outputs
        """
        try:
            self._stub.DisconnectAllCvOutputsFromProcessor(self._sushi_proto.ProcessorIdentifier(id=processor))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disconnect_all_gate_inputs_from_processor(self, processor: int) -> None:
        """
        Disconnects all Gate inputs from a processor.

        Parameters:
            processor (int): the processor ID from which to disconnect Gate inputs
        """
        try:
            self._stub.DisconnectAllGateInputsFromProcessor(self._sushi_proto.ProcessorIdentifier(id=processor))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disconnect_all_gate_outputs_from_processor(self, processor: int) -> None:
        """
        Disconnects all Gate outputs from a processor.

        Parameters:
            processor (int): the processor ID from which to disconnect Gate outputs
        """
        try:
            self._stub.DisconnectAllGateOutputsFromProcessor(self._sushi_proto.ProcessorIdentifier(id=processor))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)
