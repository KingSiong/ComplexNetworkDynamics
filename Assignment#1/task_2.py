import numpy as np

n = 7
m = 18
d = 0.85
INF = 1e9

# 函数，接收一个矩阵 A，返回最大特征值以及归一化后的特征向量
def get_eigen(A):
    # 获取特征值与特征向量
    eigen_values, eigen_vectors = np.linalg.eig(A)

    i = np.argmax(eigen_values) # 获得最大特征值的索引
    max_eigen_value = eigen_values.max() # 获得最大特征值
    max_eigen_vector = eigen_vectors.T[i] # 获得对应特征向量

    # 最大特征值
    max_eigen_value = np.real(max_eigen_value) # 实化

    # 归一化后的特征向量
    max_eigen_vector = np.real(max_eigen_vector) # 实化
    max_eigen_vector = max_eigen_vector / max_eigen_vector.sum() # 归一化

    # 返回矩阵，最大特征值以及对应归一化后的特征向量
    return A, max_eigen_value, max_eigen_vector.T

# 邻接矩阵
b =[[0, 1, 1, 1, 1, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0], 
    [0, 1, 1, 0, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0], 
    [1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0]
    ]
B = np.matrix(b)

np.set_printoptions(formatter={'float': '{:.8f}'.format}) # 设置输出精度

# 要求 1 输出
B, B_eigen_value, B_eigen_vector = get_eigen(B)
print('邻接矩阵: \n{}\n最大特征值: {:.8f}\n归一化后的特征向量: \n{}\n'.format(B, B_eigen_value, B_eigen_vector))

# page rank 计算
P = np.array([r / r.sum() for r in B]) * d + np.repeat(1.0 / n, n) * (1 - d) # 计算 P
P = P.flatten().reshape((n, n)) # 规范化

# 要求 2 输出
print('状态转移概率矩阵: \n{}'.format(P))
P, P_eigen_value, P_eigen_vector = get_eigen(P.T)
print('状态转移概率矩阵的转置: \n{}\n最大特征值: {:.8f}\n平稳分布: \n{}\n'.format(P, P_eigen_value, P_eigen_vector))
