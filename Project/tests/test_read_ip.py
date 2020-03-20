import unittest
import pandas as pd
import numpy as np
from Simulator.read_ip import read_ip

class TestReadIP(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.totalTime, self.bookScores, self.libStats = read_ip('a_example.txt')

    @classmethod
    def tearDownClass(self):
        del self.bookScores
        del self.libStats
        

    def test_read_ip(self):
        self.assertIsInstance(self.bookScores, pd.DataFrame)
        self.assertIsInstance(self.libStats, pd.DataFrame)
        self.assertEqual(len(self.bookScores), 6)
        self.assertEqual(len(self.libStats), 2)
        self.assertEqual(self.totalTime, 7)
        self.assertEqual(self.bookScores.loc[3, 'score'], 6)
        self.assertEqual(self.libStats.loc[1, 'books'], (0, 2, 3, 5))
        self.assertEqual(self.libStats['totalScore'].sum(), 31)

if __name__ == '__main__':
    unittest.main()