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

import os
import sys
import inspect
import unittest
import time
from elkpy import sushi_info_types as types

from elkpy import grpc_gen

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
                min_domain_value = 0,
                max_domain_value = 8
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = types.ParameterType.BOOL
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.unit = 'test'
        expected_result.automatable = True
        expected_result.min_domain_value = 0.0
        expected_result.max_domain_value = 8.0

        self.assertEqual(result, expected_result)

    def test_missing_id(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                type = SUSHI_PROTO.ParameterType(type = 1),
                label = 'test',
                name = 'test',
                unit = 'test',
                automatable = True,
                min_domain_value = 0,
                max_domain_value = 8
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 0
        expected_result.type = types.ParameterType.BOOL
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.unit = 'test'
        expected_result.automatable = True
        expected_result.min_domain_value = 0.0
        expected_result.max_domain_value = 8.0

        self.assertEqual(result, expected_result)

    def test_missing_type(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                id = 1,
                label = 'test',
                name = 'test',
                unit = 'test',
                automatable = True,
                min_domain_value = 0,
                max_domain_value = 8
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = 'DUMMY'
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.unit = 'test'
        expected_result.automatable = True
        expected_result.min_domain_value = 0.0
        expected_result.max_domain_value = 8.0

        self.assertEqual(result, expected_result)

    def test_missing_label(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                id = 1,
                type = SUSHI_PROTO.ParameterType(type = 1),
                name = 'test',
                unit = 'test',
                automatable = True,
                min_domain_value = 0,
                max_domain_value = 8
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = types.ParameterType.BOOL
        expected_result.label = ''
        expected_result.name = 'test'
        expected_result.unit = 'test'
        expected_result.automatable = True
        expected_result.min_domain_value = 0.0
        expected_result.max_domain_value = 8.0

        self.assertEqual(result, expected_result)

    def test_missing_name(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                id = 1,
                type = SUSHI_PROTO.ParameterType(type = 1),
                label = 'test',
                unit = 'test',
                automatable = True,
                min_domain_value = 0,
                max_domain_value = 8
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = types.ParameterType.BOOL
        expected_result.label = 'test'
        expected_result.name = ''
        expected_result.unit = 'test'
        expected_result.automatable = True
        expected_result.min_domain_value = 0.0
        expected_result.max_domain_value = 8.0

        self.assertEqual(result, expected_result)

    def test_missing_unit(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                id = 1,
                type = SUSHI_PROTO.ParameterType(type = 1),
                label = 'test',
                name = 'test',
                automatable = True,
                min_domain_value = 0,
                max_domain_value = 8
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = types.ParameterType.BOOL
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.unit = ''
        expected_result.automatable = True
        expected_result.min_domain_value = 0.0
        expected_result.max_domain_value = 8.0

        self.assertEqual(result, expected_result)

    def test_missing_automatable(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                id = 1,
                type = SUSHI_PROTO.ParameterType(type = 1),
                label = 'test',
                name = 'test',
                unit = 'test',
                min_domain_value = 0,
                max_domain_value = 8
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = types.ParameterType.BOOL
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.unit = 'test'
        expected_result.automatable = False
        expected_result.min_domain_value = 0.0
        expected_result.max_domain_value = 8.0

        self.assertEqual(result, expected_result)

    def test_missing_min_domain_value(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                id = 1,
                type = SUSHI_PROTO.ParameterType(type = 1),
                label = 'test',
                name = 'test',
                unit = 'test',
                automatable = True,
                max_domain_value = 8
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = types.ParameterType.BOOL
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.unit = 'test'
        expected_result.automatable = True
        expected_result.min_domain_value = 0.0
        expected_result.max_domain_value = 8.0

        self.assertEqual(result, expected_result)

    def test_missing_max_domain_value(self):
        result = types.ParameterInfo(
            SUSHI_PROTO.ParameterInfo(
                id = 1,
                type = SUSHI_PROTO.ParameterType(type = 1),
                label = 'test',
                name = 'test',
                unit = 'test',
                automatable = True,
                min_domain_value = 0
            )
        )
        expected_result = types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = types.ParameterType.BOOL
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.unit = 'test'
        expected_result.automatable = True
        expected_result.min_domain_value = 0.0
        expected_result.max_domain_value = 0.0

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
            channels = 2,
            buses = 1,
            type = SUSHI_PROTO.TrackType(type = 2),
            processors = [SUSHI_PROTO.ProcessorIdentifier(id = 10),
                          SUSHI_PROTO.ProcessorIdentifier(id = 20)]
        ))

        expected_result = types.TrackInfo()
        expected_result.id = 1
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.channels = 2
        expected_result.buses = 1
        expected_result.type = types.TrackType.PRE
        expected_result.processors = [10, 20]

        self.assertEqual(result, expected_result)

    def test_missing_id(self):
        result = types.TrackInfo(SUSHI_PROTO.TrackInfo(
            label = 'test',
            name = 'test',
            channels = 2,
            buses = 1,
            type = SUSHI_PROTO.TrackType(type = 1),
            processors = [SUSHI_PROTO.ProcessorIdentifier(id = 10),
                          SUSHI_PROTO.ProcessorIdentifier(id = 20)]
        ))

        expected_result = types.TrackInfo()
        expected_result.id = 0
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.channels = 2
        expected_result.buses = 1
        expected_result.type = types.TrackType.REGULAR
        expected_result.processors = [10, 20]

        self.assertEqual(result, expected_result)

    def test_missing_label(self):
        result = types.TrackInfo(SUSHI_PROTO.TrackInfo(
            id = 1,
            name = 'test',
            channels = 2,
            buses = 1,
            type = SUSHI_PROTO.TrackType(type = 1),
            processors = [SUSHI_PROTO.ProcessorIdentifier(id = 10),
                          SUSHI_PROTO.ProcessorIdentifier(id = 20)]
        ))

        expected_result = types.TrackInfo()
        expected_result.id = 1
        expected_result.label = ''
        expected_result.name = 'test'
        expected_result.channels = 2
        expected_result.buses = 1
        expected_result.type = types.TrackType.REGULAR
        expected_result.processors = [10, 20]

        self.assertEqual(result, expected_result)

    def test_missing_name(self):
        result = types.TrackInfo(SUSHI_PROTO.TrackInfo(
            id = 1,
            label = 'test',
            channels = 2,
            buses = 1,
            type = SUSHI_PROTO.TrackType(type = 1),
            processors = [SUSHI_PROTO.ProcessorIdentifier(id = 10),
                          SUSHI_PROTO.ProcessorIdentifier(id = 20)]
        ))

        expected_result = types.TrackInfo()
        expected_result.id = 1
        expected_result.label = 'test'
        expected_result.name = ''
        expected_result.channels = 2
        expected_result.buses = 1
        expected_result.type = types.TrackType.REGULAR
        expected_result.processors = [10, 20]

        self.assertEqual(result, expected_result)

    def test_missing_channels(self):
        result = types.TrackInfo(SUSHI_PROTO.TrackInfo(
            id = 1,
            label = 'test',
            name = 'test',
            buses = 1,
            type = SUSHI_PROTO.TrackType(type = 1),
            processors = [SUSHI_PROTO.ProcessorIdentifier(id = 10),
                          SUSHI_PROTO.ProcessorIdentifier(id = 20)]
        ))

        expected_result = types.TrackInfo()
        expected_result.id = 1
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.channels = 0
        expected_result.buses = 1
        expected_result.type = types.TrackType.REGULAR
        expected_result.processors = [10, 20]

        self.assertEqual(result, expected_result)

    def test_missing_busses(self):
        result = types.TrackInfo(SUSHI_PROTO.TrackInfo(
            id = 1,
            label = 'test',
            name = 'test',
            channels = 2,
            type = SUSHI_PROTO.TrackType(type = 1),
            processors = [SUSHI_PROTO.ProcessorIdentifier(id = 10),
                          SUSHI_PROTO.ProcessorIdentifier(id = 20)]
        ))

        expected_result = types.TrackInfo()
        expected_result.id = 1
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.channels = 2
        expected_result.buses = 0
        expected_result.type = types.TrackType.REGULAR
        expected_result.processors = [10, 20]

        self.assertEqual(result, expected_result)

    def test_missing_processors(self):
        result = types.TrackInfo(SUSHI_PROTO.TrackInfo(
            id = 1,
            label = 'test',
            name = 'test',
            channels = 2,
            buses = 1,
            type =  SUSHI_PROTO.TrackType(type = 1),
        ))

        expected_result = types.TrackInfo()
        expected_result.id = 1
        expected_result.label = 'test'
        expected_result.name = 'test'
        expected_result.channels = 2
        expected_result.buses = 1
        expected_result.type = types.TrackType.REGULAR
        expected_result.processors = []
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
