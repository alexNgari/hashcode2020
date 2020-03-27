# hashcode 2020
#%%
import numpy as np
import pandas as pd
#%%

def read_ip(filename, bookcsv, libcsv):
    with open(filename, 'r') as reader:
        for count, line in enumerate(reader, start=1):
            # print(count)
            data = list(map(int, line.split()))
            if not data:
                continue
            if count == 1:
                # N_books l_libs d_days
                assert len(data) == 3
                [_, _, totalTime] = data
                # read N, L, D so init objects
                continue
            else:
                break
        book_scores = pd.read_csv(bookcsv)
        lib_stats = pd.read_csv(libcsv)
    
    # print('book_scores:\n', book_scores)
    # print('libs: \n', lib_stats)
    return (totalTime, book_scores, lib_stats)

#%%
if __name__ == "__main__":
    *_, lib_stats, bookCols = read_ip('../d_tough_choices.txt')
    # # How to get books in a library
    # print(np.where(np.array(lib_stats.iloc[0].iloc[list(lib_stats.iloc[0].index).index('b0'):]))[0].tolist())

# %%
