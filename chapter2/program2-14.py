import numpy as np #numpyモジュールの導入

w=np.array([1, 2, 3, 4, 5])
q=np.array([6, 7, 8, 9, 10])
z=np.array([[0,1],[2,3]])
a=np.array([[4,5],[6,7]])

y=np.dot(w,q)
x=z + a
b=np.dot(z,a)

print(y)
print(x)
print(b)