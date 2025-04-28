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

from enum import IntEnum
from types import ModuleType

################
# Custom Enums #
################


class CommandResponseStatus(IntEnum):
    """
    Enum class to hold the values matching the different status code in Command Responses.

    Attributes:
        SUCCESS
        ASYNC_RESPONSE
        ERROR
        UNSUPPORTED_OPERATION
        NOT_FOUND
        OUT_OF_RANGE
        INVALID_ARGUMENTS
    """

    SUCCESS = 1
    ASYNC_RESPONSE = 2
    ERROR = 3
    UNSUPPORTED_OPERATION = 4
    NOT_FOUND = 5
    OUT_OF_RANGE = 6
    INVALID_ARGUMENTS = 7


class PlayingMode(IntEnum):
    """
    Enum class to hold the values matching the different playing modes.

    Attributes:
        STOPPED,
        PLAYING,
        RECORDING
    """

    STOPPED = 1
    PLAYING = 2
    RECORDING = 3


class SyncMode(IntEnum):
    """
    Enum class to hold the values matching the different sync modes.

    Attributes:
        INTERNAL,
        MIDI,
        LINK
    """

    INTERNAL = 1
    MIDI = 2
    LINK = 3


class ParameterType(IntEnum):
    """
    Enum class to hold the values matching the different parameter types.

    Attributes:
        BOOL,
        INT,
        FLOAT,
        STRING_PROPERTY,
        DATA_PROPERTY
    """

    BOOL = 1
    INT = 2
    FLOAT = 3
    STRING_PROPERTY = 4
    DATA_PROPERTY = 5


class PluginType(IntEnum):
    """
    Enum class to hold the values matching the different plugin types.

    Attributes:
        INTERNAL,
        VST2X,
        VST3X,
        LV2
    """

    INTERNAL = 1
    VST2X = 2
    VST3X = 3
    LV2 = 4


class TrackType(IntEnum):
    """
    Enum class to hold the type of track

    Attributes:
        REGULAR,
        PRE,
        POST
    """

    REGULAR = 1
    PRE = 2
    POST = 3


################
# Info Classes #
################


class SushiBuildInfo:
    """
    Class to represent build info from sushi in a clear way

    Attributes:
        version (str): The sushi version
        build_options (List[str]) : A list of build options
        audio_buffer_size (int) : The buffer size used when building sushi
        commit_hash (str) : Commit hash of the build
        build_date (str) : The date sushi was built
    """

    def __init__(self, grpc_SushiBuildInfo: ModuleType) -> None:
        try:
            self.version = grpc_SushiBuildInfo.version
        except AttributeError:
            self._version = ""

        try:
            self.build_options = grpc_SushiBuildInfo.build_options
        except AttributeError:
            self.build_options = [""]

        try:
            self.audio_buffer_size = grpc_SushiBuildInfo.audio_buffer_size
        except AttributeError:
            self.audio_buffer_size = -1

        try:
            self.commit_hash = grpc_SushiBuildInfo.commit_hash
        except AttributeError:
            self.commit_hash = ""

        try:
            self.build_date = grpc_SushiBuildInfo.build_date
        except AttributeError:
            self.build_date = "1-1-1970"

    def __str__(self) -> str:
        s = "{\n"
        s += " version: %s \n" % self.version
        s += " build options: %s \n" % self.build_options
        s += " audio buffer size: %s \n" % self.audio_buffer_size
        s += " commit hash: %s \n" % self.commit_hash
        s += " build date: %s \n" % self.build_date
        s += "}"
        return s

    def __eq__(self, other):
        return (
            self.version == other.version
            and self.build_options == other.build_options
            and self.audio_buffer_size == other.audio_buffer_size
            and self.commit_hash == other.commit_hash
            and self.build_date == other.build_date
        )


