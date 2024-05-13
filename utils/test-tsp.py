import numpy as np
import random
import matplotlib.pyplot as plt

# 城市坐标
C = np.array([
    [1304, 2312], [3639, 1315], [4177, 2244], [3712, 1399], [3488, 1535],
    [3326, 1556], [3238, 1229], [4196, 1044], [4312, 790], [4386, 570],
    [3007, 1970], [2562, 1756], [2788, 1491], [2381, 1676], [1332, 695],
    [3715, 1678], [3918, 2179], [4061, 2370], [3780, 2212], [3676, 2578],
    [4029, 2838], [4263, 2931], [3429, 1908], [3507, 2376], [3394, 2643],
    [3439, 3201], [2935, 3240], [3140, 3550], [2545, 2357], [2778, 2826],
    [2370, 2975]])

N = len(C)  # 城市数目
D = np.zeros((N, N))  # 距离矩阵

# 计算距离矩阵
for i in range(N):
    for j in range(N):
        D[i, j] = np.sqrt((C[i, 0] - C[j, 0]) ** 2 + (C[i, 1] - C[j, 1]) ** 2)

NP = 200  # 种群规模
G = 2000  # 最大遗传代数
f = np.zeros((NP, N), dtype=int)  # 种群
F = []  # 存储更新的种群
R = None  # 最优路径
np_len = np.zeros(NP)  # 路径长度
fitness = np.zeros(NP)  # 归一化适应值
gen = 0
Rlength = []
minlen = 0
maxlen = 0

# 随机生成初始种群
for i in range(NP):
    f[i] = np.random.permutation(N)

# 遗传算法循环
while gen < G:
    # 计算路径长度
    for i in range(NP):
        np_len[i] = D[f[i, -1], f[i, 0]]
        for j in range(N - 1):
            np_len[i] += D[f[i, j], f[i, j + 1]]

    maxlen = np.max(np_len)  # 最长路径
    minlen = np.min(np_len)  # 最短路径

    # 更新最短路径
    rr = np.where(np_len == minlen)[0]
    R = f[rr[0]].copy()

    # 计算归一化适应值
    fitness = 1 - ((np_len - minlen) / (maxlen - minlen + 0.001))

    # 选择操作
    F = []
    for i in range(NP):
        if fitness[i] >= random.random():
            F.append(f[i].copy())

    while len(F) < NP:
        nnper = np.random.permutation(len(F))
        A = F[nnper[0]].copy()
        B = F[nnper[1]].copy()

        # 交叉操作
        W = int(np.ceil(N / 10))
        p = np.random.randint(0, N - W + 1)
        for i in range(W):
            x = np.where(A == B[p + i])[0][0]
            y = np.where(B == A[p + i])[0][0]
            temp = A[p + i]
            A[p + i] = B[p + i]
            B[p + i] = temp
            temp = A[x]
            A[x] = B[y]
            B[y] = temp

        # 变异操作
        p1 = np.random.randint(0, N)
        p2 = np.random.randint(0, N)
        while p1 == p2:
            p1 = np.random.randint(0, N)
            p2 = np.random.randint(0, N)
        A[p1], A[p2] = A[p2], A[p1]
        B[p1], B[p2] = B[p2], B[p1]

        F.append(A)
        F.append(B)

    if len(F) > NP:
        F = F[:NP]

    f = np.array(F)
    f[0] = R
    gen += 1
    Rlength.append(minlen)

plt.figure()
for i in range(N - 1):
    plt.plot([C[R[i], 0], C[R[i + 1], 0]], [C[R[i], 1], C[R[i + 1], 1]], 'bo-')
plt.plot([C[R[-1], 0], C[R[0], 0]], [C[R[-1], 1], C[R[0], 1]], 'ro-')
plt.title('优化最短距离: ' + str(minlen))

plt.figure()
plt.plot(Rlength)
plt.xlabel('迭代次数')
plt.ylabel('目标函数值')
plt.title('适应度进化曲线')
plt.show()
