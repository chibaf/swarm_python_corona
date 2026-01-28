#--------------------使用モジュールの宣言-----------------------
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt
from module import condition, graph

#--------------------初期設定----------------------------------
pos=condition.make_pos(30, 30) #ヒツジの初期座標を考える．
fig = plt.figure()
graph.graph_setting("scatter_movie_test")
ims = []

#--------------------制御ループ---------------------------------
for i in range(0, 51): #１頭ずつのヒツジの動作処理
    pos=pos + 0.05*pos #位置の更新

#--------------------グラフ描画---------------------------------
    img_s = plt.scatter(pos[:,0] , pos[:,1],c="blue") # グラフを作成
    name= plt.text(-95,90,"k=" + str(i),fontsize=15) #時間の描画
    ims.append([img_s,name]) #グラフを配列に追加

#----------------アニメーション描画------------------------------
ani=animation.ArtistAnimation(fig, ims, interval=1)
ani.save("scatter_movie_test.gif", writer="imagemagick") #gif画像を保存