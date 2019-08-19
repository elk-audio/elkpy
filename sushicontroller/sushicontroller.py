import grpc
import sushi_rpc_pb2
import sushi_rpc_pb2_grpc

class SushiController(object):
    def __init__(self, address):
        # Initialize necessary members and fields

    # rpc GetSamplerate (GenericVoidValue) returns (GenericFloatValue) {}
    # rpc GetPlayingMode (GenericVoidValue) returns (PlayingMode) {}
    # rpc SetPlayingMode (PlayingMode) returns (GenericVoidValue) {}
    # rpc GetSyncMode (GenericVoidValue) returns (SyncMode) {}
    # rpc SetSyncMode (SyncMode) returns (GenericVoidValue) {}
    # rpc GetTempo (GenericVoidValue) returns (GenericFloatValue) {}
    # rpc SetTempo (GenericFloatValue) returns (GenericVoidValue) {}
    # rpc GetTimeSignature (GenericVoidValue) returns (TimeSignature) {}
    # rpc SetTimeSignature (TimeSignature) returns (GenericVoidValue) {}
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
