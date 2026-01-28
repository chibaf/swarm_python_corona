import numpy as np #numpyモジュールの導入

a=np.array([1,2,3,4,5])

#ノルムの計算
norm0_a = np.linalg.norm(a,ord=0) #L0 ノルム
norm1_a= np.linalg.norm(a,ord=1)  #L1 ノルム
norm2_a= np.linalg.norm(a,ord=2)  #L2 ノルム

print(norm0_a)
print(norm1_a)
print(norm2_a)