import unittest
import pandas as pd
import numpy as np
from Simulator.read_ip import read_ip
from Simulator.library import Library
from Simulator.libQueue import LibQueue
from Simulator.organisation import Organisation

class TestOrganisation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        totalTime, bookScores, libStat = read_ip('a_example.txt')
        self.lib0 = Library(*libStat.iloc[0, 1:4], [0,1,2,3,4])
        self.lib1 = Library(*libStat.iloc[1, 1:4], [5])
        self.libQueue = LibQueue(self.lib0)
        self.libQueue.insert(self.lib1)
        self.organisation = Organisation(bookScores, totalTime, self.libQueue)

    @classmethod
    def tearDownClass(self):
        del self.organisation
        del self.libQueue
        del self.lib0
        del self.lib1

    def test_initialisation(self):
        self.assertIsInstance(self.organisation, Organisation)
        self.assertEqual(self.organisation.books['book'].tolist(), [0,1,2,3,4,5])
        self.assertEqual(self.organisation.time, 7)
        self.assertIs(self.organisation.libQueue, self.libQueue)
        self.assertFalse(self.organisation.signedUpLibs)
        self.assertFalse(self.organisation.scannedBooks)
        self.assertEqual(self.organisation.score, 0)

    def test_passDays(self):
        dayCounter = 0
        for day, _ in self.organisation.passDays():
            dayCounter += 1
            self.assertEqual(day, dayCounter)
        self.assertEqual(dayCounter, 7)
        self.assertEqual(self.organisation.score, 21)
        self.assertTrue(all(book in self.organisation.scannedBooks for book in self.organisation.books['book'].tolist()))

    def test_computeScore(self):
        with self.assertRaises(AttributeError):
            self.organisation.__computeScore()

    def test_getScore(self):
        self.assertEqual(self.organisation.getScore(), self.organisation.score)

    def test_getScannedBooks(self):
        self.assertEqual(self.organisation.getScannedBooks(), self.organisation.scannedBooks)
        