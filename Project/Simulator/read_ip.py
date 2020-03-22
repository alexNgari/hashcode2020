# hashcode 2020
#%%
import numpy as np
import pandas as pd
#%%

def read_ip(filename):
    N_books = 0     # no of books
    l_libs = 0      # no of libraries
    totalTime = 0      # no of days
    book_scores = None
    lib_stats = pd.DataFrame(columns=['noOfBooks', 'signUpTime', 'shipRate', 'totalScore']) # each lib stat = [N of books, signup time (I), ship rate (R), score of its books (bS)]
    lib_books = None
    
    with open(filename, 'r') as reader:

        lib_n_books = 0

        I_max, I_min = 0, 99999
        bS_max, bS_min = 0, 99999
        R_max, R_min = 0, 99999

        for count, line in enumerate(reader, start=1):
            data = list(map(int, line.split()))
            # sort empty lines at end of file
            if len(data) == 0:
                break
            
            if count == 1:
                # N_books l_libs d_days
                assert len(data) == 3
                [N_books, l_libs, totalTime] = data
                continue
            elif count == 2:
                # S_b0 S_b1 S_b2 ... S_bN
                assert len(data) == N_books
                book_scores = pd.DataFrame(data=list(enumerate(data)), columns=['book', 'score'])
                continue

            # read libraries, odd lines -> lib stats. even lines -> lib books
            if count%2 != 0:
                # n_books signup shiprate
                assert len(data) == 3, 'length of line %d is %d'%(count, len(data))

                [lib_n_books, I, R] = data

                if I > I_max: I_max = I
                if I < I_min: I_min = I

                if R > R_max: R_max = R
                if R < R_min: R_min = R

                stats = [lib_n_books, I, R, 0]
                lib_stats.loc[len(lib_stats)] = stats
            else:
                # b0 b1 b2 ... bn
                assert len(data) == lib_n_books
                # still use lib_books
                books = np.zeros(N_books, bool)
                books[data] = True
                if lib_books is None:
                    lib_books = books
                else:
                    lib_books = np.vstack((lib_books, books))
                # compute lib score
                bS = np.array(book_scores['score'].iloc[data]).sum()
                # update lib score
                lib_stats.at[len(lib_stats)-1, 'totalScore'] = bS

                if bS > bS_max: bS_max = bS
                if bS < bS_min: bS_min = bS
    
    bookCols = ['b%d'%i for i in range(N_books)]
    books = pd.DataFrame(data=lib_books, columns=bookCols)
    lib_stats = lib_stats.join(books)

    print('N_books:', N_books, 'l_libs:', l_libs, 'd_days:', totalTime)
    print('book_scores:\n', book_scores)
    print('libs')
    print(lib_stats)
    return (book_scores, lib_stats, bookCols, N_books, l_libs, totalTime)

#%%
if __name__ == "__main__":
    book_scores, lib_stats, bookCols, N, L, D = read_ip('../a_example.txt')                

# %%
