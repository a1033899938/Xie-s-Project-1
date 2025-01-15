import lumapi
import matplotlib.pyplot as plt
import numpy as np

# 打开Lumerical仿真文件
fdtd = lumapi.FDTD("C:/Users/Admin/Desktop/PLS/pythonProject2/lianxu_run/fanzhen10.fsp")

# 提取x方向电场数据并保存
Ex = fdtd.getresult('monitor1', 'Ex')  # 获取x方向电场
np.save('Ex.npy', Ex)  # 保存Ex数据为.npy文件

# 提取坐标数据并保存
x_E = fdtd.getresult('monitor1', 'x')  # 获取x坐标
z_E = fdtd.getresult('monitor1', 'z')  # 获取z坐标
np.save('x_E.npy', x_E)  # 保存x坐标为.npy文件
np.save('z_E.npy', z_E)  # 保存z坐标为.npy文件

# 载入保存的Ex和坐标数据
Ex = np.load('Ex.npy')
x_E = np.load('x_E.npy')
z_E = np.load('z_E.npy')

# 压缩维度并处理Ex
Ex = np.squeeze(Ex)
Ix = np.abs(Ex) ** 2  # 计算强度
Ix = Ix[:, ::-1]  # 反转列方向
Ix = Ix.T  # 转置矩阵

# 处理z_E
z_E = z_E.T
z_E = z_E[:, ::-1]

# 设置参数
z_min = -30e-6
theta = 30

# 计算相关参数
xy = Ix.shape
p1 = round(xy[0] * abs(z_min) / (100 * 1e-6))

Isum = 0

# 加判断和计算
for ii in range(1):  # 假设只需处理第一个值
    y1 = z_E[ii, 0]  # 确保y1是单个数值
    y2 = z_E[ii, 0]  # 确保y2是单个数值

    x1 = -(y1 - z_min) / np.tan(np.deg2rad(90 - theta / 2))
    x2 = (y2 - z_min) / np.tan(np.deg2rad(90 - theta / 2))

    # 输出 x1 和 x2 的值
    print(f"x1: {x1}, x2: {x2}")

    x_lim1 = np.where(x_E >= x1)[0]
    x_lim2 = np.where(x_E <= x2)[0]

    print(f"x_E: {x_E}")
    plt.plot(x_E, marker='o')

    # 输出 x_lim1 和 x_lim2 的值
    print(f"x_lim1: {x_lim1}, x_lim2: {x_lim2}")

    if len(x_lim1) > 0 and len(x_lim2) > 0:
        x_left = x_lim1[0]+1
        x_right = x_lim2[-1]+1
        Isum += np.sum(Ix[0, x_left:x_right])

print(f"x_left: {x_left}")
print(f"x_right: {x_right}")

# 输出结果
print("Isum:", Isum)
print("Sum of Ix:", np.sum(Ix))