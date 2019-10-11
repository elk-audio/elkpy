import os
import sys
import unittest
import time
from ELKpy import sushicontroller as sc
from ELKpy import sushi_info_types as info_types

from ELKpy import grpc_gen

proto_file = os.environ.get('SUSHI_GRPC_ELKPY_PROTO')
if proto_file is None:
    print("Environment variable SUSHI_GRPC_ELKPY_PROTO not defined, set it to point the .proto definition")
    sys.exit(-1)

SUSHI_PROTO, _dummy = grpc_gen.modules_from_proto(proto_file)

SUSHI_ADDRESS = ('localhost:51051')

# Run sushi with arguments: -j --connect-ports --timing-statistics -c ~/work/sushi/example_configs/config_temper.json
# The config file has andes followed by temper on a single stereo channel called main

class TestSushiController(unittest.TestCase):
    def setUp(self):
        self._sc = sc.SushiController(SUSHI_ADDRESS, proto_file)

    def test_get_samplerate(self):
        self.assertEqual(self._sc.get_samplerate(), 48000.0)

    def test_get_playing_mode(self):
        self.assertEqual(self._sc.get_playing_mode(), 1)

    def test_set_playing_mode_positive(self):
        wait_time = 0.1

        for i in range(1, 4):
            self._sc.set_playing_mode(i)
            time.sleep(wait_time)
            self.assertEqual(self._sc.get_playing_mode(), i)
            time.sleep(wait_time)

        self._sc.set_playing_mode(info_types.PlayingMode.STOPPED)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_playing_mode(),
                         info_types.PlayingMode.STOPPED)
        time.sleep(wait_time)
        self._sc.set_playing_mode(info_types.PlayingMode.PLAYING)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_playing_mode(),
                         info_types.PlayingMode.PLAYING)
        time.sleep(wait_time)
        self._sc.set_playing_mode(info_types.PlayingMode.RECORDING)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_playing_mode(),
                         info_types.PlayingMode.RECORDING)
        time.sleep(wait_time)

        self._sc.set_playing_mode(1)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_playing_mode(), 1)

    def test_get_sync_mode(self):
        self.assertEqual(self._sc.get_sync_mode(), 1)

    def test_set_sync_mode(self):
        wait_time = 0.1

        for i in range(1, 4):
            self._sc.set_sync_mode(i)
            time.sleep(wait_time)
            self.assertEqual(self._sc.get_sync_mode(), i)
            time.sleep(wait_time)

        self._sc.set_sync_mode(info_types.SyncMode.INTERNAL)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_sync_mode(),
                         info_types.SyncMode.INTERNAL)
        time.sleep(wait_time)
        self._sc.set_sync_mode(info_types.SyncMode.MIDI)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_sync_mode(), info_types.SyncMode.MIDI)
        time.sleep(wait_time)
        self._sc.set_sync_mode(info_types.SyncMode.LINK)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_sync_mode(), info_types.SyncMode.LINK)
        time.sleep(wait_time)

        self._sc.set_sync_mode(1)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_sync_mode(), 1)
        time.sleep(wait_time)

    def test_get_tempo(self):
        self.assertEqual(self._sc.get_tempo(), 120)

    def test_set_tempo(self):
        wait_time = 0.1

        for i in range(1, 11):
            self._sc.set_tempo(i*20)
            time.sleep(wait_time)
            self.assertEqual(self._sc.get_tempo(), i*20)
            time.sleep(wait_time)

        self._sc.set_tempo(120)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_tempo(), 120)
        time.sleep(wait_time)

    def test_get_time_signature(self):
        self.assertEqual(self._sc.get_time_signature(), (4, 4))

    def test_set_time_signature(self):
        wait_time = 0.1

        for i in range(1, 12):
            self._sc.set_time_signature(i, 4)
            time.sleep(wait_time)
            self.assertEqual(self._sc.get_time_signature(), (i, 4))
            time.sleep(wait_time)

            self._sc.set_time_signature(i, 8)
            time.sleep(wait_time)
            self.assertEqual(self._sc.get_time_signature(), (i, 8))
            time.sleep(wait_time)

        self._sc.set_time_signature(4, 4)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_time_signature(), (4, 4))
        time.sleep(wait_time)

    def test_get_tracks(self):    
        expected_result = []

        expected_result.append(info_types.TrackInfo())

        expected_result[0].id = 0
        expected_result[0].label = ''
        expected_result[0].name = 'main'
        expected_result[0].input_channels = 2
        expected_result[0].input_busses = 1
        expected_result[0].output_channels = 2
        expected_result[0].output_busses = 1
        expected_result[0].processor_count = 2

        self.assertEqual(self._sc.get_tracks(), expected_result)