class ParameterInfo:
    """
    Class to represent the parameter info received from sushi in a clear way.

    Attributes:
        id (int): The id of the parameter.
        type (str): The type of the parameter.
        label (str): The label of the parameter.
        name (str): The name of the parameter.
        unit (str): The unit of the parameter.
        automatable (bool): If the parameter is automatable or not.
        min_domain_value (float): The minimum value of the parameter.
        max_domain_value (float): The maximum value of the parameter.
    """

    def __init__(self, grpc_ParameterInfo):
        """
        The constructor of the ParameterInfo class.

        Parameters:
            grpc_ParameterInfo (sushi_rpc_pb2.ParameterInfo): the gRPC parameter info object to get the data from.
        """
        try:
            self.id = grpc_ParameterInfo.id
        except AttributeError:
            self.id = 0

        try:
            self.type = ParameterType(grpc_ParameterInfo.type.type)
        except AttributeError:
            self.type = "DUMMY"

        try:
            self.label = grpc_ParameterInfo.label
        except AttributeError:
            self.label = ""

        try:
            self.name = grpc_ParameterInfo.name
        except AttributeError:
            self.name = ""

        try:
            self.unit = grpc_ParameterInfo.unit
        except AttributeError:
            self.unit = ""

        try:
            self.automatable = grpc_ParameterInfo.automatable
        except AttributeError:
            self.automatable = False

        try:
            self.min_domain_value = grpc_ParameterInfo.min_domain_value
        except AttributeError:
            self.min_domain_value = 0.0

        try:
            self.max_domain_value = grpc_ParameterInfo.max_domain_value
        except AttributeError:
            self.max_domain_value = 0.0

    def __str__(self):
        s = "{\n"
        s += " id: %s \n" % self.id
        s += " type: %s \n" % self.type
        s += " label: %s \n" % self.label
        s += " name: %s \n" % self.name
        s += " unit: %s \n" % self.unit
        s += " automatable: %s \n" % self.automatable
        s += " min_domain_value: %s \n" % self.min_domain_value
        s += " max_domain_value: %s \n" % self.max_domain_value
        s += "}"
        return s

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.type == other.type
            and self.label == other.label
            and self.name == other.name
            and self.unit == other.unit
            and self.automatable == other.automatable
            and self.min_domain_value == other.min_domain_value
            and self.max_domain_value == other.max_domain_value
        )


class PropertyInfo:
    """
    Class to represent the property info received from sushi in a clear way.

    Attributes:
        id (int): The id of the property.
        label (str): The label of the property.
        name (str): The name of the property.
    """

    def __init__(self, grpc_PropertyInfo):
        """
        The constructor of the PropertyInfo class.

        Parameters:
            grpc_PropertyInfo (sushi_rpc_pb2.PropertyInfo): the gRPC parameter info object to get the data from.
        """
        try:
            self.id = grpc_PropertyInfo.id
        except AttributeError:
            self.id = 0

        try:
            self.label = grpc_PropertyInfo.label
        except AttributeError:
            self.label = ""

        try:
            self.name = grpc_PropertyInfo.name
        except AttributeError:
            self.name = ""

    def __str__(self):
        s = "{\n"
        s += " id: %s \n" % self.id
        s += " label: %s \n" % self.label
        s += " name: %s \n" % self.name
        s += "}"
        return s

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.label == other.label
            and self.name == other.name
        )


class ProcessorInfo:
    """
    Class to represent the processor info received from sushi in a clear way.

    Attributes:
        id (int): The id of the processor.
        label (str): The label of the processor.
        name (str): The name of the processor.
        parameter_count (int): The number of parameters available to the processor.
        program_count (int): The number of programs available to the processor.
    """

    def __init__(self, grpc_ProcessorInfo):
        try:
            self.id = grpc_ProcessorInfo.id
        except AttributeError:
            self.id = 0

        try:
            self.label = grpc_ProcessorInfo.label
        except AttributeError:
            self.label = ""

        try:
            self.name = grpc_ProcessorInfo.name
        except AttributeError:
            self.name = ""

        try:
            self.parameter_count = grpc_ProcessorInfo.parameter_count
        except AttributeError:
            self.parameter_count = 0

        try:
            self.program_count = grpc_ProcessorInfo.program_count
        except AttributeError:
            self.program_count = 0

    def __str__(self):
        s = "{\n"
        s += " id: %s \n" % self.id
        s += " label: %s \n" % self.label
        s += " name: %s \n" % self.name
        s += " parameter count: %s \n" % self.parameter_count
        s += " program count: %s \n" % self.program_count
        s += "}"
        return s

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.label == other.label
            and self.name == other.name
            and self.parameter_count == other.parameter_count
            and self.program_count == other.program_count
        )


