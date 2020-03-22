# hashcode2020
import numpy as np
import pandas as pd

class Library:
    """Lib object created to scan booksToScan"""
    def __init__(self, libRecord, booksToScan):
        """Takes in the a pandas series, and a list containing books to scan.
        Obtain said series from indexing the record of the subject lib in the lib_stats dataframe"""
        libBooks = np.where(np.array(libRecord.iloc[list(libRecord.index).index('b0'):]))[0].tolist()
        assert all(book in libBooks for book in booksToScan), "One or more of the books to scan do not exist in library!"
        self.signUpTime = libRecord['signUpTime']
        self.shipRate = libRecord['shipRate']
        self.booksToScan = booksToScan
        self.next = None
        self.previous = None
    
    def signUp(self):
        """Reduce sign-up time by a day, return time before reduction"""
        timeLeft = self.signUpTime
        self.signUpTime -= 1
        return timeLeft         # So that we can check if time==0, without erroneously beginning scanning before time

    def scanBooks(self):
        """Return shipped books, constrained by ship-rate"""
        if len(self.booksToScan) > self.shipRate:
            scannedBooks = self.booksToScan[:self.shipRate]
            del self.booksToScan[:self.shipRate]
            return [*scannedBooks] #if len(scannedBooks)>1 else [scannedBooks]
        else:
            scannedBooks = self.booksToScan[:]
            self.booksToScan = None
            return [*scannedBooks] #if len(scannedBooks)>1 else [scannedBooks]