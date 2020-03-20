import unittest
import pandas as pd
import numpy as np
from Simulator.read_ip import read_ip

class TestReadIP(unittest.TestCase):

    def test_read_ip(self):
        bookScores, libStats = read_ip('a_example.txt')
        self.assertIsInstance(bookScores, pd.DataFrame)
        self.assertIsInstance(libStats, pd.DataFrame)
        self.assertEqual(len(bookScores), 6)
        self.assertEqual(len(libStats), 2)
        self.assertEqual(bookScores.loc[3, 'score'], 6)
        self.assertEqual(libStats.loc[1, 'books'], (0, 2, 3, 5))
        self.assertEqual(libStats['totalScore'].sum(), 31)

if __name__ == '__main__':
    unittest.main()