class TrackInfo:
    """
    Class to represent the track info received from sushi in a clear way.

    Attributes:
        id (int): The id of the track.
        label (str): The label of the track.
        name (str): The name of the track.
        channels (int): The number of input channels available to the track.
        buses (int): The number input buses available to the track.
        type (TrackType): The type of track
    """

    def __init__(self, grpc_TrackInfo):
        try:
            self.id = grpc_TrackInfo.id
        except AttributeError:
            self.id = 0

        try:
            self.label = grpc_TrackInfo.label
        except AttributeError:
            self.label = ""

        try:
            self.name = grpc_TrackInfo.name
        except AttributeError:
            self.name = ""

        try:
            self.channels = grpc_TrackInfo.channels
        except AttributeError:
            self.channels = 0

        try:
            self.buses = grpc_TrackInfo.buses
        except AttributeError:
            self.buses = 0

        try:
            self.type = TrackType(grpc_TrackInfo.type.type)
        except Exception:
            self.type = TrackType.REGULAR

        try:
            self.processors = []
            for processor in grpc_TrackInfo.processors:
                self.processors.append(processor.id)
        except AttributeError:
            self.processors = []

    def __str__(self):
        s = "{\n"
        s += " id: %s \n" % self.id
        s += " label: %s \n" % self.label
        s += " name: %s \n" % self.name
        s += " channels: %s \n" % self.channels
        s += " buses: %s \n" % self.buses
        s += " type: %s \n" % self.type
        s += " processors: %s \n" % self.processors
        s += "}"
        return s

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.label == other.label
            and self.name == other.name
            and self.channels == other.channels
            and self.buses == other.buses
            and self.type == other.type
            and self.processors == other.processors
        )


class ProgramInfo:
    """
    Class to represent the program info received from sushi in a clear way.

    Attributes:
        id (int): The id of the program.
        name (str): The name of the program.
    """

    def __init__(self, grpc_ProgramInfo):
        try:
            self.id = grpc_ProgramInfo.id.program
        except AttributeError:
            self.id = 0

        try:
            self.name = grpc_ProgramInfo.name
        except AttributeError:
            self.name = ""

    def __str__(self):
        s = "{ \n"
        s += " id: %s \n" % self.id
        s += " name: %s \n" % self.name
        s += "}"
        return s

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name


class ProcessorState:
    """
    Class to represent the processor state info received from sushi in a clear way.

    Attributes:
        program_id (int): The id of the current program.
        bypassed (bool): Whether the processor is currently bypassed or not.
        properties ((int, str)): All property values of the processor.
        parameters ((int, float)): All parameter values of the processor.
        binary_data (bytes): Opaque binary data saved by the plugin.
    """

    def __init__(self, grpc_ProcessorState):
        try:
            self.program_id = grpc_ProcessorState.program_id.value
        except AttributeError:
            self.program_id = None

        try:
            self.bypassed = grpc_ProcessorState.bypassed.value
        except AttributeError:
            self.bypassed = None

        try:
            self.properties = []
            for property in grpc_ProcessorState.properties:
                self.properties.append((property.property.id, property.value))
        except AttributeError:
            self.properties = []

        try:
            self.parameters = []
            for parameter in grpc_ProcessorState.parameters:
                self.parameters.append(
                    (parameter.parameter.parameter_id, parameter.value)
                )
        except AttributeError:
            self.parameters = []

        try:
            self.binary_data = grpc_ProcessorState.binary_data
        except AttributeError:
            self.binary_data = bytes()

    def __str__(self):
        s = "{\n"
        s += " program_id: %s \n" % self.program_id
        s += " bypassed: %s \n" % self.bypassed
        s += " properties: %s \n" % self.properties
        s += " parameters: %s \n" % self.parameters
        s += " binary_data: %s \n" % self.binary_data
        s += "}"
        return s

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.program_id == other.program_id
            and self.bypassed == other.bypassed
            and self.properties == other.properties
            and self.parameters == other.parameters
            and self.binary_data == other.binary_data
        )


