#--------------------使用モジュールの宣言--------------------------
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

#自作関数のインポート
from module import condition, graph, Boids_p

#--------------------初期設定----------------------------------
N=30 #ヒツジの数
r=100   #初期配置半径
Ir=50   #相互作用半径
iter=51 #更新回数
K1=0.6  #分離力ゲイン
K2=0.1  #整列力ゲイン
K3=0.5  #結合力ゲイン

pos=condition.make_pos(r, N) #ヒツジの初期位置を決定
v=v1=v2=v3=np.zeros([N, 2]) #ヒツジの初期速度の設定
fig=plt.figure() #グラフ描画の準備
graph.graph_setting("boid")
ims = []

#--------------------制御ループ---------------------------------
for i in range(0,iter):
    
    for k in range(N): #ヒツジの動作処理
        
        x_i=pos[k] #k番目のヒツジに着目    
        x_j=np.delete(pos, k, axis=0) #k番目以外のヒツジに着目
        v_j=np.delete(v, k, axis=0)
        v1[k]=Boids_p.make_v1(x_i, x_j, Ir)    #分離力の計算
        v2[k]=Boids_p.make_v2(x_i, x_j, v_j, Ir)#整列力の計算    
        v3[k]=Boids_p.make_v3(x_i, x_j, Ir)    #結合力の計算  
    
    v=K1*v1+K2*v2+K3*v3 #速度の計算
    pos +=v #位置の更新
    
    #--------------------グラフ描画---------------------------------
    img=plt.scatter(pos[:,0] , pos[:,1], c="blue") #グラフを作成    
    name=plt.text(-95,90,"k=" + str(i),fontsize=15) #時間の描画
    ims.append([img,name]) #データを記録

#----------------アニメーション描画------------------------------
ani=animation.ArtistAnimation(fig, ims, interval=10) #アニメーションの表示
ani.save("Boids.gif", writer="Pillow") #gif画像としてアニメーションを保存