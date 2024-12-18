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
#   Sushi Audio Routing Controller class   #
############################################


class AudioRoutingController(object):
    """
    A class to control audio routing in Sushi via gRPC. It manages audio input and output
    connections between different tracks in sushi and how they connect to external inputs and outputs.

    Attributes:
        _stub (AudioRoutingControllerStub): connection stub to the gRPC audio routing interface in sushi
    """
    def __init__(self,
                 address: str='localhost:51051',
                 sushi_proto_def: str='/usr/share/sushi/sushi_rpc.proto') -> None:
        """
        The constructor for the AudioRoutingController class setting up the gRPC connection with sushi.

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
        self._stub = self._sushi_grpc.AudioRoutingControllerStub(channel)

    def get_all_input_connections(self) -> List[info_types.AudioConnection]:
        """
        Gets a list of all input connections.

        Returns:
            List[info_types.AudioConnection]: a list of AudioConnection objects.
        """
        try:
            response = self._stub.GetAllInputConnections(self._sushi_proto.GenericVoidValue())
            return [info_types.AudioConnection(connection) for connection in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_all_output_connections(self) -> List[info_types.AudioConnection]:
        """
        Gets a list of all output connections.

        Returns:
            List[info_types.AudioConnection]: a list of AudioConnection objects.
        """
        try:
            response = self._stub.GetAllOutputConnections(self._sushi_proto.GenericVoidValue())
            return [info_types.AudioConnection(connection) for connection in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_input_connections_for_track(self, track_id: int) -> List[info_types.AudioConnection]:
        """
        Gets a list of input connections for a specific track.

        Parameters:
            track_id (int): The id of the track to get the input connections from

        Returns:
            List[info_types.AudioConnection]: a list of AudioConnection objects.
        """
        try:
            response = self._stub.GetInputConnectionsForTrack(self._sushi_proto.TrackIdentifier(id=track_id))
            return [info_types.AudioConnection(connection) for connection in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_output_connections_for_track(self, track_id: int) -> List[info_types.AudioConnection]:
        """
        Gets a list of output connections for a specific track.

        Parameters:
            track_id (int): The id of the track to get the output connections from

        Returns:
            List[info_types.AudioConnection]: a list of AudioConnection objects.

        """
        try:
            response = self._stub.GetOutputConnectionsForTrack(self._sushi_proto.TrackIdentifier(id=track_id))
            return [info_types.AudioConnection(connection) for connection in response.connections]
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def connect_input_channel_to_track(self, track: int, track_channel: int, engine_channel: int) -> None:
        """
        Connects an input channel to a track

        Parameters:
            track (int): The index of the track to connect to
            track_channel (int): The index of the channel on the track to connect
            engine_channel (int): The index of the channel on the engine to connect
        """
        try:
            self._stub.ConnectInputChannelToTrack(self._sushi_proto.AudioConnection(track=self._sushi_proto.TrackIdentifier(id=track),
                                                                                    track_channel=track_channel,
                                                                                    engine_channel=engine_channel
                                                                                    ))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With track id: {track}, track_channel: {track_channel} "
                                               f"and engine_channel: {engine_channel}")

    def connect_output_channel_from_track(self, track: int, track_channel: int, engine_channel: int) -> None:
        """
        Connects an output channel from a track

        Parameters:
            track (int): The index of the track to connect to
            track_channel (int): The index of the channel on the track to connect
            engine_channel (int): The index of the channel on the engine to connect
        """
        try:
            self._stub.ConnectOutputChannelFromTrack(
                self._sushi_proto.AudioConnection(track=self._sushi_proto.TrackIdentifier(id=track),
                                                  track_channel=track_channel,
                                                  engine_channel=engine_channel
                                                  ))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With track id: {track}, track_channel: {track_channel} "
                                               f"and engine_channel: {engine_channel}")

    def disconnect_input(self, track: int, track_channel: int, engine_channel: int) -> None:
        """
        Disconnects an input from a track

        Parameters:
            track (int): The index of the track to disconnect to
            track_channel (int): The index of the channel on the track to disconnect
            engine_channel (int): The index of the channel on the engine to disconnect
        """
        try:
            self._stub.DisconnectInput(
                self._sushi_proto.AudioConnection(track=self._sushi_proto.TrackIdentifier(id=track),
                                                  track_channel=track_channel,
                                                  engine_channel=engine_channel
                                                  ))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With track id: {track}, track_channel: {track_channel} "
                                               f"and engine_channel: {engine_channel}")

    def disconnect_output(self, track: int, track_channel: int, engine_channel: int) -> None:
        """
        Disconnects an output from a track

        Parameters:
            track (int): The index of the track to disconnect to
            track_channel (int): The index of the channel on the track to disconnect
            engine_channel (int): The index of the channel on the engine to disconnect
        """
        try:
            self._stub.DisconnectOutput(
                self._sushi_proto.AudioConnection(track=self._sushi_proto.TrackIdentifier(id=track),
                                                  track_channel=track_channel,
                                                  engine_channel=engine_channel
                                                  ))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With track id: {track}, track_channel: {track_channel} "
                                               f"and engine_channel: {engine_channel}")

    def disconnect_all_inputs_from_track(self, track_id: int) -> None:
        """
        Disconnects all inputs from a track

        Parameters:
            track_id (int): a track ID for which all inputs will be disconnected
         """
        try:
            self._stub.DisconnectAllInputsFromTrack(self._sushi_proto.TrackIdentifier(id=track_id))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With track id: {track_id}")

    def disconnect_all_outputs_from_track(self, track_id: int) -> None:
        """
        Disconnects all outputs from a track

        Parameters:
            track_id (int): a track ID for which all inputs will be disconnected
          """
        try:
            self._stub.DisconnectAllOutputsFromTrack(self._sushi_proto.TrackIdentifier(id=track_id))
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, f"With track id: {track_id}")
