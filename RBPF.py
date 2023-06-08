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
h = lambda x, t: x ** 2 / 20 + np.random.randn(1) * np.sqrt(x_R)
# plt.hist(x_P,N, normed=True)

z_out = [h(x, 0)]  # 实际测量值
x_out = [x]  # 测量值的输出向量
x_est = x  # 估计值
x_est_out = [x_est]
# print(x_out)

for t in range(1, T):
    x = 0.5 * x + 25 * x / (1 + x ** 2) + 8 * np.cos(1.2 * (t - 1)) + np.random.randn() * np.sqrt(x_N)
    z = h(x, t)
    # 对于直接依赖于观测变量的粒子，粒子和权重的估计有效
    direct_particles = x_P ** 2
    direct_weights = h(x_P, t) ** 2 / x_R
    w_direct = direct_weights / np.sum(direct_weights)
    x_direct_est, var_direct_est = estimate(direct_particles, w_direct)
    # 对于间接依赖于观测变量的粒子，只更新权重，粒子估计无意义
    indirect_particles = 0.5 * x_P + 25 * x_P / (1 + x_P ** 2) + 8 * np.cos(1.2 * (t - 1)) + np.random.randn(N) * np.sqrt(x_N)
    indirect_weights = (h(indirect_particles, t) - z)**2 / x_R
    w_indirect = np.exp(-indirect_weights/2) / np.sum(np.exp(-indirect_weights/2))
    # 对于每个粒子，用直接依赖的粒子的估计值来估计表示不同粒子值所代表的概率分布的粒子的权重
    resampled_particles = np.copy(x_P)
    resampled_weights = np.copy(w_indirect)
    for i in range(N):
        if np.abs(direct_particles - resampled_particles[i]).argmin() != np.abs(direct_particles - resampled_particles).argmin():
            resampled_weights[i] = w_direct[np.abs(direct_particles - resampled_particles).argmin()]
    # 估计
    x_est, var = estimate(resampled_particles, resampled_weights)
    # 重采样
    x_P, w_resampled = simple_resample(resampled_particles, resampled_weights)
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