# hashcode2020

import pandas as pd
import numpy as np

class Organisation:
    """Simulates the operations
    Initialise with books dataFrame, time int and libqueue linkedlist"""
    def __init__(self, books, time, libQueue):
        self.books = books      # all available books
        self.time = time        # total alloted time
        self.libQueue = libQueue
        self.signedUpLibs = []
        self.scannedBooks = []
        self.score = 0
    
    def passDays(self):
        """Iterate over in for loop to simulate operations: returns day, score"""
        self.libQueue.current = self.libQueue.head
        scannedAllBooks = False
        for day in range(1, self.time+1):
            if scannedAllBooks:
                raise StopIteration
            # Continue with signup process for libs in queue
            if not self.libQueue.isEmpty():
                timeleft = self.libQueue.current.signUp()
                if timeleft == 0:
                    self.signedUpLibs.append(self.libQueue.current)
                    self.libQueue.current = self.libQueue.current.next
                    self.libQueue.removeFromTop()
            # Scan books in already signed-up libraries
            for lib in self.signedUpLibs[:]:
                self.scannedBooks = list(set(self.scannedBooks + lib.scanBooks()))
                if not lib.booksToScan:
                    self.signedUpLibs.remove(lib)
            # print(day, self.scannedBooks)
            if self.libQueue.isEmpty() and not self.signedUpLibs:
                # print(f'Scanned all books in {day} days: If you don\'t get the max score you fucked up.')
                scannedAllBooks = True

            current_score = self.__computeScore()
            yield day, current_score
    
    
    def __computeScore(self):
        self.score = np.array(self.books['score'].iloc[self.scannedBooks]).sum()
        return self.score

    def getScore(self):
        return self.score

    def getScannedBooks(self):
        return self.scannedBooks
                