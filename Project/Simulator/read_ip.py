# hashcode 2020
#%%
import numpy as np
import pandas as pd
#%%

def read_ip(filename):
    N_books = 0     # no of books
    book_scores = None
    lib_stats = None
    lib_books = None
    
    with open(filename, 'r') as reader:

        lib_n_books = 0

        I_max, I_min = 0, 99999
        bS_max, bS_min = 0, 99999
        R_max, R_min = 0, 99999

        for count, line in enumerate(reader, start=1):
            # print(count)
            data = list(map(int, line.split()))
            if not data:
                continue
            if count == 1:
                # N_books l_libs d_days
                assert len(data) == 3
                [N_books, l_libs, totalTime] = data
                # read N, L, D so init objects
                lib_stats = pd.DataFrame(np.empty((l_libs,5), int), columns=['library', 'noOfBooks', 'signUpTime', 'shipRate', 'totalScore'])
                lib_books = np.zeros((l_libs, N_books), bool)
                continue
            elif count == 2:
                # S_b0 S_b1 S_b2 ... S_bN
                assert len(data) == N_books
                book_scores = pd.DataFrame(data=list(enumerate(data)), columns=['book', 'score'])
                print(f'Max Score: {book_scores.sum().tolist()[1]}')
                continue


            # read libraries, odd lines -> lib stats. even lines -> lib books
            if count%2 != 0:
                # n_books signup shiprate
                assert len(data) == 3, f'Error in line {count}! Expected list of length 3, got: \n {data}'

                [lib_n_books, I, R] = data

                if I > I_max: I_max = I
                if I < I_min: I_min = I

                if R > R_max: R_max = R
                if R < R_min: R_min = R

                pos = count//2-1
                stats = [pos, lib_n_books, I, R, 0]
                lib_stats.loc[pos] = stats
            else:
                pos = (count-1)//2-1
                # b0 b1 b2 ... bn
                assert len(data) == lib_n_books, f'Error in line {count}! Expected {lib_books} books, got {len(data)}'
                # still use lib_books
                books = np.zeros(N_books, bool)
                books[data] = True
                lib_books[pos] = books
                # compute lib score
                bS = np.array(book_scores['score'].iloc[data]).sum()
                # update lib score
                lib_stats.at[pos, 'totalScore'] = bS

                if bS > bS_max: bS_max = bS
                if bS < bS_min: bS_min = bS
    
    bookCols = ['b%d'%i for i in range(N_books)]
    lib_stats = lib_stats.join(pd.DataFrame(data=lib_books, columns=bookCols))
    print(f'Inserted {len(lib_stats)} libraries, {N_books} books, {totalTime} days')

    # print('book_scores:\n', book_scores)
    # print('libs: \n', lib_stats)
    return (totalTime, book_scores, lib_stats, bookCols)

#%%
if __name__ == "__main__":
    *_, lib_stats, bookCols = read_ip('../d_tough_choices.txt')
    # # How to get books in a library
    # print(np.where(np.array(lib_stats.iloc[0].iloc[list(lib_stats.iloc[0].index).index('b0'):]))[0].tolist())

# %%
