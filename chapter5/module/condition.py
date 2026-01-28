import numpy as np

#ヒツジの初期座標生成モジュール
def make_pos(initial_radius, N):
    np.random.seed(314)
    r=initial_radius* np.random.rand(N)
    theta = 2*(np.pi) * np.random.rand(N) -np.pi
    pos=np.stack([r*np.sin(theta), r*np.cos(theta)], 1)
    return pos