class TestSushiControllerKeyboardControl(unittest.TestCase):
    def setUp(self):
        self._sc = sc.SushiController(SUSHI_ADDRESS, proto_file)

    def test_keyboard_control(self):
        wait_time = 0.5

        self._sc.send_note_on(0, 1, 63, 1.0)
        self._sc.send_aftertouch(0, 1, 0.5)
        self._sc.send_modulation(0, 1, 0.5)
        time.sleep(wait_time)
        self._sc.send_pitch_bend(0, 1, 1.0)
        time.sleep(wait_time)
        self._sc.send_pitch_bend(0, 1, 0.0)
        time.sleep(wait_time)
        self._sc.send_pitch_bend(0, 1, 0.5)
        time.sleep(wait_time)
        self._sc.send_note_off(0, 1, 63, 1.0)


class TestSushiControllerCPUTimings(unittest.TestCase):
    def setUp(self):
        self._sc = sc.SushiController(SUSHI_ADDRESS, proto_file)

    def test_get_engine_timings(self):
        self._sc.reset_all_timings()
        time.sleep(0.75)
        result_average, result_min, result_max = self._sc.get_engine_timings()

        self.assertGreater(result_average, 0)
        self.assertGreater(result_min, 0)
        self.assertGreater(result_max, 0)

    def test_get_track_timings(self):
        for i in range(0, 3):
            with self.subTest(track_id=i):
                result_average, result_min, result_max = self._sc.get_track_timings(
                    i)

                self.assertGreater(result_average, 0)
                self.assertGreater(result_min, 0)
                self.assertGreater(result_max, 0)

    def test_get_processor_timings(self):
        for i in range(0, 3):
            with self.subTest(processor_id=i):
                result_average, result_min, result_max = self._sc.get_processor_timings(
                    i)

                self.assertGreater(result_average, 0)
                self.assertGreater(result_min, 0)
                self.assertGreater(result_max, 0)

    # TODO: make a good test
    def test_reset_timings(self):
        self._sc.reset_all_timings()
        self._sc.reset_processor_timings(0)
        self._sc.reset_track_timings(0)


class TestSushiControllerTrackControl(unittest.TestCase):
    def setUp(self):
        self._sc = sc.SushiController(SUSHI_ADDRESS, proto_file)

    def test_get_track_id(self):
        result = self._sc.get_track_id('main')
        expected_result = 0

        self.assertEqual(result, expected_result)

    def test_get_track_info(self):
        result = self._sc.get_track_info(0)
        expected_result = SUSHI_PROTO.TrackInfo(
            name='main',
            input_channels=2,
            input_busses=1,
            output_channels=2,
            output_busses=1,
            processor_count=2
        )

        self.assertEqual(result, expected_result)

    def test_get_track_processors(self):
        result = self._sc.get_track_processors(0)

        expected_result = []

        expected_result.append(info_types.ProcessorInfo())
        expected_result.append(info_types.ProcessorInfo())

        expected_result[0].id = 1
        expected_result[0].label = 'Andes-1'
        expected_result[0].name = 'andes'
        expected_result[0].parameter_count = 8
        expected_result[0].program_count = 100

        expected_result[1].id = 2
        expected_result[1].label = 'Temper'
        expected_result[1].name = 'Temper'
        expected_result[1].parameter_count = 7
        expected_result[1].program_count = 5

        self.assertEqual(result, expected_result)

    def test_get_track_parameters(self):
        result = self._sc.get_track_parameters(0)
        
        expected_result = []
        
        expected_result.append(info_types.ParameterInfo())
        expected_result.append(info_types.ParameterInfo())
        
        expected_result[0].id = 0
        expected_result[0].type = 'FLOAT'
        expected_result[0].label = 'Gain'
        expected_result[0].name = 'gain'
        expected_result[0].automatable = True
        expected_result[0].min_range = -120
        expected_result[0].max_range = 24 

        expected_result[1].id = 1
        expected_result[1].type = 'FLOAT'
        expected_result[1].label = 'Pan'
        expected_result[1].name = 'pan'
        expected_result[1].automatable = True
        expected_result[1].min_range = -1
        expected_result[1].max_range = 1 

        self.assertEqual(result, expected_result)


