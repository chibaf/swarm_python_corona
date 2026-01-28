#--------------------使用モジュールの宣言-----------------------------
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt
import matplotlib.patches as pat

#自作関数のインポート
from module import Boids_p, condition, graph

#--------------------関数の宣言---------------------------------
def make_v4(x_i,pos_xd): #牧羊犬からの分離力生成
    posVN=np.linalg.norm(pos_xd - x_i, ord=2) #ノルムの計算
    return (pos_xd - x_i)/posVN #分離力

def make_vd4(pos_xd,goal): #牧羊犬と目的地に対する分離力を計算
    posVN=np.linalg.norm(pos_xd - goal, ord=2) #ノルムの計算
    return -(pos_xd - goal)/posVN #分離力

#--------------------初期設定-----------------------------------
N=10 #ヒツジの数
r=100 #初期配置半径
Ir=50   #相互作用半径
iter=51 #更新回数
#ヒツジの制御ゲイン
K1=1.5
K2=0.1
K3=0.1
K4=3
K5=3.5
goal=np.array([75, 75]) #目的地
pos=condition.make_pos(r, N) #ヒツジの初期位置の決定
pos_xd=np.array([-10.0, -10.0]) #牧羊犬の初期位置の決定

v=v1=v2=v3=v4=np.zeros([N, 2]) #ヒツジの初期速度を設定
vd=vd1=vd2=vd3=vd4=np.zeros([1, 2]) #牧羊犬の初期速度を設定
fig,ax=plt.subplots() #グラフ描画の準備
graph.graph_setting("leader_follower")
ims=[]

#--------------------制御ループ---------------------------------
for i in range(0,iter):
    for k in range(N):  #ヒツジの動作処理

        x_i=pos[k] #k番目のヒツジに着目    
        x_j=np.delete(pos, k, axis=0) #k番目以外のヒツジに着目
        v_j=np.delete(v, k, axis=0)
        
        v1[k]=Boids_p.make_v1(x_i, x_j, Ir)    #分離力の計算
        v2[k]=Boids_p.make_v2(x_i, x_j, v_j, Ir)#整列力の計算   
        v3[k]=Boids_p.make_v3(x_i, x_j, Ir)    #結合力の計算   
        v4[k]=make_v4(x_i, pos_xd)           #牧羊犬からの分離力 
    
    v=K1*v1+K2*v2+K3*v3+K4*v4 #速度の計算
    pos +=v#位置の更新
    
    #牧羊犬の制御処理
    vd1=Boids_p.make_v1(x_i, x_j, Ir)     #分離力の計算
    vd2=Boids_p.make_v2(x_i, x_j, v_j, Ir) #整列力の計算
    vd3=Boids_p.make_v3(x_i, x_j, Ir)     #結合力の計算
    vd4=make_vd4(pos_xd,goal)          #ゴールとの分離力を計算
    vd=K1*vd1+K2*vd2+K3*vd3+K4*vd4 #牧羊犬の制御処理
    pos_xd +=vd #牧羊犬の位置更新
    
    #--------------------グラフ描画---------------------------------
    [img, img_d, name]=graph.graph_write(pos, pos_xd, i)
    ims.append([img, img_d, name]) #データを記録
    if (np.all(np.linalg.norm(pos - goal, ord=2, axis=1) < 20) ):
        break 

#----------------アニメーション描画------------------------------
ax.add_patch(pat.Circle(goal, 20, ec='blue', fc='none', lw=2)) #目標円
ani=animation.ArtistAnimation(fig, ims, interval=1) #アニメーションの表示
ani.save("leader_follower.gif", writer="Pillow") #gif画像としてアニメーションを保存