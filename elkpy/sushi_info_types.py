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
from . import grpc_gen

################
# Custom Enums #
################

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

################
# Info Classes #
################

class ParameterInfo(object):
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

    def __init__(self, grpc_ParameterInfo = None):
        """
        The constructor of the ParameterInfo class.

        Parameters:
            grpc_ParameterInfo (sushi_rpc_pb2.ParameterInfo): the gRPC parameter info object to get the data from.
        """
        try:
            self.id = grpc_ParameterInfo.id
        except:
            self.id = 0

        grpc_types = {0: "DUMMY", 1: "BOOL", 2: "INT", 3: "FLOAT", 4: "STRING_PROPERTY", 5: "DATA_PROPERTY"}
        try:
            self.type = ParameterType(grpc_ParameterInfo.type.type)

        except:
            self.type = "DUMMY"

        try:
            self.label = grpc_ParameterInfo.label
        except:
            self.label = ''

        try:
            self.name = grpc_ParameterInfo.name
        except:
            self.name = ''

        try:
            self.unit = grpc_ParameterInfo.unit
        except:
            self.unit = ''

        try:
            self.automatable = grpc_ParameterInfo.automatable
        except:
            self.automatable = False

        try:
            self.min_domain_value = grpc_ParameterInfo.min_domain_value
        except:
            self.min_domain_value = 0.0

        try:
            self.max_domain_value = grpc_ParameterInfo.max_domain_value
        except:
            self.max_domain_value = 0.0

    def __str__(self):
        s = '{\n'
        s += ' id: %s \n' %self.id
        s += ' type: %s \n' %self.type
        s += ' label: %s \n' %self.label
        s += ' name: %s \n' %self.name
        s += ' unit: %s \n' %self.unit
        s += ' automatable: %s \n' %self.automatable
        s += ' min_domain_value: %s \n' %self.min_domain_value
        s += ' max_domain_value: %s \n' %self.max_domain_value
        s += '}'
        return s

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other):
        return self.id == other.id \
            and self.type == other.type \
            and self.label == other.label \
            and self.name == other.name \
            and self.unit == other.unit \
            and self.automatable == other .automatable \
            and self.min_domain_value == other.min_domain_value \
            and self.max_domain_value == other.max_domain_value

class ProcessorInfo(object):
    """
    Class to represent the processor info received from sushi in a clear way.

    Attributes:
        id (int): The id of the processor.
        label (str): The label of the processor.
        name (str): The name of the processor.
        parameter_count (int): The number of parameters available to the processor.
        program_count (int): The number of programs available to the processor.
    """
    def __init__(self, grpc_ProcessorInfo = None):
        try:
            self.id = grpc_ProcessorInfo.id
        except:
            self.id = 0

        try:
            self.label = grpc_ProcessorInfo.label
        except:
            self.label = ''

        try:
            self.name = grpc_ProcessorInfo.name
        except:
            self.name = ''

        try:
            self.parameter_count = grpc_ProcessorInfo.parameter_count
        except:
            self.parameter_count = 0

        try:
            self.program_count = grpc_ProcessorInfo.program_count
        except:
            self.program_count = 0

    def __str__(self):
        s = '{\n'
        s += (' id: %s \n' %self.id)
        s += (' label: %s \n' %self.label)
        s += (' name: %s \n' %self.name)
        s += (' parameter count: %s \n' %self.parameter_count)
        s += (' program count: %s \n' %self.program_count)
        s += '}'
        return s

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.id == other.id \
            and self.label == other.label \
            and self.name == other.name \
            and self.parameter_count == other.parameter_count \
            and self.program_count == other.program_count


