import grpc
from . import sushi_rpc_pb2
from . import sushi_rpc_pb2_grpc
from . import sushi_info_types as info_types

from enum import IntEnum
from typing import List

_author__ = "Ruben Svensson"
__copyright__ = "Copyright 2019, Mind Music Labs"

def grpc_error_handling(e):
    print('Grpc error: ' + str(e.code().name) + ', ' + e.details())

class SushiController(object):
    ''' 
    A class to control sushi via gRPC.

    Attributes:
        _stub (SushiControllerStub): Connection stubs to the gRPC interface implemented in sushi.
    '''
    def __init__(self, address = 'localhost:51051'):
        '''
        The constructor for the SushiController class.

        Parameters:
            address (str): 'ip-addres:port' The ip-addres and port at which to connect to sushi.
        '''
        channel = grpc.insecure_channel(address)
        self._stub = sushi_rpc_pb2_grpc.SushiControllerStub(channel)

    # rpc GetSamplerate (GenericVoidValue) returns (GenericFloatValue) {}
    def get_samplerate(self) -> float:
        '''
        Get the current samplerate.
        
        Returns:
            float: Current samplerate.  
        '''
        try:
            response = self._stub.GetSamplerate(sushi_rpc_pb2.GenericVoidValue())
            return response.value

        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1

    # rpc GetPlayingMode (GenericVoidValue) returns (PlayingMode) {}
    def get_playing_mode(self) -> int:
        '''
        Get the current playing mode.
        
        Returns:
            int: Current playing mode.
                1 = Stopped,
                2 = Playing,
                3 = Recording (not implemented)
        '''
        try: 
            response = self._stub.GetPlayingMode(sushi_rpc_pb2.GenericVoidValue())
            return response.mode

        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1

    # rpc SetPlayingMode (PlayingMode) returns (GenericVoidValue) {}
    # TODO: PlayingMode DUMMY=0 not working
    def set_playing_mode(self, _playing_mode: int) -> None:
        '''
        Set the playing mode.
        
        Parameters:
            playing_mode (int): The playing mode to set.
                                1 = Stopped,
                                2 = Playing,
                                3 = Recording (not implemented)
        '''
        try:
            self._stub.SetPlayingMode(sushi_rpc_pb2.PlayingMode(
                mode = int(_playing_mode)
            ))
        
        except grpc.RpcError as e:
            grpc_error_handling(e)
            
    # rpc GetSyncMode (GenericVoidValue) returns (SyncMode) {}
    def get_sync_mode(self) -> int:
        '''
        Get the current sync mode.

        Returns:
            int: Current sync mode.
                1 = Internal,
                2 = MIDI,
                3 = Link
        '''
        try:
            response = self._stub.GetSyncMode(sushi_rpc_pb2.GenericVoidValue())
            return response.mode
        
        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1

    # rpc SetSyncMode (SyncMode) returns (GenericVoidValue) {}
    # TODO: DUMMY=0 mode doesn't seem to work
    def set_sync_mode(self, _sync_mode: int) -> None:
        '''
        Set the sync mode.

        Parameters:
            _sync_mode (int): The sync mode to set.
                            1 = Internal,
                            2 = MIDI,
                            3 = Link
        '''
        try:
            self._stub.SetSyncMode(sushi_rpc_pb2.SyncMode(
                mode = int(_sync_mode)
            ))
        
        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetTempo (GenericVoidValue) returns (GenericFloatValue) {}
    def get_tempo(self) -> float:
        '''
        Get the current tempo.

        Returns:
            float: Current tempo in BPM(Beats Per Minute).
        '''
        try:
            response = self._stub.GetTempo(sushi_rpc_pb2.GenericVoidValue())
            return response.value
        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1

    # rpc SetTempo (GenericFloatValue) returns (GenericVoidValue) {}
    def set_tempo(self, _tempo: float) -> None:
        '''
        Set the tempo.
            
        Parameters:
            _tempo (float): The tempo in BPM(Beats Per Minute).
        '''
        try:
            self._stub.SetTempo(sushi_rpc_pb2.GenericFloatValue(
                value = _tempo
            ))

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetTimeSignature (GenericVoidValue) returns (TimeSignature) {}
        # TODO: change denomainator to denominator when spelled correctly in compiled proto buff file

    def get_time_signature(self) -> (int, int):
        '''
        Get the current time signature.

        Returns:
            int: The nominator of the time signature.
            int: The denominator of the time signature.
        '''
        try:
            response = self._stub.GetTimeSignature(sushi_rpc_pb2.GenericVoidValue())
            return response.numerator, response.denomainator
        
        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1, -1

    # rpc SetTimeSignature (TimeSignature) returns (GenericVoidValue) {}
    # TODO: change denomainator to denominator when spelled correctly in compiled proto buff file
    def set_time_signature(self, _numerator: int, _denominator: int) -> None:
        '''
        Set the time signature

        Parameters:
            _numerator (int): The numerator of the time signature.
            _denominator (int): The denominator of the time signature. Should be either 4 or 8.
        '''
        try:
            self._stub.SetTimeSignature(sushi_rpc_pb2.TimeSignature(
                numerator = _numerator,
                denomainator = _denominator
            ))
        
        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetTracks(GenericVoidValue) returns (TrackInfoList) {}
    def get_tracks(self) -> List[info_types.TrackInfo]:
        '''
        Gets a list of all available track.

        Returns:
            List[info_types.TrackInfo]: A list with the info of all the available tracks.
        '''
        try:
            response = self._stub.GetTracks(sushi_rpc_pb2.GenericVoidValue())
            
            track_info_list = []
            for track_info in response.tracks:
                track_info_list.append(info_types.TrackInfo(track_info))
            return track_info_list

        except grpc.RpcError as e:
            grpc_error_handling(e)
        
    #######################
    # // Keyboard control #
    #######################

    # rpc SendNoteOn(NoteOnRequest) returns (GenericVoidValue) {}
    def send_note_on(self, _track_identifier: int, _channel: int, _note: int, _velocity: float) -> None:
        '''
        Sends a note on message to the specified track.

        Parameters:
            _track_identifier (int): The id of the track that should receive the message.
            _channel (int): The channel on which the message should be sent.
            _note (int): The note to send. Follows the MIDI standard where middle c = 60.
            _velocity (float): The velocity of the note. Should be in range (0.0-1.0).

        '''
        try:
            self._stub.SendNoteOn(sushi_rpc_pb2.NoteOnRequest(
                track = sushi_rpc_pb2.TrackIdentifier(id = _track_identifier),
                channel = _channel,
                note = _note,
                velocity = _velocity
            ))

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc SendNoteOff(NoteOffRequest) returns (GenericVoidValue) {}
    def send_note_off(self, _track_identifier: int, _channel: int, _note: int, _velocity: float) -> None:
        '''
        Sends a note off message to the specified track.

        Parameters:
            _track_identifier (int): The id of the track that should receive the message.
            _channel (int): The channel on which the message should be sent.
            _note (int): The note to send. Follows the MIDI standard where middle c = 60.
            _velocity (float): The velocity of the note. Should be in range (0.0-1.0).
        '''
        try:
            self._stub.SendNoteOff(sushi_rpc_pb2.NoteOffRequest(
                track = sushi_rpc_pb2.TrackIdentifier(id = _track_identifier),
                channel = _channel,
                note = _note,
                velocity = _velocity
            ))

        except grpc.RpcError as e:
            grpc_error_handling(e)
    
    # rpc SendNoteAftertouch(NoteAftertouchRequest) returns (GenericVoidValue) {}
    def send_note_aftertouch(self, _track_identifier: int, _channel: int, _note: int, _value: float) -> None:
        '''
        Sends a aftertouch message to the specified track and note.

        Parameters:
            _track_identifier (int): The id of the track that should receive the message.
            _channel (int): The channel on which the message should be sent.
            _note (int): The note which should receive the message. Follows the MIDI standard where middle c = 60.
            _value (float): The aftertouch value of the note. Should be in range (0.0-1.0).
        '''
        try:
            self._stub.SendNoteAftertouch(sushi_rpc_pb2.NoteAftertouchRequest(
                track = sushi_rpc_pb2.TrackIdentifier(id = _track_identifier),
                channel = _channel,
                note = _note,
                value = _value
            ))
        
        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc SendAftertouch(NoteModulationRequest) returns (GenericVoidValue) {}
    def send_aftertouch(self, _track_identifier: int, _channel: int, _value: float) -> None:
        '''
        Sends a aftertouch message to the specified track.

        Parameters:
            _track_identifier (int): The id of the track that should receive the message.
            _channel (int): The channel on which the message should be sent.
            _value (float): The aftertouch value. Should be in range (0.0-1.0).
        '''
        try:
            self._stub.SendAftertouch(sushi_rpc_pb2.NoteModulationRequest(
                track = sushi_rpc_pb2.TrackIdentifier(id = _track_identifier),
                channel = _channel,
                value = _value
            ))
        
        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc SendPitchBend(NoteModulationRequest) returns (GenericVoidValue) {}
    def send_pitch_bend(self, _track_identifier: int, _channel: int, _value: float) -> None:
        '''
        Sends a pitch bend message to the specified track.

        Parameters:
            _track_identifier (int): The id of the track that should receive the message.
            _channel (int): The channel on which the message should be sent.
            _value (float): The pitch bend value. Should be in range (0.0-1.0).
        '''
        try:
            self._stub.SendPitchBend(sushi_rpc_pb2.NoteModulationRequest(
                track = sushi_rpc_pb2.TrackIdentifier(id = _track_identifier),
                channel = _channel,
                value = _value
            ))

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc SendModulation(NoteModulationRequest) returns (GenericVoidValue) {}
    def send_modulation(self, _track_identifier: int, _channel: int, _value: float) -> None:
        '''
        Sends a modulation message to the specified track.

        Parameters:
            _track_identifier (int): The id of the track that should receive the message.
            _channel (int): The channel on which the message should be sent.
            _value (float): The modulation value. Should be in range (0.0-1.0).
        '''
        try:
            self._stub.SendModulation(sushi_rpc_pb2.NoteModulationRequest(
                track = sushi_rpc_pb2.TrackIdentifier(id = _track_identifier),
                channel = _channel,
                value = _value
            ))
        
        except grpc.RpcError as e:
            grpc_error_handling(e)

    ###################
    # // Cpu timings  #
    ###################

    # rpc GetEngineTimings(GenericVoidValue) returns (CpuTimings) {}
    # TODO: Check that the order of the output is correct
    def get_engine_timings(self) -> (float, float, float):
        '''
        Get the average, max and min timings of the engine. --timing-statistics need to be enabled

        Returns:
            float: The average engine processing time in ms.
            float: The minimum engine processing time in ms.
            float: The maximum engine processing time in ms.
        '''
        try:
            response = self._stub.GetEngineTimings(sushi_rpc_pb2.GenericVoidValue())
            return response.average, response.min, response.max

        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1, -1, -1

    # rpc GetTrackTimings(TrackIdentifier) returns (CpuTimings) {}
    def get_track_timings(self, _track_identifier: int) -> (float, float, float):
        '''
        Get the average, max and min timings of the specified track. --timing-statistics need to be enabled

        Parameters:
            _track_identifier (int): The id of the track to get timings from.

        Returns:
            float: The average track processing time in ms.
            float: The minimum track processing time in ms.
            float: The maximum track processing time in ms.
        '''
        try:
            response = self._stub.GetTrackTimings(sushi_rpc_pb2.TrackIdentifier(
                id = _track_identifier
            ))
            return response.average, response.min, response.max

        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1, -1, -1

    # rpc GetProcessorTimings(ProcessorIdentifier) returns (CpuTimings) {}
    def get_processor_timings(self, _processor_identifier: int) -> (float, float, float):
        '''
        Get the average, max and min timings of the specified processor. --timing-statistics need to be enabled

        Parameters:
            _processor_identifier (int): The id of the processor to get timings from.

        Returns:
            float: The average processor processing time in ms.
            float: The minimum processor processing time in ms.
            float: The maximum processor processing time in ms.
        '''
        try:
            response = self._stub.GetProcessorTimings(sushi_rpc_pb2.ProcessorIdentifier(
                id = _processor_identifier
            ))
            return response.average, response.min, response.max
        
        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1, -1, -1

    # rpc ResetAllTimings(GenericVoidValue) returns (GenericVoidValue) {}
    def reset_all_timings(self) -> None:
        '''
        Reset all the timings.
        '''
        try:
            self._stub.ResetAllTimings(sushi_rpc_pb2.GenericVoidValue())
        
        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc ResetTrackTimings(TrackIdentifier) returns (GenericVoidValue) {}
    def reset_track_timings(self, _track_identifier: int) -> None:
        '''
        Reset the timings of the specified track.

        Parameters:
            _track_identifier (int): The id of the track to reset the timings of.
        '''
        try:
            self._stub.ResetTrackTimings(sushi_rpc_pb2.TrackIdentifier(
                id = _track_identifier
            ))

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc ResetProcessorTimings(ProcessorIdentifier) returns (GenericVoidValue) {}
    def reset_processor_timings(self, _processor_identifier: int) -> None:
        '''
        Reset the timings of the specified processor.

        Parameters:
            _processor_identifier (int): The id of the processor to reset the timings of.
        '''
        try:
            self._stub.ResetProcessorTimings(sushi_rpc_pb2.ProcessorIdentifier(
                id = _processor_identifier
            ))

        except grpc.RpcError as e:
            grpc_error_handling(e)

    ####################
    # // Track control #
    ####################

    # rpc GetTrackId(GenericStringValue) returns (TrackIdentifier) {}
    def get_track_id(self, _track_name: str) -> int:
        '''
        Get the id of a track from its name.

        Parameters:
            _track_name (str): The name of the track.

        Returns:
            int: The id of the track matching the name.
        '''
        try:
            response = self._stub.GetTrackId(sushi_rpc_pb2.GenericStringValue(
                value = _track_name
            ))
            return response.id
        
        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1

    # rpc GetTrackInfo(TrackIdentifier) returns (TrackInfo) {}
    def get_track_info(self, _track_identifier: int) -> info_types.TrackInfo:
        '''
        Get the info of a track from its id.

        Parameters:
            _track_identifier (int): The id of the track to get the info from.

        Returns:
            info_types.TrackInfo: The info of the track matching the id.
        '''
        try:
            response = self._stub.GetTrackInfo(sushi_rpc_pb2.TrackIdentifier(
                id = _track_identifier
            ))
            return info_types.TrackInfo(response)

        except grpc.RpcError as e:
            grpc_error_handling(e)
            return sushi_rpc_pb2.TrackInfo(
                name = 'null',
                input_channels = -1,
                input_busses = -1,
                output_channels = -1,
                output_busses = -1
            )

    # rpc GetTrackProcessors(TrackIdentifier) returns (ProcessorInfoList) {}
    def get_track_processors(self, _track_identifier: int) -> List[info_types.ProcessorInfo]:
        '''
        Get a list of processors assigned on the specified track.

        Parameters:
            _track_identifier (int): The id of the track to get the processor list from.

        Returns:
            List[info_types.ProcessorInfo]: A list of the info of the processors assigned to the track matching the id.
        '''
        try:
            response = self._stub.GetTrackProcessors(sushi_rpc_pb2.TrackIdentifier(
                id = _track_identifier
            ))
            
            processor_info_list = []
            for processor_info in response.processors:
                processor_info_list.append(info_types.ProcessorInfo(processor_info))
            
            return processor_info_list
        
        except grpc.RpcError as e:
            grpc_error_handling(e)
    
    # rpc GetTrackParameters(TrackIdentifier) returns (ParameterInfoList) {}
    def get_track_parameters(self, _track_identifier: int) -> List[info_types.ParameterInfo]:
        '''
        Get a list of parameters available on the specified track.

        Parameters:
            _track_identifier (int): The id of the track to get the parameter list from.

        Returns:
            List[info_types.ParameterInfo]: A list of the info of the parameters assigned to the track matching the id.
        '''
        try:
            response = self._stub.GetTrackParameters(sushi_rpc_pb2.TrackIdentifier(
                id = _track_identifier
            ))
            
            parameter_info_list = []
            for parameter_info in response.parameters:
                parameter_info_list.append(info_types.ParameterInfo(parameter_info))
            
            return parameter_info_list

        except grpc.RpcError as e:
            grpc_error_handling(e)
    # // list requests left out for now

    ########################
    # // Processor control #
    ########################

    # rpc GetProcessorId (GenericStringValue) returns (ProcessorIdentifier) {}
    def get_processor_id(self, _processor_name: str) -> int:
        '''
        Get the id of a processor from its name.

        Parameters:
            _processor_name (str): The name of the processor to get the id from.

        Returns:
            int: The id of the processor matching the name.
        '''
        try:
            response = self._stub.GetProcessorId(sushi_rpc_pb2.GenericStringValue(
                value = _processor_name
            ))
            return response.id
        
        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1

    # rpc GetProcessorInfo (ProcessorIdentifier) returns (ProcessorInfo) {}
    def get_processor_info(self, _processor_identifier: int) -> info_types.ProcessorInfo:
        '''
        Get the info of a processor from its id.

        Parameters:
            _track_identifier (int): The id of the processor to get the info from.

        Returns:
            info_types.ProcessorInfo: The info of the processor matching the id.
        '''
        try:
            response = self._stub.GetProcessorInfo(sushi_rpc_pb2.ProcessorIdentifier(
                id = _processor_identifier
            ))
            return info_types.ProcessorInfo(response)

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetProcessorBypassState (ProcessorIdentifier) returns (GenericBoolValue) {}
    def get_processor_bypass_state(self, _processor_identifier: int) -> bool:
        '''
        Get the bypass state of the specified processor.

        Parameters:
            _processor_identifier (int): The id of processor to get the bypass state from.

        Returns:
            bool: The bypass state of the processor matching the id.
        '''
        try:
            response = self._stub.GetProcessorBypassState(sushi_rpc_pb2.ProcessorIdentifier(
                id = _processor_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc SetProcessorBypassState (ProcessorBypassStateSetRequest) returns (GenericVoidValue) {}
    # TODO: try with more modern Sushi
    def set_processor_bypass_state(self, _processor_identifier: int, _bypass_state: bool) -> None:
        '''
        Set the bypass state of the specified processor.

        Parameters:
            _processor_identifier (int): The id of the processor to set the bypass state of.
            _bypass_sate (bool): The bypass state of the processor matching the id.
        '''
        try:
            self._stub.SetProcessorBypassState(sushi_rpc_pb2.ProcessorBypassStateSetRequest(
                processor = sushi_rpc_pb2.ProcessorIdentifier(id = _processor_identifier),
                value = _bypass_state
            ))
        
        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetProcessorCurrentProgram (ProcessorIdentifier) returns (ProgramIdentifier) {}
    def get_processor_current_program(self, _processor_identifier: int) -> int:
        '''
        Get the id of the current program of the specified processor.

        Parameters:
            _processor_identifier (int): The id of the processor to get the current program id from.

        Returns:
            int: The id of the processors current program.
        '''
        try:
            response = self._stub.GetProcessorCurrentProgram(sushi_rpc_pb2.ProcessorIdentifier(
                id = _processor_identifier
            ))
            return response.program

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetProcessorCurrentProgramName (ProcessorIdentifier) returns (GenericStringValue) {}
    def get_processor_current_program_name(self, _processor_identifier: int) -> str:
        '''
        Get the name of the current program of the specified processor.

        Parameters:
            _processor_identifier (int): The id of the processor to get the current program name from.

        Returns:
            str: The name of the processors current program.
        '''
        try:
            response = self._stub.GetProcessorCurrentProgramName(sushi_rpc_pb2.ProcessorIdentifier(
                id = _processor_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetProcessorProgramName (ProcessorProgramIdentifier) returns (GenericStringValue) {}
    def get_processor_program_name(self, _processor_identifier: int, _program: int) -> str:
        '''
        Get the name of the specified program on the specified processor.

        Parameters:
            _processor_identifier (int): The id of the processor to get the program name from.
            _program (int): The id of the program to get the name of.

        Returns:
            str: The name of the program matching the processor and program id.
        '''
        try:
            response = self._stub.GetProcessorProgramName(sushi_rpc_pb2.ProcessorProgramIdentifier(
                processor = sushi_rpc_pb2.ProcessorIdentifier(id = _processor_identifier),
                program = _program
            ))
            return response.value

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetProcessorPrograms (ProcessorIdentifier) returns (ProgramInfoList) {}
    def get_processor_programs(self, _processor_identifier: int) -> List[info_types.ProgramInfo]:
        '''
        Get a list of the available programs of the specified processor.

        Parameters:
            _processor_identifier (int): The id of the processor to get the programs from.

        Returns:
            List[info_types.ProgramInfo]: A list of the programs available to the processor matching the id.
        '''
        try:
            response = self._stub.GetProcessorPrograms(sushi_rpc_pb2.ProcessorIdentifier(
                id = _processor_identifier
            ))
            
            program_info_list = []
            for program_info in response.programs:
                program_info_list.append(info_types.ProgramInfo(program_info))
            
            return program_info_list

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc SetProcessorProgram (ProcessorProgramSetRequest) returns (GenericVoidValue) {}
    def set_processor_program(self, _processor_identifier: int, _program: int) -> None:
        '''
        Set the program of the specified processor to the one matching the specified program id.

        Parameters:
            _processor_identifier (int): The id of the processor to set the program of.
            _program (int): The id of the program to set.
        '''
        try:
            self._stub.SetProcessorProgram(sushi_rpc_pb2.ProcessorProgramSetRequest(
                processor = sushi_rpc_pb2.ProcessorIdentifier(id = _processor_identifier),
                program = sushi_rpc_pb2.ProgramIdentifier(program = _program)
            ))
        
        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetProcessorParameters (ProcessorIdentifier) returns (ParameterInfoList) {}
    def get_processor_parameters(self, _processor_identifier: int) -> List[info_types.ParameterInfo]:
        '''
        Get a list of the parameters available to the specified processor.

        Parameters:
            _processor_identifier (int): The id of the processor to get the parameters from.

        Returns:
            List[info_types.ParameterInfo]: A list of the parameters available to the processor matching the id.
        '''
        try:
            response = self._stub.GetProcessorParameters(sushi_rpc_pb2.ProcessorIdentifier(
                id = _processor_identifier
            ))
            
            parameter_info_list = []
            for parameter_info in response.parameters:
                parameter_info_list.append(info_types.ParameterInfo(parameter_info))
            
            return parameter_info_list

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # // list requests left out

    ########################
    # // Parameter control #
    ########################

    # rpc GetParameterId (ParameterIdRequest) returns (ParameterIdentifier) {}
    def get_parameter_id(self, _processor_identifier: int, _parameter_name: str) -> int:
        '''
        Get the id of the parameter of the specified processor corresponding to the specified parameter name.

        Parameters:
            _processor_identifier (int): The id of the processor to get the parameter id from.
            _parameter_name (str): The name of the parameter to get the id from.

        Returns:
            int: The id of the parameter matching the parameter name.
        '''
        try:
            response = self._stub.GetParameterId(sushi_rpc_pb2.ParameterIdRequest(
                processor = sushi_rpc_pb2.ProcessorIdentifier(id = _processor_identifier),
                ParameterName = _parameter_name
            ))
            return response.processor_id, response.parameter_id

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetParameterInfo (ParameterIdentifier) returns (ParameterInfo) {}
    def get_parameter_info(self, _processor_identifier: int, _parameter_identifier: int) -> info_types.ParameterInfo:
        '''
        Get info about the specified parameter on the specified processor.

        Parameters:
            _processor_identifier (int): The id of the processor to get the parameter info from.
            _parameter_identifier (int): The id of the parameter to get the info from.

        Returns:
            info_types.ParameterInfo: Info of the parameter matching the id.
        '''
        try:
            response = self._stub.GetParameterInfo(sushi_rpc_pb2.ParameterIdentifier(
                processor_id = _processor_identifier,
                parameter_id = _parameter_identifier
            ))
            return info_types.ParameterInfo(response)

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetParameterValue(ParameterIdentifier) returns (GenericFloatValue) {}
    def get_parameter_value(self, _processor_identifier: int, _parameter_identifier: int) -> float:
        '''
        Get the value of the parameter matching the specified parameter on the specified processor.

        Parameters:
            _processor_identifier (int): The id of the processor to get the parameter value from.
            _parameter_identifier (int): The id of the parameter to get the value from.

        Returns:
            float: The value of the parameter matching the id.
        '''
        try:
            response = self._stub.GetParameterValue(sushi_rpc_pb2.ParameterIdentifier(
                processor_id = _processor_identifier,
                parameter_id = _parameter_identifier
            ))
            return response.value
        
        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetParameterValueNormalised(ParameterIdentifier) returns (GenericFloatValue) {}
    def get_parameter_value_normalised(self, _processor_identifier: int, _parameter_identifier: int) -> float:
        '''
        Get the normalised value of the parameter matching the specified parameter on the specified processor.

        Parameters:
            _processor_identifier (int): The id of the processor to get the normalised parameter value from.
            _parameter_identifier (int): The id of the parameter to get the normalised value from.

        Returns:
            float: The normalised value of the parameter matching the id.
        '''
        try:
            response = self._stub.GetParameterValueNormalised(sushi_rpc_pb2.ParameterIdentifier(
                processor_id = _processor_identifier,
                parameter_id = _parameter_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetParameterValueAsString(ParameterIdentifier) returns (GenericStringValue) {}
    def get_parameter_value_as_string(self, _processor_identifier: int, _parameter_identifier: int) -> str:
        '''
        Get the value of the parameter matching the specified parameter on the specified processor as a string.

        Parameters:
            _processor_identifier (int): The id of the processor to get the parameter value string from.
            _parameter_identifier (int): The id of the parameter to get value string from.

        Returns:
            str: The value as a string of the parameter matching the id.
        '''
        try:
            response = self._stub.GetParameterValueAsString(sushi_rpc_pb2.ParameterIdentifier(
                processor_id = _processor_identifier,
                parameter_id = _parameter_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            grpc_error_handling(e)
        
    # rpc GetStringPropertyValue(ParameterIdentifier) returns (GenericStringValue) {}
    # TODO: Not implemented in sushi yet
    def get_string_property_value(self, _processor_identifier: int, _parameter_identifier: int) -> str:
        '''
        CURRENTLY NOT IMPLEMENTED IN SUSHI
        '''
        try:
            response = self._stub.GetStringPropertyValue(sushi_rpc_pb2.ParameterIdentifier(
                processor_id = _processor_identifier,
                parameter_id = _parameter_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc SetParameterValue(ParameterSetRequest) returns (GenericVoidValue) {}
    def set_parameter_value(self, _processor_identifier: int, _parameter_identifier: int, _value: float) -> None:
        '''
        Set the value of the specified parameter on the specified processor.

        Parameters:
            _processor_identifier (int): The id of the processor that has the parameter to be changed.
            _parameter_identifier (int): The id of the parameter to set the value of.
        '''
        try:
            self._stub.SetParameterValue(sushi_rpc_pb2.ParameterSetRequest(
                parameter = sushi_rpc_pb2.ParameterIdentifier(
                    processor_id = _processor_identifier,
                    parameter_id = _parameter_identifier
                    ),
                value = _value
            ))

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc SetParameterValueNormalised(ParameterSetRequest) returns (GenericVoidValue) {}
    def set_parameter_value_normalised(self, _processor_identifier: int, _parameter_identifier: int, _value: float) -> None:
        '''
        Set the nomralised value of the specified parameter on the specified processor.

        Parameters:
            _processor_identifier (int): The id of the processor that has the parameter to be changed.
            _parameter_identifier (int): The id of the parameter to set the normalised value of.
        '''
        try:
            self._stub.SetParameterValueNormalised(sushi_rpc_pb2.ParameterSetRequest(
                parameter = sushi_rpc_pb2.ParameterIdentifier(
                    processor_id = _processor_identifier,
                    parameter_id = _parameter_identifier
                ),
                value = _value
            ))

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc SetStringPropertyValue(StringPropertySetRequest) returns (GenericVoidValue) {}
    # TODO: Not implemented in sushi yet
    def set_string_property_value(self, _processor_identifier: int, _parameter_identifier: int, _value: str) -> None:
        '''
        CURRENTLY NOT IMPLEMTED IN SUSHI
        '''
        try:
            self._stub.SetStringPropertyValue(sushi_rpc_pb2.StringPropertySetRequest(
                property = sushi_rpc_pb2.ParameterIdentifier(
                    processor_id = _processor_identifier,
                    parameter_id = _parameter_identifier
                ),
                value = _value
            ))

        except grpc.RpcError as e:
            grpc_error_handling(e)

    #########################
    # //Custom data objects #
    #########################

    class PlayingMode(IntEnum):
        '''
        Enum class to hold the values matching the different playing modes.
        '''
        DUMMY = 0
        STOPPED = 1
        PLAYING = 2
        RECORDING = 3

    class SyncMode(IntEnum):
        '''
        Enum class to hold the values matching the different sync modes.
        '''
        DUMMY = 0
        INTERNAL = 1
        MIDI = 2
        LINK = 3

    class ParameterType(IntEnum):
        '''
        Enum class to hold the values matching the different variable types.
        '''
        DUMMY = 0
        BOOL = 1
        INT = 2
        FLOAT = 3
        STRING_PROPERTY = 4
        DATA_PROPERTY = 5
