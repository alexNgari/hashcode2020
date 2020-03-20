# hashcode2020

import pandas as pd
import numpy as np

class Organisation:
    """Simulates the operations"""
    def __init__(self, books, time, libQueue):
        """Initialise with books dataFrame, time int and libqueue linkedlist"""
        self.books = books      # all available books
        self.time = time        # total alloted time
        self.libQueue = libQueue
        self.signedUpLibs = []
        self.scannedBooks = []
        self.score = 0
    
    def passDays(self):
        """Iterate over in for loop to simulate operations: returns a tuple, (day, score)"""
        for day in range(1, self.time+1):
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
            
            self.score = np.array(self.books['score'].iloc[self.scannedBooks]).sum()
            yield (day, self.score)
    
    def computeScore(self):
        self.score = np.array(self.books['score'].iloc[self.scannedBooks]).sum()
        return self.score

    def returnScore(self):
        return self.score
                