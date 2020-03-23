#%%
import numpy as np
import pandas as pd

#%%
from libQueue import LibQueue
from library import Library

lib_queue = LibQueue()

def findLibQueue(book_scores, lib_stats, bookCols, N, L, D, Wi, file):
    global lib_queue
    shipped_t = np.ones(N, bool) # this is technically 'not_shipped_t' but ...
    today = 0
    index_copy = np.arange(L)
    while today < D:
        scores = book_scores['score'].to_numpy()
        books = lib_stats[bookCols].to_numpy()
        R = lib_stats['shipRate'].to_numpy()
        I = lib_stats['signUpTime'].to_numpy()

        # TODO: remove already shipped books
        books = shipped_t*books

        # get sorted lib scores
        book_inds = np.arange(N)*books
        lib_scores = scores[book_inds]
        lib_scores[~books] = 0
        lib_scores *= -1
        lib_scores.sort(axis=1)
        lib_scores *= -1

        # days it takes each lib to ship. not needed?
        # dts = np.ceil(np.sum(books, axis=1)/R)

        # actual available shipping days for each lib
        dtsA = D-today-I
        dtsA[dtsA < 0] = 0
        # books each lib can ship in available days.
        #  truncated to N. cant ship more than there are
        books_shippable = dtsA*R
        books_shippable[books_shippable > N] = N
        books_shippable = np.expand_dims(books_shippable, axis=1)

        shippable_mask = np.arange(N)*np.ones_like(lib_scores)
        shipped_all = (shippable_mask>=books_shippable)
        lib_scores[shipped_all] = 0

        # actual lib scores (from only the books it can ship)
        lscores = np.sum(lib_scores, axis=1)
        # factor in sigup time. Balance between signing up highscore libs only and many libs
        I.astype('float64')
        I = I / np.max(I)
        lscores = lscores / np.max(lscores)
        lscores = lscores + Wi/I
        # get best lib
        libo_i = np.argmax(lscores)
        # get the lib
        lib_o = lib_stats.loc[libo_i]
        # get books lib_o shipped
        books_o = books[libo_i]
        scores_o = scores[book_inds[libo_i]]
        scores_o[~books_o] = 0
        book_inds_o = book_inds[libo_i]
        scores_o_sort = np.argsort(scores_o*-1)
        
        # update shipped books with books from lib_o
        shipped_o_mask = books_o[scores_o_sort]*~(shipped_all[libo_i])
        libo_shipped = book_inds_o[scores_o_sort][shipped_o_mask]
        shipped_t[libo_shipped] = False

        Io, Ro = lib_o['signUpTime'], lib_o['shipRate']
        libO = Library(
            lib_o,
            libo_shipped.tolist()
            )
        # add libO to queue
        lib_queue.insert(libO)
        # advance the date
        today += lib_o['signUpTime']
        # remove signed up lib for next iter
        lib_stats = lib_stats.drop(libo_i).reset_index(drop=True)

        libo_i_orig = index_copy[libo_i]
        index_copy = np.delete(index_copy, libo_i)
        if len(libo_shipped) <= 10:
            print('%s: signed up lib %d to ship %s'%(file, libo_i_orig,libo_shipped))
        else:
            print('%s: signed up lib %d to ship %d books'%(file, libo_i_orig,len(libo_shipped)))
        yield

# %%
from organisation import Organisation
def computeScore(totalTime, books, lib_queue, file):
    organisation = Organisation(books, totalTime, lib_queue)
    for day, score in organisation.passDays():
        print(f'{file}: day: {day}, score: {score}')
        yield score

#%%
files = [
    'a_example.txt',
    'b_read_on.txt',
    'c_incunabula.txt',
    'd_tough_choices.txt',
    'e_so_many_books.txt',
    'f_libraries_of_the_world.txt'
]
#%%
D, book_scores, lib_stats, bookCols = read_ip(f'../{files[0]}')
N = len(bookCols)
L = len(lib_stats)
flag1 = 0
next(findLibQueue(book_scores, lib_stats, bookCols, N, L, D, 1, files[0]))
#%%
from read_ip import read_ip
def runfile(file, Wi):
    print('task:', file)
    D, book_scores, lib_stats, bookCols = read_ip(f'../{file}')
    N = len(bookCols)
    L = len(lib_stats)
    flag1 = 0
    gen1 = findLibQueue(book_scores, lib_stats, bookCols, N, L, D, Wi, file)
    gen2 = computeScore(D, book_scores, lib_queue, file)
    score = 0
    while True:
        if not flag1:
            try:
                next(gen1)
            except Exception as e:
                print("Loaded all libraries!!!")
                flag1 = 1
        try:
            score = next(gen2)
        except StopIteration:
            break
    return score
# %%
runfile(files[0], 1)

#%%
from multiprocessing import Pool
nproc = 5
if __name__ == "__main__":
    with Pool(nproc) as pool:
        scores = dict(zip(files, pool.map(runfile, files)))
        print('final scores: \n', scores)

# %%
import cProfile
def profiling_tests():
    def getQ():
        findLibQueue(book_scores, lib_stats, bookCols, N, L, D, 'f')
    cProfile.run('getQ()', 'statsQ')

    import pstats
    p = pstats.Stats('statsQ')
    p.strip_dirs().sort_stats('cumulative').print_stats()
