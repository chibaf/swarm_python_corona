#--------------------使用モジュールの宣言---------------------------------
import numpy as np
import matplotlib.pyplot as plt
from module import condition
import matplotlib.patches as pat

#自作関数のインポート
from module import graph

pos=condition.make_pos(100, 10) #ヒツジの初期座標を考える．
pos_xd=np.array([-10.0, -10.0]) #牧羊犬の初期座標を考える

fig,ax = plt.subplots() #グラフ描画の準備
graph.graph_setting("scatter plot")
plt.scatter(pos[:,0] , pos[:,1],c="blue") #ヒツジの位置座標  
plt.scatter(pos_xd[0] , pos_xd[1],c="red") #牧羊犬の位置座標 
plt.text(-95,90,"hello world",fontsize=15) #時間の描画
ax.add_patch(pat.Circle([-50,-50], 30, ec='blue', fc='none', lw=2)) #目標円
ax.add_patch(pat.Ellipse([50, -50], width=50, height=40, 
ec='green', fc='none', lw=2)) #楕円
ax.add_patch(pat.Rectangle([50, 50], width=35, height=35, 
ec='red', fc='none', lw=2)) #長方形
plt.savefig("scatter_plot.png") #scatter_plot.pngとして保存する
plt.show()