#--------------------モジュールの宣言-------------------------
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

#自作関数のインポート
from module import condition, graph

#--------------------初期設定----------------------------------
N=30 #ヒツジの数
r=70 #初期配置半径
Ir=20   #相互作用半径
iter=51 #更新回数
K3=0.5 #結合力ゲイン

pos=condition.make_pos(r, N) #ヒツジの初期位置を決定
v=v3=np.zeros([N,2]) #ヒツジの初期速度を設定
fig=plt.figure() #グラフ描画の準備
graph.graph_setting("boid_3")
ims=[]

#--------------------制御ループ---------------------------------
for i in range(0,iter):
    for k in range(N):  #ヒツジの動作処理
        x_i=pos[k] #k番目のヒツジに着目     
        x_j=np.delete(pos, k, axis=0) #k番目以外のヒツジに着目
     
        #結合力の計算
        D = np.linalg.norm(x_j - x_i, axis=1) #距離の計算
        x_j_in = x_j[D < Ir] #力が及ぼす範囲の計算
        posVN=np.linalg.norm(x_j_in - x_i,ord=2,axis=1) #ノルムを計算
        posVN_m=np.where(posVN < 1, 1, posVN) #ノルムの下限値を演算
        posVD=(x_j_in - x_i)/posVN_m[:, None] #向きベクトルの計算
        v3[k] = np.average(posVD,axis=0) if (len(x_j_in) > 0) else 0 #結合力    
    
    v=K3*v3 #速度の計算
    pos +=v #位置の更新
    
    #--------------------グラフ描画---------------------------------
    img = plt.scatter(pos[:,0] , pos[:,1], c="blue") # グラフを作成   
    name= plt.text(-95, 90,"k=" + str(i), fontsize=15) #時間の描画 
    ims.append([img,name]) #データを記録
    
#----------------アニメーション描画------------------------------
ani=animation.ArtistAnimation(fig, ims, interval=10) #アニメーションの表示
ani.save("Boids3.gif", writer="Pillow") #gif画像としてアニメーションを保存