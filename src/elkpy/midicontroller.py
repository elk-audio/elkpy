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

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from elkpy.sushicontroller import SushiController

from .events import SushiCommandResponse
import grpc

from . import sushierrors
from . import sushi_info_types as info_types
from . import grpc_gen

############################################
#   Sushi MIDI Controller class   #
############################################


class MidiController(object):
    """
    A class to manage MIDI connections in Sushi via gRPC.
    It can create and remove keyboard, CC and PC connections from an external midi device to tracks,
    processors, and parameters in sushi.
    """
    def __init__(self,
                 parent: 'SushiController',
                 address: str='localhost:51051',
                 sushi_proto_def: str='/usr/share/sushi/sushi_rpc.proto',
                 sushi_proto = None, sushi_grpc = None) -> None:
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

        if sushi_proto and sushi_grpc:
            self._sushi_proto = sushi_proto
            self._sushi_grpc = sushi_grpc
        else:
            self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(sushi_proto_def)
        self._stub = self._sushi_grpc.MidiControllerStub(channel)
        self._parent = parent

    def get_input_ports(self) -> int:
        """
        Gets the number of MIDI input ports.

        Returns:
            int: The number of MIDI input ports enabled in Sushi
        """
        try:
            response = self._stub.GetInputPorts(self._sushi_proto.GenericVoidValue())
            return response.value
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_output_ports(self) -> int:
        """
        Gets the number of MIDI output ports.

        Returns:
            int: The number of MIDI output ports enabled in Sushi
        """
        try:
            response = self._stub.GetOutputPorts(self._sushi_proto.GenericVoidValue())
            return response.value
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_all_kbd_input_connections(self) -> List[info_types.MidiKbdConnection]:
        """
        Gets a list of all MIDI Keyboard input Connections in Sushi

        Returns:
            List[info_types.MidiKbdConnection]: List of MidiKbdConnection objects
        """
        try:
            response = self._stub.GetAllKbdInputConnections(self._sushi_proto.GenericVoidValue())
            return [info_types.MidiKbdConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_all_kbd_output_connections(self) -> List[info_types.MidiKbdConnection]:
        """
        Gets a list of all MIDI Keyboard output Connections in Sushi

        Returns:
            List[info_types.MidiKbdConnection]: List of MidiKbdConnection objects
        """
        try:
            response = self._stub.GetAllKbdOutputConnections(self._sushi_proto.GenericVoidValue())
            return [info_types.MidiKbdConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_all_cc_input_connections(self) -> List[info_types.MidiCCConnection]:
        """
        Gets a list of all MIDI Control Change input connections in Sushi

        Returns:
            List[info_types.MidiCCConnection]: List of MidiCCConnection objects
        """
        try:
            response = self._stub.GetAllCCInputConnections(self._sushi_proto.GenericVoidValue())
            return [info_types.MidiCCConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_all_pc_input_connections(self) -> List[info_types.MidiPCConnection]:
        """
        Gets a list of all MIDI Program Change input connections in Sushi

        Returns:
            List[info_types.MidiPCConnection]: List of MidiPCConnection objects
        """
        try:
            response = self._stub.GetAllPCInputConnections(self._sushi_proto.GenericVoidValue())
            return [info_types.MidiPCConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_cc_input_connections_for_processor(self, processor_id: int) -> List[info_types.MidiCCConnection]:
        """
        Gets a list of all MIDI Control Change connection for a processor.

        Parameters:
            processor_id (int): The id of the processor to get the input connections from

        Returns:
            List[info_types.MidiCCConnection]: List of MidiCCConnection objects
        """
        try:
            cr = self._stub.GetCCInputConnectionsForProcessor(self._sushi_proto.ProcessorIdentifier(id=processor_id))
            response = self._parent.validate_command_response(cr, f"Get CC input connections for processor {processor_id}")
            return [info_types.MidiCCConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With processor_id: {processor_id}")

    def get_pc_input_connections_for_processor(self, processor_id: int) -> List[info_types.MidiPCConnection]:
        """
        Gets a list of all MIDI Program Change connection for a processor.

        Parameters:
            processor_id (int): The id of the processor to get the input connections from

        Returns:
            List[info_types.MidiPCConnection]: List of MidiPCConnection objects
        """
        try:
            cr = self._stub.GetPCInputConnectionsForProcessor(
                self._sushi_proto.ProcessorIdentifier(id=processor_id))
            response = self._parent.validate_command_response(cr, f"Get PC input connections for processor {processor_id}")
            return [info_types.MidiPCConnection(c) for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With processor_id: {processor_id}")

    def get_midi_clock_output_enabled(self, port: int) -> bool:
        """
        Gets whether MIDI clock output is enabled for a midi port.

        Parameters:
            port (int): The id of the processor to query

        Returns:
            bool: true if midi clock is enabled for that midi output port
        """
        try:
            response = self._stub.GetMidiClockOutputEnabled(self._sushi_proto.GenericIntValue(value=port))
            return response.value
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With port: {port}")

    def set_midi_clock_output_enabled(self, port: int, enabled: bool) -> SushiCommandResponse:
        """
        Enable or disable MIDI clock output for a midi port.

        Parameters:
            port (int): The id of the output port to toggle
            enabled (bool): True to turn on clock output, False to turn off

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.SetMidiClockOutputEnabled(
                self._sushi_proto.MidiClockSetRequest(port=port, enabled=enabled))
            return self._parent.validate_command_response(cr, f"Set MIDI clock output to {enabled}")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With port: {port}, enabled: {enabled}")

    def connect_kbd_input_to_track(self, track: int, channel: int, port: int, raw_midi: bool) -> SushiCommandResponse:
        """
        Connects MIDI Keyboard messages to a track

        Parameters:
            track (int): The id of the track to connect to
            channel (int): The id of the channel to connect to
            port (int): The id of the port to connect to
            raw_midi (bool): Enable raw MIDI

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.ConnectKbdInputToTrack(self._sushi_proto.MidiKbdConnection(track=self._sushi_proto.TrackIdentifier(id=track),
                                                                                  channel=self._sushi_proto.MidiChannel(channel=channel),
                                                                                  port=port,
                                                                                  raw_midi=raw_midi))
            return self._parent.validate_command_response(cr, "Connect Keyboard input to track")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With MidiKbdConnection: track: {track}, channel: {channel}, "
                                               f"port: {port}, raw_midi: {raw_midi}")

    def connect_kbd_output_from_track(self, track: int, channel: int, port: int, raw_midi: bool) -> SushiCommandResponse:
        """
        Connects MIDI Keyboard messages from a track to a MIDI output port

        Parameters:
            track (int): The id of the track to connect to
            channel (int): The id of the channel to connect to
            port (int): The id of the port to connect to
            raw_midi (bool): Enable raw MIDI

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.ConnectKbdOutputFromTrack(self._sushi_proto.MidiKbdConnection(track=self._sushi_proto.TrackIdentifier(id=track),
                                                                                     channel=self._sushi_proto.MidiChannel(channel=channel),
                                                                                     port=port,
                                                                                     raw_midi=raw_midi))
            return self._parent.validate_command_response(cr, "Connect Keyboard output to track")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With MidiKbdConnection: track: {track}, channel: {channel}, "
                                               f"port: {port}, raw_midi: {raw_midi}")

    def connect_cc_to_parameter(self, processor_id: int, parameter_id: int, channel: int, port: int, cc_number: int,
                                min_range: float, max_range: float, relative_mode: bool) -> SushiCommandResponse:
        """
        Connects MIDI Control Change messages to a parameter

        Parameters:
            processor_id (int): The id of processor that the parameter belongs to
            parameter_id (int): The id of the parameter to connect to
            channel (int): The MIDI channel to use for the connection
            port (int): The id of the MIDI port to use for the connection
            cc_number (int): The CC number to use for the connection
            min_range (float): The minimum parameter value used for the connection
            max_range (float): The maximum parameter value used for the connection
            relative_mode (bool): Whether the parameter changes relative to a previous value

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.ConnectCCToParameter(self._sushi_proto.MidiCCConnection(parameter=self._sushi_proto.ParameterIdentifier(processor_id=processor_id, parameter_id=parameter_id),
                                                                               channel=self._sushi_proto.MidiChannel(channel=channel),
                                                                               port=port,
                                                                               cc_number=cc_number,
                                                                               min_range=min_range,
                                                                               max_range=max_range,
                                                                               relative_mode=relative_mode))
            return self._parent.validate_command_response(cr, f"Connect CC{cc_number} to parameter {parameter_id}")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With MidiCCConnection: parameter: {parameter_id}, channel: {channel}, "
                                               f"port: {port}, cc_number: {cc_number}, min_range: {min_range}, "
                                               f"max_range: {max_range}, relative_mode: {relative_mode}.")

    def connect_pc_to_processor(self, processor: int, channel: int, port: int) -> SushiCommandResponse:
        """
        Connects MIDI Program Change messages to a processor

        Parameters:
            processor (int): The id of the processor to connect
            channel (int): The MIDI channel to use for the connection
            port (int): The MIDI port to use for the connection

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.ConnectPCToProcessor(self._sushi_proto.MidiPCConnection(processor=self._sushi_proto.ProcessorIdentifier(id=processor),
                                                                               channel=self._sushi_proto.MidiChannel(channel=channel),
                                                                               port=port))
            return self._parent.validate_command_response(cr, f"Connect PC to processor {processor}")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With MidiPCConnection: processor: {processor}, channel: {channel}, "
                                               f"port: {port}.")

    def disconnect_kbd_input(self, track: int, channel: int, port: int, raw_midi: bool) -> SushiCommandResponse:
        """
        Disconnects a MIDI Keyboard input connection from a track

        Parameters:
            track (int): The id of the track to disconnect
            channel (int): The MIDI channel to disconnect
            port (int): The MIDI port to disconnect
            raw_midi (bool): Disconnect raw MIDI

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DisconnectKbdInput(self._sushi_proto.MidiKbdConnection(track=self._sushi_proto.TrackIdentifier(id=track),
                                                                              channel=self._sushi_proto.MidiChannel(channel=channel),
                                                                              port=port,
                                                                              raw_midi=raw_midi))
            return self._parent.validate_command_response(cr, f"Disconnect Keyboard input from track {track}")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With MidiKbdConnection: track: {track}, channel: {channel}, "
                                               f"port: {port}, raw_midi: {raw_midi}.")

    def disconnect_kbd_output(self, track: int, channel: int, port: int, raw_midi: bool) -> SushiCommandResponse:
        """
        Disconnects a MIDI Keyboard output connection from a track

        Parameters:
            track (int): The id of the track to disconnect
            channel (int): The MIDI channel to disconnect
            port (int): The MIDI port to disconnect
            raw_midi (bool): Disconnect raw MIDI

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DisconnectKbdOutput(self._sushi_proto.MidiKbdConnection(track=self._sushi_proto.TrackIdentifier(id=track),
                                                                               channel=self._sushi_proto.MidiChannel(channel=channel),
                                                                               port=port,
                                                                               raw_midi=raw_midi))
            return self._parent.validate_command_response(cr, f"Disconnect MIDI output from track {track}")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With MidiKbdConnection: track: {track}, channel: {channel}, "
                                               f"port: {port}, raw_midi: {raw_midi}.")

    def disconnect_cc(self, processor_id: int, parameter_id: int, channel: int, port: int, cc_number: int,
                                min_range: float, max_range: float, relative_mode: bool) -> SushiCommandResponse:
        """
        Disconnects a MIDI Control Change connection

        Parameters:
            processor_id (int): The id of the processor the parameter belongs to
            parameter (int): The id of the parameter to connect to
            channel (int): The MIDI channel to use for the connection
            port (int): The id of the MIDI port to use for the connection
            cc_number (int): The cc number to use for the connection
            min_range (float): The minimum parameter value used for the connection
            max_range (float): The maximum parameter value used for the connection
            relative_mode (bool): Whether the parameter changes relative to a previous value

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DisconnectCC(self._sushi_proto.MidiCCConnection(parameter=self._sushi_proto.ParameterIdentifier(processor_id=processor_id, parameter_id=parameter_id),
                                                                       channel=self._sushi_proto.MidiChannel(channel=channel),
                                                                       port=port,
                                                                       cc_number=cc_number,
                                                                       min_range=min_range,
                                                                       max_range=max_range,
                                                                       relative_mode=relative_mode))
            return self._parent.validate_command_response(cr, f"Disconnect CC from parameter {parameter_id}")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With MidiCCConnection: parameter: {parameter_id}, channel: {channel}, "
                                               f"port: {port}, cc_number: {cc_number}, min_range: {min_range}, "
                                               f"max_range: {max_range}, relative_mode: {relative_mode}.")

    def disconnect_pc(self, processor: int, channel: int, port: int) -> SushiCommandResponse:
        """
        Disconnects a MIDI Program Change connection

        Parameters:
            processor (int): The id of the processor to connect
            channel (int): The MIDI channel to use for the connection
            port (int): The MIDI port to use for the connection

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DisconnectPC(self._sushi_proto.MidiPCConnection(processor=self._sushi_proto.ProcessorIdentifier(id=processor),
                                                                       channel=self._sushi_proto.MidiChannel(channel=channel),
                                                                       port=port))
            return self._parent.validate_command_response(cr, f"Disconnect PC from processor {processor}")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With MidiPCConnection: processor: {processor}, channel: {channel}, "
                                               f"port: {port}.")

    def disconnect_all_cc_from_processor(self, processor_id: int) -> SushiCommandResponse:
        """
        Disconnects all MIDI Control Change connections from a processor

        Parameters:
            processor_id (int): The id of the processor to disconnect

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DisconnectAllCCFromProcessor(self._sushi_proto.ProcessorIdentifier(id=processor_id))
            return self._parent.validate_command_response(cr, f"Disconnect all CC from processor {processor_id}")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With processor_id: {processor_id}")

    def disconnect_all_pc_from_processor(self, processor_id: int) -> SushiCommandResponse:
        """
        Disconnects all MIDI Program Change connections from a processor

        Parameters:
            processor_id (int): The id of processor to disconnect

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DisconnectAllPCFromProcessor(self._sushi_proto.ProcessorIdentifier(id=processor_id))
            return self._parent.validate_command_response(cr, f"Disconnect all PC from processor {processor_id}")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With processor_id: {processor_id}")
