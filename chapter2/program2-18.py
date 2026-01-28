import numpy as np #numpyモジュールの導入

w1 = np.array([1,2,3,4])
w2 = np.array([5,6,7,8])
w3 = np.stack([w1, w2],0) #新たな軸に沿って結合
w4 = np.stack([w1, w2],1)

print(w3)
print(w4)