class TrackInfo(object):
    """
    Class to represent the track info received from sushi in a clear way.

    Attributes:
        id (int): The id of the track.
        label (str): The label of the track.
        name (str): The name of the track.
        input_channels (int): The number of input channels available to the track.
        input_busses (int): The number input busses available to the track.
        output_channels (int): The number of output channels available to the track.
        output_busses (int): The number of output busses available to the track.
    """
    def __init__(self, grpc_TrackInfo = None):
        try:
            self.id = grpc_TrackInfo.id
        except:
            self.id = 0

        try:
            self.label = grpc_TrackInfo.label
        except:
            self.label = ''

        try:
            self.name = grpc_TrackInfo.name
        except:
            self.name = ''

        try:
            self.input_channels = grpc_TrackInfo.input_channels
        except:
            self.input_channels = 0

        try:
            self.input_busses = grpc_TrackInfo.input_busses
        except:
            self.input_busses = 0

        try:
            self.output_channels = grpc_TrackInfo.output_channels
        except:
            self.output_channels = 0

        try:
            self.output_busses = grpc_TrackInfo.output_busses
        except:
            self.output_busses = 0

        try:
            self.processors = []
            for processor in grpc_TrackInfo.processors:
                self.processors.append(processor.id)
        except:
            self.processors = []

    def __str__(self):
        s = '{\n'
        s += ' id: %s \n' %self.id
        s += ' label: %s \n' %self.label
        s += ' name: %s \n' %self.name
        s += ' input_channels: %s \n' %self.input_channels
        s += ' input_busses: %s \n' %self.input_busses
        s += ' output_channels: %s \n' %self.output_channels
        s += ' output_busses: %s \n' %self.output_busses
        s += ' processors: %s \n' %self.processors
        s += '}'
        return s

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.id == other.id \
            and self.label == other.label \
            and self.name == other.name \
            and self.input_channels == other.input_channels \
            and self.input_busses == other.input_busses \
            and self.output_channels == other.output_channels \
            and self.output_busses == other.output_busses \
            and self.processors == other.processors

class ProgramInfo(object):
    """
    Class to represent the program info received from sushi in a clear way.

    Attributes:
        id (int): The id of the program.
        name (str): The name of the program.
    """
    def __init__(self, grpc_ProgramInfo = None):
        try:
            self.id = grpc_ProgramInfo.id.program
        except:
            self.id = 0

        try:
            self.name = grpc_ProgramInfo.name
        except:
            self.name = ''

    def __str__(self):
        s = '{ \n'
        s += ' id: %s \n' %self.id
        s += ' name: %s \n' %self.name
        s += '}'
        return s

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.id == other.id \
            and self.name == other.name


class AudioConnection(object):
    """
    Class to represent an audio connection info received from Sushi in a cleaner way.

    Attributes:
        track (TrackIdentifier): an int
        track_channel (int):
        engine_channel (int):
    """
    def __init__(self, grpc_AudioConnection = None):
        try:
            self.track = grpc_AudioConnection.track.id
        except:
            self.track = 0
        try:
            self.track_channel = grpc_AudioConnection.track_channel
        except:
            self.track_channel = 0
        try:
            self.engine_channel = grpc_AudioConnection.engine_channel
        except:
            self.engine_channel = 0

    def __str__(self):
        return f"{{ \n track: {self.track}\n" \
               f" track_channel: {self.track_channel}\n" \
               f" engine_channel: {self.engine_channel}\n}}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.track == other.track \
               and self.track_channel == other.track_channel \
               and self.engine_channel == other.engine_channel


class MidiKbdConnection(object):
    """
    Class to represent a MIDI keyboard connection in Sushi in a cleaner way.

    Attributes:
        track (_sushi_proto.TrackIdentifier): a track id
        channel (_sushi_proto.MidiChannel): a MIDI channel
        port (int): a MIDI port number
        raw_midi (bool): is this track a raw MIDI track or not.
    """
    def __init__(self, grpc_MidiKbdConnection=None):
        try:
            self.track = grpc_MidiKbdConnection.track.id
        except:
            self.track = 0
        try:
            self.channel = grpc_MidiKbdConnection.channel.channel
        except:
            self.channel = 0
        try:
            self.port = grpc_MidiKbdConnection.port
        except:
            self.port = 0
        try:
            self.raw_midi = grpc_MidiKbdConnection.raw_midi
        except:
            self.raw_midi = False

    def __str__(self):
        return f"{{\n track: {self.track}\n" \
               f" channel: {self.channel}\n" \
               f" port: {self.port}\n" \
               f" raw_midi: {self.raw_midi}\n}}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.track == other.track and self.channel == other.channel \
               and self.port == other.port and self.raw_midi == other.raw_midi


