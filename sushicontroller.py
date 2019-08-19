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
    # TODO: PlayingMode RECORDING=3 not working
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
    # TODO: LINK=3 mode doesn't seem to work
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

    # // Keyboard control
    # rpc SendNoteOn(NoteOnRequest) returns (GenericVoidValue) {}
    # rpc SendNoteOff(NoteOffRequest) returns (GenericVoidValue) {}
    # rpc SendNoteAftertouch(NoteAftertouchRequest) returns (GenericVoidValue) {}
    # rpc SendAftertouch(NoteModulationRequest) returns (GenericVoidValue) {}
    # rpc SendPitchBend(NoteModulationRequest) returns (GenericVoidValue) {}
    # rpc SendModulation(NoteModulationRequest) returns (GenericVoidValue) {}

    # // Cpu timings
    # rpc GetEngineTimings(GenericVoidValue) returns (CpuTimings) {}
    # rpc GetTrackTimings(TrackIdentifier) returns (CpuTimings) {}
    # rpc GetProcessorTimings(ProcessorIdentifier) returns (CpuTimings) {}
    # rpc ResetAllTimings(GenericVoidValue) returns (GenericVoidValue) {}
    # rpc ResetTrackTimings(TrackIdentifier) returns (GenericVoidValue) {}
    # rpc ResetProcessorTimings(ProcessorIdentifier) returns (GenericVoidValue) {}

    # // Track control
    # rpc GetTrackId(GenericStringValue) returns (TrackIdentifier) {}
    # rpc GetTrackInfo(TrackIdentifier) returns (TrackInfo) {}
    # rpc GetTrackProcessors(TrackIdentifier) returns (ProcessorInfoList) {}
    # rpc GetTrackParameters(TrackIdentifier) returns (ParameterInfoList) {}
    # // list requests left out for now

    # // Processor control
    # rpc GetProcessorId (GenericStringValue) returns (ProcessorIdentifier) {}
    # rpc GetProcessorInfo (ProcessorIdentifier) returns (ProcessorInfo) {}
    # rpc GetProcessorBypassState (ProcessorIdentifier) returns (GenericBoolValue) {}
    # rpc SetProcessorBypassState (ProcessorBypassStateSetRequest) returns (GenericVoidValue) {}
    # rpc GetProcessorCurrentProgram (ProcessorIdentifier) returns (ProgramIdentifier) {}
    # rpc GetProcessorCurrentProgramName (ProcessorIdentifier) returns (GenericStringValue) {}
    # rpc GetProcessorProgramName (ProcessorProgramIdentifier) returns (GenericStringValue) {}
    # rpc GetProcessorPrograms (ProcessorIdentifier) returns (ProgramInfoList) {}
    # rpc SetProcessorProgram (ProcessorProgramSetRequest) returns (GenericVoidValue) {}
    # rpc GetProcessorParameters (ProcessorIdentifier) returns (ParameterInfoList) {}
    # // list requests left out

    # // Parameter control
    # rpc GetParameterId (ParameterIdRequest) returns (ParameterIdentifier) {}
    # rpc GetParameterInfo (ParameterIdentifier) returns (ParameterInfo) {}
    # rpc GetParameterValue(ParameterIdentifier) returns (GenericFloatValue) {}
    # rpc GetParameterValueNormalised(ParameterIdentifier) returns (GenericFloatValue) {}
    # rpc GetParameterValueAsString(ParameterIdentifier) returns (GenericStringValue) {}
    # rpc GetStringPropertyValue(ParameterIdentifier) returns (GenericStringValue) {}
    # rpc SetParameterValue(ParameterSetRequest) returns (GenericVoidValue) {}
    # rpc SetParameterValueNormalised(ParameterSetRequest) returns (GenericVoidValue) {}
    # rpc SetStringPropertyValue(StringPropertySetRequest) returns (GenericVoidValue) {}

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
