import numpy as np

def make_pos_FA(pos, goal): #ゴールから最遠のヒツジを計算するモジュール
    distance_sg = np.linalg.norm(pos - goal, axis=1) #距離の計算
    x_j_FA=pos[np.argmax(distance_sg)] #距離の最大値を持つヒツジを導き出す．
    return x_j_FA

def make_vd1(pos_xd, x_j_FA): #牧羊犬の分離力を計算するモジュール
    posV= pos_xd - x_j_FA #重心位置の差分を計算
    posVN=np.linalg.norm(posV, ord=2) #ノルムを計算
    #pos_sub_norm3=np.where(pos_sub_norm3 < 1,1,pos_sub_norm3)#ノルムの下限値を演算
    posVD=posV/posVN #各要素を演算する．
    return -posVD #分離力を計算する． 

def make_vd2(pos_xd, x_j_FA): #牧羊犬の結合力を計算するモジュール
    posV= pos_xd - x_j_FA #重心位置の差分を計算
    posVN=np.linalg.norm(posV, ord=2) #ノルムを計算
    #pos_sub_norm3=np.where(pos_sub_norm3 < 1,1,pos_sub_norm3) #ノルムの下限値を演算
    posVD=posV/posVN**3 #各要素を演算する． 
    return posVD #結合力を計算する．

def make_vd3(pos_xd, goal): #牧羊犬と目的地に対する分離力を計算するモジュール
    posV= pos_xd - goal #ゴール位置の差分を計算
    posVN=np.linalg.norm(posV, ord=2) #ノルムを計算
    #pos_sub_norm3=np.where(pos_sub_norm3 < 1,1,pos_sub_norm3) #ノルムの下限値を演算
    posVD=posV/posVN #各要素を演算する．
    return posVD #分離力を計算する．