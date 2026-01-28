import numpy as np #numpyモジュールの導入

w  = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
w2 = w[w < 4] #条件を満たした要素の取り出し
w3 = np.where(w > 5 , 1, w) #条件を満たした要素の置き換え
w4 = np.delete(w, 3, axis=0) #3+1番目の要素を削除

print(w)
print(w2)
print(w3)
print(w4)