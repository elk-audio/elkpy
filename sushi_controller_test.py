import sys
import unittest
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
        # for i in range (0,3):
        #     self._sc.set_playing_mode(i)
        #     self.assertEqual(self._sc.get_playing_mode(),i)

        self._sc.set_playing_mode(self._sc.PlayingMode.DUMMY)
        self.assertEqual(self._sc.get_playing_mode(),self._sc.PlayingMode.DUMMY)
        self._sc.set_playing_mode(self._sc.PlayingMode.STOPPED)
        self.assertEqual(self._sc.get_playing_mode(),self._sc.PlayingMode.STOPPED)
        self._sc.set_playing_mode(self._sc.PlayingMode.PLAYING)
        self.assertEqual(self._sc.get_playing_mode(),self._sc.PlayingMode.PLAYING)
        self._sc.set_playing_mode(self._sc.PlayingMode.RECORDING)
        self.assertEqual(self._sc.get_playing_mode(),self._sc.PlayingMode.RECORDING)

    def test_set_playing_mode_false(self):
        return


if __name__ == '__main__':
    unittest.main()
