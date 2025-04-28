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

import grpc

from . import sushierrors
from . import grpc_gen
from . import sushi_info_types as info_types
from .events import SushiCommandResponse

from typing import List

####################################
# Sushi audio graph controller class #
####################################


class AudioGraphController:
    """
    A class to control the audio graph in sushi via gRPC. It has functions to create, move, delete and get info
    about audio graph object like tracks and processors.

    Attributes:
        _stub (AudioGraphControllerStub): Connection stubs to the gRPC audio graph interface implemented in sushi.
    """

    def __init__(
        self,
        parent,
        address="localhost:51051",
        sushi_proto_def="/usr/share/sushi/sushi_rpc.proto",
        sushi_proto=None,
        sushi_grpc=None,
    ):
        """
        The constructor for the AudioGraphController class setting up the gRPC connection with sushi.

        Parameters:
            address (str): 'ip-addres:port' The ip-addres and port at which to connect to sushi.
            sushi_proto_def (str): path to .proto file with SUSHI's gRPC services definition
        """
        self._parent: "SushiController" = parent

        try:
            channel = grpc.insecure_channel(address)
        except AttributeError as e:
            raise TypeError(
                "Parameter address = {}. Should be a string containing the ip-address and port of sushi ('ip-address:port')".format(
                    address
                )
            ) from e

        if sushi_proto and sushi_grpc:
            self._sushi_proto = sushi_proto
            self._sushi_grpc = sushi_grpc
        else:
            self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(
                sushi_proto_def
            )

        self._stub = self._sushi_grpc.AudioGraphControllerStub(channel)

    def get_all_processors(self) -> List[info_types.ProcessorInfo]:
        """
        Gets a list of all available processors.

        Returns:
            List[info_types.ProcessorInfo]: A list with the info of all the available processors.
        """
        try:
            response = self._stub.GetAllProcessors(self._sushi_proto.GenericVoidValue())
            processor_info_list = []
            for processor_info in response.processors:
                processor_info_list.append(info_types.ProcessorInfo(processor_info))
            return processor_info_list

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_all_tracks(self) -> List[info_types.TrackInfo]:
        """
        Gets a list of all available tracks.

        Returns:
            List[info_types.TrackInfo]: A list with the info of all the available tracks.
        """
        try:
            response = self._stub.GetAllTracks(self._sushi_proto.GenericVoidValue())

            track_info_list = []
            for track_info in response.tracks:
                track_info_list.append(info_types.TrackInfo(track_info))
            return track_info_list

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)

    def get_track_id(self, track_name: str) -> int:
        """
        Get the id of a track from its name.

        Parameters:
            track_name (str): The name of the track.

        Returns:
            id (int): The track id in Sushi
        """
        try:
            cr = self._stub.GetTrackId(
                self._sushi_proto.GenericStringValue(value=track_name)
            )
            response = self._parent.validate_command_response(
                cr, context_info=f"Getting id for track {track_name}"
            )
            return response.id

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With track name: {}".format(track_name))

    def get_track_info(self, track_identifier: int) -> info_types.TrackInfo:
        """
        Get the info of a track from its id.

        Parameters:
            track_identifier (int): The id of the track to get the info from.

        Returns:
            info_types.TrackInfo: The info of the track matching the id.
        """
        try:
            cr = self._stub.GetTrackInfo(
                self._sushi_proto.TrackIdentifier(id=track_identifier)
            )
            response = self._parent.validate_command_response(
                cr, context_info=f"Getting track info for track {track_identifier}"
            )
            return info_types.TrackInfo(response.info)

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e, "With track id: {}".format(track_identifier)
            )

    def get_track_processors(
        self, track_identifier: int
    ) -> List[info_types.ProcessorInfo]:
        """
        Get a list of processors assigned on the specified track.

        Parameters:
            track_identifier (int): The id of the track to get the processor list from.

        Returns:
            List[info_types.ProcessorInfo]: A list of the info of the processors assigned to the track matching the id.
        """
        try:
            cr = self._stub.GetTrackProcessors(
                self._sushi_proto.TrackIdentifier(id=track_identifier)
            )
            response = self._parent.validate_command_response(
                cr, f"Getting track processors for track {track_identifier}"
            )
            processor_info_list = []
            for processor_info in response.processors:
                processor_info_list.append(info_types.ProcessorInfo(processor_info))

            return processor_info_list

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e, "With track id: {}".format(track_identifier)
            )

    def get_processor_id(self, processor_name: str) -> int:
        """
        Get the id of a processor from its name.

        Parameters:
            processor_name (str): The name of the processor to get the id from.

        Returns:
            int: The id of the processor matching the name.
        """
        try:
            cr = self._stub.GetProcessorId(
                self._sushi_proto.GenericStringValue(value=processor_name)
            )
            response = self._parent.validate_command_response(
                cr, f"Getting id for processor {processor_name}"
            )
            return response.id

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e, "With processor name: {}".format(processor_name)
            )

    def get_processor_info(self, processor_identifier: int) -> info_types.ProcessorInfo:
        """
        Get the info of a processor from its id.

        Parameters:
            track_identifier (int): The id of the processor to get the info from.

        Returns:
            info_types.ProcessorInfo: The info of the processor matching the id.
        """
        try:
            cr = self._stub.GetProcessorInfo(
                self._sushi_proto.ProcessorIdentifier(id=processor_identifier)
            )
            response = self._parent.validate_command_response(
                cr, f"Getting processor info for processor {processor_identifier}"
            )
            return info_types.ProcessorInfo(response.processor)

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e, "With processor id: {}".format(processor_identifier)
            )

    def get_processor_bypass_state(self, processor_identifier: int) -> bool:
        """
        Get the bypass state of the specified processor.

        Parameters:
            processor_identifier (int): The id of processor to get the bypass state from.

        Returns:
            bool: The bypass state of the processor matching the id.
        """
        try:
            cr = self._stub.GetProcessorBypassState(
                self._sushi_proto.ProcessorIdentifier(id=processor_identifier)
            )
            response = self._parent.validate_command_response(
                cr, f"Getting bypass state for processor {processor_identifier}"
            )
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e, "With processor id: {}".format(processor_identifier)
            )

    def get_processor_state(
        self, processor_identifier: int
    ) -> info_types.ProcessorState:
        """
        Get the full state of the specified processor.

        Parameters:
            processor_identifier (int): The id of processor to get the full state from.

        Returns:
            ProcessorState: An object describing the full the processor matching the id.
        """
        try:
            cr = self._stub.GetProcessorState(
                self._sushi_proto.ProcessorIdentifier(id=processor_identifier)
            )
            response = self._parent.validate_command_response(
                cr, f"Getting the state of processor {processor_identifier}"
            )
            return response.state

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e, "With processor id: {}".format(processor_identifier)
            )

    def set_processor_bypass_state(
        self, processor_identifier: int, bypass_state: bool
    ) -> SushiCommandResponse:
        """
        Set the bypass state of the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to set the bypass state of.
            bypass_sate (bool): The bypass state of the processor matching the id.

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.SetProcessorBypassState(
                self._sushi_proto.ProcessorBypassStateSetRequest(
                    processor=self._sushi_proto.ProcessorIdentifier(
                        id=processor_identifier
                    ),
                    value=bypass_state,
                )
            )
            return self._parent.validate_command_response(
                cr,
                f"Setting bypass state of processor {processor_identifier} to {bypass_state}",
            )

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e,
                "With processor id: {}, bypass state: {}".format(
                    processor_identifier, bypass_state
                ),
            )

    def set_discrete_processor_state(
        self,
        processor_identifier: int,
        program_id: int | None = None,
        bypassed: bool | None = False,
        property_values: list[tuple[int, str]] = [],
        parameter_values: list[tuple[int, float]] = [],
    ) -> None:
        """
        Set the full or partial state of the specified processor.

        Parameters:
            program_id (int): The id of the program to set.
            bypassed (bool): Whether the processor should be bypassed or not.
            properties ((int, str)): A list of tuples (id, value) of string properties to set.
            parameters ((int, float)): A list of tuples (id, value) of parameter values to set.
        """
        try:
            grpc_state = self._sushi_proto.ProcessorState()

            if program_id:
                grpc_state.program_id.value = program_id
                grpc_state.program_id.has_value = True

            if bypassed is not None:
                grpc_state.bypassed.value = bypassed
                grpc_state.bypassed.has_value = True

            for property in property_values:
                grpc_property = grpc_state.properties.add()
                grpc_property.property.property_id = property[0]
                grpc_property.value = property[1]

            for parameter in parameter_values:
                grpc_parameter = grpc_state.parameters.add()
                grpc_parameter.parameter.parameter_id = parameter[0]
                grpc_parameter.value = parameter[1]

            self._stub.SetProcessorState(
                self._sushi_proto.ProcessorStateSetRequest(
                    processor=self._sushi_proto.ProcessorIdentifier(
                        id=processor_identifier
                    ),
                    state=grpc_state,
                )
            )

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e, "With processor id: {}".format(processor_identifier)
            )

    def set_processor_state(
        self, processor_identifier: int, state: info_types.ProcessorState
    ) -> None:
        """
        Set the full or partial state of the specified processor from an existing state object.

        Parameters:
            state (info_types.ProcessorState): a state object either populated manually or received from a call to get_processor_state.
        """
        try:
            grpc_state = self._sushi_proto.ProcessorState()

            if state.program_id:
                grpc_state.program_id.value = state.program_id
                grpc_state.program_id.has_value = True

            if state.bypassed is not None:
                grpc_state.bypassed.value = state.bypassed
                grpc_state.bypassed.has_value = True

            for property in state.properties:
                grpc_property = grpc_state.properties.add()
                grpc_property.property.property_id = property[0]
                grpc_property.value = property[1]

            for parameter in state.parameters:
                grpc_parameter = grpc_state.parameters.add()
                grpc_parameter.parameter.parameter_id = parameter[0]
                grpc_parameter.value = parameter[1]

            if len(state.binary_data) > 0:
                grpc_state.binary_data = state.binary_data

            self._stub.SetProcessorState(
                self._sushi_proto.ProcessorStateSetRequest(
                    processor=self._sushi_proto.ProcessorIdentifier(
                        id=processor_identifier
                    ),
                    state=grpc_state,
                )
            )

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e, "With processor id: {}".format(processor_identifier)
            )

    def create_track(self, name: str, channels: int) -> SushiCommandResponse:
        """
        Create a new track in sushi.

        Parameters:
            name (str): The name of the new track.
            channels (int): The number of channels to assign the new track.

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.CreateTrack(
                self._sushi_proto.CreateTrackRequest(name=name, channels=channels)
            )
            return self._parent.validate_command_response(cr, f"Creating track {name}")
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e, "With track name: {}, number of channels: {}".format(name, channels)
            )

    def create_multibus_track(self, name: str, buses: int) -> SushiCommandResponse:
        """
        Create a new multibus track in sushi.

        Parameters:
            name (str): The name of the new track.
            buses (int): The number of audio buses in the new track.

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.CreateMultibusTrack(
                self._sushi_proto.CreateMultibusTrackRequest(name=name, buses=buses)
            )
            return self._parent.validate_command_response(
                cr, f"Creating multibus track {name}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e, "With track name: {}, buses: {}".format(name, buses)
            )

    def create_pre_track(self, name: str) -> SushiCommandResponse:
        """
        Create a new pre track in sushi.

        Parameters:
            name (str): The name of the new track.

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.CreatePreTrack(
                self._sushi_proto.CreatePreTrackRequest(name=name)
            )
            return self._parent.validate_command_response(
                cr, f"Creating pre-track {name}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With track name: {}".format(name))

    def create_post_track(self, name: str) -> SushiCommandResponse:
        """
        Create a new POST track in sushi.

        Parameters:
            name (str): The name of the new track.

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.CreatePostTrack(
                self._sushi_proto.CreatePostTrackRequest(name=name)
            )
            return self._parent.validate_command_response(
                cr, f"Creating post-track {name}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With track name: {}".format(name))

    def create_processor_on_track(
        self,
        name: str,
        uid: str,
        path: str,
        processor_type: info_types.PluginType,
        track_id: int,
        before_processor: int,
        add_to_back: bool,
    ) -> SushiCommandResponse:
        """
        Create a new processor on an existing track.

        Parameters:
            name (str): The name to assign the processor. Must be unique.
            uid (str): The uid of an internal Sushi processor. Not applicable for vst2, vst3 and lv2.
            path (str): The path to the processor library (for vst2 or vst3 processors) or the URI of an installed lv2 plugin.
            processor_type (info_type.PluginType): The type of processor to create.
            track_id (int): The id of the track to add the processor to.
            before_processor (int): Which existing processor to create the new processor in front of.
            add_to_back (bool): Set to true to add the processor to the back of the processing chain on the track.

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """

        try:
            cr = self._stub.CreateProcessorOnTrack(
                self._sushi_proto.CreateProcessorRequest(
                    name=name,
                    uid=uid,
                    path=path,
                    type=self._sushi_proto.PluginType(type=processor_type),
                    track=self._sushi_proto.TrackIdentifier(id=track_id),
                    position=self._sushi_proto.ProcessorPosition(
                        add_to_back=add_to_back,
                        before_processor=self._sushi_proto.ProcessorIdentifier(
                            id=before_processor
                        ),
                    ),
                )
            )
            return self._parent.validate_command_response(
                cr, f"Creating processor {name} on track {track_id}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e,
                "With processor name: {}, uid: {}, path: {}, type: {}, id: {}, position: {}, add_to_back: {}".format(
                    name,
                    uid,
                    path,
                    processor_type,
                    track_id,
                    before_processor,
                    add_to_back,
                ),
            )

    def move_processor_on_track(
        self,
        processor: int,
        source_track: int,
        destination_track: int,
        before_processor: int,
        add_to_back: bool,
    ) -> SushiCommandResponse:
        """
        Move an existing processor.

        Parameters:
            processor (int): The id of the processor to move.
            source_track (int): The id of the track to move the processor from.
            destination_track (int): The id of the track to move the processor to.
            before_processor (int): The id of another processor to move this processor in front of.
            add_to_back (bool): Set to true to add the processor to the back of the processing chain on the track.

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.MoveProcessorOnTrack(
                self._sushi_proto.MoveProcessorRequest(
                    processor=self._sushi_proto.ProcessorIdentifier(id=processor),
                    source_track=self._sushi_proto.TrackIdentifier(id=source_track),
                    dest_track=self._sushi_proto.TrackIdentifier(id=destination_track),
                    position=self._sushi_proto.ProcessorPosition(
                        add_to_back=add_to_back,
                        before_processor=self._sushi_proto.ProcessorIdentifier(
                            id=before_processor
                        ),
                    ),
                )
            )
            return self._parent.validate_command_response(
                cr,
                f"Moving processor {processor} from track {source_track} to track {destination_track}",
            )

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e,
                "With processor id: {}, source_track: {}, dest_track: {}, before_processor: {}, add_to_back: {}".format(
                    processor,
                    source_track,
                    destination_track,
                    before_processor,
                    add_to_back,
                ),
            )

    def delete_processor_from_track(
        self, processor: int, track: int
    ) -> SushiCommandResponse:
        """
        Delete an existing processor from a track.

        Parameters:
            processor (int): The id of the processor to delete.
            track (int): The id of the track that contains the processor.

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """

        try:
            cr = self._stub.DeleteProcessorFromTrack(
                self._sushi_proto.DeleteProcessorRequest(
                    processor=self._sushi_proto.ProcessorIdentifier(id=processor),
                    track=self._sushi_proto.TrackIdentifier(id=track),
                )
            )
            return self._parent.validate_command_response(
                cr, f"Deleting processor {processor} from track {track}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(
                e, "With processor id: {}, track id: {}".format(processor, track)
            )

    def delete_track(self, track_id: int) -> SushiCommandResponse:
        """
        Delete a track.

        Parameters:
            track_id (int): The id of the track to delete.

        Returns:
            SushiCommandResponse: an asyncio.Event that will be set asynchronously by elkpy when
            the command has been completed.
            The user MAY await it in an asynchronous program, or check .is_set() on it in a
            loop.
        """
        try:
            cr = self._stub.DeleteTrack(self._sushi_proto.TrackIdentifier(id=track_id))
            return self._parent.validate_command_response(
                cr, f"Deleting track {track_id}"
            )
        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With track id: {}".format(track_id))
