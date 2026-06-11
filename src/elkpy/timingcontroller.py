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

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from elkpy.sushicontroller import SushiController

from . import sushierrors
from .rpc import sushi_rpc_pb2


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

    def __init__(self, parent, stub):
        self._stub = stub
        self._parent: "SushiController" = parent

    def get_timings_enabled(self) -> bool | None:
        """
        Get the state of timing statstics.

        Returns:
            bool: True if statistics is enabled, False if not.
        """
        try:
            response = self._stub.GetTimingsEnabled(sushi_rpc_pb2.GenericVoidValue())
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
            cr = self._stub.SetTimingsEnabled(
                sushi_rpc_pb2.GenericBoolValue(value=enabled)
            )
            return self._parent.validate_command_response(
                cr, context_info=f"Setting timings_enabled to {enabled}"
            )

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_engine_timings(self) -> tuple | None:
        """
        Get the average, min and max timings of the engine.
        When Sushi multiprocessor mode is active, gets timings for each thread.

        Timings:
            float: The average engine processing time in ms.
            float: The minimum engine processing time in ms.
            float: The maximum engine processing time in ms.

        Returns:
            a tuple of (main: Timing, threads: list of Timings)
        """
        try:
            response = self._stub.GetEngineTimings(sushi_rpc_pb2.GenericVoidValue())
            return response.main, response.threads

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_track_timings(
        self, track_identifier: int
    ) -> tuple[float, float, float] | None:
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
            cr = self._stub.GetTrackTimings(
                sushi_rpc_pb2.TrackIdentifier(id=track_identifier)
            )
            response = self._parent.validate_command_response(
                cr, f"Getting timings for track {track_identifier}"
            )
            return response.timings.average, response.timings.max, response.timings.min

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e, "With track id: {}".format(track_identifier)
            )

    def get_processor_timings(
        self, processor_identifier: int
    ) -> tuple[float, float, float] | None:
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
            cr = self._stub.GetProcessorTimings(
                sushi_rpc_pb2.ProcessorIdentifier(id=processor_identifier)
            )
            response = self._parent.validate_command_response(
                cr, f"Getting timings for processor {processor_identifier}"
            )
            return response.timings.average, response.timings.max, response.timings.min

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e, "With processor id: {}".format(processor_identifier)
            )

    def reset_all_timings(self):
        """
        Reset all the timings.
        """
        try:
            cr = self._stub.ResetAllTimings(sushi_rpc_pb2.GenericVoidValue())
            return self._parent.validate_command_response(cr, "Resetting all timings.")

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def reset_track_timings(self, track_identifier: int):
        """
        Reset the timings of the specified track.

        Parameters:
            track_identifier (int): The id of the track to reset the timings of.
        """
        try:
            cr = self._stub.ResetTrackTimings(
                sushi_rpc_pb2.TrackIdentifier(id=track_identifier)
            )
            return self._parent.validate_command_response(
                cr, f"Resetting timings for track {track_identifier}"
            )

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e, "With track id: {}".format(track_identifier)
            )

    def reset_processor_timings(self, processor_identifier: int):
        """
        Reset the timings of the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to reset the timings of.
        """
        try:
            cr = self._stub.ResetProcessorTimings(
                sushi_rpc_pb2.ProcessorIdentifier(id=processor_identifier)
            )
            return self._parent.validate_command_response(
                cr, f"Resetting timnigs for processor {processor_identifier}"
            )

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e, "With processor id: {}".format(processor_identifier)
            )
