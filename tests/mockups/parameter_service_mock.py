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

expected_property = info.PropertyInfo()
expected_property.id = 1
expected_property.label = "Prop 1"
expected_property.name = "prop_1"

expected_property_1_value = "prop_1_value"

expected_property_list = [expected_property, expected_property]

grpc_property = proto.PropertyInfo(
    id = expected_property.id,
    label = expected_property.label,
    name = expected_property.name
)

grpc_property_list = proto.PropertyInfoList(properties = [grpc_property, grpc_property])

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

    def GetTrackProperties(self, request, context):
        if request.id == expected_track_identifier:
            return grpc_property_list

    def GetProcessorProperties(self, request, context):
        if request.id == expected_processor_identifier:
            return grpc_property_list

    def GetPropertyId(self, request, context):
        if request.property_name == expected_property.name and \
           request.processor.id == expected_processor_identifier:
            return proto.PropertyIdentifier(processor_id = expected_processor_identifier,
                                            property_id = expected_property.id)

    def GetPropertyInfo(self, request, context):
        if request.property_id == expected_property.id and \
           request.processor_id == expected_processor_identifier:
           return grpc_property

    def GetPropertyValue(self, request, context):
        if request.property_id == expected_property.id and \
           request.processor_id == expected_processor_identifier:
           return proto.GenericStringValue(value = expected_property_1_value)

    def SetPropertyValue(self, request, context):
        if request.property.property_id == expected_property.id and \
           request.property.processor_id == expected_processor_identifier and \
           request.value == expected_property_1_value:
            self.called = True
            return proto.GenericVoidValue()

    def was_called(self):
        temp = self.called
        self.called = False
        return temp

    def get_recent_request(self):
        temp = self.recent_request
        self.recent_request = None
        return temp
