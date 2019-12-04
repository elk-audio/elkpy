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
    '''
    Enum class to hold the values matching the different playing modes.
    '''
    STOPPED = 1
    PLAYING = 2
    RECORDING = 3

class SyncMode(IntEnum):
    '''
    Enum class to hold the values matching the different sync modes.
    '''
    INTERNAL = 1
    MIDI = 2
    LINK = 3

class ParameterType(IntEnum):
    '''
    Enum class to hold the values matching the different variable types.
    '''
    BOOL = 1
    INT = 2
    FLOAT = 3
    STRING_PROPERTY = 4
    DATA_PROPERTY = 5

################
# Info Classes #
################

class ParameterInfo(object):
    '''
    Class to represent the parameter info received from sushi in a clear way.

    Attributes:
        id (int): The id of the parameter.
        type (str): The type of the parameter.
        label (str): The label of the parameter.
        name (str): The name of the parameter.
        unit (str): The unit of the parameter.
        automatable (bool): If the parameter is automatable or not.
        min_range (float): The minimum value of the parameter.
        max_range (float): The maximum value of the parameter.
    '''

    def __init__(self, grpc_ParameterInfo = None):
        '''
        The constructor of the ParameterInfo class.

        Parameters:
            grpc_ParameterInfo (sushi_rpc_pb2.ParameterInfo): the gRPC parameter info object to get the data from.
        '''
        try:
            self.id = grpc_ParameterInfo.id
        except:
            self.id = 0
        
        grpc_types = {0: "DUMMY", 1: "BOOL", 2: "INT", 3: "FLOAT", 4: "STRING_PROPERTY", 5: "DATA_PROPERTY"}
        try:
            self.type = grpc_types.get(grpc_ParameterInfo.type.type)

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
            self.min_range = grpc_ParameterInfo.min_range
        except:
            self.min_range = 0.0

        try:
            self.max_range = grpc_ParameterInfo.max_range
        except:
            self.max_range = 0.0

    def __str__(self):
        s = '{\n'
        s += ' id: %s \n' %self.id
        s += ' type: %s \n' %self.type
        s += ' label: %s \n' %self.label
        s += ' name: %s \n' %self.name
        s += ' unit: %s \n' %self.unit
        s += ' automatable: %s \n' %self.automatable
        s += ' min_range: %s \n' %self.min_range
        s += ' max_range: %s \n' %self.max_range
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
            and self.min_range == other.min_range \
            and self.max_range == other.max_range

class ProcessorInfo(object):
    '''
    Class to represent the processor info received from sushi in a clear way.

    Attributes:
        id (int): The id of the processor.
        label (str): The label of the processor.
        name (str): The name of the processor.
        parameter_count (int): The number of parameters available to the processor.
        program_count (int): The number of programs available to the processor.
    '''
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
    '''
    Class to represent the track info received from sushi in a clear way.

    Attributes:
        id (int): The id of the track.
        label (str): The label of the track.
        name (str): The name of the track.
        input_channels (int): The number of input channels available to the track.
        input_busses (int): The number input busses available to the track.
        output_channels (int): The number of output channels available to the track.
        output_busses (int): The number of output busses available to the track.
    '''
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
            self.processor_count = grpc_TrackInfo.processor_count
        except:
            self.processor_count = 0

    def __str__(self):
        s = '{\n'
        s += ' id: %s \n' %self.id
        s += ' label: %s \n' %self.label
        s += ' name: %s \n' %self.name
        s += ' input_channels: %s \n' %self.input_channels
        s += ' input_busses: %s \n' %self.input_busses
        s += ' output_channels: %s \n' %self.output_channels
        s += ' output_busses: %s \n' %self.output_busses
        s += ' processor_count: %s \n' %self.processor_count
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
            and self.processor_count == other.processor_count

class ProgramInfo(object):
    '''
    Class to represent the program info received from sushi in a clear way.

    Attributes:
        id (int): The id of the program.
        name (str): The name of the program.
    '''
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
