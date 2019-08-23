import sys
import unittest
import time
from sushicontroller import SushiController
from sushicontroller import sushi_rpc_pb2

SUSHI_ADDRESS = ('localhost:51051')

class TestSushiController(unittest.TestCase):
    def setUp(self):
        self._sc = SushiController(SUSHI_ADDRESS)

    def test_get_samplerate(self):
        self.assertEqual(self._sc.get_samplerate(), 48000.0)

    def test_get_playing_mode(self):
        self.assertEqual(self._sc.get_playing_mode(), 1)

    def test_set_playing_mode_positive(self):
        wait_time = 0.1

        #TODO: DUMMY NOT AVAIALBLE

        for i in range (1,4):
            self._sc.set_playing_mode(i)
            time.sleep(wait_time)
            self.assertEqual(self._sc.get_playing_mode(),i)
            time.sleep(wait_time)

        self._sc.set_playing_mode(self._sc.PlayingMode.STOPPED)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_playing_mode(),int(self._sc.PlayingMode.STOPPED))
        time.sleep(wait_time)
        self._sc.set_playing_mode(self._sc.PlayingMode.PLAYING)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_playing_mode(),int(self._sc.PlayingMode.PLAYING))
        time.sleep(wait_time)
        self._sc.set_playing_mode(self._sc.PlayingMode.RECORDING)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_playing_mode(),int(self._sc.PlayingMode.RECORDING))
        time.sleep(wait_time)

        self._sc.set_playing_mode(1)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_playing_mode(),1)


    def test_set_playing_mode_false(self):
        wait_time = 0.1

        self._sc.set_playing_mode(-1)
        time.sleep(wait_time)
        self.assertNotEqual(self._sc.get_playing_mode(),-1)
        time.sleep(wait_time)

        self._sc.set_playing_mode(4)
        time.sleep(wait_time)
        self.assertNotEqual(self._sc.get_playing_mode(),4)
        time.sleep(wait_time)

    def test_get_sync_mode(self):
        self.assertEqual(self._sc.get_sync_mode(),1)

    def test_set_sync_mode(self):
        wait_time = 0.1

        # TODO: DUMMY=0 mode doesn't seem to work

        for i in range(1,4):
            self._sc.set_sync_mode(i)
            time.sleep(wait_time)
            self.assertEqual(self._sc.get_sync_mode(), i)
            time.sleep(wait_time)

        self._sc.set_sync_mode(self._sc.SyncMode.INTERNAL)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_sync_mode(), int(self._sc.SyncMode.INTERNAL))
        time.sleep(wait_time)
        self._sc.set_sync_mode(self._sc.SyncMode.MIDI)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_sync_mode(), int(self._sc.SyncMode.MIDI))
        time.sleep(wait_time)
        self._sc.set_sync_mode(self._sc.SyncMode.LINK)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_sync_mode(), int(self._sc.SyncMode.LINK))
        time.sleep(wait_time)

        self._sc.set_sync_mode(1)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_sync_mode(), 1)
        time.sleep(wait_time)

    def test_get_tempo(self):
        self.assertEqual(self._sc.get_tempo(),120)

    def test_set_tempo(self):
        wait_time = 0.1

        for i in range (1,11):
            self._sc.set_tempo(i*20)
            time.sleep(wait_time)
            self.assertEqual(self._sc.get_tempo(), i*20)
            time.sleep(wait_time)

        self._sc.set_tempo(120)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_tempo(), 120)
        time.sleep(wait_time)

    def test_get_time_signature(self):
        self.assertEqual(self._sc.get_time_signature(), (4,4))

    def test_set_time_signature(self):
        wait_time = 0.1

        for i in range (1,12):
            self._sc.set_time_signature(i,4)
            time.sleep(wait_time)
            self.assertEqual(self._sc.get_time_signature(),(i,4))
            time.sleep(wait_time)

            self._sc.set_time_signature(i,8)
            time.sleep(wait_time)
            self.assertEqual(self._sc.get_time_signature(),(i,8))
            time.sleep(wait_time)

        self._sc.set_time_signature(4,4)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_time_signature(),(4,4))
        time.sleep(wait_time)

    def test_get_tracks(self):
        track_list = []
        # TODO: data types of this doesn't match the proto file. doesn't have id and label
        track_list.append(sushi_rpc_pb2.TrackInfo(
                name = 'main',
                input_channels = 2,
                input_busses = 1,
                output_channels = 2,
                output_busses = 1,
                processor_count = 2
            ))

        expected_result = sushi_rpc_pb2.TrackInfoList(
            tracks = track_list
        )
        self.assertEqual(self._sc.get_tracks(),expected_result)

class TestSushiControllerKeyboardControl(unittest.TestCase):
    def setUp(self):
        self._sc = SushiController(SUSHI_ADDRESS)

    def test_keyboard_control(self):
        wait_time = 0.5

        self._sc.send_note_on(0,63,1,127)
        self._sc.send_aftertouch(0,1,63)
        self._sc.send_modulation(0,1,63)
        time.sleep(wait_time)
        self._sc.send_pitch_bend(0,1,127)
        time.sleep(wait_time)
        self._sc.send_note_off(0,63,1,127)

