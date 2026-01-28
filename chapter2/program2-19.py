import numpy as np #numpyモジュールの導入

w1 = np.array([1, 2, 3, 4, 5, 6, 7, 8])
w2 = w1.reshape(2, 4)
w3 = np.average(w1, axis=0) #横方向へ平均値を計算
w4 = np.average(w2, axis=1)

print(w3)
print(w4)