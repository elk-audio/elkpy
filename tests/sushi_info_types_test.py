import os
import sys
import inspect
import unittest
import time
from ELKpy import sushi_info_types as types

from ELKpy import grpc_gen

proto_file = os.environ.get('SUSHI_GRPC_ELKPY_PROTO')
if proto_file is None:
    print("Environment variable SUSHI_GRPC_ELKPY_PROTO not defined, set it to point the .proto definition")
    sys.exit(-1)

SUSHI_PROTO, _dummy = grpc_gen.modules_from_proto(proto_file)

class TestSushiParameterInfo(unittest.TestCase):

    def test_all_parameters(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                id = 1,
                type = SUSHI_PROTO.ParameterType(type = 1),
                label = 'test',
                name = 'test',
                unit = 'test',
                automatable = True,
                min_range = 0,
                max_range = 8
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = "BOOL"
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.unit = 'test'
        expected_result.automatable = True
        expected_result.min_range = 0.0
        expected_result.max_range = 8.0

        self.assertEqual(result, expected_result)

    def test_missing_id(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                type = SUSHI_PROTO.ParameterType(type = 1),
                label = 'test',
                name = 'test',
                unit = 'test',
                automatable = True,
                min_range = 0,
                max_range = 8
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 0
        expected_result.type = "BOOL"
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.unit = 'test'
        expected_result.automatable = True
        expected_result.min_range = 0.0
        expected_result.max_range = 8.0

        self.assertEqual(result, expected_result)

    def test_missing_type(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                id = 1,
                label = 'test',
                name = 'test',
                unit = 'test',
                automatable = True,
                min_range = 0,
                max_range = 8
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = 'DUMMY'
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.unit = 'test'
        expected_result.automatable = True
        expected_result.min_range = 0.0
        expected_result.max_range = 8.0

        self.assertEqual(result, expected_result)

    def test_missing_label(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                id = 1,
                type = SUSHI_PROTO.ParameterType(type = 1),
                name = 'test',
                unit = 'test',
                automatable = True,
                min_range = 0,
                max_range = 8
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = "BOOL"
        expected_result.label = ''
        expected_result.name = 'test'
        expected_result.unit = 'test'
        expected_result.automatable = True
        expected_result.min_range = 0.0
        expected_result.max_range = 8.0

        self.assertEqual(result, expected_result)

    def test_missing_name(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                id = 1,
                type = SUSHI_PROTO.ParameterType(type = 1),
                label = 'test',
                unit = 'test',
                automatable = True,
                min_range = 0,
                max_range = 8
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = "BOOL"
        expected_result.label = 'test'
        expected_result.name = ''
        expected_result.unit = 'test'
        expected_result.automatable = True
        expected_result.min_range = 0.0
        expected_result.max_range = 8.0

        self.assertEqual(result, expected_result)

    def test_missing_unit(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                id = 1,
                type = SUSHI_PROTO.ParameterType(type = 1),
                label = 'test',
                name = 'test',
                automatable = True,
                min_range = 0,
                max_range = 8
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = "BOOL"
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.unit = ''
        expected_result.automatable = True
        expected_result.min_range = 0.0
        expected_result.max_range = 8.0

        self.assertEqual(result, expected_result)

    def test_missing_automatable(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                id = 1,
                type = SUSHI_PROTO.ParameterType(type = 1),
                label = 'test',
                name = 'test',
                unit = 'test',
                min_range = 0,
                max_range = 8
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = "BOOL"
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.unit = 'test'
        expected_result.automatable = False
        expected_result.min_range = 0.0
        expected_result.max_range = 8.0

        self.assertEqual(result, expected_result)

    def test_missing_min_range(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                id = 1,
                type = SUSHI_PROTO.ParameterType(type = 1),
                label = 'test',
                name = 'test',
                unit = 'test',
                automatable = True,
                max_range = 8
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = "BOOL"
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.unit = 'test'
        expected_result.automatable = True
        expected_result.min_range = 0.0
        expected_result.max_range = 8.0

        self.assertEqual(result, expected_result)

    def test_missing_max_range(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                id = 1,
                type = SUSHI_PROTO.ParameterType(type = 1),
                label = 'test',
                name = 'test',
                unit = 'test',
                automatable = True,
                min_range = 0
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = "BOOL"
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.unit = 'test'
        expected_result.automatable = True
        expected_result.min_range = 0.0
        expected_result.max_range = 0.0

        self.assertEqual(result, expected_result)

class TestSushiProcessorInfo(unittest.TestCase):

    def test_all_parameters(self):
        result = types.ProcessorInfo(
            SUSHI_PROTO.ProcessorInfo(
                id = 1,
                label = 'test',
                name = 'test',
                parameter_count = 10,
                program_count = 10
            )
        )
        expected_result = types.ProcessorInfo()
        expected_result.id = 1
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.parameter_count = 10
        expected_result.program_count = 10

        self.assertEqual(result, expected_result)

    def test_missing_id(self):
        result = types.ProcessorInfo(
            SUSHI_PROTO.ProcessorInfo(
                label = 'test',
                name = 'test',
                parameter_count = 10,
                program_count = 10
            )
        )
        expected_result = types.ProcessorInfo()
        expected_result.id = 0
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.parameter_count = 10
        expected_result.program_count = 10

        self.assertEqual(result, expected_result)

    def test_missing_label(self):
        result = types.ProcessorInfo(
            SUSHI_PROTO.ProcessorInfo(
                id = 1,
                name = 'test',
                parameter_count = 10,
                program_count = 10
            )
        )
        expected_result = types.ProcessorInfo()
        expected_result.id = 1
        expected_result.label = ''
        expected_result.name = 'test'
        expected_result.parameter_count = 10
        expected_result.program_count = 10

        self.assertEqual(result, expected_result)

    def test_missing_name(self):
        result = types.ProcessorInfo(
            SUSHI_PROTO.ProcessorInfo(
                id = 1,
                label = 'test',
                parameter_count = 10,
                program_count = 10
            )
        )
        expected_result = types.ProcessorInfo()
        expected_result.id = 1
        expected_result.label = 'test'
        expected_result.name = ''
        expected_result.parameter_count = 10
        expected_result.program_count = 10

        self.assertEqual(result, expected_result)

    def test_missing_parameter_count(self):
        result = types.ProcessorInfo(
            SUSHI_PROTO.ProcessorInfo(
                id = 1,
                label = 'test',
                name = 'test',
                program_count = 10
            )
        )
        expected_result = types.ProcessorInfo()
        expected_result.id = 1
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.parameter_count = 0
        expected_result.program_count = 10

        self.assertEqual(result, expected_result)

    def test_missing_program_count(self):
        result = types.ProcessorInfo(
            SUSHI_PROTO.ProcessorInfo(
                id = 1,
                label = 'test',
                name = 'test',
                parameter_count = 10
            )
        )
        expected_result = types.ProcessorInfo()
        expected_result.id = 1
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.parameter_count = 10
        expected_result.program_count = 0

        self.assertEqual(result, expected_result)

class TestSushiTrackInfo(unittest.TestCase):

    def test_all_parameters(self):
        result = types.TrackInfo(SUSHI_PROTO.TrackInfo(
            id = 1,
            label = 'test',
            name = 'test',
            input_channels = 2,
            input_busses = 1,
            output_channels = 2,
            output_busses = 1,
            processor_count = 10
        ))

        expected_result = types.TrackInfo()
        expected_result.id = 1
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.input_channels = 2
        expected_result.input_busses = 1
        expected_result.output_channels = 2
        expected_result.output_busses = 1
        expected_result.processor_count = 10

        self.assertEqual(result, expected_result)

    def test_missing_id(self):
        result = types.TrackInfo(SUSHI_PROTO.TrackInfo(
            label = 'test',
            name = 'test',
            input_channels = 2,
            input_busses = 1,
            output_channels = 2,
            output_busses = 1,
            processor_count = 10
        ))

        expected_result = types.TrackInfo()
        expected_result.id = 0
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.input_channels = 2
        expected_result.input_busses = 1
        expected_result.output_channels = 2
        expected_result.output_busses = 1
        expected_result.processor_count = 10

        self.assertEqual(result, expected_result)

    def test_missing_label(self):
        result = types.TrackInfo(SUSHI_PROTO.TrackInfo(
            id = 1,
            name = 'test',
            input_channels = 2,
            input_busses = 1,
            output_channels = 2,
            output_busses = 1,
            processor_count = 10
        ))

        expected_result = types.TrackInfo()
        expected_result.id = 1
        expected_result.label = ''
        expected_result.name = 'test'
        expected_result.input_channels = 2
        expected_result.input_busses = 1
        expected_result.output_channels = 2
        expected_result.output_busses = 1
        expected_result.processor_count = 10

        self.assertEqual(result, expected_result)

    def test_missing_name(self):
        result = types.TrackInfo(SUSHI_PROTO.TrackInfo(
            id = 1,
            label = 'test',
            input_channels = 2,
            input_busses = 1,
            output_channels = 2,
            output_busses = 1,
            processor_count = 10
        ))

        expected_result = types.TrackInfo()
        expected_result.id = 1
        expected_result.label = 'test'
        expected_result.name = ''
        expected_result.input_channels = 2
        expected_result.input_busses = 1
        expected_result.output_channels = 2
        expected_result.output_busses = 1
        expected_result.processor_count = 10

        self.assertEqual(result, expected_result)

    def test_missing_input_channels(self):
        result = types.TrackInfo(SUSHI_PROTO.TrackInfo(
            id = 1,
            label = 'test',
            name = 'test',
            input_busses = 1,
            output_channels = 2,
            output_busses = 1,
            processor_count = 10
        ))

        expected_result = types.TrackInfo()
        expected_result.id = 1
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.input_channels = 0
        expected_result.input_busses = 1
        expected_result.output_channels = 2
        expected_result.output_busses = 1
        expected_result.processor_count = 10

        self.assertEqual(result, expected_result)
        
    def test_missing_busses(self):
        result = types.TrackInfo(SUSHI_PROTO.TrackInfo(
            id = 1,
            label = 'test',
            name = 'test',
            input_channels = 2,
            output_channels = 2,
            output_busses = 1,
            processor_count = 10
        ))

        expected_result = types.TrackInfo()
        expected_result.id = 1
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.input_channels = 2
        expected_result.input_busses = 0
        expected_result.output_channels = 2
        expected_result.output_busses = 1
        expected_result.processor_count = 10

        self.assertEqual(result, expected_result)
    
    def test_missing_output_channels(self):
        result = types.TrackInfo(SUSHI_PROTO.TrackInfo(
            id = 1,
            label = 'test',
            name = 'test',
            input_channels = 2,
            input_busses = 1,
            output_busses = 1,
            processor_count = 10
        ))

        expected_result = types.TrackInfo()
        expected_result.id = 1
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.input_channels = 2
        expected_result.input_busses = 1
        expected_result.output_channels = 0
        expected_result.output_busses = 1
        expected_result.processor_count = 10

        self.assertEqual(result, expected_result)

    def test_missing_output_busses(self):
        result = types.TrackInfo(SUSHI_PROTO.TrackInfo(
            id = 1,
            label = 'test',
            name = 'test',
            input_channels = 2,
            input_busses = 1,
            output_channels = 2,
            processor_count = 10
        ))

        expected_result = types.TrackInfo()
        expected_result.id = 1
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.input_channels = 2
        expected_result.input_busses = 1
        expected_result.output_channels = 2
        expected_result.output_busses = 0
        expected_result.processor_count = 10

        self.assertEqual(result, expected_result)

    def test_missing_processor_count(self):
        result = types.TrackInfo(SUSHI_PROTO.TrackInfo(
            id = 1,
            label = 'test',
            name = 'test',
            input_channels = 2,
            input_busses = 1,
            output_channels = 2,
            output_busses = 1
        ))

        expected_result = types.TrackInfo()
        expected_result.id = 1
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.input_channels = 2
        expected_result.input_busses = 1
        expected_result.output_channels = 2
        expected_result.output_busses = 1
        expected_result.processor_count = 0

        self.assertEqual(result, expected_result)

class TestSushiProgramInfo(unittest.TestCase):

    def test_all_parameters(self):
        result = types.ProgramInfo(SUSHI_PROTO.ProgramInfo(
            id = SUSHI_PROTO.ProgramIdentifier(program = 1),
            name = 'test'
        ))

        expected_result = types.ProgramInfo()

        expected_result.id = 1
        expected_result.name = 'test'

        self.assertEqual(result, expected_result)

    def test_missing_id(self):
        result = types.ProgramInfo(SUSHI_PROTO.ProgramInfo(
            name = 'test'
        ))

        expected_result = types.ProgramInfo()

        expected_result.id = 0
        expected_result.name = 'test'

        self.assertEqual(result, expected_result)

    def test_missing_name(self):
        result = types.ProgramInfo(SUSHI_PROTO.ProgramInfo(
            id = SUSHI_PROTO.ProgramIdentifier(program = 1)
        ))

        expected_result = types.ProgramInfo()

        expected_result.id = 1
        expected_result.name = ''

        self.assertEqual(result, expected_result)

    
if __name__ == "__main__":
    unittest.main()

