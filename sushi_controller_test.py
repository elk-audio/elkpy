import sys
import unittest
import time
from sushicontroller import SushiController

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



if __name__ == '__main__':
    unittest.main()
