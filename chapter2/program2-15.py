import numpy as np #numpyモジュールの導入

a=np.array([4,5])
b=np.array([2,3])

#内積の計算
x= np.inner(a,b)
print(x)

#ベクトルの大きさを演算
s=np.linalg.norm(a)
t=np.linalg.norm(b)
print(s)
print(t)

#二つのベクトルのなす角を求める
theta = np.arccos(x/(s*t))
print(theta)          #ラジアン出力
print(theta*180/3.14) #度出力