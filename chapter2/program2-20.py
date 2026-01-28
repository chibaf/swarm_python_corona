import numpy as np #numpyモジュールの導入
import math

ransu=np.random.rand() #0~1の範囲でランダムな値を出力
ransu3=np.random.rand(3) #0~1の範囲で3つの要素を持つベクトルを出力
A=-1
B=1
ransu_range = (B-A) * np.random.rand(5) + A #-1~1の範囲で5個の要素をもつベクトルを出力

#以下応用である．半径０～３０の円上にベクトルを出力
initial_radius=30
N=5
r=initial_radius* np.random.rand(N)
theta = 2*(math.pi) * np.random.rand(N) -math.pi
pos=np.stack([r*np.sin(theta), r*np.cos(theta)], 1)

print(ransu)
print(ransu3)
print(ransu_range)
print(pos)