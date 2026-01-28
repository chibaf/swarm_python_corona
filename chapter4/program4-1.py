#--------------------使用モジュールの宣言---------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.patches as pat

#自作関数の宣言
from module import condition, graph, FAT_p, power

#--------------------関数の宣言---------------------------------
def make_hat_a_s(pos_i,pos_j,r_a): #生成モジュール1
    D=np.linalg.norm(pos_j - pos_i, axis=1) #距離の計算
    pos_j_in = pos_j[D < r_a] #力が及ぼす範囲の計算
    posV=np.average(pos_j_in - pos_i, axis=0) #他のヒツジの位置の差分を計算
    posVN=np.linalg.norm(posV, ord=2) #ノルムを計算
    return posV/posVN  if (len(pos_j_in) > 0) else 0 #結合力を計算する． 

def make_hat_b_s(pos_i, pos_j, r_s): #生成モジュール2
    D=np.linalg.norm(pos_j - pos_i, axis=1) #距離の計算
    pos_j_in=pos_j[D < r_s] #力が及ぼす範囲の計算
    posVN=np.linalg.norm(pos_j_in - pos_i, ord=2, axis=1) #ノルムを計算
    posVD=(pos_j_in - pos_i)/posVN[:, None] #各要素を演算する．
    b_s=-np.sum(posVD, axis=0)
    b_s_n=np.linalg.norm(b_s, ord=2) #ノルムを計算
    return  b_s/b_s_n if (len(pos_j_in) > 0) else 0 #分離力を計算する．

def make_hat_c_s(pos_i, pos_xd, r_s): #生成モジュール3
    D=np.linalg.norm(pos_xd - pos_i) #距離の計算
    pos_i_in=pos_i[D <= r_s] #力が及ぼす範囲の計算
    if (len(pos_i_in) > 0) :
        posVN=np.linalg.norm(pos_xd-pos_i_in, ord=2)
        posVD=(pos_xd - pos_i_in)/posVN**3 #各要素を演算する．
        return -posVD #分離力を計算する．
    else :
        return [0,0]
    
#--------------------シミュレーション条件の設定---------------------------------
N=10 #ヒツジ数
r=15 #半径
iter=115 #更新回数
#パラメータ
delta=1
c=1.05
h=1
r_a = 30
r_s = 40
Cs1=5.0
Cs2=1.0
Cs3=20.0
Cs4=1
#牧羊犬の制御ゲイン
K_FAT1=10
K_FAT2=500
K_FAT3=4.5
pos_xd=np.array([-10.0, -10.0]) #牧羊犬の初期座標
goal=np.array([75, 75]) #目的地
pos=condition.make_pos(r, N) #ヒツジの初期座標
#ヒツジの初期速度を設定する．
u_s=hat_us=hat_as=hat_bs=hat_cs=hat_ds=np.zeros([N, 2])

#グラフ描画の準備
fig,ax = plt.subplots()
graph.graph_setting("daniel")
ims=[]
#--------------------制御ループ---------------------------------
for i in range(0,iter):
    for k in range(N):  #1頭ずつのヒツジの動作処理
        pos_i=pos[k] #k番目のヒツジに着目
        pos_j=np.delete(pos, k, axis=0) #k番目以外のヒツジに着目
        hat_as[k]=make_hat_a_s(pos_i, pos_j, r_a)  #結合の計算
        hat_bs[k]=make_hat_b_s(pos_i, pos_j, r_s)  #分離力の計算
        hat_cs[k]=make_hat_c_s(pos_i, pos_xd, r_s) #分離力の計算
    us=h*hat_us+Cs1*hat_as + Cs2 * hat_bs+Cs3*hat_cs #速度ベクトルの計算

    hat_u_s=power.cal_uni_vec(us) #単位ベクトルの計算
    pos +=delta*hat_us #ヒツジの位置の更新
    x_j_FA=FAT_p.make_pos_FA(pos,goal) #最遠のヒツジの座標を求める．
    #牧羊犬の制御処理
    vd1=FAT_p.make_vd1(pos_xd, x_j_FA)  #分離力の計算
    vd2=FAT_p.make_vd2(pos_xd, x_j_FA) #結合力の計算
    vd3=FAT_p.make_vd3(pos_xd, goal) #ゴールとの分離力の計算
    vd=K_FAT1*vd1+K_FAT2*vd2+K_FAT3*vd3
    pos_xd +=vd #牧羊犬の位置更新

    #--------------------グラフ描画---------------------------------
    [img, img_d, name]=graph.graph_write(pos, pos_xd, i)
    ims.append([img, img_d, name])#情報の追加
    if (np.all(np.linalg.norm(pos - goal, ord=2, axis=1) < 20) ):
        break #シミュレーションの終了判定

#----------------アニメーション描画------------------------------  
ax.add_patch(pat.Circle((goal), 20, ec='blue', fc='none', lw=2)) #目標円
ani=animation.ArtistAnimation(fig, ims, interval=1) #アニメーション描画
ani.save("daniel.gif", writer="imagemagick") #gif画像を保存