import numpy as np
import matplotlib.pyplot as plt #グラフ描画用のモジュールの導入

#グラフ描画の準備
x = np.linspace(0, 10, 100) #横軸：時間
y = x + np.random.randn(100) #縦軸：データ

fig = plt.figure()
#グラフの描画
plt.plot(x, y,c="blue") # グラフを作成
plt.xlim(0,10)
plt.ylim(-2,15)
plt.xlabel("x")
plt.ylabel("y")
plt.title("plot test")
plt.grid(True)
plt.savefig("plot_test.png")   #plot_test.pngに保存する
plt.show()