class AudioConnection:
    """
    Class to represent an audio connection info received from Sushi in a cleaner way.

    Attributes:
        track (TrackIdentifier): an int
        track_channel (int):
        engine_channel (int):
    """

    def __init__(self, grpc_AudioConnection):
        try:
            self.track = grpc_AudioConnection.track.id
        except AttributeError:
            self.track = 0

        try:
            self.track_channel = grpc_AudioConnection.track_channel
        except AttributeError:
            self.track_channel = 0

        try:
            self.engine_channel = grpc_AudioConnection.engine_channel
        except AttributeError:
            self.engine_channel = 0

    def __str__(self):
        return (
            f"{{ \n track: {self.track}\n"
            f" track_channel: {self.track_channel}\n"
            f" engine_channel: {self.engine_channel}\n}}"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.track == other.track
            and self.track_channel == other.track_channel
            and self.engine_channel == other.engine_channel
        )


class MidiKbdConnection:
    """
    Class to represent a MIDI keyboard connection in Sushi in a cleaner way.

    Attributes:
        track (_sushi_proto.TrackIdentifier): a track id
        channel (_sushi_proto.MidiChannel): a MIDI channel
        port (int): a MIDI port number
        raw_midi (bool): is this track a raw MIDI track or not.
    """

    def __init__(self, grpc_MidiKbdConnection):
        try:
            self.track = grpc_MidiKbdConnection.track.id
        except AttributeError:
            self.track = 0

        try:
            self.channel = grpc_MidiKbdConnection.channel.channel
        except AttributeError:
            self.channel = 0

        try:
            self.port = grpc_MidiKbdConnection.port
        except AttributeError:
            self.port = 0

        try:
            self.raw_midi = grpc_MidiKbdConnection.raw_midi
        except AttributeError:
            self.raw_midi = False

    def __str__(self):
        return (
            f"{{\n track: {self.track}\n"
            f" channel: {self.channel}\n"
            f" port: {self.port}\n"
            f" raw_midi: {self.raw_midi}\n}}"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.track == other.track
            and self.channel == other.channel
            and self.port == other.port
            and self.raw_midi == other.raw_midi
        )


class MidiCCConnection:
    """
    Class to represent a MIDI Continious Controller connection in Sushi in a cleaner way.

    Attributes:
        parameter_id (_sushi_proto.ParameterIdentifier):
        channel (MidiChannel)
        port (int)
        cc_number (int)
        min_range (float)
        max_range (float)
        relative_mode (bool)
    """

    def __init__(self, grpc_MidiCCConnection):
        try:
            self.processor_id = grpc_MidiCCConnection.parameter.processor_id
        except AttributeError:
            self.processor_id = 0

        try:
            self.parameter_id = grpc_MidiCCConnection.parameter.parameter_id
        except AttributeError:
            self.parameter_id = 0

        try:
            self.channel = grpc_MidiCCConnection.channel.channel
        except AttributeError:
            self.channel = 0

        try:
            self.port = grpc_MidiCCConnection.port
        except AttributeError:
            self.port = 0

        try:
            self.cc_number = grpc_MidiCCConnection.cc_number
        except AttributeError:
            self.cc_number = 0

        try:
            self.min_range = grpc_MidiCCConnection.min_range
        except AttributeError:
            self.min_range = 0.0

        try:
            self.max_range = grpc_MidiCCConnection.max_range
        except AttributeError:
            self.max_range = 0.0

        try:
            self.relative_mode = grpc_MidiCCConnection.relative_mode
        except AttributeError:
            self.relative_mode = False

    def __str__(self):
        return (
            f"{{\n parameter: {self.parameter_id}\n"
            f" channel: {self.channel}\n"
            f" port: {self.port}\n"
            f" cc_number: {self.cc_number}\n"
            f" min_range: {self.min_range}\n"
            f" max_range: {self.max_range}\n"
            f" relative_mode: {self.relative_mode}\n}}"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.processor_id == other.processor_id
            and self.parameter_id == other.parameter_id
            and self.channel == other.channel
            and self.port == other.port
            and self.cc_number == other.cc_number
            and self.min_range == other.min_range
            and self.max_range == other.max_range
            and self.relative_mode == other.relative_mode
        )


