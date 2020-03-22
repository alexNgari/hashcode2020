import unittest
import pandas as pd
import numpy as np
from Simulator.read_ip import read_ip
from Simulator.library import Library
from Simulator.libQueue import LibQueue

class TestLibQueue(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        *_, libStat = read_ip('a_example.txt')
        self.lib0 = Library(libStat.iloc[0], [0,1,2,3,4])
        self.lib1 = Library(libStat.iloc[1], [5])
        self.libQueue = LibQueue(self.lib0)
        self.libQueue.insert(self.lib1)

    @classmethod
    def tearDownClass(self):
        del self.lib0
        del self.lib1
        del self.libQueue

    def test_libQueueInitialisation(self):
        self.assertIsInstance(self.libQueue, LibQueue)
        self.assertIs(self.libQueue.head, self.lib0)
        self.assertIs(self.libQueue.tail, self.lib1)

    def test_insert(self):
        self.assertIs(self.libQueue.head.next, self.lib1)
        self.assertIs(self.libQueue.tail.previous, self.lib0)

    def test_isEmpty(self):
        self.assertFalse(self.libQueue.isEmpty())

    def test_iteration(self):
        counter = 0
        for lib in self.libQueue:
            self.assertIsInstance(lib, Library)
            counter += 1
        self.assertEqual(counter, 2)

    def test_removeFromTop(self):
        self.libQueue.removeFromTop()
        self.assertIs(self.libQueue.head, self.lib1)
        self.assertIs(self.libQueue.tail, self.lib1)
        self.libQueue.removeFromTop()
        self.assertFalse(self.libQueue.head or self.libQueue.tail)

