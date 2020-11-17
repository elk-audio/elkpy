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

from elkpy import sushierrors
from elkpy import grpc_gen
from elkpy import sushi_info_types as info_types
from typing import List

####################################
# Sushi transport controller class #
####################################

class TransportController(object):
    """
    A class to control the transport in sushi via gRPC. It controls transport related information in sushi
    like samplerate, playback mode, sync mode, time signature and tempo.

    Attributes:
        _stub (TransportControllerStub): Connection stubs to the gRPC transport interface implemented in sushi.
    """
    def __init__(self,
                 address = 'localhost:51051',
                 sushi_proto_def = '/usr/share/sushi/sushi_rpc.proto'):
        """
        The constructor for the TransportController class setting up the gRPC connection with sushi.

        Parameters:
            address (str): 'ip-addres:port' The ip-addres and port at which to connect to sushi.
            sushi_proto_def (str): path to .proto file with SUSHI's gRPC services definition
        """
        try:
            channel = grpc.insecure_channel(address)
        except AttributeError as e:
            raise TypeError("Parameter address = {}. Should be a string containing the ip-address and port of sushi ('ip-address:port')".format(address)) from e

        self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(sushi_proto_def)
        self._stub = self._sushi_grpc.TransportControllerStub(channel)

    def get_samplerate(self) -> float:
        """
        Get the current samplerate.

        Returns:
            float: Current samplerate.
        """
        try:
            response = self._stub.GetSamplerate(self._sushi_proto.GenericVoidValue())
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)
            return -1

    def get_playing_mode(self) -> int:
        """
        Get the current playing mode.

        Returns:
            int: Current playing mode.
                1 = Stopped,
                2 = Playing,
                3 = Recording (not implemented)
        """
        try:
            response = self._stub.GetPlayingMode(self._sushi_proto.GenericVoidValue())
            return info_types.PlayingMode(response.mode)

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def set_playing_mode(self, playing_mode: info_types.PlayingMode) -> None:
        """
        Set the playing mode.

        Parameters:
            playing_mode (PlayingMode): The playing mode to set.
                                1 = Stopped,
                                2 = Playing,
                                3 = Recording (not implemented)
        """

        if info_types.PlayingMode(playing_mode) in info_types.PlayingMode:
            try:
                self._stub.SetPlayingMode(self._sushi_proto.PlayingMode(
                    mode = int(playing_mode)
                ))

            except grpc.RpcError as e:
                sushierrors.grpc_error_handling(e, " With playing mode: {}".format(playing_mode))

    def get_sync_mode(self) -> info_types.SyncMode:
        """
        Get the current sync mode.

        Returns:
            int: Current sync mode.
                1 = Internal,
                2 = MIDI,
                3 = Link
        """
        try:
            response = self._stub.GetSyncMode(self._sushi_proto.GenericVoidValue())
            return info_types.SyncMode(response.mode)

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def set_sync_mode(self, sync_mode: info_types.SyncMode) -> None:
        """
        Set the sync mode.

        Parameters:
            sync_mode (SyncMode): The sync mode to set.
                            1 = Internal,
                            2 = MIDI,
                            3 = Link
        """
        if info_types.SyncMode(sync_mode) in info_types.SyncMode:
            try:
                self._stub.SetSyncMode(self._sushi_proto.SyncMode(
                    mode = int(sync_mode)
                ))

            except grpc.RpcError as e:
                sushierrors.grpc_error_handling(e, " With sync mode: {}".format(sync_mode))

    def get_tempo(self) -> float:
        """
        Get the current tempo.

        Returns:
            float: Current tempo in BPM(Beats Per Minute).
        """
        try:
            response = self._stub.GetTempo(self._sushi_proto.GenericVoidValue())
            return response.value
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def set_tempo(self, tempo: float) -> None:
        """
        Set the tempo.

        Parameters:
            tempo (float): The tempo in BPM(Beats Per Minute).
        """
        try:
            self._stub.SetTempo(self._sushi_proto.GenericFloatValue(
                value = tempo
            ))

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, " With tempo: {}".format(tempo))

    def get_time_signature(self) -> (int, int):
        """
        Get the current time signature.

        Returns:
            int: The nominator of the time signature.
            int: The denominator of the time signature.
        """
        try:
            response = self._stub.GetTimeSignature(self._sushi_proto.GenericVoidValue())
            return response.numerator, response.denominator

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def set_time_signature(self, numerator: int, denominator: int) -> None:
        """
        Set the time signature

        Parameters:
            numerator (int): The numerator of the time signature.
            denominator (int): The denominator of the time signature. Should be either 4 or 8.
        """
        try:
            self._stub.SetTimeSignature(self._sushi_proto.TimeSignature(
                numerator = numerator,
                denominator = denominator
            ))

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, " With numerator: {}, denominator: {}".format(numerator, denominator))
