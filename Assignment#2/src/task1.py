from cmath import sqrt
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

samples = 50
n = 3000
bins_size = 50
bins = np.linspace(start=-5, stop=5, num=bins_size, endpoint=True)

def get_spectrum_density(n, samples, p, bins_size):
    x = np.zeros(bins_size)
    y = np.zeros(bins_size)
    # 采样
    for i in range(samples):
        # 生成 ER 随机网络
        G = nx.random_graphs.erdos_renyi_graph(n, p)
        eigen_values = list(nx.adjacency_spectrum(G).real)
        hist, bins_x = np.histogram(a=sorted(eigen_values), bins=bins_size, density=True)
        
        # 用区间中点作为 lambda 近似值
        new_bins = [(bins_x[j] + bins_x[j + 1]) / 2 for j in range(len(bins_x) - 1)]
        x += np.array(new_bins)
        y += hist # 采样值累加
    return x / samples, y / samples

size = 4
c = [0.5, 1, 1, 10]
z = [1, 1, 1.5, 1]
color = ['r', 'b', 'g', 'y']

plt.figure(figsize=(11,5))
for i in range(size):
    p = c[i] * pow(n, -z[i])
    x, y = get_spectrum_density(n, samples, p, bins_size)
    par = np.sqrt(n * p * (1 - p))
    plt.plot(
        x / par,
        y * par,
        str(color[i]) + '--',
        label='$c={}, z={}$'.format(c[i], z[i])
    )

x = np.array([(bins[i] + bins[i + 1]) / 2 for i in range(bins_size - 1)])
y = np.array([np.sqrt(np.maximum(4 - lam * lam, 0)) / (2 * np.pi) for lam in x])

plt.plot(
    x,
    y,
    'k-',
    label='theoretical value when $N\\to\infty$'
)

plt.legend(loc=1, fontsize=16)
plt.xlabel(r"$\lambda /\sqrt{Np(1-p)}$", fontsize=12)
plt.ylabel(r"$\rho \sqrt{Np(1-p)}$", fontsize=12)
plt.xlim(-5, 5)
plt.ylim(0, 4)
plt.tight_layout()
plt.savefig('./task1.jpg')
