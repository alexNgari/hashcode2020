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
def findLibQueue(book_scores, lib_stats, d_days):
    books = np.array(list(lib_stats['books']))
    print(books)
    for i, lib in lib_stats.iterrows():
        print(book_scores[books])
    
#%%
from read_ip import read_ip
if __name__ == "__main__":
    book_scores, lib_stats, bookCols = read_ip('a_example.txt')

#%%
scores = np.array(book_scores['score'])
print(scores)
print(lib_stats['books'])
# findLibQueue(scores, lib_stats, 7)

# %%
