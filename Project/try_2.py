
import numpy as np
import pandas as pd
from Simulator.libQueue import LibQueue
from Simulator.library import Library
from Simulator.read_ip2 import read_ip
from Simulator.organisation import Organisation
import time



def getStats(fileName, bookcsv, libcsv):    
    totalTime, books, libStats = read_ip(fileName, bookcsv, libcsv)
    libStats.insert(1, 'paramX', (libStats['noOfBooks']/libStats['shipRate'])/(totalTime-libStats['signUpTime']))
    # print(libStats.dtypes)
    # print(f'Memory usage: {libStats.memory_usage(deep=True).sum()}')
    
    # numColumns = libStats.select_dtypes(include=['object'])
    # numColumns = numColumns.astype({'library': 'int', 'paramX': 'float', 'noOfBooks': 'int', 'signUpTime': 'int', 'shipRate': 'int', 'totalScore': 'int'})
    # libStats.loc[:,:'totalScore'] = numColumns.apply(pd.to_numeric, downcast='unsigned')
    # print(libStats.dtypes)
    # print(f'Memory usage: {libStats.memory_usage(deep=True).sum()}')

    # libStats.loc[:, 'b0':] = libStats.loc[:, 'b0':].astype('category')
    # print(libStats.dtypes)
    # print(f'Memory usage: {libStats.memory_usage(deep=True).sum()}')
    return totalTime, books, libStats

# getStats('b_read_on.txt')
libQueue = LibQueue()
def iterOptimise(totalTime, books, libStats):
    # Initialise stuff
    # saveTime = totalTime
    # Create paramX variablefileName
    # count = 1
    # Loop till libStats dataFrame is empty
    while True:
        # Update number of books remaining, net score from those books, and paramX: (netNoOfBooks/shipRate)/(netTotalTime-1)
        libStats['totalScore'] = np.sum(np.multiply(np.array(books)[:,1], np.array(libStats.loc[:, 'b0':])), axis=1)
        libStats['noOfBooks'] = np.sum(np.array(libStats.loc[:, 'b0':]), axis=1)
        libStats['paramX'] = (libStats['signUpTime']/(libStats['totalScore']*libStats['totalScore']*libStats['shipRate']))
        # libStats.eval('paramX = (noOfBooks/shipRate)/(@totalTime-signUpTime', inplace=True)
        # Sort libStats 
        libStats.sort_values(by=['paramX'], ascending=[True], kind='mergesort', inplace=True, ignore_index=True)
        # Insert top library into queue
        libQueue.insert(Library(libStats.iloc[0], np.where(np.array(libStats.iloc[0].iloc[list(libStats.iloc[0].index).index('b0'):]))[0].tolist()))
        # Update remaining time
        totalTime -= libQueue.tail.signUpTime

        # Remove all books present in the inserted lib
        tic = time.perf_counter()
        libStats.loc[:, 'b0':] = elementWiseMultiply(np.where(np.array(libStats.loc[0, 'b0':]), False, True), np.array(libStats.loc[:, 'b0':]))
        toc = time.perf_counter()
        print(f'Multiplication took {toc-tic} seconds')
        # Delete the lib from libStats
        tic = time.perf_counter()
        libStats.drop(0,inplace=True)
        print(f'Dropping took {time.perf_counter()-tic} seconds')
        # libStats.iloc[0, :] = 0
        # Delete all libs whose sign-up time is more than the remaining time
        # libStats = libStats[libStats.signUpTime<totalTime]
        tic = time.perf_counter()
        libStats.query('signUpTime<@totalTime', inplace=True)
        print(f'Query took {time.perf_counter()-tic} seconds')
        # libStats[libStats.signUpTime>=totalTime]=0

        # print(libStats)
        yield
        # print(f'Loaded {count} libraries to queue')
        # count += 1

        if not (len(libStats) and totalTime):
            raise StopIteration
    
# @jit()
# @vectorize()
def elementWiseMultiply(array1, array2):
    return array1 & array2
    


def computeScore(totalTime, books, libQueue):
    organisation = Organisation(books, totalTime, libQueue)
    for day, score in organisation.passDays():
        print(f'day: {day}, score: {score}')
        yield score


if __name__ == '__main__':
    totalTime, books, libStats = getStats('c_incunabula.txt', 'c_books.csv', 'c_libStats.csv')
    flag1 = 0
    gen1 = iterOptimise(totalTime, books, libStats)
    gen2 = computeScore(totalTime, books, libQueue)

    while True:
        if not flag1:
            try:
                next(gen1)
            except Exception as e:
                print("Loaded all libraries!!!")
                flag1 = 1
        try:
            next(gen2)
        except StopIteration:
            break

    # for cat in iterOptimise(totalTime, books, libStats):
    #     print(cat)

    # g = iterOptimise(totalTime, books, libStats)
    # next(g)
    # next(g)