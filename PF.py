import numpy as np
import matplotlib.pyplot as plt


def estimate(particles, weights):
    """returns mean and variance of the weighted particles"""
    mean = np.average(particles, weights=weights)
    var = np.average((particles - mean) ** 2, weights=weights)
    return mean, var


def simple_resample(particles, weights):
    N = len(particles)
    cumulative_sum = np.cumsum(weights)
    cumulative_sum[-1] = 1.  # avoid round-off error
    rn = np.random.rand(N)
    indexes = np.searchsorted(cumulative_sum, rn)
    # resample according to indexes
    particles[:] = particles[indexes]
    weights.fill(1.0 / N)
    return particles, weights


x = 0.1  # 初始真实状态
x_N = 1  # 系统过程噪声的协方差（由于是一维的，这里就是方差）
x_R = 1  # 测量的协方差
T = 75  # 共进行75次
N = 100  # 粒子数，越大效果越好，计算量也越大

V = 2  # 初始分布的方差
x_P = x + np.random.randn(N) * np.sqrt(V)
x_P_out = [x_P]
# plt.hist(x_P,N, normed=True)

z_out = [x ** 2 / 20 + np.random.randn(1) * np.sqrt(x_R)]  # 实际测量值
x_out = [x]  # 测量值的输出向量
x_est = x  # 估计值
x_est_out = [x_est]
# print(x_out)

for t in range(1, T):
    x = 0.5 * x + 25 * x / (1 + x ** 2) + 8 * np.cos(1.2 * (t - 1)) + np.random.randn() * np.sqrt(x_N)
    z = x ** 2 / 20 + np.random.randn() * np.sqrt(x_R)
    # 更新粒子
    # 从先验p(x(k) | x(k - 1))中采样
    x_P_update = 0.5 * x_P + 25 * x_P / (1 + x_P ** 2) + 8 * np.cos(1.2 * (t - 1)) + np.random.randn(N) * np.sqrt(x_N)
    z_update = x_P_update ** 2 / 20
    # 计算权重
    P_w = (1 / np.sqrt(2 * np.pi * x_R)) * np.exp(-(z - z_update) ** 2 / (2 * x_R))
    P_w /= np.sum(P_w)
    # 估计
    x_est, var = estimate(x_P_update, P_w)
    # 重采样
    x_P, P_w = simple_resample(x_P_update, P_w)
    # 保存数据
    x_out.append(x)
    z_out.append(z)
    x_est_out.append(x_est)
    x_P_out.append(x_P)

# 显示粒子轨迹、真实值、估计值
t = np.arange(0, T)
x_P_out = np.asarray(x_P_out)
for i in range(0, N):
    plt.plot(t, x_P_out[:, i], color='gray')
plt.plot(t, x_out, color='lime', linewidth=2, label='true value')
plt.plot(t, x_est_out, color='red', linewidth=2, label='estimate value')
plt.legend()
plt.show()
