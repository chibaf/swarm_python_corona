#--------------------モジュールの宣言---------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.patches as pat

#自作モジュールの宣言
from module import Boids_p, graph, condition, power5

#--------------------関数の宣言---------------------------------
def make_pos_FA(pos, pos_any): #ある地点から最遠のヒツジとその距離を計算
    D_sg=np.linalg.norm(pos - pos_any, axis=1) #距離の計算
    x_j_FA=pos[np.argmax(D_sg)] #距離の最大値を持つヒツジ
    return x_j_FA,np.max(D_sg)

def make_vd1_st(x_j_C, x_j_FA): #STの第1項の向きベクトルを計算
    posVN=np.linalg.norm(x_j_FA - x_j_C, ord=2) #ノルムを計算
    return (x_j_FA - x_j_C)/posVN #分離力

def make_vd_Pc(pos_xd, Pc): #牧羊犬の結合力を計算
    posVN=np.linalg.norm(pos_xd - Pc, ord=2) #ノルムを計算
    return (pos_xd - Pc)/posVN #結合力

def check_distance(pos_xd, pos, c0, interaction_radius):
    posVN=np.linalg.norm(pos_xd - pos, ord=2, axis=1)
    judge=np.all(posVN <= c0*interaction_radius)
    return judge

#--------------------初期設定---------------------------------
N=10 #ヒツジの数
r=15 #初期配置半径
Ir=20   #相互作用半径
iter=260 #更新回数
#ヒツジの制御ゲイン
K1=200
K2=0.5
K3=2.0
K4=200
#牧羊犬の制御ゲイン
c0=0.001
c1=24/(Ir*np.power(N,2/3))
c2=30/(20*np.sqrt(10))
c3=15/20
K0=3.0
fN=20.0
Lc=50.0
Ld=30.0
goal=np.array([45, 45]) #目的地
pos=condition.make_pos(r, N) #ヒツジの初期位置の決定
pos_xd=np.array([-10.0, -10.0]) #牧羊犬の初期位置の決定

v=v1=v2=v3=v4=np.zeros([N, 2]) #ヒツジの初期速度を設定
vd=vd1=vd2=vd3=np.zeros([1, 2]) #牧羊犬の初期速度を設定
fig,ax = plt.subplots()#グラフ描画の準備
graph.graph_setting("switching targeting")
ims=[]

#--------------------制御ループ---------------------------------
for i in range(0,iter):
    for k in range(N): #ヒツジの動作処理

        x_i=pos[k] #k番目のヒツジに着目   
        x_j=np.delete(pos, k, axis=0) #k番目以外のヒツジに着目
        v_j=np.delete(v, k, axis=0)
        v1[k]=Boids_p.make_v1(x_i, x_j, Ir)     #分離力の計算
        v2[k]=Boids_p.make_v2(x_i, x_j, v_j, Ir) #整列力の計算    
        v3[k]=Boids_p.make_v3(x_i, x_j, Ir)     #結合力の計算
        v4[k]=power5.make_v4(x_i, pos_xd)     #牧羊犬からの分離力の計算
    v=K1*v1+K2*v2+K3*v3+K4*v4 #速度の計算
    pos +=v #ヒツジの位置の更新
    x_j_C=power5.make_posC(pos) #ヒツジの重心を計算
    [x_j_FA, df]=make_pos_FA(pos, x_j_C) #最遠のヒツジの位置を計算

    #牧羊犬の制御処理
    if check_distance(pos_xd, pos, c0, Ir):#距離がc0rs
        vd=np.array([0.0, 0.0])
    elif df > fN:
        st_muki=make_vd1_st(x_j_C, x_j_FA)
        Pc=x_j_C+st_muki*Lc
        vd=K0*-make_vd_Pc(pos_xd, Pc)
    elif df < fN:
        st_muki=-make_vd1_st(x_j_C, goal)
        Pd=x_j_C+st_muki*Ld
        vd=K0*-make_vd_Pc(pos_xd, Pd)
    pos_xd +=vd #牧羊犬の位置更新
    
    #--------------------グラフ描画---------------------------------
    [img, img_d, name]=graph.graph_write(pos, pos_xd, i)
    ims.append([img, img_d, name]) #情報の追加
    if (np.all(np.linalg.norm(pos - goal, ord=2, axis=1) < 20) ):
        break  

#----------------アニメーション描画------------------------------
ax.add_patch(pat.Circle(goal, 20,ec='blue', fc='none', lw=2)) #目標円
ani=animation.ArtistAnimation(fig, ims, interval=10) #アニメの表示
ani.save("switching targeting.gif", writer="Pillow") #gif画像としてアニメを保存