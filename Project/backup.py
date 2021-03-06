# hashcode 2020
#%%
import numpy as np
import pandas as pd
#%%

def read_ip(filename):
    N_books = 0     # no of books
    book_scores = None
    lib_stats = pd.DataFrame(columns=['library','noOfBooks', 'signUpTime', 'shipRate', 'totalScore']) # each lib stat = [N of books, signup time (I), ship rate (R), score of its books (bS)]
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
                [N_books, _, totalTime] = data
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

                stats = [count//2-1, lib_n_books, I, R, 0]
                lib_stats.loc[len(lib_stats)] = stats
            else:
                # b0 b1 b2 ... bn
                assert len(data) == lib_n_books, f'Error in line {count}! Expected {lib_books} books, got {len(data)}'
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
            print(f'Inserted {len(lib_stats)} libraries')
    
    bookCols = ['b%d'%i for i in range(N_books)]
    lib_stats = lib_stats.join(pd.DataFrame(data=lib_books, columns=bookCols))

    # print('book_scores:\n', book_scores)
    # print('libs: \n', lib_stats)
    return (totalTime, book_scores, lib_stats)

#%%
if __name__ == "__main__":
    # _, bookScores, lib_stats = read_ip('a_example.txt')
    # bookScores.to_csv('a_books.csv', index=False)
    # lib_stats.to_csv('a_libStats.csv', index=False)

    # del bookScores
    # del lib_stats

    # _, bookScores, lib_stats = read_ip('b_read_on.txt')
    # bookScores.to_csv('b_books.csv', index=False)
    # lib_stats.to_csv('b_libStats.csv', index=False)

    # del bookScores
    # del lib_stats

    # _, bookScores, lib_stats = read_ip('c_incunabula.txt')
    # bookScores.to_csv('c_books.csv', index=False)
    # lib_stats.to_csv('c_libStats.csv', index=False)

    # del bookScores
    # del lib_stats


    _, bookScores, lib_stats = read_ip('c_incunabula.txt')
    bookScores.to_csv('c_books.csv', index=False)
    lib_stats.to_csv('c_libStats.csv', index=False)

    del bookScores
    del lib_stats

   
    # # How to get books in a library
    # print(np.where(np.array(lib_stats.iloc[0].iloc[list(lib_stats.iloc[0].index).index('b0'):]))[0].tolist())

# %%
