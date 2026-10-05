import struct
import threading

import zmq

from . import sushi_rpc_pb2 as pb2
from .sushi_rpc_zmq import (
    Service,
    AudioGraphControllerCommand,
    AudioRoutingControllerCommand,
    CvGateControllerCommand,
    KeyboardControllerCommand,
    MidiControllerCommand,
    NotificationControllerCommand,
    OscControllerCommand,
    ParameterControllerCommand,
    ProgramControllerCommand,
    SessionControllerCommand,
    SystemControllerCommand,
    TimingControllerCommand,
    TransportControllerCommand,
)
from .. import sushierrors


class SushiZmqStub:
    """ZMQ transport stub implementing all controller methods.

    Sends each call as a 2-frame multipart message:
      frame 0 – two little-endian uint32: (service, command)
      frame 1 – serialised protobuf request
    Receives a single frame with the serialised protobuf response.
    """

    def __init__(self, address: str, timeout_ms: int = 5000) -> None:
        ctx = zmq.Context.instance()
        self._socket = ctx.socket(zmq.REQ)
        self._socket.setsockopt(zmq.RCVTIMEO, timeout_ms)
        self._socket.connect(address)
        self._lock = threading.Lock()

    def _call(self, service: int, command: int, request, response_type):
        header = struct.pack("<II", service, command)
        payload = request.SerializeToString()
        with self._lock:
            try:
                self._socket.send_multipart([header, payload])
                frames = self._socket.recv_multipart()
                return response_type.FromString(frames[0])
            except zmq.error.Again:
                raise sushierrors.SushiUnavailableError(
                    "ZMQ socket timed out",
                    f"service={service} command={command}",
                )
            except Exception as e:
                raise sushierrors.SushiUnkownError(
                    str(e),
                    f"service={service} command={command}",
                )

    # ── SystemController ─────────────────────────────────────────────────────

    def GetSushiVersion(self, request):
        return self._call(Service.SYSTEM_CONTROLLER, SystemControllerCommand.GET_SUSHI_VERSION, request, pb2.GenericStringValue)

    def GetSushiApiVersion(self, request):
        return self._call(Service.SYSTEM_CONTROLLER, SystemControllerCommand.GET_SUSHI_API_VERSION, request, pb2.GenericStringValue)

    def GetBuildInfo(self, request):
        return self._call(Service.SYSTEM_CONTROLLER, SystemControllerCommand.GET_BUILD_INFO, request, pb2.SushiBuildInfo)

    def GetInputAudioChannelCount(self, request):
        return self._call(Service.SYSTEM_CONTROLLER, SystemControllerCommand.GET_INPUT_AUDIO_CHANNEL_COUNT, request, pb2.GenericIntValue)

    def GetOutputAudioChannelCount(self, request):
        return self._call(Service.SYSTEM_CONTROLLER, SystemControllerCommand.GET_OUTPUT_AUDIO_CHANNEL_COUNT, request, pb2.GenericIntValue)

    # ── TransportController ───────────────────────────────────────────────────

    def GetSamplerate(self, request):
        return self._call(Service.TRANSPORT_CONTROLLER, TransportControllerCommand.GET_SAMPLERATE, request, pb2.GenericFloatValue)

    def GetPlayingMode(self, request):
        return self._call(Service.TRANSPORT_CONTROLLER, TransportControllerCommand.GET_PLAYING_MODE, request, pb2.PlayingMode)

    def GetSyncMode(self, request):
        return self._call(Service.TRANSPORT_CONTROLLER, TransportControllerCommand.GET_SYNC_MODE, request, pb2.SyncMode)

    def GetTimeSignature(self, request):
        return self._call(Service.TRANSPORT_CONTROLLER, TransportControllerCommand.GET_TIME_SIGNATURE, request, pb2.TimeSignature)

    def GetTempo(self, request):
        return self._call(Service.TRANSPORT_CONTROLLER, TransportControllerCommand.GET_TEMPO, request, pb2.GenericFloatValue)

    def SetTempo(self, request):
        return self._call(Service.TRANSPORT_CONTROLLER, TransportControllerCommand.SET_TEMPO, request, pb2.CommandResponse)

    def SetPlayingMode(self, request):
        return self._call(Service.TRANSPORT_CONTROLLER, TransportControllerCommand.SET_PLAYING_MODE, request, pb2.CommandResponse)

    def SetSyncMode(self, request):
        return self._call(Service.TRANSPORT_CONTROLLER, TransportControllerCommand.SET_SYNC_MODE, request, pb2.CommandResponse)

    def SetTimeSignature(self, request):
        return self._call(Service.TRANSPORT_CONTROLLER, TransportControllerCommand.SET_TIME_SIGNATURE, request, pb2.CommandResponse)

    # ── TimingController ──────────────────────────────────────────────────────

    def GetTimingsEnabled(self, request):
        return self._call(Service.TIMING_CONTROLLER, TimingControllerCommand.GET_TIMINGS_ENABLED, request, pb2.GenericBoolValue)

    def SetTimingsEnabled(self, request):
        return self._call(Service.TIMING_CONTROLLER, TimingControllerCommand.SET_TIMINGS_ENABLED, request, pb2.CommandResponse)

    def GetEngineTimings(self, request):
        return self._call(Service.TIMING_CONTROLLER, TimingControllerCommand.GET_ENGINE_TIMINGS, request, pb2.CpuTimings)

    def GetTrackTimings(self, request):
        return self._call(Service.TIMING_CONTROLLER, TimingControllerCommand.GET_TRACK_TIMINGS, request, pb2.TimingResponse)

    def GetProcessorTimings(self, request):
        return self._call(Service.TIMING_CONTROLLER, TimingControllerCommand.GET_PROCESSOR_TIMINGS, request, pb2.TimingResponse)

    def ResetAllTimings(self, request):
        return self._call(Service.TIMING_CONTROLLER, TimingControllerCommand.RESET_ALL_TIMINGS, request, pb2.CommandResponse)

    def ResetTrackTimings(self, request):
        return self._call(Service.TIMING_CONTROLLER, TimingControllerCommand.RESET_TRACK_TIMINGS, request, pb2.CommandResponse)

    def ResetProcessorTimings(self, request):
        return self._call(Service.TIMING_CONTROLLER, TimingControllerCommand.RESET_PROCESSOR_TIMINGS, request, pb2.CommandResponse)

    # ── KeyboardController ────────────────────────────────────────────────────

    def SendNoteOn(self, request):
        return self._call(Service.KEYBOARD_CONTROLLER, KeyboardControllerCommand.SEND_NOTE_ON, request, pb2.CommandResponse)

    def SendNoteOff(self, request):
        return self._call(Service.KEYBOARD_CONTROLLER, KeyboardControllerCommand.SEND_NOTE_OFF, request, pb2.CommandResponse)

    def SendNoteAftertouch(self, request):
        return self._call(Service.KEYBOARD_CONTROLLER, KeyboardControllerCommand.SEND_NOTE_AFTERTOUCH, request, pb2.CommandResponse)

    def SendAftertouch(self, request):
        return self._call(Service.KEYBOARD_CONTROLLER, KeyboardControllerCommand.SEND_AFTERTOUCH, request, pb2.CommandResponse)

    def SendPitchBend(self, request):
        return self._call(Service.KEYBOARD_CONTROLLER, KeyboardControllerCommand.SEND_PITCH_BEND, request, pb2.CommandResponse)

    def SendModulation(self, request):
        return self._call(Service.KEYBOARD_CONTROLLER, KeyboardControllerCommand.SEND_MODULATION, request, pb2.CommandResponse)

    # ── AudioGraphController ──────────────────────────────────────────────────

    def GetAllProcessors(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.GET_ALL_PROCESSORS, request, pb2.ProcessorInfoList)

    def GetAllTracks(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.GET_ALL_TRACKS, request, pb2.TrackInfoList)

    def GetTrackId(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.GET_TRACK_ID, request, pb2.TrackIdentifierResponse)

    def GetTrackInfo(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.GET_TRACK_INFO, request, pb2.TrackInfoResponse)

    def GetTrackProcessors(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.GET_TRACK_PROCESSORS, request, pb2.ProcessorInfoListResponse)

    def GetProcessorId(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.GET_PROCESSOR_ID, request, pb2.ProcessorIdentifierResponse)

    def GetProcessorInfo(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.GET_PROCESSOR_INFO, request, pb2.ProcessorInfoResponse)

    def GetProcessorBypassState(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.GET_PROCESSOR_BYPASS_STATE, request, pb2.BoolResponse)

    def GetProcessorState(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.GET_PROCESSOR_STATE, request, pb2.ProcessorStateResponse)

    def SetProcessorBypassState(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.SET_PROCESSOR_BYPASS_STATE, request, pb2.CommandResponse)

    def SetProcessorState(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.SET_PROCESSOR_STATE, request, pb2.CommandResponse)

    def CreateTrack(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.CREATE_TRACK, request, pb2.CommandResponse)

    def CreateMultibusTrack(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.CREATE_MULTIBUS_TRACK, request, pb2.CommandResponse)

    def CreatePreTrack(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.CREATE_PRE_TRACK, request, pb2.CommandResponse)

    def CreatePostTrack(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.CREATE_POST_TRACK, request, pb2.CommandResponse)

    def CreateProcessorOnTrack(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.CREATE_PROCESSOR_ON_TRACK, request, pb2.CommandResponse)

    def MoveProcessorOnTrack(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.MOVE_PROCESSOR_ON_TRACK, request, pb2.CommandResponse)

    def DeleteProcessorFromTrack(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.DELETE_PROCESSOR_FROM_TRACK, request, pb2.CommandResponse)

    def DeleteTrack(self, request):
        return self._call(Service.AUDIO_GRAPH_CONTROLLER, AudioGraphControllerCommand.DELETE_TRACK, request, pb2.CommandResponse)

    # ── ProgramController ─────────────────────────────────────────────────────

    def GetProcessorCurrentProgram(self, request):
        return self._call(Service.PROGRAM_CONTROLLER, ProgramControllerCommand.GET_PROCESSOR_CURRENT_PROGRAM, request, pb2.ProgramIdentifierResponse)

    def GetProcessorCurrentProgramName(self, request):
        return self._call(Service.PROGRAM_CONTROLLER, ProgramControllerCommand.GET_PROCESSOR_CURRENT_PROGRAM_NAME, request, pb2.StringResponse)

    def GetProcessorProgramName(self, request):
        return self._call(Service.PROGRAM_CONTROLLER, ProgramControllerCommand.GET_PROCESSOR_PROGRAM_NAME, request, pb2.StringResponse)

    def GetProcessorPrograms(self, request):
        return self._call(Service.PROGRAM_CONTROLLER, ProgramControllerCommand.GET_PROCESSOR_PROGRAMS, request, pb2.ProgramInfoListResponse)

    def SetProcessorProgram(self, request):
        return self._call(Service.PROGRAM_CONTROLLER, ProgramControllerCommand.SET_PROCESSOR_PROGRAM, request, pb2.CommandResponse)

    # ── ParameterController ───────────────────────────────────────────────────

    def GetTrackParameters(self, request):
        return self._call(Service.PARAMETER_CONTROLLER, ParameterControllerCommand.GET_TRACK_PARAMETERS, request, pb2.ParameterInfoListResponse)

    def GetProcessorParameters(self, request):
        return self._call(Service.PARAMETER_CONTROLLER, ParameterControllerCommand.GET_PROCESSOR_PARAMETERS, request, pb2.ParameterInfoListResponse)

    def GetParameterId(self, request):
        return self._call(Service.PARAMETER_CONTROLLER, ParameterControllerCommand.GET_PARAMETER_ID, request, pb2.ParameterIdentifierResponse)

    def GetParameterInfo(self, request):
        return self._call(Service.PARAMETER_CONTROLLER, ParameterControllerCommand.GET_PARAMETER_INFO, request, pb2.ParameterInfoResponse)

    def GetParameterValue(self, request):
        return self._call(Service.PARAMETER_CONTROLLER, ParameterControllerCommand.GET_PARAMETER_VALUE, request, pb2.FloatResponse)

    def GetParameterValueInDomain(self, request):
        return self._call(Service.PARAMETER_CONTROLLER, ParameterControllerCommand.GET_PARAMETER_VALUE_IN_DOMAIN, request, pb2.FloatResponse)

    def GetParameterValueAsString(self, request):
        return self._call(Service.PARAMETER_CONTROLLER, ParameterControllerCommand.GET_PARAMETER_VALUE_AS_STRING, request, pb2.StringResponse)

    def SetParameterValue(self, request):
        return self._call(Service.PARAMETER_CONTROLLER, ParameterControllerCommand.SET_PARAMETER_VALUE, request, pb2.CommandResponse)

    def GetTrackProperties(self, request):
        return self._call(Service.PARAMETER_CONTROLLER, ParameterControllerCommand.GET_TRACK_PROPERTIES, request, pb2.PropertyInfoListResponse)

    def GetProcessorProperties(self, request):
        return self._call(Service.PARAMETER_CONTROLLER, ParameterControllerCommand.GET_PROCESSOR_PROPERTIES, request, pb2.PropertyInfoListResponse)

    def GetPropertyId(self, request):
        return self._call(Service.PARAMETER_CONTROLLER, ParameterControllerCommand.GET_PROPERTY_ID, request, pb2.PropertyIdentifierResponse)

    def GetPropertyInfo(self, request):
        return self._call(Service.PARAMETER_CONTROLLER, ParameterControllerCommand.GET_PROPERTY_INFO, request, pb2.PropertyInfoResponse)

    def GetPropertyValue(self, request):
        return self._call(Service.PARAMETER_CONTROLLER, ParameterControllerCommand.GET_PROPERTY_VALUE, request, pb2.StringResponse)

    def SetPropertyValue(self, request):
        return self._call(Service.PARAMETER_CONTROLLER, ParameterControllerCommand.SET_PROPERTY_VALUE, request, pb2.CommandResponse)

    # ── MidiController ────────────────────────────────────────────────────────

    def GetInputPorts(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.GET_INPUT_PORTS, request, pb2.GenericIntValue)

    def GetOutputPorts(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.GET_OUTPUT_PORTS, request, pb2.GenericIntValue)

    def GetAllKbdInputConnections(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.GET_ALL_KBD_INPUT_CONNECTIONS, request, pb2.MidiKbdConnectionList)

    def GetAllKbdOutputConnections(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.GET_ALL_KBD_OUTPUT_CONNECTIONS, request, pb2.MidiKbdConnectionList)

    def GetAllCCInputConnections(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.GET_ALL_C_C_INPUT_CONNECTIONS, request, pb2.MidiCCConnectionList)

    def GetAllPCInputConnections(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.GET_ALL_P_C_INPUT_CONNECTIONS, request, pb2.MidiPCConnectionList)

    def GetCCInputConnectionsForProcessor(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.GET_C_C_INPUT_CONNECTIONS_FOR_PROCESSOR, request, pb2.MidiCCConnectionListResponse)

    def GetPCInputConnectionsForProcessor(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.GET_P_C_INPUT_CONNECTIONS_FOR_PROCESSOR, request, pb2.MidiPCConnectionListResponse)

    def GetMidiClockOutputEnabled(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.GET_MIDI_CLOCK_OUTPUT_ENABLED, request, pb2.GenericBoolValue)

    def SetMidiClockOutputEnabled(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.SET_MIDI_CLOCK_OUTPUT_ENABLED, request, pb2.CommandResponse)

    def ConnectKbdInputToTrack(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.CONNECT_KBD_INPUT_TO_TRACK, request, pb2.CommandResponse)

    def ConnectKbdOutputFromTrack(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.CONNECT_KBD_OUTPUT_FROM_TRACK, request, pb2.CommandResponse)

    def ConnectCCToParameter(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.CONNECT_C_C_TO_PARAMETER, request, pb2.CommandResponse)

    def ConnectPCToProcessor(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.CONNECT_P_C_TO_PROCESSOR, request, pb2.CommandResponse)

    def DisconnectKbdInput(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.DISCONNECT_KBD_INPUT, request, pb2.CommandResponse)

    def DisconnectKbdOutput(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.DISCONNECT_KBD_OUTPUT, request, pb2.CommandResponse)

    def DisconnectCC(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.DISCONNECT_C_C, request, pb2.CommandResponse)

    def DisconnectPC(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.DISCONNECT_P_C, request, pb2.CommandResponse)

    def DisconnectAllCCFromProcessor(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.DISCONNECT_ALL_C_C_FROM_PROCESSOR, request, pb2.CommandResponse)

    def DisconnectAllPCFromProcessor(self, request):
        return self._call(Service.MIDI_CONTROLLER, MidiControllerCommand.DISCONNECT_ALL_P_C_FROM_PROCESSOR, request, pb2.CommandResponse)

    # ── AudioRoutingController ────────────────────────────────────────────────

    def GetAllInputConnections(self, request):
        return self._call(Service.AUDIO_ROUTING_CONTROLLER, AudioRoutingControllerCommand.GET_ALL_INPUT_CONNECTIONS, request, pb2.AudioConnectionList)

    def GetAllOutputConnections(self, request):
        return self._call(Service.AUDIO_ROUTING_CONTROLLER, AudioRoutingControllerCommand.GET_ALL_OUTPUT_CONNECTIONS, request, pb2.AudioConnectionList)

    def GetInputConnectionsForTrack(self, request):
        return self._call(Service.AUDIO_ROUTING_CONTROLLER, AudioRoutingControllerCommand.GET_INPUT_CONNECTIONS_FOR_TRACK, request, pb2.AudioConnectionListResponse)

    def GetOutputConnectionsForTrack(self, request):
        return self._call(Service.AUDIO_ROUTING_CONTROLLER, AudioRoutingControllerCommand.GET_OUTPUT_CONNECTIONS_FOR_TRACK, request, pb2.AudioConnectionListResponse)

    def ConnectInputChannelToTrack(self, request):
        return self._call(Service.AUDIO_ROUTING_CONTROLLER, AudioRoutingControllerCommand.CONNECT_INPUT_CHANNEL_TO_TRACK, request, pb2.CommandResponse)

    def ConnectOutputChannelFromTrack(self, request):
        return self._call(Service.AUDIO_ROUTING_CONTROLLER, AudioRoutingControllerCommand.CONNECT_OUTPUT_CHANNEL_FROM_TRACK, request, pb2.CommandResponse)

    def DisconnectInput(self, request):
        return self._call(Service.AUDIO_ROUTING_CONTROLLER, AudioRoutingControllerCommand.DISCONNECT_INPUT, request, pb2.CommandResponse)

    def DisconnectOutput(self, request):
        return self._call(Service.AUDIO_ROUTING_CONTROLLER, AudioRoutingControllerCommand.DISCONNECT_OUTPUT, request, pb2.CommandResponse)

    def DisconnectAllInputsFromTrack(self, request):
        return self._call(Service.AUDIO_ROUTING_CONTROLLER, AudioRoutingControllerCommand.DISCONNECT_ALL_INPUTS_FROM_TRACK, request, pb2.CommandResponse)

    def DisconnectAllOutputFromTrack(self, request):
        return self._call(Service.AUDIO_ROUTING_CONTROLLER, AudioRoutingControllerCommand.DISCONNECT_ALL_OUTPUT_FROM_TRACK, request, pb2.GenericVoidValue)

    def DisconnectAllOutputsFromTrack(self, request):
        return self._call(Service.AUDIO_ROUTING_CONTROLLER, AudioRoutingControllerCommand.DISCONNECT_ALL_OUTPUTS_FROM_TRACK, request, pb2.CommandResponse)

    # ── CvGateController ──────────────────────────────────────────────────────

    def GetCvInputChannelCount(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.GET_CV_INPUT_CHANNEL_COUNT, request, pb2.GenericIntValue)

    def GetCvOutputChannelCount(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.GET_CV_OUTPUT_CHANNEL_COUNT, request, pb2.GenericIntValue)

    def GetAllCvInputConnections(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.GET_ALL_CV_INPUT_CONNECTIONS, request, pb2.CvConnectionList)

    def GetAllCvOutputConnections(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.GET_ALL_CV_OUTPUT_CONNECTIONS, request, pb2.CvConnectionList)

    def GetAllGateInputConnections(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.GET_ALL_GATE_INPUT_CONNECTIONS, request, pb2.GateConnectionList)

    def GetAllGateOutputConnections(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.GET_ALL_GATE_OUTPUT_CONNECTIONS, request, pb2.GateConnectionList)

    def GetCvInputConnectionsForProcessor(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.GET_CV_INPUT_CONNECTIONS_FOR_PROCESSOR, request, pb2.CvConnectionListResponse)

    def GetCvOutputConnectionsForProcessor(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.GET_CV_OUTPUT_CONNECTIONS_FOR_PROCESSOR, request, pb2.CvConnectionListResponse)

    def GetGateInputConnectionsForProcessor(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.GET_GATE_INPUT_CONNECTIONS_FOR_PROCESSOR, request, pb2.GateConnectionListResponse)

    def GetGateOutputConnectionsForProcessor(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.GET_GATE_OUTPUT_CONNECTIONS_FOR_PROCESSOR, request, pb2.GateConnectionListResponse)

    def ConnectCvInputToParameter(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.CONNECT_CV_INPUT_TO_PARAMETER, request, pb2.CommandResponse)

    def ConnectCvOutputFromParameter(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.CONNECT_CV_OUTPUT_FROM_PARAMETER, request, pb2.CommandResponse)

    def ConnectGateInputToProcessor(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.CONNECT_GATE_INPUT_TO_PROCESSOR, request, pb2.CommandResponse)

    def ConnectGateOutputFromProcessor(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.CONNECT_GATE_OUTPUT_FROM_PROCESSOR, request, pb2.CommandResponse)

    def DisconnectCvInput(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.DISCONNECT_CV_INPUT, request, pb2.CommandResponse)

    def DisconnectCvOutput(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.DISCONNECT_CV_OUTPUT, request, pb2.CommandResponse)

    def DisconnectGateInput(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.DISCONNECT_GATE_INPUT, request, pb2.CommandResponse)

    def DisconnectGateOutput(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.DISCONNECT_GATE_OUTPUT, request, pb2.CommandResponse)

    def DisconnectAllCvInputsFromProcessor(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.DISCONNECT_ALL_CV_INPUTS_FROM_PROCESSOR, request, pb2.CommandResponse)

    def DisconnectAllCvOutputsFromProcessor(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.DISCONNECT_ALL_CV_OUTPUTS_FROM_PROCESSOR, request, pb2.CommandResponse)

    def DisconnectAllGateInputsFromProcessor(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.DISCONNECT_ALL_GATE_INPUTS_FROM_PROCESSOR, request, pb2.CommandResponse)

    def DisconnectAllGateOutputsFromProcessor(self, request):
        return self._call(Service.CV_GATE_CONTROLLER, CvGateControllerCommand.DISCONNECT_ALL_GATE_OUTPUTS_FROM_PROCESSOR, request, pb2.CommandResponse)

    # ── OscController ─────────────────────────────────────────────────────────

    def GetSendIP(self, request):
        return self._call(Service.OSC_CONTROLLER, OscControllerCommand.GET_SEND_I_P, request, pb2.GenericStringValue)

    def GetSendPort(self, request):
        return self._call(Service.OSC_CONTROLLER, OscControllerCommand.GET_SEND_PORT, request, pb2.GenericIntValue)

    def GetReceivePort(self, request):
        return self._call(Service.OSC_CONTROLLER, OscControllerCommand.GET_RECEIVE_PORT, request, pb2.GenericIntValue)

    def GetEnabledParameterOutputs(self, request):
        return self._call(Service.OSC_CONTROLLER, OscControllerCommand.GET_ENABLED_PARAMETER_OUTPUTS, request, pb2.OscParameterOutputList)

    def EnableOutputForParameter(self, request):
        return self._call(Service.OSC_CONTROLLER, OscControllerCommand.ENABLE_OUTPUT_FOR_PARAMETER, request, pb2.CommandResponse)

    def DisableOutputForParameter(self, request):
        return self._call(Service.OSC_CONTROLLER, OscControllerCommand.DISABLE_OUTPUT_FOR_PARAMETER, request, pb2.CommandResponse)

    def EnableAllOutput(self, request):
        return self._call(Service.OSC_CONTROLLER, OscControllerCommand.ENABLE_ALL_OUTPUT, request, pb2.CommandResponse)

    def DisableAllOutput(self, request):
        return self._call(Service.OSC_CONTROLLER, OscControllerCommand.DISABLE_ALL_OUTPUT, request, pb2.CommandResponse)

    # ── SessionController ─────────────────────────────────────────────────────

    def SaveSession(self, request):
        return self._call(Service.SESSION_CONTROLLER, SessionControllerCommand.SAVE_SESSION, request, pb2.SessionState)

    def RestoreSession(self, request):
        return self._call(Service.SESSION_CONTROLLER, SessionControllerCommand.RESTORE_SESSION, request, pb2.CommandResponse)

    # ── NotificationController ────────────────────────────────────────────────

    def SubscribeToTransportChanges(self, request):
        return self._call(Service.NOTIFICATION_CONTROLLER, NotificationControllerCommand.SUBSCRIBE_TO_TRANSPORT_CHANGES, request, pb2.CommandStatus)

    def SubscribeToEngineCpuTimingUpdates(self, request):
        return self._call(Service.NOTIFICATION_CONTROLLER, NotificationControllerCommand.SUBSCRIBE_TO_ENGINE_CPU_TIMING_UPDATES, request, pb2.CommandStatus)

    def SubscribeToTrackChanges(self, request):
        return self._call(Service.NOTIFICATION_CONTROLLER, NotificationControllerCommand.SUBSCRIBE_TO_TRACK_CHANGES, request, pb2.CommandStatus)

    def SubscribeToProcessorChanges(self, request):
        return self._call(Service.NOTIFICATION_CONTROLLER, NotificationControllerCommand.SUBSCRIBE_TO_PROCESSOR_CHANGES, request, pb2.CommandStatus)

    def SubscribeToParameterUpdates(self, request):
        return self._call(Service.NOTIFICATION_CONTROLLER, NotificationControllerCommand.SUBSCRIBE_TO_PARAMETER_UPDATES, request, pb2.CommandStatus)

    def SubscribeToPropertyUpdates(self, request):
        return self._call(Service.NOTIFICATION_CONTROLLER, NotificationControllerCommand.SUBSCRIBE_TO_PROPERTY_UPDATES, request, pb2.CommandStatus)

    def SubscribeToAsyncCommandUpdates(self, request):
        return self._call(Service.NOTIFICATION_CONTROLLER, NotificationControllerCommand.SUBSCRIBE_TO_ASYNC_COMMAND_UPDATES, request, pb2.CommandStatus)
