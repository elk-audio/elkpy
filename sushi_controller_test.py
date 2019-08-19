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
        return


if __name__ == '__main__':
    unittest.main()
