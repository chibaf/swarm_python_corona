#自作関数のインポート
from module import condition#関数が入ったプログラムをモジュールとして導入

N=10 #ヒツジの数
radius_ini=100 #半径

pos=condition.make_pos(radius_ini, N) #ヒツジの初期座標
print(pos)