class MidiPCConnection:
    """
    Class to represent a MIDI Program Change connection in Sushi in a cleaner way.

    Attributes:
        processor (_sushi_proto.ProcessorIdentifier): a processor id
        channel (_sushi_proto.MidiChannel): a MIDI channel
        port (int): a MIDI port number
    """

    def __init__(self, grpc_MidiPCConnection):
        try:
            self.processor = grpc_MidiPCConnection.processor.id
        except AttributeError:
            self.processor = 0

        try:
            self.channel = grpc_MidiPCConnection.channel.channel
        except AttributeError:
            self.channel = 0

        try:
            self.port = grpc_MidiPCConnection.port
        except AttributeError:
            self.port = 0

    def __str__(self):
        return (
            f"{{\n processor: {self.processor}\n"
            f" channel: {self.channel}\n"
            f" port: {self.port}\n}}"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.processor == other.processor
            and self.channel == other.channel
            and self.port == other.port
        )


class CvConnection:
    """
    Class to represent a CV connection in Sushi in a cleaner way

    Attributes:
        parameter_id (int): The id of the connected parameter
        cv_port_id (int): The id of the connected CV port
    """

    def __init__(self, grpc_CvConnection):
        try:
            self.processor_id = grpc_CvConnection.parameter.processor_id
        except AttributeError:
            self.processor_id = 0

        try:
            self.parameter_id = grpc_CvConnection.parameter.parameter_id
        except AttributeError:
            self.parameter_id = 0

        try:
            self.cv_port_id = grpc_CvConnection.cv_port_id
        except AttributeError:
            self.cv_port_id = 0

    def __str__(self):
        return (
            f"{{\n parameter: {self.parameter_id}\n cv_port_id: {self.cv_port_id}\n}}"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.processor_id == other.processor_id
            and self.parameter_id == other.parameter_id
            and self.cv_port_id == other.cv_port_id
        )


class GateConnection:
    """
    Class to represent a Gate connection in Sushi in a cleaner way

    Attributes:
        processor_id (int): The id of the connected processor
        gate_port_id (int): The id of the connected Gate port
        channel (int): The connected midi channel number
        note_no (int): The midi note number to trigger
    """

    def __init__(self, grpc_CvConnection):
        try:
            self.processor_id = grpc_CvConnection.processor.id
        except AttributeError:
            self.processor_id = 0

        try:
            self.gate_port_id = grpc_CvConnection.gate_port_id
        except AttributeError:
            self.gate_port_id = 0

        try:
            self.channel = grpc_CvConnection.channel
        except AttributeError:
            self.channel = 0

        try:
            self.note_no = grpc_CvConnection.note_no
        except AttributeError:
            self.note_no = 0

    def __str__(self):
        return (
            f"{{\n processor: {self.processor_id}\n"
            f" gate_port_id: {self.gate_port_id}\n"
            f" channel: {self.channel}\n"
            f" note_no: {self.note_no}\n}}"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.processor_id == other.processor_id
            and self.gate_port_id == other.gate_port_id
            and self.channel == other.channel
            and self.note_no == other.note_no
        )
