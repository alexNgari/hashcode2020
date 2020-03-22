## Call everything from here

import numpy as np
from Simulator.libQueue import LibQueue
from Simulator.library import Library
from Simulator.read_ip import read_ip
from Simulator.organisation import Organisation

def iterOptimise(fileName):
    # Initialise stuff
    totalTime, books, libStats = read_ip(fileName)
    libQueue = LibQueue()
    saveTime = totalTime
    # Create paramX variable
    libStats.insert(1, 'paramX', (libStats['noOfBooks']/libStats['shipRate'])/(totalTime-libStats['signUpTime']))
    print(libStats)
    count = 1
    # Loop till libStats dataFrame is empty
    while True:
        # Update number of books remaining, net score from those books, and paramX: (netNoOfBooks/shipRate)/(netTotalTime-1)
        libStats['totalScore'] = np.sum(np.multiply(np.array(books)[:,1], np.array(libStats.loc[:, 'b0':])), axis=1)
        libStats['noOfBooks'] = np.sum(np.array(libStats.loc[:, 'b0':]), axis=1)
        libStats['paramX'] = (libStats['noOfBooks']/libStats['shipRate'])/(totalTime-libStats['signUpTime'])
        # Sort libStats 
        libStats.sort_values(by=['totalScore', 'signUpTime', 'paramX'], ascending=[False, True, True], kind='mergesort', inplace=True, ignore_index=True)
        # Insert top library into queue
        libQueue.insert(Library(libStats.iloc[0], np.where(np.array(libStats.iloc[0].iloc[list(libStats.iloc[0].index).index('b0'):]))[0].tolist()))
        # Update remaining time
        totalTime -= libQueue.tail.signUpTime
        # Remove all books present in the inserted lib
        libStats.loc[:, 'b0':] = np.multiply(np.where(np.array(libStats.loc[0, 'b0':]), False, True), np.array(libStats.loc[:, 'b0':]))
        # Delete the lib from libStats
        libStats.drop(0,inplace=True)
        # libStats.iloc[0, :] = 0
        # Delete all libs whose sign-up time is more than the remaining time
        libStats = libStats[libStats.signUpTime<totalTime]
        # libStats[libStats.signUpTime>=totalTime]=0

        print(f'Loaded {count} libraries to queue')
        count += 1

        if not len(libStats):
            break
    
    return saveTime, books, libQueue

def computeScore(totalTime, books, libQueue):
    organisation = Organisation(books, totalTime, libQueue)    
    for day, score in organisation.passDays():
        print(day, score)
    return score


time, books, libQueue = iterOptimise('c_incunabula.txt')
print(computeScore(time, books, libQueue))

