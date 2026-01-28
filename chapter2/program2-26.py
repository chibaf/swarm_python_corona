import numpy as np
import matplotlib.pyplot as plt
from module import condition

pos=condition.make_pos(100, 30) #ヒツジの初期座標を考える．
pos_xd=np.array([-10.0, -10.0]) #牧羊犬の初期座標を考える

plt.subplots() #グラフ描画の準備
plt.scatter(pos[:, 0] , pos[:, 1],c="blue") #ヒツジの位置座標  
plt.scatter(pos_xd[0] , pos_xd[1],c="red") # 牧羊犬の位置座標 
plt.xlim(-100, 100)
plt.ylim(-100, 100)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("scatter plot")
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.savefig("scatter_plot.png")   #プロットしたグラフをファイルscatter.pngに保存する
plt.show()