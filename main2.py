# hashcode 2020
#%%
import numpy as np
import pandas as pd
#%%
N_books = 0     # no of books
l_libs = 0      # no of libraries
d_days = 0      # no of days
book_scores = None
lib_stats = pd.DataFrame(columns=['noOfBooks', 'signUpTime', 'shipRate', 'booksScore']) # each lib stat = [N of books, signup time (I), ship rate (R), score of its books (bS)]
lib_books = []

#%%
reader = open('a_example.txt', 'r') 
lib_i = 0
lib_n_books = 0

I_max, I_min = 0, 99999
bS_max, bS_min = 0, 99999
R_max, R_min = 0, 99999

#%%
for count, line in enumerate(reader, start=1):
    print('read line %d: %s'%(count, line), end='')
    data = line.split()
    if count == 1:
        # N_books l_libs d_days
        assert len(data) == 3
        [N_books, l_libs, d_days] = list(map(int, data))
        continue
    elif count == 2:
        # S_b0 S_b1 S_b2 ... S_bN
        assert len(data) == N_books
        book_scores = pd.DataFrame(data=dict(list(enumerate(data))), columns=['book', 'score'])
        continue

    # read libraries, odd lines -> lib stats. even lines -> lib books
    if count%2 != 0:
        # n_books signup shiprate
        assert len(data) == 3

        lib_n_books = int(data[0])
        I = int(data[1]) # signup time
        R = int(data[2]) # ship rate

        if I > I_max: I_max = I
        if I < I_min: I_min = I

        if R > R_max: R_max = R
        if R < R_min: R_min = R

        stats = [lib_n_books, I, R, 0]
        lib_stats.append(pd.Series(stats, index=lib_stats.columns), ignore_index=True)
    else:
        # b0 b1 b2 ... bn
        assert len(data) == lib_n_books
        books = [ int(index) for index in data ]
        lib_books.append(books)
        # compute lib score
        book_scores
        books
        bS = np.array(book_scores['score'].iloc[books]).sum()
        # update lib score
        lib_stats.at[lib_i, 'booksScore'] = bS

        if bS > bS_max: bS_max = bS
        if bS < bS_min: bS_min = bS

        print(f'lib: {lib_i} stats: \n{lib_stats.iloc[lib_i]}')
        # next lib
        lib_i += 1
#%%
print('N_books:', N_books, 'l_libs:', l_libs, 'd_days:', d_days)
print('book_scores:', book_scores)
print('libs')
print(lib_stats)
print('lib_books')
print(lib_books)

                

# %%
