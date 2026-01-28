import numpy as np

def make_v4(x_i,pos_xd): #牧羊犬から逃げる力生成
    posVN=np.linalg.norm(pos_xd - x_i,ord=2) #ノルムを計算
    return -(pos_xd - x_i)/posVN**3 #逃げる力

def make_vd4(pos_xd,goal): #牧羊犬と目的地に対する斥力を計算
    posVN=np.linalg.norm(pos_xd - goal,ord=2) #ノルムを計算
    return (pos_xd - goal)/posVN #斥力

def make_posC(pos): #ヒツジの重心座標を計算
    x_j_C = np.average(pos,axis = 0)
    return x_j_C

def cal_uni_vec(u_s): #単位ベクトルを計算するモジュール
    p_s_n=np.linalg.norm(u_s,ord=2,axis=1) #ノルムを計算
    p_s_n=np.where(p_s_n< 1,1,p_s_n) #ノルムの下限値を演算
    hat_u_s=u_s/p_s_n[:,None]  #各要素を演算する．
    return hat_u_s