# hashcode2020

class Library:
    """Lib object created to scan booksToScan"""
    def __init__(self, signUpTime, shipRate, libBooks, booksToScan):
        assert booksToScan in libBooks, "One or more of the books to scan do not exist in library!"
        self.signUpTime = signUpTime
        self.shipRate = shipRate
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
            return scannedBooks
        else:
            scannedBooks = self.booksToScan[:]
            self.booksToScan = None
            return scannedBooks