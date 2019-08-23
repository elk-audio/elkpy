import grpc
from enum import IntEnum
import sushi_rpc_pb2
import sushi_rpc_pb2_grpc

def grpc_error_handling(e):
    print('Grpc error: ' + str(e.code().name) + ', ' + e.details())

def print_hello():
    print("hello world!")

class SushiController(object):
    def __init__(self, address):
        # Initialize necessary members and fields
        channel = grpc.insecure_channel(address)
        self._stub = sushi_rpc_pb2_grpc.SushiControllerStub(channel)

    # rpc GetSamplerate (GenericVoidValue) returns (GenericFloatValue) {}
    def get_samplerate(self):
        try:
            response = self._stub.GetSamplerate(sushi_rpc_pb2.GenericVoidValue())
            return response.value

        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1

    # rpc GetPlayingMode (GenericVoidValue) returns (PlayingMode) {}
    def get_playing_mode(self):
        try: 
            response = self._stub.GetPlayingMode(sushi_rpc_pb2.GenericVoidValue())
            return response.mode

        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1

    # rpc SetPlayingMode (PlayingMode) returns (GenericVoidValue) {}
    # TODO: PlayingMode DUMMY=0 not working
    def set_playing_mode(self, _playing_mode):
        try:
            self._stub.SetPlayingMode(sushi_rpc_pb2.PlayingMode(
                mode = int(_playing_mode)
            ))
        
        except grpc.RpcError as e:
            grpc_error_handling(e)
            
    # rpc GetSyncMode (GenericVoidValue) returns (SyncMode) {}
    def get_sync_mode(self):
        try:
            response = self._stub.GetSyncMode(sushi_rpc_pb2.GenericVoidValue())
            return response.mode
        
        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1

    # rpc SetSyncMode (SyncMode) returns (GenericVoidValue) {}
    # TODO: DUMMY=0 mode doesn't seem to work
    def set_sync_mode(self, _sync_mode):
        try:
            self._stub.SetSyncMode(sushi_rpc_pb2.SyncMode(
                mode = int(_sync_mode)
            ))
        
        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetTempo (GenericVoidValue) returns (GenericFloatValue) {}
    def get_tempo(self):
        try:
            response = self._stub.GetTempo(sushi_rpc_pb2.GenericVoidValue())
            return response.value
        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1

    # rpc SetTempo (GenericFloatValue) returns (GenericVoidValue) {}
    def set_tempo(self, _tempo):
        try:
            self._stub.SetTempo(sushi_rpc_pb2.GenericFloatValue(
                value = _tempo
            ))

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetTimeSignature (GenericVoidValue) returns (TimeSignature) {}
        # TODO: change denomainator to denominator when spelled correctly in compiled proto buff file

    def get_time_signature(self):
        try:
            response = self._stub.GetTimeSignature(sushi_rpc_pb2.GenericVoidValue())
            return response.numerator, response.denomainator
        
        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1, -1

    # rpc SetTimeSignature (TimeSignature) returns (GenericVoidValue) {}
    # TODO: change denomainator to denominator when spelled correctly in compiled proto buff file
    def set_time_signature(self, _numerator, _denominator):
        try:
            self._stub.SetTimeSignature(sushi_rpc_pb2.TimeSignature(
                numerator = _numerator,
                denomainator = _denominator
            ))
        
        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetTracks(GenericVoidValue) returns (TrackInfoList) {}
    def get_tracks(self):
        try:
            response = self._stub.GetTracks(sushi_rpc_pb2.GenericVoidValue())
            return response

        except grpc.RpcError as e:
            grpc_error_handling(e)
        
    #######################
    # // Keyboard control #
    #######################

    # rpc SendNoteOn(NoteOnRequest) returns (GenericVoidValue) {}
    def send_note_on(self, _track_identifier, _note, _channel, _velocity):
        try:
            self._stub.SendNoteOn(sushi_rpc_pb2.NoteOnRequest(
                track = sushi_rpc_pb2.TrackIdentifier(id = _track_identifier),
                note = _note,
                channel = _channel,
                velocity = _velocity
            ))

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc SendNoteOff(NoteOffRequest) returns (GenericVoidValue) {}
    def send_note_off(self, _track_identifier, _note, _channel, _velocity):
        try:
            self._stub.SendNoteOff(sushi_rpc_pb2.NoteOffRequest(
                track = sushi_rpc_pb2.TrackIdentifier(id = _track_identifier),
                note = _note,
                channel = _channel,
                velocity = _velocity
            ))

        except grpc.RpcError as e:
            grpc_error_handling(e)
    
    # rpc SendNoteAftertouch(NoteAftertouchRequest) returns (GenericVoidValue) {}
    def send_note_aftertouch(self, _track_identifier, _note, _channel, _value):
        try:
            self._stub.SendNoteAftertouch(sushi_rpc_pb2.NoteAftertouchRequest(
                track = sushi_rpc_pb2.TrackIdentifier(id = _track_identifier),
                note = _note,
                channel = _channel,
                value = _value
            ))
        
        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc SendAftertouch(NoteModulationRequest) returns (GenericVoidValue) {}
    def send_aftertouch(self, _track_identifier, _channel, _value):
        try:
            self._stub.SendAftertouch(sushi_rpc_pb2.NoteModulationRequest(
                track = sushi_rpc_pb2.TrackIdentifier(id = _track_identifier),
                channel = _channel,
                value = _value
            ))
        
        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc SendPitchBend(NoteModulationRequest) returns (GenericVoidValue) {}
    def send_pitch_bend(self, _track_identifier, _channel, _value):
        try:
            self._stub.SendPitchBend(sushi_rpc_pb2.NoteModulationRequest(
                track = sushi_rpc_pb2.TrackIdentifier(id = _track_identifier),
                channel = _channel,
                value = _value
            ))

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc SendModulation(NoteModulationRequest) returns (GenericVoidValue) {}
    def send_modulation(self, _track_identifier, _channel, _value):
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
    def get_engine_timings(self):
        try:
            response = self._stub.GetEngineTimings(sushi_rpc_pb2.GenericVoidValue())
            return response.average, response.min, response.max

        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1, -1, -1

    # rpc GetTrackTimings(TrackIdentifier) returns (CpuTimings) {}
    def get_track_timings(self, _track_identifier):
        try:
            response = self._stub.GetTrackTimings(sushi_rpc_pb2.TrackIdentifier(
                id = _track_identifier
            ))
            return response.average, response.min, response.max

        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1, -1, -1

    # rpc GetProcessorTimings(ProcessorIdentifier) returns (CpuTimings) {}
    def get_processor_timings(self, _processor_identifier):
        try:
            response = self._stub.GetProcessorTimings(sushi_rpc_pb2.ProcessorIdentifier(
                id = _processor_identifier
            ))
            return response.average, response.min, response.max
        
        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1, -1, -1

    # rpc ResetAllTimings(GenericVoidValue) returns (GenericVoidValue) {}
    def reset_all_timings(self):
        try:
            self._stub.ResetAllTimings(sushi_rpc_pb2.GenericVoidValue())
        
        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc ResetTrackTimings(TrackIdentifier) returns (GenericVoidValue) {}
    def reset_track_timings(self, _track_identifier):
        try:
            self._stub.ResetTrackTimings(sushi_rpc_pb2.TrackIdentifier(
                id = _track_identifier
            ))

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc ResetProcessorTimings(ProcessorIdentifier) returns (GenericVoidValue) {}
    def reset_processor_timings(self, _processor_identifier):
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
    def get_track_id(self, _track_name):
        try:
            response = self._stub.GetTrackId(sushi_rpc_pb2.GenericStringValue(
                value = _track_name
            ))
            return response.id
        
        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1

    # rpc GetTrackInfo(TrackIdentifier) returns (TrackInfo) {}
    def get_track_info(self, _track_identifier):
        try:
            response = self._stub.GetTrackInfo(sushi_rpc_pb2.TrackIdentifier(
                id = _track_identifier
            ))
            return response

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
    def get_track_processors(self, _track_identifier):
        try:
            response = self._stub.GetTrackProcessors(sushi_rpc_pb2.TrackIdentifier(
                id = _track_identifier
            ))
            return response
        
        except grpc.RpcError as e:
            grpc_error_handling(e)
    
    # rpc GetTrackParameters(TrackIdentifier) returns (ParameterInfoList) {}
    def get_track_parameters(self, _track_identifier):
        try:
            response = self._stub.GetTrackParameters(sushi_rpc_pb2.TrackIdentifier(
                id = _track_identifier
            ))
            return response

        except grpc.RpcError as e:
            grpc_error_handling(e)
    # // list requests left out for now

    ########################
    # // Processor control #
    ########################

    # rpc GetProcessorId (GenericStringValue) returns (ProcessorIdentifier) {}
    def get_processor_id(self, _processor_name):
        try:
            response = self._stub.GetProcessorId(sushi_rpc_pb2.GenericStringValue(
                value = _processor_name
            ))
            return response.id
        
        except grpc.RpcError as e:
            grpc_error_handling(e)
            return -1

    # rpc GetProcessorInfo (ProcessorIdentifier) returns (ProcessorInfo) {}
    def get_processor_info(self, _processor_identifier):
        try:
            response = self._stub.GetProcessorInfo(sushi_rpc_pb2.ProcessorIdentifier(
                id = _processor_identifier
            ))
            return response

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetProcessorBypassState (ProcessorIdentifier) returns (GenericBoolValue) {}
    def get_processor_bypass_state(self, _processor_identifier):
        try:
            response = self._stub.GetProcessorBypassState(sushi_rpc_pb2.ProcessorIdentifier(
                id = _processor_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc SetProcessorBypassState (ProcessorBypassStateSetRequest) returns (GenericVoidValue) {}
    # TODO: try with more modern Sushi
    def set_processor_bypass_state(self, _processor_identifier, _bypass_state):
        try:
            self._stub.SetProcessorBypassState(sushi_rpc_pb2.ProcessorBypassStateSetRequest(
                processor = sushi_rpc_pb2.ProcessorIdentifier(id = _processor_identifier),
                value = _bypass_state
            ))
        
        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetProcessorCurrentProgram (ProcessorIdentifier) returns (ProgramIdentifier) {}
    def get_processor_current_program(self, _processor_identifier):
        try:
            response = self._stub.GetProcessorCurrentProgram(sushi_rpc_pb2.ProcessorIdentifier(
                id = _processor_identifier
            ))
            return response.program

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetProcessorCurrentProgramName (ProcessorIdentifier) returns (GenericStringValue) {}
    def get_processor_current_program_name(self, _processor_identifier):
        try:
            response = self._stub.GetProcessorCurrentProgramName(sushi_rpc_pb2.ProcessorIdentifier(
                id = _processor_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetProcessorProgramName (ProcessorProgramIdentifier) returns (GenericStringValue) {}
    def get_processor_program_name(self, _processor_identifier, _program):
        try:
            response = self._stub.GetProcessorProgramName(sushi_rpc_pb2.ProcessorProgramIdentifier(
                processor = sushi_rpc_pb2.ProcessorIdentifier(id = _processor_identifier),
                program = _program
            ))
            return response.value

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetProcessorPrograms (ProcessorIdentifier) returns (ProgramInfoList) {}
    def get_processor_programs(self, _processor_identifier):
        try:
            response = self._stub.GetProcessorPrograms(sushi_rpc_pb2.ProcessorIdentifier(
                id = _processor_identifier
            ))
            return response

        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc SetProcessorProgram (ProcessorProgramSetRequest) returns (GenericVoidValue) {}
    def set_processor_program(self, _processor_identifier, _program):
        try:
            self._stub.SetProcessorProgram(sushi_rpc_pb2.ProcessorProgramSetRequest(
                processor = sushi_rpc_pb2.ProcessorIdentifier(id = _processor_identifier),
                program = sushi_rpc_pb2.ProgramIdentifier(program = _program)
            ))
        
        except grpc.RpcError as e:
            grpc_error_handling(e)

    # rpc GetProcessorParameters (ProcessorIdentifier) returns (ParameterInfoList) {}
    def get_processor_parameters(self, _processor_identifier):
        pass

    # // list requests left out

    ########################
    # // Parameter control #
    ########################

    # rpc GetParameterId (ParameterIdRequest) returns (ParameterIdentifier) {}
    # rpc GetParameterInfo (ParameterIdentifier) returns (ParameterInfo) {}
    # rpc GetParameterValue(ParameterIdentifier) returns (GenericFloatValue) {}
    # rpc GetParameterValueNormalised(ParameterIdentifier) returns (GenericFloatValue) {}
    # rpc GetParameterValueAsString(ParameterIdentifier) returns (GenericStringValue) {}
    # rpc GetStringPropertyValue(ParameterIdentifier) returns (GenericStringValue) {}
    # rpc SetParameterValue(ParameterSetRequest) returns (GenericVoidValue) {}
    # rpc SetParameterValueNormalised(ParameterSetRequest) returns (GenericVoidValue) {}
    # rpc SetStringPropertyValue(StringPropertySetRequest) returns (GenericVoidValue) {}

    #########################
    # //Custom data objects #
    #########################

    class PlayingMode(IntEnum):
        DUMMY = 0
        STOPPED = 1
        PLAYING = 2
        RECORDING = 3

    class SyncMode(IntEnum):
        DUMMY = 0
        INTERNAL = 1
        MIDI = 2
        LINK = 3

    class ParameterType(IntEnum):
        DUMMY = 0
        BOOL = 1
        INT = 2
        FLOAT = 3
        STRING_PROPERTY = 4
        DATA_PROPERTY = 5
