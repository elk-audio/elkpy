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


####################################
# Sushi timing controller class #
####################################

class TimingController:
    """
    A class to control the timing in sushi via gRPC. It can get and reset the different timing statistics
    provided by sushi.

    Attributes:
        _stub (TimingControllerStub): Connection stubs to the gRPC timing interface implemented in sushi.
    """
    def __init__(self,
                 address = 'localhost:51051',
                 sushi_proto_def = '/usr/share/sushi/sushi_rpc.proto'):
        """
        The constructor for the TimingController class setting up the gRPC connection with sushi.

        Parameters:
            address (str): 'ip-addres:port' The ip-addres and port at which to connect to sushi.
            sushi_proto_def (str): path to .proto file with SUSHI's gRPC services definition
        """
        try:
            channel = grpc.insecure_channel(address)
        except AttributeError as e:
            raise TypeError("Parameter address = {}. Should be a string containing the ip-address and port of sushi ('ip-address:port')".format(address)) from e

        self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(sushi_proto_def)
        self._stub = self._sushi_grpc.TimingControllerStub(channel)

    def get_timings_enabled(self) -> bool | None:
        """
        Get the state of timing statstics.

        Returns:
            bool: True if statistics is enabled, False if not.
        """
        try:
            response = self._stub.GetTimingsEnabled(self._sushi_proto.GenericVoidValue())
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def set_timings_enabled(self, enabled: bool) -> None:
        """
        Set the state of timing statstics.

        Parameters:
            bool: True if statistics is enabled, False if not.
        """
        try:
            self._stub.SetTimingsEnabled(self._sushi_proto.GenericBoolValue(value = enabled))

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_engine_timings(self) -> tuple[float, float, float] | None:
        """
        Get the average, min and max timings of the engine.

        Returns:
            float: The average engine processing time in ms.
            float: The minimum engine processing time in ms.
            float: The maximum engine processing time in ms.
        """
        try:
            response = self._stub.GetEngineTimings(self._sushi_proto.GenericVoidValue())
            return response.average, response.min, response.max

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_track_timings(self, track_identifier: int) -> tuple[float, float, float] | None:
        """
        Get the average, min and max timings of the specified track.

        Parameters:
            track_identifier (int): The id of the track to get timings from.

        Returns:
            float: The average track processing time in ms.
            float: The minimum track processing time in ms.
            float: The maximum track processing time in ms.
        """
        try:
            response = self._stub.GetTrackTimings(self._sushi_proto.TrackIdentifier(
                id = track_identifier
            ))
            return response.average, response.min, response.max

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With track id: {}".format(track_identifier))

    def get_processor_timings(self, processor_identifier: int) -> tuple[float, float, float] | None:
        """
        Get the average, min and max timings of the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get timings from.

        Returns:
            float: The average processor processing time in ms.
            float: The minimum processor processing time in ms.
            float: The maximum processor processing time in ms.
        """
        try:
            response = self._stub.GetProcessorTimings(self._sushi_proto.ProcessorIdentifier(
                id = processor_identifier
            ))
            return response.average, response.min, response.max

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}".format(processor_identifier))

    def reset_all_timings(self) -> None:
        """
        Reset all the timings.
        """
        try:
            self._stub.ResetAllTimings(self._sushi_proto.GenericVoidValue())

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def reset_track_timings(self, track_identifier: int) -> None:
        """
        Reset the timings of the specified track.

        Parameters:
            track_identifier (int): The id of the track to reset the timings of.
        """
        try:
            self._stub.ResetTrackTimings(self._sushi_proto.TrackIdentifier(
                id = track_identifier
            ))

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With track id: {}".format(track_identifier))

    def reset_processor_timings(self, processor_identifier: int) -> None:
        """
        Reset the timings of the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to reset the timings of.
        """
        try:
            self._stub.ResetProcessorTimings(self._sushi_proto.ProcessorIdentifier(
                id = processor_identifier
            ))

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}".format(processor_identifier))
