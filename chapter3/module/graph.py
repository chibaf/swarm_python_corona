import matplotlib.pyplot as plt

def graph_setting(title):
    plt.xlim(-100,100)
    plt.ylim(-100,100)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(title)
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    return

def graph_write(pos,pos_xd,i):
    img = plt.scatter(pos[:,0] , pos[:,1],c="blue")    # ヒツジの位置  
    img_d = plt.scatter(pos_xd[0] , pos_xd[1],c="red") # 牧羊犬の位置
    name= plt.text(-95,90,"k=" + str(i),fontsize=15)   #時間の描画
    return [img,img_d,name]

