#--------------------使用モジュールの宣言---------------------------------
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt
import matplotlib.patches as pat

#自作関数のインポート
from module import condition, graph, FAT_p, power

#--------------------関数の宣言---------------------------------
def make_fm_i(pm_i, pm_j, Rr, Ra, G, m_i, m_j): #分離力生成モジュール
    D=np.linalg.norm(pm_j - pm_i, axis=1) #距離の計算
    #力が及ぼす範囲の計算 Cパターン 
    pm_j_A=pm_j[(Rr <= D) == (D < Ra)]
    m_j_A=m_j[(Rr <= D) == (D < Ra)]
    
    pm_j_B=pm_j[(0 < D) == (D < Rr)]
    m_j_B=m_j[(0 < D) == (D < Rr)]
    powerA=cal_vec3(pm_i, pm_j_A, G, m_i, m_j_A)
    powerB=cal_vec3(pm_i, pm_j_B, G, m_i, m_j_B)
    return powerA - powerB

def make_dm_i(pm_i, pos_xd, Rd): #牧羊犬からの分離力生成モジュール
    D=np.linalg.norm(pos_xd - pm_i) #距離の計算
    pm_i_in = pm_i[D <= Rd] #力が及ぼす範囲の計算
    if (len(pm_i_in) > 0) :
        posVN=np.linalg.norm(pos_xd-pm_i_in, ord=2, axis=1)
        posVD=(pos_xd - pm_i_in)/posVN**3 #各要素を演算する．
        return -posVD #分離力を計算する．
    else :
        return [0,0]
    
def cal_vec3(pm_i, pm_j, G, m_i, m_j):
    posVN=np.linalg.norm(pm_j - pm_i, ord=2, axis=1) #ノルムを計算
    posVD=G*m_i*m_j*(pm_j - pm_i)/posVN[:,None]**3 #各要素を演算する．
    return np.average(posVD,axis=0) if (len(pm_j) > 0) else 0 #分離力を計算する．
#--------------------シミュレーション条件の設定---------------------------------
N=10 #ヒツジの数
r=20 #半径
iter=150 #更新回数
#パラメータ
delta=1
h=0.95
C_m1=40
C_m2=10
#牧羊犬の制御ゲイン
K_FAT1=10.0
K_FAT2=500
K_FAT3=4.5
m=np.ones([N,1]) #ヒツジの質量
G=100 #万有引力定数
Rr=9 #分離力領域の半径
Ra=15 #結合力領域の半径
Rd=30 #牧羊犬から分離力を受ける判定円の半径
goal=np.array([75, 75]) #目的地
pos=condition.make_pos(r, N) #ヒツジの初期座標
pos_xd=np.array([-10.0, -10.0]) #牧羊犬の初期座標

um=fm=dm=np.zeros([N, 2]) #ヒツジの初期速度を設定する．
vd=np.zeros([1, 2]) #牧羊犬の初期速度を設定する．
#グラフ描画の準備
fig,ax = plt.subplots()
graph.graph_setting("Physicomimetic model")
ims=[]
#--------------------制御ループ---------------------------------
for i in range(0,iter):
    for k in range(N):   #1頭ずつのヒツジの動作処理
        pm_i=pos[k] #k番目のヒツジに着目
        um_i=u_m[k]
        m_i=m[k]         
        pm_j=np.delete(pos, k, axis=0) #k番目以外のヒツジに着目
        um_j=np.delete(u_m, k, axis=0)
        m_j=np.delete(m, k, axis =0)
        fm[k]=make_fm_i(pm_i, pm_j, Rr, Ra, G, m_i, m_j) #力，第2項の計算
        dm[k]=make_dm_i(pm_i, pos_xd, Rd)#力，第3項の計算 
    u_m=h*u_m+C_m1*fm+C_m2*dm #速度ベクトルの計算
    
    hat_um=power.cal_uni_vec(um) #u_mの単位ベクトルを計算する．
    pos +=delta*hat_um #位置の更新
    x_j_FA=FAT_p.make_pos_FA(pos, goal) #最遠のヒツジの座標を求める．
    #牧羊犬の制御処理
    vd1=FAT_p.make_vd1(pos_xd, x_j_FA) #分離力の計算
    vd2=FAT_p.make_vd2(pos_xd, x_j_FA) #結合力の計算
    vd3=FAT_p.make_vd3(pos_xd, goal) #ゴールとの分離力の計算
    vd=K_FAT1*vd1+K_FAT2*vd2+K_FAT3*vd3
    pos_xd +=vd #牧羊犬の位置更新
    
    #--------------------グラフ描画---------------------------------
    [img, img_d, name]=graph.graph_write(pos, pos_xd, i)
    ims.append([img, img_d, name]) #情報の追加
    if (np.all(np.linalg.norm(pos - goal, ord=2, axis=1) < 20) ):
        break  
    
#----------------アニメーション描画------------------------------
ax.add_patch(pat.Circle(goal, 20, ec='blue', fc='none', lw=2)) #目標円
ani=animation.ArtistAnimation(fig, ims, interval=1) #アニメーション描画
ani.save("Physicomimetic model.gif", writer="imagemagick") #gif画像を保存