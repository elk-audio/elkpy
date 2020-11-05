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

############################################
#   Sushi MIDI Controller class   #
############################################


class MidiController(object):
    """
    A class to manage MIDI connections in Sushi via gRPC.
    """
    def __init__(self,
                 address: str='localhost:51051',
                 sushi_proto_def: str='/usr/share/sushi/sushi_rpc.proto') -> None:
        """
        Args:
            address: IP address to Sushi in the uri form : 'ip-addr:port'
            sushi_proto_def: path to the .proto file with SUSHI gRPC services definitions
        """
        try:
            channel = grpc.insecure_channel(address)
        except AttributeError as e:
            raise TypeError(f"Parameter address = {address}. Should be a string containing the ip-address and port "
                            f"to Sushi") from e

        self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(sushi_proto_def)
        self._stub = self._sushi_grpc.MidiControllerStub(channel)

    def get_input_ports(self) -> int:
        """
        Gets MIDI input ports.
        Returns:
            ports (int)
        """
        try:
            response = self._stub.GetInputPorts(self._sushi_proto.GenericVoidValue())
            return response.value
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_output_ports(self) -> int:
        """
        Gets MIDI output ports.
        Returns:
            ports (int)
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
            List of MidiKbdConnection objects

        """
        try:
            response = self._stub.GetAllKbdInputConnections(self._sushi_proto.GenericVoidValue())
            return [c for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_all_kbd_output_connections(self) -> List[info_types.MidiKbdConnection]:
        """
        Gets a list of all MIDI Keyboard output Connections in Sushi
        Returns:
            List of MidiKbdConnection objects

        """
        try:
            response = self._stub.GetAllKbdOutputConnections(self._sushi_proto.GenericVoidValue())
            return [c for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_all_cc_input_connections(self) -> List[info_types.MidiCCConnection]:
        """
         Gets a list of all MIDI CC input connections in Sushi
         Returns:
             List of MidiCCConnection objects

         """
        try:
            response = self._stub.GetAllCCInputConnections(self._sushi_proto.GenericVoidValue())
            return [c for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_all_pc_input_connections(self) -> List[info_types.MidiPCConnection]:
        """
         Gets a list of all MIDI PC input connections in Sushi
         Returns:
             List of MidiPCConnection objects

         """
        try:
            response = self._stub.GetAllPCInputConnections(self._sushi_proto.GenericVoidValue())
            return [c for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_cc_input_connections_for_processor(self, processor_id: int) -> List[info_types.MidiCCConnection]:
        """
        Gets a list of all MIDI CC connection for processor_id.
        Args:
            processor_id: int

        Returns:
            List of MidiCCConnection objects
        """
        try:
            response = self._stub.GetCCInputConnectionsForProcessor(self._sushi_proto.ProcessorIdentifier(id=processor_id))
            return [c for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With processor_id: {processor_id}")

    def get_pc_input_connections_for_processor(self, processor_id: int) -> List[info_types.MidiPCConnection]:
        """
        Gets a list of all MIDI PC connection for processor_id.
        Args:
            processor_id: int

        Returns:
            List of MidiPCConnection objects
        """
        try:
            response = self._stub.GetPCInputConnectionsForProcessor(
                self._sushi_proto.ProcessorIdentifier(id=processor_id))
            return [c for c in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With processor_id: {processor_id}")

    def connect_kbd_input_to_track(self, track: int, channel: int, port: int, raw_midi: bool) -> None:
        """
        Connects a Midi Keyboard input connection to a track
        Args:
            track:
            channel:
            port:
            raw_midi:
        """
        try:
            self._stub.ConnectKbdInputToTrack(self._sushi_proto.MidiKbdConnection(track=track,
                                                                                  channel=channel,
                                                                                  port=port,
                                                                                  raw_midi=raw_midi))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With MidiKbdConnection: track: {track}, channel: {channel}, "
                                               f"port: {port}, raw_midi: {raw_midi}")

    def connect_kbd_output_from_track(self, track: int, channel: int, port: int, raw_midi: bool) -> None:
        """
        Connects a Midi Keyboard connection to a track
        Args:
            track:
            channel:
            port:
            raw_midi:
        """
        try:
            self._stub.ConnectKbdInputToTrack(self._sushi_proto.MidiKbdConnection(track=track,
                                                                                  channel=channel,
                                                                                  port=port,
                                                                                  raw_midi=raw_midi))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With MidiKbdConnection: track: {track}, channel: {channel}, "
                                               f"port: {port}, raw_midi: {raw_midi}")

    def connect_cc_to_parameter(self, parameter: int, channel: int, port: int, cc_number: int,
                                min_range: float, max_range: float, relative_mode: bool) -> None:
        """
        Connects a Midi CC connection to a parameter
        Args:
            parameter:
            channel:
            port:
            cc_number:
            min_range:
            max_range:
            relative_mode: bool
        """
        try:
            self._stub.ConnectCCToParameter(self._sushi_proto.MidiCCConnection(parameter=parameter,
                                                                               channel=channel,
                                                                               port=port,
                                                                               cc_number=cc_number,
                                                                               min_range=min_range,
                                                                               max_range=max_range,
                                                                               relative_mode=relative_mode))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With MidiCCConnection: parameter: {parameter}, channel: {channel}, "
                                               f"port: {port}, cc_number: {cc_number}, min_range: {min_range}, "
                                               f"max_range: {max_range}, relative_mode: {relative_mode}.")

    def connect_pc_to_processor(self, processor: int, channel: int, port: int) -> None:
        """
        Connects a Midi PC connection to a processor
        Args:
            processor:
            channel:
            port:
        """
        try:
            self._stub.ConnectPCToProcessor(self._sushi_proto.MidiPCConnection(processor=processor,
                                                                               channel=channel,
                                                                               port=port))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With MidiPCConnection: processor: {processor}, channel: {channel}, "
                                               f"port: {port}.")

    def disconnect_kbd_input(self, track: int, channel: int, port: int, raw_midi: bool) -> None:
        """
        Disconnects a Midi Keyboard input connection from a track
        Args:
            track:
            channel:
            port:
            raw_midi:
        """
        try:
            self._stub.DisconnectKbdInput(self._sushi_proto.MidiKbdConnection(track=track,
                                                                              channel=channel,
                                                                              port=port,
                                                                              raw_midi=raw_midi))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With MidiKbdConnection: track: {track}, channel: {channel}, "
                                               f"port: {port}, raw_midi: {raw_midi}.")

    def disconnect_kbd_output(self, track: int, channel: int, port: int, raw_midi: bool) -> None:
        """
        Disconnects a Midi Keyboard output connection from a track
        Args:
            track:
            channel:
            port:
            raw_midi:
        """
        try:
            self._stub.DisconnectKbdOutput(self._sushi_proto.MidiKbdConnection(track=track,
                                                                               channel=channel,
                                                                               port=port,
                                                                               raw_midi=raw_midi))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With MidiKbdConnection: track: {track}, channel: {channel}, "
                                               f"port: {port}, raw_midi: {raw_midi}.")

    def disconnect_cc(self, parameter: int, channel: int, port: int, cc_number: int,
                                min_range: float, max_range: float, relative_mode: bool) -> None:
        """
        Disconnects a Midi CC connection
        Args:
            parameter:
            channel:
            port:
            cc_number:
            min_range:
            max_range:
            relative_mode: bool
        """
        try:
            self._stub.DisconnectCC(self._sushi_proto.MidiCCConnection(parameter=parameter,
                                                                       channel=channel,
                                                                       port=port,
                                                                       cc_number=cc_number,
                                                                       min_range=min_range,
                                                                       max_range=max_range,
                                                                       relative_mode=relative_mode))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With MidiCCConnection: parameter: {parameter}, channel: {channel}, "
                                               f"port: {port}, cc_number: {cc_number}, min_range: {min_range}, "
                                               f"max_range: {max_range}, relative_mode: {relative_mode}.")

    def disconnect_pc(self, processor: int, channel: int, port: int) -> None:
        """
        Disconnects a Midi PC connection
        Args:
            processor:
            channel:
            port:
        """
        try:
            self._stub.DisconnectPC(self._sushi_proto.MidiPCConnection(processor=processor,
                                                                       channel=channel,
                                                                       port=port))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With MidiPCConnection: processor: {processor}, channel: {channel}, "
                                               f"port: {port}.")

    def disconnect_all_cc_from_processor(self, processor_id: int) -> None:
        """
        Disconnects all Midi CC connections from processor
        Args:
            processor_id (int)
        """
        try:
            self._stub.DisconnectAllCCFromProcessor(self._sushi_proto.ProcessorIdentifier(id=processor_id))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With processor_id: {processor_id}")

    def disconnect_all_pc_from_processor(self, processor_id: int) -> None:
        """
        Disconnects all Midi PC connections from processor
        Args:
            processor_id (int)
        """
        try:
            self._stub.DisconnectAllPCFromProcessor(self._sushi_proto.ProcessorIdentifier(id=processor_id))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With processor_id: {processor_id}")
