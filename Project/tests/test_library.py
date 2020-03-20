import unittest
import pandas as pd
import numpy as np
from Simulator.read_ip import read_ip
from Simulator.library import Library

class TestLibrary(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        *_, libStat = read_ip('a_example.txt')
        self.lib0 = Library(*libStat.iloc[0, 1:4], [0,1,2,3,4])
        self.lib1 = Library(*libStat.iloc[1, 1:4], [5])
        self.lib0.next = self.lib1
        self.lib1.previous = self.lib0

    @classmethod
    def tearDownClass(self):
        del self.lib0
        del self.lib1

    def test_libraryInitialisation(self):
        self.assertIsInstance(self.lib0, Library)
        self.assertIsInstance(self.lib1, Library)
        self.assertEqual(self.lib0.booksToScan, [0,1,2,3,4])
        self.assertEqual(self.lib1.booksToScan, [5])
        self.assertEqual(self.lib0.signUpTime, 2)
        self.assertEqual(self.lib0.shipRate, 2)
        self.assertEqual(self.lib1.signUpTime, 3)
        self.assertEqual(self.lib1.shipRate, 1)
        self.assertIs(self.lib0.next, self.lib1)
        self.assertIs(self.lib1.previous, self.lib0)
        self.assertFalse(self.lib0.previous)
        self.assertFalse(self.lib1.next)

    def test_librarySignup(self):
        timeLeft0 = self.lib0.signUp()
        self.assertEqual(timeLeft0, 2)
        timeLeft0 = self.lib0.signUp()
        self.assertEqual(timeLeft0, 1)
        timeLeft0 = self.lib0.signUp()
        self.assertEqual(timeLeft0, 0)

    def test_libraryScanBooks(self):
        scannedBooks = self.lib0.scanBooks()
        self.assertEqual(len(scannedBooks), 2)
        self.assertEqual(scannedBooks, [0, 1])
        self.assertEqual(self.lib0.scanBooks(), [2,3])
        self.assertEqual(self.lib0.scanBooks(), [4])