#%%
import numpy as np
import pandas as pd

#%%
# def signup(libs, scores, libOrder):
#     scores = pd.to_numeric(scores['score']).to_numpy()
#     books = libs['books'].to_numpy()
#     print(books.dtype)
#     # libs['scores'] = scores['score'][libs['books']]
#     # print(libs['scores'])

#%%
from libQueue import LibQueue
from library import Library

def findLibQueue(book_scores, lib_stats, bookCols, N, L, D):
    shipped_t = np.ones(N, bool) # this is technically 'not_shipped_t' but ...
    libQueue = LibQueue()
    today = 0
    index_copy = np.arange(L)
    for i, lib in lib_stats.iterrows():
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
        lib_scores_act = np.sum(lib_scores, axis=1)
        libo_i = np.argmax(lib_scores_act)
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
            Io, Ro,
            book_inds_o[books_o],
            libo_shipped
            )
        # add libO to queue
        libQueue.insert(libO)
        # advance the date
        today += lib_o['signUpTime']
        # remove signed up lib for next iter
        lib_stats = lib_stats.drop(libo_i).reset_index(drop=True)

        libo_i_orig = index_copy[libo_i]
        index_copy = np.delete(index_copy, libo_i)
        if len(libo_shipped) <= 10:
            print('signed up lib %d to ship %s'%(libo_i_orig,libo_shipped))
        else:
            print('signed up lib %d to ship %d books'%(libo_i_orig,len(libo_shipped)))
    # return queue
    return libQueue

    
#%%
from read_ip import read_ip
if __name__ == "__main__":
    book_scores, lib_stats, bookCols, N, L, D = read_ip('../b_read_on.txt')

#%%
scores = np.array(book_scores['score'])
print(scores)
print(lib_stats['books'])
# findLibQueue(scores, lib_stats, 7)

# %%
import cProfile
def getQ():
    findLibQueue(book_scores, lib_stats, bookCols, N, L, D)
cProfile.run('getQ()', 'statsQ')

# %%
import pstats
p = pstats.Stats('statsQ')
p.strip_dirs().sort_stats('cumulative').print_stats()

# %%
