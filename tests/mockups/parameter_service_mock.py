import grpc
import sushi_rpc_pb2 as proto
import sushi_rpc_pb2_grpc
from elkpy import sushi_info_types as info

expected_parameter_1 = info.ParameterInfo()
expected_parameter_1.id = 1
expected_parameter_1.type = info.ParameterType.FLOAT
expected_parameter_1.label = "Test Parameter 1"
expected_parameter_1.name = "test_parameter_1"
expected_parameter_1.unit = "unit_1"
expected_parameter_1.automatable = True
expected_parameter_1.min_domain_value = -10.0
expected_parameter_1.max_domain_value = 100.0

expected_parameter_1_value = 0.12
expected_parameter_1_value_in_domain = 11.0

grpc_param_1 = proto.ParameterInfo(
    id = expected_parameter_1.id,
    type = proto.ParameterType(type = expected_parameter_1.type),
    label = expected_parameter_1.label,
    name = expected_parameter_1.name,
    unit = expected_parameter_1.unit,
    automatable = expected_parameter_1.automatable,
    min_domain_value = expected_parameter_1.min_domain_value,
    max_domain_value = expected_parameter_1.max_domain_value
)

expected_parameter_2 = info.ParameterInfo()
expected_parameter_2.id = 2
expected_parameter_2.type = info.ParameterType.FLOAT
expected_parameter_2.label = "Test Parameter 2"
expected_parameter_2.name = "test_parameter_2"
expected_parameter_2.unit = "unit_2"
expected_parameter_2.automatable = True
expected_parameter_2.min_domain_value = -20.0
expected_parameter_2.max_domain_value = 200.0

expected_parameter_2_value = 0.5
expected_parameter_2_value_in_domain = 22.0

grpc_param_2 = proto.ParameterInfo(
    id = expected_parameter_2.id,
    type = proto.ParameterType(type = expected_parameter_2.type),
    label = expected_parameter_2.label,
    name = expected_parameter_2.name,
    unit = expected_parameter_2.unit,
    automatable = expected_parameter_2.automatable,
    min_domain_value = expected_parameter_2.min_domain_value,
    max_domain_value = expected_parameter_2.max_domain_value
)

grpc_param_list = proto.ParameterInfoList(parameters = [grpc_param_1, grpc_param_2])

expected_track_identifier = 1
expected_processor_identifier = 1

expected_parameter_value_request = proto.ParameterValue(
    parameter = proto.ParameterIdentifier(processor_id = 3,
                                          parameter_id = 3),
    value = 0.666
)

class ParameterControllerServiceMockup(sushi_rpc_pb2_grpc.ParameterControllerServicer):

    def __init__(self):
        super().__init__()
        self.called = False
        self.recent_request = None

    def GetTrackParameters(self, request, context):
        if request.id == expected_track_identifier:
            return grpc_param_list
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Track with id {} doesn't exist.".format(request.id))

    def GetProcessorParameters(self, request, context):
        if request.id == expected_processor_identifier:
            return grpc_param_list
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Processor with id {} doesn't exist.".format(request.id))

    def GetParameterId(self, request, context):
        if request.processor.id == expected_processor_identifier:
            if request.ParameterName == expected_parameter_1.name:
                return proto.ParameterIdentifier(processor_id = expected_processor_identifier,
                                                 parameter_id = expected_parameter_1.id)
            elif request.ParameterName == expected_parameter_2.name:
                return proto.ParameterIdentifier(processor_id = expected_processor_identifier,
                                                 parameter_id = expected_parameter_2.id)
            else:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Parameter with name {} doesn't exist.".format(request.name))
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Processor with id {} doesn't exist".format(request.processor.id))

    def GetParameterInfo(self, request, context):
        if request.processor_id == expected_processor_identifier:
            if request.parameter_id == expected_parameter_1.id:
                return grpc_param_1
            elif request.parameter_id == expected_parameter_2.id:
                return grpc_param_2
            else:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Parameter with id {} doesn't exist.".format(request.parameter_id))
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Processor with id {} doesn't exist".format(request.processor_id))

    def GetParameterValue(self, request, context):
        if request.processor_id == expected_processor_identifier:
            if request.parameter_id == expected_parameter_1.id:
                return proto.GenericFloatValue(value = expected_parameter_1_value)
            elif request.parameter_id == expected_parameter_2.id:
                return proto.GenericFloatValue(value = expected_parameter_2_value)
            else:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Parameter with id {} doesn't exist.".format(request.parameter_id))
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Processor with id {} doesn't exist".format(request.processor_id))

    def GetParameterValueInDomain(self, request, context):
        if request.processor_id == expected_processor_identifier:
            if request.parameter_id == expected_parameter_1.id:
                return proto.GenericFloatValue(value = expected_parameter_1_value_in_domain)
            elif request.parameter_id == expected_parameter_2.id:
                return proto.GenericFloatValue(value = expected_parameter_2_value_in_domain)
            else:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Parameter with id {} doesn't exist.".format(request.parameter_id))
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Processor with id {} doesn't exist".format(request.processor_id))

    def GetParameterValueAsString(self, request, context):
        if request.processor_id == expected_processor_identifier:
            if request.parameter_id == expected_parameter_1.id:
                return proto.GenericStringValue(value = str(expected_parameter_1_value))
            elif request.parameter_id == expected_parameter_2.id:
                return proto.GenericStringValue(value = str(expected_parameter_2_value))
            else:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Parameter withid {} doesn't exist.".format(request.parameter_id))
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Processor with id {} doesn't exist".format(request.processor_id))

    def SetParameterValue(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def was_called(self):
        temp = self.called
        self.called = False
        return temp

    def get_recent_request(self):
        temp = self.recent_request
        self.recent_request = None
        return temp
