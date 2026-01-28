#--------------------モジュールの宣言---------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.patches as pat

#自作関数の宣言
from module import Boids_p, graph, condition, power

#--------------------関数の宣言---------------------------------
def make_posC(pos): #ヒツジの重心座標を計算
    x_j_C = np.average(pos,axis = 0)
    return x_j_C

def make_vd1(pos_xd, x_j_C): #牧羊犬の分離力を計算
    posVN=np.linalg.norm(pos_xd - x_j_C, ord=2) #ノルムを計算
    return -(pos_xd - x_j_C)/posVN #分離力 

def make_vd2(pos_xd, x_j_C): #牧羊犬の結合力
    posVN=np.linalg.norm(pos_xd - x_j_C, ord=2) #ノルムを計算
    return (pos_xd - x_j_C)/posVN**3 #結合力

#--------------------初期設定---------------------------------
N=10 #ヒツジの数
r=10 #初期配置半径
Ir=40   #相互作用半径
iter=100 #更新回数
#ヒツジの制御ゲイン
K1=0.01
K2=500
K3=10000
K4=300
#牧羊犬の制御ゲイン
Kc1=10
Kc2=100
Kc3=8
goal=np.array([50, 50]) #目的地
pos=condition.make_pos(r, N) #ヒツジの初期位置の決定
pos_xd=np.array([-30.0, -30.0]) #牧羊犬の初期位置の決定

v=v1=v2=v3=v4=np.zeros([N, 2]) #ヒツジの初期速度を設定
vd=vd1=vd2=vd3=np.zeros([1, 2]) #牧羊犬の初期速度を設定
fig,ax=plt.subplots() #グラフ描画の準備
graph.graph_setting("center_of_targeting")
ims = []

#--------------------制御ループ---------------------------------
for i in range(0,iter):

    for k in range(N): #ヒツジの動作処理

        x_i=pos[k] #k番目のヒツジに着目
        x_j=np.delete(pos, k, axis=0)  #k番目以外のヒツジに着目
        v_j=np.delete(v, k, axis=0)
        v1[k]=Boids_p.make_v1(x_i, x_j, Ir)     #分離力の計算
        v2[k]=Boids_p.make_v2(x_i, x_j, v_j, Ir) #整列力の計算    
        v3[k]=Boids_p.make_v3(x_i, x_j, Ir)     #結合力の計算
        v4[k]=power.make_v4(x_i,pos_xd)      #牧羊犬からの分離力の計算

    v=K1*v1+K2*v2+K3*v3+K4*v4 #速度の計算
    pos +=v #ヒツジの位置の更新
    
    #牧羊犬の制御処理
    x_j_C=make_posC(pos) #ヒツジの重心座標を計算
    vd1=make_vd1(pos_xd, x_j_C)      #分離力の計算
    vd2=make_vd2(pos_xd, x_j_C)      #結合力の計算
    vd3=power.make_vd4(pos_xd,goal) #ゴールとの分離力の計算

    vd=Kc1*vd1+Kc2*vd2+Kc3*vd3 #牧羊犬の速度更新
    pos_xd +=vd #牧羊犬の位置更新

    #--------------------グラフ描画---------------------------------
    [img, img_d, name]=graph.graph_write(pos, pos_xd, i)
    ims.append([img, img_d, name]) #データを記録
    if (np.all(np.linalg.norm(pos - goal, ord=2, axis=1) < 30) ):
        break 
    
#----------------アニメーション描画------------------------------
ax.add_patch(pat.Circle((goal), 30, ec='blue', fc='none', lw=2)) #目標円
ani=animation.ArtistAnimation(fig, ims, interval=10) #アニメーションの表示
ani.save("center_of_targeting.gif", writer="Pillow") #gif画像としてアニメーションを保存