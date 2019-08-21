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

        #TODO: Recording mode does not seem to work

        for i in range (0,3):
            self._sc.set_playing_mode(i)
            time.sleep(wait_time)
            self.assertEqual(self._sc.get_playing_mode(),i)
            time.sleep(wait_time)

        self._sc.set_playing_mode(self._sc.PlayingMode.DUMMY)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_playing_mode(),int(self._sc.PlayingMode.DUMMY))
        time.sleep(wait_time)
        self._sc.set_playing_mode(self._sc.PlayingMode.STOPPED)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_playing_mode(),int(self._sc.PlayingMode.STOPPED))
        time.sleep(wait_time)
        self._sc.set_playing_mode(self._sc.PlayingMode.PLAYING)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_playing_mode(),int(self._sc.PlayingMode.PLAYING))
        time.sleep(wait_time)
        # self._sc.set_playing_mode(self._sc.PlayingMode.RECORDING)
        # time.sleep(wait_time)
        # self.assertEqual(self._sc.get_playing_mode(),int(self._sc.PlayingMode.RECORDING))
        # time.sleep(wait_time)

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
        self.assertEqual(self._sc.get_sync_mode(),0)

    def test_set_sync_mode(self):
        wait_time = 0.1

        # TODO: LINK=3 mode doesn't seem to work

        for i in range(0,3):
            self._sc.set_sync_mode(i)
            time.sleep(wait_time)
            self.assertEqual(self._sc.get_sync_mode(), i)
            time.sleep(wait_time)

        self._sc.set_sync_mode(self._sc.SyncMode.DUMMY)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_sync_mode(), int(self._sc.SyncMode.DUMMY))
        time.sleep(wait_time)
        self._sc.set_sync_mode(self._sc.SyncMode.INTERNAL)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_sync_mode(), int(self._sc.SyncMode.INTERNAL))
        time.sleep(wait_time)
        self._sc.set_sync_mode(self._sc.SyncMode.MIDI)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_sync_mode(), int(self._sc.SyncMode.MIDI))
        time.sleep(wait_time)
        # self._sc.set_sync_mode(self._sc.SyncMode.LINK)
        # time.sleep(wait_time)
        # self.assertEqual(self._sc.get_sync_mode(), int(self._sc.SyncMode.LINK))
        # time.sleep(wait_time)

        self._sc.set_sync_mode(0)
        time.sleep(wait_time)
        self.assertEqual(self._sc.get_sync_mode(), 0)
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
        # TODO: data types of this doesn't match the proto file. doesn't have id, label and processor_count
        track_list.append(sushi_rpc_pb2.TrackInfo(
                name = 'main',
                input_channels = 2,
                input_busses = 1,
                output_channels = 2,
                output_busses = 1
            ))

        expected_result = sushi_rpc_pb2.TrackInfoList(
            tracks = track_list
        )
        self.assertEqual(self._sc.get_tracks(),expected_result)

    def test_keyboard_control(self):
        wait_time = 0.5

        self._sc.send_note_on(0,63,1,127)
        self._sc.send_aftertouch(0,1,63)
        self._sc.send_modulation(0,1,63)
        time.sleep(wait_time)
        self._sc.send_pitch_bend(0,1,127)
        time.sleep(wait_time)
        self._sc.send_note_off(0,63,1,127)

    def test_get_engine_timings(self):
        result_average, result_min, result_max = self._sc.get_engine_timings()
        
        self.assertAlmostEqual(result_average,0.1)
        self.assertAlmostEqual(result_min,0.2)
        self.assertAlmostEqual(result_max,5.0)

    def test_get_track_timings(self):
        for i in range(0,8):
            result_average, result_min, result_max = self._sc.get_track_timings(i)
        
            self.assertAlmostEqual(result_average,0.05)
            self.assertAlmostEqual(result_min,0.1)
            self.assertAlmostEqual(result_max,0.02)

    def test_get_processor_timings(self):
        result_average, result_min, result_max = self._sc.get_processor_timings(0)
        
        self.assertAlmostEqual(result_average,0.05)
        self.assertAlmostEqual(result_min,0.1)
        self.assertAlmostEqual(result_max,0.02)

        result_average, result_min, result_max = self._sc.get_processor_timings(1)
        
        self.assertAlmostEqual(result_average,0.05)
        self.assertAlmostEqual(result_min,0.1)
        self.assertAlmostEqual(result_max,0.02)

    # TODO: make a good test
    def test_reset_timings(self):
        self._sc.reset_all_timings()
        self._sc.reset_processor_timings(0)
        self._sc.reset_track_timings(0)

    def test_get_track_id(self):
        result = self._sc.get_track_id('main')
        expected_result = 0

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