class TestSushiControllerCPUTimings(unittest.TestCase):
    def setUp(self):
        self._sc = SushiController(SUSHI_ADDRESS)

    def test_get_engine_timings(self):
        self._sc.reset_all_timings()
        time.sleep(0.75)
        result_average, result_min, result_max = self._sc.get_engine_timings()
        
        self.assertGreater(result_average,0)
        self.assertGreater(result_min,0)
        self.assertGreater(result_max,0)

    def test_get_track_timings(self):
        for i in range(0,3):
            with self.subTest(track_id=i):
                result_average, result_min, result_max = self._sc.get_track_timings(i)
        
                self.assertGreater(result_average,0)
                self.assertGreater(result_min,0)
                self.assertGreater(result_max,0)

    def test_get_processor_timings(self):
        for i in range(0,3):
            with self.subTest(processor_id = i):
                result_average, result_min, result_max = self._sc.get_processor_timings(i)
        
                self.assertGreater(result_average,0)
                self.assertGreater(result_min,0)
                self.assertGreater(result_max,0)

    # TODO: make a good test
    def test_reset_timings(self):
        self._sc.reset_all_timings()
        self._sc.reset_processor_timings(0)
        self._sc.reset_track_timings(0)

class TestSushiControllerTrackControl(unittest.TestCase):
    def setUp(self):
        self._sc = SushiController(SUSHI_ADDRESS)

    def test_get_track_id(self):
        result = self._sc.get_track_id('main')
        expected_result = 0

        self.assertEqual(result, expected_result)

    def test_get_track_info(self):
        result = self._sc.get_track_info(0)
        expected_result = sushi_rpc_pb2.TrackInfo(
            name = 'main',
            input_channels = 2,
            input_busses = 1,
            output_channels = 2,
            output_busses = 1,
            processor_count = 2
        )

        self.assertEqual(result,expected_result)

    def test_get_track_processors(self):
        result = self._sc.get_track_processors(0)
        expected_result = sushi_rpc_pb2.ProcessorInfoList(
            processors = (
                sushi_rpc_pb2.ProcessorInfo(
                    id = 1,
                    label = 'Andes-1',
                    name = 'andes',
                    parameter_count = 8,
                    program_count = 100
                ),
                sushi_rpc_pb2.ProcessorInfo(
                    id = 2,
                    label = 'Temper',
                    name = 'Temper',
                    parameter_count = 7,
                    program_count = 5
                )
            )
        )

        self.assertEqual(result,expected_result)

    def test_get_track_parameters(self):
        result = self._sc.get_track_parameters(0)
        expected_result = sushi_rpc_pb2.ParameterInfoList(
            parameters = (
                sushi_rpc_pb2.ParameterInfo(
                    type = sushi_rpc_pb2.ParameterType(type = int(self._sc.ParameterType.FLOAT)),
                    label = 'Gain',
                    name = 'gain',
                    automatable = True,
                    min_range = -120,
                    max_range = 24
                ),
                sushi_rpc_pb2.ParameterInfo(
                    id = 1,
                    type = sushi_rpc_pb2.ParameterType(type = int(self._sc.ParameterType.FLOAT)),
                    label = 'Pan',
                    name = 'pan',
                    automatable = True,
                    min_range = -1,
                    max_range = 1
                )
            )
        )

        self.assertEqual(result,expected_result)

class TestSushiControllerProcessorControl(unittest.TestCase):
    def setUp(self):
        self._sc = SushiController(SUSHI_ADDRESS)

    def test_get_processor_id(self):
        result = self._sc.get_processor_id("andes")
        expecter_result = 1
        
        with self.subTest(test_code=1):
            self.assertEqual(result,expecter_result)

        result = self._sc.get_processor_id("Temper")
        expecter_result = 2
        
        with self.subTest(test_code=2):
            self.assertEqual(result,expecter_result)

    def test_get_processor_info(self):
        result = self._sc.get_processor_info(0)
        expected_result = sushi_rpc_pb2.ProcessorInfo(
            name = 'main',
            parameter_count = 2
        )

        with self.subTest(processorId = 0):
            self.assertEqual(result,expected_result)

        result = self._sc.get_processor_info(1)
        expected_result = sushi_rpc_pb2.ProcessorInfo(
            id = 1,
            label = 'Andes-1',
            name = 'andes',
            parameter_count = 8,
            program_count = 100
        )

        with self.subTest(processorId = 1):
            self.assertEqual(result,expected_result)

        result = self._sc.get_processor_info(2)
        expected_result = sushi_rpc_pb2.ProcessorInfo(
            id = 2,
            label = 'Temper',
            name = 'Temper',
            parameter_count = 7,
            program_count = 5
        )

        with self.subTest(processorId = 2):
            self.assertEqual(result,expected_result)

    def test_get_processor_bypass_state(self):
        result = self._sc.get_processor_bypass_state(0)
        expected_result = False

        with self.subTest(processorId = 0):
            self.assertEqual(result,expected_result)

        result = self._sc.get_processor_bypass_state(1)
        expected_result = False

        with self.subTest(processorId = 1):
            self.assertEqual(result,expected_result)

        result = self._sc.get_processor_bypass_state(2)
        expected_result = False

        with self.subTest(processorId = 2):
            self.assertEqual(result,expected_result)

    def test_set_processor_bypass_state(self):
        wait_time = 0.5
        for i in range(0,3):
            with self.subTest(processorId = i):
                self._sc.set_processor_bypass_state(i,True)
                time.sleep(wait_time)
                result = self._sc.get_processor_bypass_state(i)
                expected_result = True

                self.assertEqual(result,expected_result)

                self._sc.set_processor_bypass_state(i,False)
                time.sleep(wait_time)
                result = self._sc.get_processor_bypass_state(i)
                expected_result = False

                self.assertEqual(result,expected_result)

if __name__ == '__main__':
    unittest.main()
