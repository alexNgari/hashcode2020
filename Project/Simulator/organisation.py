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
        self.numSignedUp = 0
    
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
                    self.numSignedUp += 1
                    books = self.libQueue.current.booksToScan
                    scores = [self.books.iloc[x, 1] for x in books]
                    sortedBooks = [book for score, book in sorted(zip(scores, books))]
                    self.libQueue.current.booksToScan = sortedBooks[::-1]
                    print(f'Signed up lib: {self.libQueue.current.id} \t noOfBooks: {len(sortedBooks)} \t shipRate: {self.libQueue.current.shipRate} \t serial: {self.numSignedUp} \t day: {day}')
                    self.libQueue.current = self.libQueue.current.next
                    self.libQueue.removeFromTop()
                    if self.libQueue.current:
                        self.libQueue.current.signUp()
            # Scan books in already signed-up libraries
            for lib in self.signedUpLibs[:]:
                self.scannedBooks = list(set(self.scannedBooks + lib.scanBooks()))
                if not lib.booksToScan:
                    self.signedUpLibs.remove(lib)
            # print(day, self.scannedBooks)
            if self.libQueue.isEmpty() and not self.signedUpLibs:
                # print(f'Scanned all books in {day} days: If you don\'t get the max score you fucked up.')
                scannedAllBooks = True

            # current_score = self.__computeScore()
            yield day
    
    
    def computeScore(self):
        self.score = np.array(self.books['score'].iloc[self.scannedBooks]).sum()
        return self.score

    def getScore(self):
        return self.score

    def getScannedBooks(self):
        return self.scannedBooks
                