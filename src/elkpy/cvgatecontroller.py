__author__ = "Maxime Gendebien"
__copyright__ = """

    Copyright 2017-2026 Elk Audio AB

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

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from elkpy.sushicontroller import SushiController

from .events import SushiCommandResponse
import grpc
from . import sushierrors
from . import sushi_info_types as info_types
from .rpc import sushi_rpc_pb2

######################################
#   Sushi CV-Gate Controller class   #
######################################


class CvGateController:
    """
    Class to manage CV/Gate connections in Sushi via gRPC. It creates, deletes and gets info about
    Cv/Gate connections on sushi tracks.

    Attributes:
        _stub (CvGateControllerStub): Connection stub to the gRPC CvGate interface.
    """

    def __init__(self, parent: "SushiController", stub) -> None:
        self._stub = stub
        self._parent = parent

    def get_cv_input_channel_count(self) -> int:
        """
        Gets a count of all CV input channels

        Returns:
            int: count
        """
        try:
            response = self._stub.GetCvInputChannelCount(
                sushi_rpc_pb2.GenericVoidValue()
            )
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
            response = self._stub.GetCvOutputChannelCount(
                sushi_rpc_pb2.GenericVoidValue()
            )
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
            response = self._stub.GetAllCvInputConnections(
                sushi_rpc_pb2.GenericVoidValue()
            )
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
            response = self._stub.GetAllCvOutputConnections(
                sushi_rpc_pb2.GenericVoidValue()
            )
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
            response = self._stub.GetAllGateInputConnections(
                sushi_rpc_pb2.GenericVoidValue()
            )
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
            response = self._stub.GetAllGateOutputConnections(
                sushi_rpc_pb2.GenericVoidValue()
            )
            return [info_types.GateConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_cv_input_connections_for_processor(
        self, processor_id: int
    ) -> List[info_types.CvConnection]:
        """
        Gets a list of all CV input connections for specified processor.

        Returns:
            List[info_types.CvConnection]: List of CvConnection objects
        """
        try:
            cr = self._stub.GetCvInputConnectionsForProcessor(
                sushi_rpc_pb2.ProcessorIdentifier(id=processor_id)
            )
            response = self._parent.validate_command_response(
                cr, f"Get CV input connections for processor {processor_id}"
            )
            return [info_types.CvConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_cv_output_connections_for_processor(
        self, processor_id: int
    ) -> List[info_types.CvConnection]:
        """
        Gets a list of all CV output connections for specified processor.

        Returns:
            List[info_types.CvConnection]: List of CvConnection objects
        """
        try:
            cr = self._stub.GetCvOutputConnectionsForProcessor(
                sushi_rpc_pb2.ProcessorIdentifier(id=processor_id)
            )
            response = self._parent.validate_command_response(
                cr, f"Get CV output connections for processor {processor_id}"
            )
            return [info_types.CvConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_gate_input_connections_for_processor(
        self, processor_id: int
    ) -> List[info_types.GateConnection]:
        """
        Gets a list of all Gate input connections for specified processor.

        Returns:
            List[info_types.GateConnection]: List of GateConnection objects
        """
        try:
            cr = self._stub.GetGateInputConnectionsForProcessor(
                sushi_rpc_pb2.ProcessorIdentifier(id=processor_id)
            )
            response = self._parent.validate_command_response(
                cr, f"Get gate input connections for processor {processor_id}"
            )
            return [info_types.GateConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_gate_output_connections_for_processor(
        self, processor_id: int
    ) -> List[info_types.GateConnection]:
        """
        Gets a list of all Gate output connections for specified processor.

        Returns:
            List[info_types.GateConnection]: List of GateConnection objects
        """
        try:
            cr = self._stub.GetGateOutputConnectionsForProcessor(
                sushi_rpc_pb2.ProcessorIdentifier(id=processor_id)
            )
            response = self._parent.validate_command_response(
                cr, f"Get gate output connections for processor {processor_id}"
            )
            return [info_types.GateConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def connect_cv_input_to_parameter(
        self, processor_id: int, parameter_id: int, cv_port_id: int
    ) -> SushiCommandResponse:
        """
        Connects a CV input to a parameter

        Parameters:
            processor_id (int): The id of the processor to parameter belongs to
            parameter_id (int): The id of parameter to connect to
            cv_port_id (int): The id of the CV port to connect to

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.ConnectCvInputToParameter(
                sushi_rpc_pb2.CvConnection(
                    parameter=sushi_rpc_pb2.ParameterIdentifier(
                        processor_id=processor_id, parameter_id=parameter_id
                    ),
                    cv_port_id=cv_port_id,
                )
            )
            return self._parent.validate_command_response(
                cr, f"Connect CV input to parameter {parameter_id}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def connect_cv_output_from_parameter(
        self, processor_id: int, parameter_id: int, cv_port_id: int
    ) -> SushiCommandResponse:
        """
        Connects a CV output to a parameter

        Parameters:
            processor_id (int): The id of the processor to parameter belongs to
            parameter_id (int): The id of parameter to connect to
            cv_port_id (int): The id of the CV port to connect to

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.ConnectCvOutputFromParameter(
                sushi_rpc_pb2.CvConnection(
                    parameter=sushi_rpc_pb2.ParameterIdentifier(
                        processor_id=processor_id, parameter_id=parameter_id
                    ),
                    cv_port_id=cv_port_id,
                )
            )
            return self._parent.validate_command_response(
                cr, f"Connect CV output to parameter {parameter_id}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def connect_gate_input_to_processor(
        self, processor: int, gate_port_id: int, channel: int, note_no: int
    ) -> SushiCommandResponse:
        """
        Connects a Gate input to a processor

        Parameters:
            processor (int): The id of the processor to connect to
            gate_port_id (int): The id of the gate port being connected
            channel (int): The midi channel number
            note_no (int): The note number to trigger

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.ConnectGateInputToProcessor(
                sushi_rpc_pb2.GateConnection(
                    processor=sushi_rpc_pb2.ProcessorIdentifier(id=processor),
                    gate_port_id=gate_port_id,
                    channel=channel,
                    note_no=note_no,
                )
            )
            return self._parent.validate_command_response(
                cr, f"Connect gate input to processor {processor}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def connect_gate_output_from_processor(
        self, processor: int, gate_port_id: int, channel: int, note_no: int
    ) -> SushiCommandResponse:
        """
        Connects a Gate output from a processor

        Parameters:
            processor (int): The id of the processor to connect to
            gate_port_id (int): The id of the gate port being connected
            channel (int): The midi channel number
            note_no (int): The note number to trigger

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.ConnectGateOutputFromProcessor(
                sushi_rpc_pb2.GateConnection(
                    processor=sushi_rpc_pb2.ProcessorIdentifier(id=processor),
                    gate_port_id=gate_port_id,
                    channel=channel,
                    note_no=note_no,
                )
            )
            return self._parent.validate_command_response(
                cr, f"Connect gate output from processor {processor}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disconnect_cv_input(
        self, processor_id: int, parameter_id: int, cv_port_id: int
    ) -> SushiCommandResponse:
        """
        Disconnects a CV input from a parameter

        Parameters:
            procsessor_id (int): The id of the processor the parameter belongs to
            parameter_id (int): The id of the parameter to disconnect
            cv_port_id (int): The id of the CV port to disconnect

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DisconnectCvInput(
                sushi_rpc_pb2.CvConnection(
                    parameter=sushi_rpc_pb2.ParameterIdentifier(
                        processor_id=processor_id, parameter_id=parameter_id
                    ),
                    cv_port_id=cv_port_id,
                )
            )
            return self._parent.validate_command_response(
                cr, f"Disconnect CV input from processor {processor_id}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disconnect_cv_output(
        self, processor_id: int, parameter_id: int, cv_port_id: int
    ) -> SushiCommandResponse:
        """
        Disconnects a CV output from a parameter

        Parameters:
            procsessor_id (int): The id of the processor the parameter belongs to
            parameter_id (int): The id of the parameter to disconnect
            cv_port_id (int): The id of the CV port to disconnect

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DisconnectCvOutput(
                sushi_rpc_pb2.CvConnection(
                    parameter=sushi_rpc_pb2.ParameterIdentifier(
                        processor_id=processor_id, parameter_id=parameter_id
                    ),
                    cv_port_id=cv_port_id,
                )
            )
            return self._parent.validate_command_response(
                cr, f"Disconnect CV output from processor {processor_id}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disconnect_gate_input(
        self, processor: int, gate_port_id: int, channel: int, note_no: int
    ) -> SushiCommandResponse:
        """
        Disconnects a Gate input from a processor

        Parameters:
            processor (int): The id of the processor to connect to
            gate_port_id (int): The id of the gate port being connected
            channel (int): The midi channel number
            note_no (int): The note number to trigger

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DisconnectGateInput(
                sushi_rpc_pb2.GateConnection(
                    processor=sushi_rpc_pb2.ProcessorIdentifier(id=processor),
                    gate_port_id=gate_port_id,
                    channel=channel,
                    note_no=note_no,
                )
            )
            return self._parent.validate_command_response(
                cr, f"Disconnect gate input from processor {processor}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disconnect_gate_output(
        self, processor: int, gate_port_id: int, channel: int, note_no: int
    ) -> SushiCommandResponse:
        """
        Disconnects a Gate output from a processor

        Parameters:
            processor (int): The id of the processor to connect to
            gate_port_id (int): The id of the gate port being connected
            channel (int): The midi channel number
            note_no (int): The note number to trigger

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DisconnectGateOutput(
                sushi_rpc_pb2.GateConnection(
                    processor=sushi_rpc_pb2.ProcessorIdentifier(id=processor),
                    gate_port_id=gate_port_id,
                    channel=channel,
                    note_no=note_no,
                )
            )
            return self._parent.validate_command_response(
                cr, f"Disconnect gate output from processor {processor}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disconnect_all_cv_inputs_from_processor(
        self, processor: int
    ) -> SushiCommandResponse:
        """
        Disconnects all CV inputs from a processor.

        Parameters:
            processor (int): the processor ID from which to disconnect CV inputs

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DisconnectAllCvInputsFromProcessor(
                sushi_rpc_pb2.ProcessorIdentifier(id=processor)
            )
            return self._parent.validate_command_response(
                cr, f"Disconnect all CV inputs from processor {processor}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disconnect_all_cv_outputs_from_processor(
        self, processor: int
    ) -> SushiCommandResponse:
        """
        Disconnects all CV outputs from a processor.

        Parameters:
            processor (int): the processor ID from which to disconnect CV outputs

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DisconnectAllCvOutputsFromProcessor(
                sushi_rpc_pb2.ProcessorIdentifier(id=processor)
            )
            return self._parent.validate_command_response(
                cr, f"Disconnect all CV outputs from processor {processor}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disconnect_all_gate_inputs_from_processor(
        self, processor: int
    ) -> SushiCommandResponse:
        """
        Disconnects all Gate inputs from a processor.

        Parameters:
            processor (int): the processor ID from which to disconnect Gate inputs

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DisconnectAllGateInputsFromProcessor(
                sushi_rpc_pb2.ProcessorIdentifier(id=processor)
            )
            return self._parent.validate_command_response(
                cr, f"Disconnect all gate inputs from processor {processor}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def disconnect_all_gate_outputs_from_processor(
        self, processor: int
    ) -> SushiCommandResponse:
        """
        Disconnects all Gate outputs from a processor.

        Parameters:
            processor (int): the processor ID from which to disconnect Gate outputs

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DisconnectAllGateOutputsFromProcessor(
                sushi_rpc_pb2.ProcessorIdentifier(id=processor)
            )
            return self._parent.validate_command_response(
                cr, f"Disconnect all gate outputs from processor {processor}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)
