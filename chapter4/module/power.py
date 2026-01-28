import numpy as np

def make_v4(x_i,pos_xd): #牧羊犬から逃げる力生成モジュール
    posVN3=np.linalg.norm(pos_xd - x_i,ord=2)**3 #差分のノルムの３乗を計算
    return -(pos_xd - x_i)/posVN3 #反発力を計算する．

def make_vd4(pos_xd,goal): #牧羊犬と目的地に対する斥力を計算するモジュール
    posVN3=np.linalg.norm(pos_xd - goal,ord=2) #差分のノルムを計算
    return (pos_xd - goal)/posVN3

def cal_uni_vec(u_s): #単位ベクトルを計算するモジュール
    p_s_n3=np.linalg.norm(u_s,ord=2,axis=1) #ノルムを計算
    p_s_n3=np.where(p_s_n3< 1,1,p_s_n3) #ノルムの下限値を演算
    hat_u_s=u_s/p_s_n3[:,None]  #各要素を演算する．
    return hat_u_s

def cal_uni_vec0(u_s): #単位ベクトルを計算するモジュール
    p_s_n3=np.linalg.norm(u_s,ord=2,axis=0) #ノルムを計算
    p_s_n3=np.where(p_s_n3< 1,1,p_s_n3) #ノルムの下限値を演算
    hat_u_s=u_s/p_s_n3  #各要素を演算する．
    return hat_u_s