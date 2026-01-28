import numpy as np
#相互作用半径 Ir: Interaction radius  
#距離 D: Distance　

#--------------------反発力生成---------------------------------
def make_v1(x_i,x_j,Ir): 
    D = np.linalg.norm(x_j - x_i, axis=1) #距離の計算
    x_j_in = x_j[D < Ir] #力が及ぼす範囲の計算
    posVN=np.linalg.norm(x_j_in - x_i,ord=2,axis=1) #ノルムを計算
    posVD=(x_j_in - x_i)/posVN[:,None]**3 #計算
    return -np.average(posVD,axis=0) if (len(x_j_in) > 0) else 0 #反発力

#--------------------整列力生成---------------------------------
def make_v2(x_i,x_j,v_j,Ir): 
    D = np.linalg.norm(x_j - x_i, axis=1) #距離の計算
    v_j_in = v_j[D < Ir] #力が及ぼす範囲の計算
    velVN=np.linalg.norm(v_j_in,ord=2,axis=1) #ノルムを計算
    velVN=np.where(velVN < 1,1,velVN) #ノルムの下限値を演算
    velD=v_j_in/velVN[:,None] #向きベクトルの計算
    return np.average(velD,axis=0) if (len(v_j_in) > 0) else 0 #整列力

#--------------------引力生成---------------------------------
def make_v3(x_i,x_j,Ir): 
    D = np.linalg.norm(x_j - x_i, axis=1) #距離の計算
    x_j_in = x_j[D < Ir] #力が及ぼす範囲の計算
    posVN=np.linalg.norm(x_j_in - x_i,ord=2,axis=1) #ノルムを計算
    posVN_m=np.where(posVN < 1,1,posVN) #ノルムの下限値を演算
    posVD=(x_j_in - x_i)/posVN_m[:,None] #向きベクトルの計算
    return np.average(posVD,axis=0) if (len(x_j_in) > 0) else 0 #引力