class MidiCCConnection(object):
    """
    Class to represent a MIDI Continious Controller connection in Sushi in a cleaner way.

    Attributes:
        parameter (_sushi_proto.ParameterIdentifier):
        channel (MidiChannel)
        port (int)
        cc_number (int)
        min_range (float)
        max_range (float)
        relative_mode (bool)
    """
    def __init__(self, grpc_MidiCCConnection=None):
        try:
            self.parameter = grpc_MidiCCConnection.parameter.parameter_id
        except:
            self.parameter = 0
        try:
            self.channel = grpc_MidiCCConnection.channel.channel
        except:
            self.channel = 0
        try:
            self.port = grpc_MidiCCConnection.port
        except:
            self.port = 0
        try:
            self.cc_number = grpc_MidiCCConnection.cc_number
        except:
            self.cc_number = 0
        try:
            self.min_range = grpc_MidiCCConnection.min_range
        except:
            self.min_range = 0.0
        try:
            self.max_range = grpc_MidiCCConnection.max_range
        except:
            self.max_range = 0.0
        try:
            self.relative_mode = grpc_MidiCCConnection.relative_mode
        except:
            self.relative_mode = False

    def __str__(self):
        return f"{{\n parameter: {self.parameter}\n" \
               f" channel: {self.channel}\n" \
               f" port: {self.port}\n" \
               f" cc_number: {self.cc_number}\n" \
               f" min_range: {self.min_range}\n" \
               f" max_range: {self.max_range}\n" \
               f" relative_mode: {self.relative_mode}\n}}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.parameter == other.parameter and self.channel == other.channel and self.port == other.port \
               and self.cc_number == other.cc_number and self.min_range == other.min_range \
               and self.max_range == other.max_range and self.relative_mode == other.relative_mode


class MidiPCConnection(object):
    """
    Class to represent a MIDI Program Change connection in Sushi in a cleaner way.

    Attributes:
        processor (_sushi_proto.ProcessorIdentifier): a processor id
        channel (_sushi_proto.MidiChannel): a MIDI channel
        port (int): a MIDI port number
    """
    def __init__(self, grpc_MidiPCConnection=None):
        try:
            self.processor = grpc_MidiPCConnection.processor.id
        except:
            self.processor = 0
        try:
            self.channel = grpc_MidiPCConnection.channel.channel
        except:
            self.channel = 0
        try:
            self.port = grpc_MidiPCConnection.port
        except:
            self.port = 0

    def __str__(self):
        return f"{{\n processor: {self.processor}\n" \
               f" channel: {self.channel}\n" \
               f" port: {self.port}\n}}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.processor == other.processor and self.channel == other.channel \
               and self.port == other.port


class CvConnection(object):
    """
    Class to represent a CV connection in Sushi in a cleaner way

    Attributes:
        parameter (int): The id of the connected parameter
        cv_port_id (int): The id of the connected CV port
    """
    def __init__(self, grpc_CvConnection=None):
        try:
            self.parameter = grpc_CvConnection.parameter.id
        except:
            self.parameter = 0
        try:
            self.cv_port_id = grpc_CvConnection.cv_port_id
        except:
            self.cv_port_id = 0

    def __str__(self):
        return f"{{\n parameter: {self.parameter}\n" \
               f" cv_port_id: {self.cv_port_id}\n}}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.parameter == other.parameter and self.cv_port_id == other.cv_port_id


class GateConnection(object):
    """
    Class to represent a Gate connection in Sushi in a cleaner way

    Attributes:
        processor (int): The id of the connected processor
        gate_port_id (int): The id of the connected Gate port
        channel (int): The connected midi channel number
        note_no (int): The midi note number to trigger
    """
    def __init__(self, grpc_CvConnection=None):
        try:
            self.processor = grpc_CvConnection.processor.id
        except:
            self.processor = 0
        try:
            self.gate_port_id = grpc_CvConnection.gate_port_id
        except:
            self.gate_port_id = 0
        try:
            self.channel = grpc_CvConnection.channel
        except:
            self.channel = 0
        try:
            self.note_no = grpc_CvConnection.note_no
        except:
            self.note_no = 0

    def __str__(self):
        return f"{{\n processor: {self.processor}\n" \
               f" gate_port_id: {self.gate_port_id}\n" \
               f" channel: {self.channel}\n" \
               f" note_no: {self.note_no}\n}}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.processor == other.processor and self.gate_port_id == other.gate_port_id \
               and self.channel == other.channel and self.note_no == other.note_no