class TestSushiControllerProcessorControl(unittest.TestCase):
    def setUp(self):
        self._sc = sc.SushiController(SUSHI_ADDRESS, proto_file)

    def test_get_processor_id(self):
        result = self._sc.get_processor_id("andes")
        expecter_result = 1

        with self.subTest(test_code=1):
            self.assertEqual(result, expecter_result)

        result = self._sc.get_processor_id("Temper")
        expecter_result = 2

        with self.subTest(test_code=2):
            self.assertEqual(result, expecter_result)

    def test_get_processor_info(self):
        result = self._sc.get_processor_info(0)
        expected_result = SUSHI_PROTO.ProcessorInfo(
            name='main',
            parameter_count=2
        )

        with self.subTest(processorId=0):
            self.assertEqual(result, expected_result)

        result = self._sc.get_processor_info(1)
        expected_result = SUSHI_PROTO.ProcessorInfo(
            id=1,
            label='Andes-1',
            name='andes',
            parameter_count=8,
            program_count=100
        )

        with self.subTest(processorId=1):
            self.assertEqual(result, expected_result)

        result = self._sc.get_processor_info(2)
        expected_result = SUSHI_PROTO.ProcessorInfo(
            id=2,
            label='Temper',
            name='Temper',
            parameter_count=7,
            program_count=5
        )

        with self.subTest(processorId=2):
            self.assertEqual(result, expected_result)

    def test_get_processor_bypass_state(self):
        result = self._sc.get_processor_bypass_state(0)
        expected_result = False

        with self.subTest(processorId=0):
            self.assertEqual(result, expected_result)

        result = self._sc.get_processor_bypass_state(1)
        expected_result = False

        with self.subTest(processorId=1):
            self.assertEqual(result, expected_result)

        result = self._sc.get_processor_bypass_state(2)
        expected_result = False

        with self.subTest(processorId=2):
            self.assertEqual(result, expected_result)

    def test_set_processor_bypass_state(self):
        wait_time = 0.5
        for i in range(0, 3):
            with self.subTest(processorId=i):
                self._sc.set_processor_bypass_state(i, True)
                time.sleep(wait_time)
                result = self._sc.get_processor_bypass_state(i)
                expected_result = True

                self.assertEqual(result, expected_result)

                self._sc.set_processor_bypass_state(i, False)
                time.sleep(wait_time)
                result = self._sc.get_processor_bypass_state(i)
                expected_result = False

                self.assertEqual(result, expected_result)

    def test_get_processor_current_program(self):
        result = self._sc.get_processor_current_program(1)
        expected_result = 0

        self.assertEqual(result, expected_result)

    def test_get_processor_current_program_name(self):
        result = self._sc.get_processor_current_program_name(1)
        expected_result = 'Default'

        self.assertEqual(result, expected_result)

    def test_get_processor_program_name(self):
        result = self._sc.get_processor_program_name(1, 1)
        expected_result = 'Default'

        self.assertEqual(result, expected_result)

    def test_get_processor_programs(self):
        result = self._sc.get_processor_programs(2)

        expected_result = []

        expected_result.append(info_types.ProgramInfo())
        expected_result.append(info_types.ProgramInfo())
        expected_result.append(info_types.ProgramInfo())
        expected_result.append(info_types.ProgramInfo())
        expected_result.append(info_types.ProgramInfo())

        expected_result[0].id = 0
        expected_result[0].name = 'Default'

        expected_result[1].id = 1
        expected_result[1].name = 'Stubbed Toe'

        expected_result[2].id = 2
        expected_result[2].name = 'Bee Sting'

        expected_result[3].id = 3
        expected_result[3].name = 'Morning at the DMV'

        expected_result[4].id = 4
        expected_result[4].name = 'Flying United'

        self.assertEqual(result, expected_result)

    def test_set_processor_program(self):
        wait_time = 0.5
        self._sc.set_processor_program(2, 2)
        time.sleep(wait_time)
        result = self._sc.get_processor_current_program(2)
        expected_result = 2
        self.assertEqual(result, expected_result)

        self._sc.set_processor_program(2, 1)
        time.sleep(wait_time)
        result = self._sc.get_processor_current_program(2)
        expected_result = 1
        self.assertEqual(result, expected_result)

    def test_get_processor_parameters(self):
        result = self._sc.get_processor_parameters(1)
    
        expected_result = []

        expected_result.append(info_types.ParameterInfo())
        expected_result.append(info_types.ParameterInfo())
        expected_result.append(info_types.ParameterInfo())
        expected_result.append(info_types.ParameterInfo())
        expected_result.append(info_types.ParameterInfo())
        expected_result.append(info_types.ParameterInfo())
        expected_result.append(info_types.ParameterInfo())
        expected_result.append(info_types.ParameterInfo())

        expected_result[0].id = 0
        expected_result[0].type = 'FLOAT'
        expected_result[0].label = 'octaves'
        expected_result[0].name = 'octaves'
        expected_result[0].unit = ''
        expected_result[0].automatable = True
        expected_result[0].min_range = 0
        expected_result[0].max_range = 1

        expected_result[1].id = 1
        expected_result[1].type = 'FLOAT'
        expected_result[1].label = 'persistence'
        expected_result[1].name = 'persistence'
        expected_result[1].unit = ''
        expected_result[1].automatable = True
        expected_result[1].min_range = 0
        expected_result[1].max_range = 1

        expected_result[2].id = 2
        expected_result[2].type = 'FLOAT'
        expected_result[2].label = 'env1att'
        expected_result[2].name = 'env1att'
        expected_result[2].unit = ''
        expected_result[2].automatable = True
        expected_result[2].min_range = 0
        expected_result[2].max_range = 1

        expected_result[3].id = 3
        expected_result[3].type = 'FLOAT'
        expected_result[3].label = 'env1dec'
        expected_result[3].name = 'env1dec'
        expected_result[3].unit = ''
        expected_result[3].automatable = True
        expected_result[3].min_range = 0
        expected_result[3].max_range = 1

        expected_result[4].id = 4
        expected_result[4].type = 'FLOAT'
        expected_result[4].label = 'env1sus'
        expected_result[4].name = 'env1sus'
        expected_result[4].unit = ''
        expected_result[4].automatable = True
        expected_result[4].min_range = 0
        expected_result[4].max_range = 1

        expected_result[5].id = 5
        expected_result[5].type = 'FLOAT'
        expected_result[5].label = 'env1rel'
        expected_result[5].name = 'env1rel'
        expected_result[5].unit = ''
        expected_result[5].automatable = True
        expected_result[5].min_range = 0
        expected_result[5].max_range = 1

        expected_result[6].id = 6
        expected_result[6].type = 'FLOAT'
        expected_result[6].label = 'offset'
        expected_result[6].name = 'offset'
        expected_result[6].unit = ''
        expected_result[6].automatable = True
        expected_result[6].min_range = 0
        expected_result[6].max_range = 1

        expected_result[7].id = 7
        expected_result[7].type = 'FLOAT'
        expected_result[7].label = 'warping'
        expected_result[7].name = 'warping'
        expected_result[7].unit = ''
        expected_result[7].automatable = True
        expected_result[7].min_range = 0
        expected_result[7].max_range = 1

        self.assertEqual(result, expected_result)

