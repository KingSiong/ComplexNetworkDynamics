from cmath import exp
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math

N = 1000
K = 6

P = [0, 0.1, 0.2, 0.4, 0.6, 0.9, 1.0]
color = ["b", "r", "g", "y", "k", "m", "c"]
PC = [(P[i], color[i]) for i in range(len(P))]

sample_size = 50
degree_size = 20

x = np.arange(degree_size)

def f(k, K):
    return int(np.minimum(k - K / 2, K / 2))
    # return int(np.maximum(k - K, K / 2))

def C(n, m):
    if n < 0 or m < 0 or n < m:
        return 0
    else:
        return math.factorial(n) / math.factorial(n - m) / math.factorial(m)

def calc_p(k, K, p):
    res = 0
    up = f(k, K)
    for i in range(up + 1):
        res = res + C(K / 2, i)\
            * pow(1 - p, i) * pow(p, np.maximum(K / 2 - i, 0)) \
            * pow(p * K / 2, np.maximum(k - K / 2 - i, 0)) * exp(-p * K / 2) \
            / math.factorial(np.maximum(k - K / 2 - i, 0))
    return res

plt.figure(figsize=(7, 4))
for p, col in PC:
    # 采样
    y = np.zeros(degree_size)
    for i in range(sample_size):
        # 随机生成 WS 小世界网络
        G = nx.random_graphs.watts_strogatz_graph(N, K, p)
        # 获取图的度分布
        dist = nx.degree_histogram(G)
        dist = np.pad(dist, (0, degree_size - len(dist)), 'constant', constant_values=(0,0))
        y += dist

    # 统计绘图
    plt.plot(x, y / (sample_size * N), col + str('-'), label="$P= " + str(p) + "$")
    # 计算理论值
    y = np.array([calc_p(k, K, p) for k in x])
    plt.plot(x, y, col + str('^'))
    
plt.legend(loc=1, fontsize=16)
plt.xlabel("$k$", fontsize=12)
plt.ylabel("$P(k)$", fontsize=12)
plt.xlim(0, degree_size)
plt.ylim(1e-4, 1)
plt.yscale('log')

plt.tight_layout()
plt.savefig('./task2.jpg')
