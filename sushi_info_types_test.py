import sys
import unittest
import time
import sushi_info_types as types
import sushi_rpc_pb2

class sushi_parameter_info_test(unittest.TestCase):
    def test_all_parameters(self):
        result = types.ParameterInfo(
            sushi_rpc_pb2.ParameterInfo(
                id = 1,
                type = sushi_rpc_pb2.ParameterType(type = 1),
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
            sushi_rpc_pb2.ParameterInfo(
                type = sushi_rpc_pb2.ParameterType(type = 1),
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
            sushi_rpc_pb2.ParameterInfo(
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
            sushi_rpc_pb2.ParameterInfo(
                id = 1,
                type = sushi_rpc_pb2.ParameterType(type = 1),
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
            sushi_rpc_pb2.ParameterInfo(
                id = 1,
                type = sushi_rpc_pb2.ParameterType(type = 1),
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
            sushi_rpc_pb2.ParameterInfo(
                id = 1,
                type = sushi_rpc_pb2.ParameterType(type = 1),
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
            sushi_rpc_pb2.ParameterInfo(
                id = 1,
                type = sushi_rpc_pb2.ParameterType(type = 1),
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
            sushi_rpc_pb2.ParameterInfo(
                id = 1,
                type = sushi_rpc_pb2.ParameterType(type = 1),
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
            sushi_rpc_pb2.ParameterInfo(
                id = 1,
                type = sushi_rpc_pb2.ParameterType(type = 1),
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

class sushi_processor_info_test(unittest.TestCase):
    def test_all_parameters(self):
        result = types.ProcessorInfo(
            sushi_rpc_pb2.ProcessorInfo(
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
            sushi_rpc_pb2.ProcessorInfo(
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
            sushi_rpc_pb2.ProcessorInfo(
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
            sushi_rpc_pb2.ProcessorInfo(
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
            sushi_rpc_pb2.ProcessorInfo(
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
            sushi_rpc_pb2.ProcessorInfo(
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

class sushi_track_info_test(unittest.TestCase):
    def __init__(self):
        expected_result = types.TrackInfo()



    
if __name__ == "__main__":
    unittest.main()