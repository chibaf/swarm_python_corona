#--------------------使用モジュールの宣言---------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.patches as pat

#自作関数のインポート
from module import condition, graph, FAT_p, power

#--------------------関数の宣言---------------------------------
def dead_zone(pos_i, pos_j, u_f_i, dead_angle): #個体どうしのなす角を計算
    xn=np.inner(u_f_i, pos_j - pos_i) #死角の計算
    xd=np.linalg.norm(u_f_i)*np.linalg.norm(pos_j - pos_i)
    theta=np.arccos(xn/xd)
    return  ( (np.pi - dead_angle/2) < theta )

def make_rfi(pos_i, pos_j, Rr, dead): #rfiの生成
    D=np.linalg.norm(pos_j - pos_i, axis=1) #距離の計算
    pos_j_in=pos_j[(D < Rr) != dead] #力が及ぼす範囲の計算
    posVD=power.cal_uni_vec(pos_j_in - pos_i)
    rfi=-np.sum(posVD, axis=0) #rfiの計算
    hat_rfi=power.cal_uni_vec0(rfi) #単位ベクトルの計算
    return  hat_rfi if (len(pos_j_in) > 0) else 0 #分離力の計算

def make_ofi(pos_i, pos_j, u_f_j, Rr, Ro, dead): #ofiの生成
    D=np.linalg.norm(pos_j - pos_i, axis=1) #距離の計算
    u_f_j_in=u_f_j[((D  < Ro) == (Rr <= D)) != dead] #力が及ぼす範囲の計算
    u_f_j_w=power.cal_uni_vec(u_f_j_in)
    ofi=np.sum(u_f_j_w, axis=0)
    hat_ofi_n=power.cal_uni_vec0(ofi) #単位ベクトルの計算
    return hat_ofi_n  if (len(u_f_j_in) > 0) else 0 #整列力を計算する．

def make_afi(pos_i, pos_j, Ro, Ra, dead): #afi生成
    D=np.linalg.norm(pos_j - pos_i, axis=1) #距離の計算
    pos_j_in=pos_j[((D  < Ra) == (Ro <= D)) != dead] #力が及ぼす範囲の計算
    posVD=power.cal_uni_vec(pos_j_in - pos_i) #単位ベクトルの計算
    afi=np.sum(posVD, axis=0) #afiの計算
    hat_afi=power.cal_uni_vec0(afi) #単位ベクトルの計算
    return  hat_afi if (len(pos_j_in) > 0) else 0 #結合力を計算する．

def make_dfi(pos_i, pos_xd, Rd): #牧羊犬からの分離力生成
    D=np.linalg.norm(pos_xd - pos_i) #距離の計算
    pos_i_in=pos_i[D <= Rd] #力が及ぼす範囲の計算
    if (len(pos_i_in) > 0) :
        pos_i_n=np.linalg.norm(pos_xd-pos_i_in, ord=2, axis=1)
        hat_dfi=-(pos_xd-pos_i_in)/pos_i_n**3 #各要素を演算する．
        return hat_dfi #分離力を計算する．
    
    else :
        return [0,0]
#--------------------シミュレーション条件の設定---------------------------------
N=10 #魚の数
r=5 #初期半径
iter=110 #更新回数
#死角
dead_angle=np.pi/6
#捕食者の制御ゲイン
K_FAT1=10.0
K_FAT2=500
K_FAT3=4.5
#パラメータ
delta=1
h=1
Cf1=100
Cf2=0.1
Cf3=100
Cf4=0.001
Rr=10
Ro=15
Ra=20
Rd=30
goal=np.array([75, 75]) #目的地
pos_xd=np.array([-10.0, -10.0]) #捕食者の初期座標を考える
pos=condition.make_pos(r, N) #魚の初期座標を考える．
#魚の初期角度を設定する． 
u_f=hat_u_f=np.ones([N, 2])

#魚の力の設定
rf=of=af=df=np.zeros([N, 2])

#グラフ描画の準備
fig,ax=plt.subplots()
graph.graph_setting("fish")
ims=[]

#--------------------制御ループ---------------------------------
for i in range(0,iter):
    for k in range(N):  #1匹ずつの魚の動作処理
        pos_i=pos[k] #k番目の魚に着目
        u_f_i=u_f[k]
        pos_j=np.delete(pos, k, axis=0) #k番目以外の魚に着目
        u_f_j=np.delete(u_f, k, axis=0)
        dead=dead_zone(pos_i, pos_j, u_f_i, dead_angle)
        rf[k]=make_rfi(pos_i, pos_j, Rr, dead) #rfの計算
        of[k]=make_ofi(pos_i, pos_j, u_f_j, Rr, Ro, dead)  #ofの計算
        af[k]=make_afi(pos_i, pos_j, Ro, Ra, dead)  #afの計算
        df[k]=make_dfi(pos_i, pos_xd, Rd)#dfの計算
    u_f=h*u_f+Cf1*rf+Cf2*of+Cf3*af+Cf4*df #速度の更新
    hat_u_f=power.cal_uni_vec(u_f) #単位ベクトルの計算
    pos +=delta*hat_u_f #位置の更新
    x_j_FA=FAT_p.make_pos_FA(pos, goal) #最遠の個体の座標を求める．
    #捕食者の制御処理
    vd1=FAT_p.make_vd1(pos_xd, x_j_FA) #分離力の計算
    vd2=FAT_p.make_vd2(pos_xd, x_j_FA) #結合力の計算
    vd3=FAT_p.make_vd3(pos_xd, goal) #ゴールとの分離力の計算
    vd=K_FAT1*vd1+K_FAT2*vd2+K_FAT3*vd3
    pos_xd +=vd #捕食者の位置更新
    
    #--------------------グラフ描画---------------------------------
    [img, img_d, name]=graph.graph_write(pos, pos_xd, i)
    ims.append([img, img_d, name]) #情報の追加
    if (np.all(np.linalg.norm(pos - goal, ord=2, axis=1) < 20) ): 
        break  

#----------------アニメーション描画------------------------------
ax.add_patch(pat.Circle(goal, 20, ec='blue', fc='none', lw=2)) #目標円
ani=animation.ArtistAnimation(fig, ims, interval=10) #アニメーション
ani.save("fish.gif", writer="imagemagick") #gif画像を保存