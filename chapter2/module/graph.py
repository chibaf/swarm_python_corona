import matplotlib.pyplot as plt

def graph_setting(title):
    plt.xlim(-100, 100)
    plt.ylim(-100, 100)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(title)
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    return