class TestSushiControllerParameterControl(unittest.TestCase):
    def setUp(self):
        self._sc = sc.SushiController(SUSHI_ADDRESS, proto_file)

    def test_get_parameter_id(self):
        result = self._sc.get_parameter_id(1,'octaves')
        expected_result = (0)

        self.assertEqual(result,expected_result)

        result = self._sc.get_parameter_id(1,'persistence')
        expected_result = (1)

        self.assertEqual(result,expected_result)

    def test_get_parameter_info(self):
        result = self._sc.get_parameter_info(1,0)

        expected_result = info_types.ParameterInfo()
        expected_result.id = 0
        expected_result.type = 'FLOAT'
        expected_result.label = 'octaves'
        expected_result.name = 'octaves'
        expected_result.unit = ''
        expected_result.automatable = True
        expected_result.min_range = 0.0
        expected_result.max_range = 1.0

        self.assertEqual(result,expected_result)

        result = self._sc.get_parameter_info(1,1)
 
        expected_result = info_types.ParameterInfo()
        expected_result.id = 1
        expected_result.type = 'FLOAT'
        expected_result.label = 'persistence'
        expected_result.name = 'persistence'
        expected_result.unit = ''
        expected_result.automatable = True
        expected_result.min_range = 0.0
        expected_result.max_range = 1.0

        self.assertEqual(result,expected_result)

    def test_get_parameter_value(self):
        result = self._sc.get_parameter_value(1,1)
        expected_result = 0

        self.assertEqual(result,expected_result)

    def test_get_parameter_value_normalised(self):
        result = self._sc.get_parameter_value_normalised(1,1)
        expected_result = 0

        self.assertEqual(result,expected_result)

    def test_get_parameter_value_as_string(self):
        result = self._sc.get_parameter_value_as_string(1,1)
        expected_result = '1.0'

        self.assertEqual(result, expected_result)

    # TODO: Not implemented in sushi yet

    # def test_get_string_property_value(self):
    #     result = self._sc.get_string_property_value(1,1)
    #     expected_result = '1'

    #     self.assertEqual(result, expected_result)

    def test_set_parameter_value(self):
        wait_time = 0.5
        self._sc.set_parameter_value(1,1,1)
        time.sleep(wait_time)
        result = self._sc.get_parameter_value(1,1)
        expected_result = 1

        self.assertEqual(result, expected_result)

        self._sc.set_parameter_value(1,1,0)
        time.sleep(wait_time)
        result = self._sc.get_parameter_value(1,1)
        expected_result = 0

        self.assertEqual(result, expected_result)

    def test_set_parameter_value_normalised(self):
        wait_time = 0.5

        self._sc.set_parameter_value_normalised(1,1,1)
        time.sleep(wait_time)
        result = self._sc.get_parameter_value_normalised(1,1)
        expected_result = 1

        self.assertEqual(result, expected_result)

        self._sc.set_parameter_value_normalised(1,1,0)
        time.sleep(wait_time)
        result = self._sc.get_parameter_value_normalised(1,1)
        expected_result = 0

        self.assertEqual(result, expected_result)

    # TODO: Not implemented in sushi yet
    # def test_set_string_property_value(self):
    #     self._sc.set_string_property_value(1,1,'1')
    #     result = self._sc.get_string_property_value(1,1)
    #     expected_result = '1'

    #     self.assertEqual(result, expected_result)

    #     self._sc.set_string_property_value(1,1,'0')
    #     result = self._sc.get_string_property_value(1,1)
    #     expected_result = '0'

    #     self.assertEqual(result, expected_result)



if __name__ == '__main__':
    unittest.main()
