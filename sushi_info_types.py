class ParameterInfo():
    def __init__(self, _grpc_ParameterInfo = None):
        try:
            self.id = _grpc_ParameterInfo.id
        except:
            self.id = None
        
        grpc_types = {0: "DUMMY", 1: "BOOL", 2: "INT", 3: "FLOAT", 4: "STRING_PROPERTY", 5: "DATA_PROPERTY"}
        try:
            self.type = grpc_types.get(_grpc_ParameterInfo.type.type)

        except:
            self.type = None

        try:
            self.label = _grpc_ParameterInfo.label
        except:
            self.label = None

        try:            
            self.name = _grpc_ParameterInfo.name
        except:
            self.name = None

        try:
            self.unit = _grpc_ParameterInfo.unit
        except:
            self.unit = None

        try:
            self.automatable = _grpc_ParameterInfo.automatable
        except:
            self.automatable = None

        try:
            self.min_range = _grpc_ParameterInfo.min_range
        except:
            self.min_range = None

        try:
            self.max_range = _grpc_ParameterInfo.max_range
        except:
            self.max_range = None

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

    def __repr__(self):
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

class ProcessorInfo():
    def __init__(self, _grpc_ProcessorInfo = None):
        try:
            self.id = _grpc_ProcessorInfo.id
        except: 
            self.id = None
        
        try:
            self.label = _grpc_ProcessorInfo.label
        except:
            self.label = None

        try:
            self.name = _grpc_ProcessorInfo.name
        except:
            self.name = None

        try:
            self.parameter_count = _grpc_ProcessorInfo.parameter_count
        except:
            self.parameter_count = None

        try:
            self.program_count = _grpc_ProcessorInfo.program_count
        except:
            self.program_count = None

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


class TrackInfo():
    def __init__(self, _grpc_TrackInfo = None):
        try:
            self.id = _grpc_TrackInfo.id
        except:
            self.id = None
        
        try:
            self.label = _grpc_TrackInfo.label
        except:
            self.label = None

        try:
            self.name = _grpc_TrackInfo.name
        except:
            self.name = None

        try:
            self.input_channels = _grpc_TrackInfo.input_channels
        except:
            self.input_channels = None

        try:
            self.input_busses = _grpc_TrackInfo.input_busses
        except:
            self.input_busses = None

        try:
            self.output_channels = _grpc_TrackInfo.output_channels
        except:
            self.output_channels = None

        try:
            self.output_busses = _grpc_TrackInfo.output_busses
        except:
            self.output_busses = None

        try:
            self.processor_count = _grpc_TrackInfo.processor_count
        except:
            self.processor_count = None

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