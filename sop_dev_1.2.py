# SOP (Spacecraft Orbit Predictor) Dev 1.2 By @Asyncio_ (Arctan, Insane)
import numpy as np
import time
from logout import logout
import matplotlib.pyplot as plt  
import matplotlib.patches as patches
import copy
import json

config = dict()
with open('config.json', 'r') as f:  
    config = json.load(f)

CONSTANT_G = 6.6743*10**-11
PLANET_MASS = config['planet']['mass']
PLANET_RADIUS = config['planet']['radius']
SPACECRAFT_MASS = config['spacecraft']['mass']
SPACECRAFT_INIT_POSITION = np.array(config['spacecraft']['init_position']) # 航天器初始位置 M
SPACECRAFT_INIT_VELOCITY_VECTOR = np.array(config['spacecraft']['init_velocity']) # 航天器初始速度矢量 M/S
SIMULATE_TIME = config['simulator']['limit']

logout("""初始参数：
\t重力加速度常数\t%s
\t模拟时长\t%s min
\t天体质量\t%s kg
\t天体半径\t%s m
\t卫星质量\t%s kg
\t卫星初始位置\t%s
\t卫星初始速度矢量\t%s
\t天体逃逸速度\t%s m/s""" % (
    CONSTANT_G, 
    SIMULATE_TIME, 
    PLANET_MASS, 
    PLANET_RADIUS, 
    SPACECRAFT_MASS, 
    "%sm\t%sm" % tuple(config['spacecraft']['init_position']),
    "%sm/s\t%sm/s" % tuple(config['spacecraft']['init_velocity']),
    2 * CONSTANT_G * PLANET_MASS / PLANET_RADIUS
))

def get_gravity(position, m1, m2): # 函数：通过航天器位置、天体质量、航天器质量计算航天器所受引力
    return CONSTANT_G * ((m1 * m2) / (position[0]**2 + position[1]**2)) # 引力公式

def average(datas):
    sum = 0
    for i in datas:
        sum += i
    return sum / len(datas)

DISTANCE_RECORDS = []
VELOCITY_RECORDS = []
GRAVITY_RECORDS = []

def simulate(position, velocity, mins): # 模拟函数，模拟航天器的位置
    global PLANET_MASS, PLANET_RADIUS, SPACECRAFT_MASS, CONSTANT_G # 引入全局常量
    global DISTANCE_RECORDS, VELOCITY_RECORDS, GRAVITY_RECORDS
    path = [] # 初始化路径列表
    for t in range(60*mins): # 计算60*mins次
        G = get_gravity(position, PLANET_MASS, SPACECRAFT_MASS) # 获取引力
        k = (G/SPACECRAFT_MASS) / np.sqrt(position[0]**2 + position[1]**2) # 获取相似比
        gravity_vector = np.array([-k * position[0], -k * position[1]]) # 计算引力向量
        GRAVITY_RECORDS.append(copy.deepcopy(G))
        velocity += gravity_vector # 速度向量+引力向量（时间为1）
        VELOCITY_RECORDS.append(np.sqrt(velocity[0]**2 + velocity[1]**2))
        position += velocity # 位置向量+速度向量（时间为1）
        DISTANCE_RECORDS.append(np.sqrt(position[0]**2 + position[1]**2))
        path.append(copy.deepcopy(position)) # 记录当前位置
    return path # 计算完毕后返回所有位置数据

path = simulate(SPACECRAFT_INIT_POSITION, SPACECRAFT_INIT_VELOCITY_VECTOR, SIMULATE_TIME) # 模拟路径
results = [] # 格式化输出
for i in path:
    results.append('%s \t %s' % (i[0], i[1]))
#logout("\n".join(results))

# 创建一个新的图形窗口和子图  
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))  # 创建两个子图，一个在上，一个在下  
  
# 第一个子图：距离图  
x = list(range(len(DISTANCE_RECORDS)))  
axs[0, 0].plot(x, DISTANCE_RECORDS, marker='o')  # 在第一个子图上绘制曲线  
axs[0, 0].set_title('Curve Plot of Distances')  
axs[0, 0].set_xlabel('Time (Sec)')  
axs[0, 0].set_ylabel('Distance (Meter)')  
axs[0, 0].axhline(y=PLANET_RADIUS, color='r', linestyle='--')  
axs[0, 0].axhline(y=average(DISTANCE_RECORDS), color='g', linestyle='--')  

# 第二个子图：速度图
x = list(range(len(VELOCITY_RECORDS)))  
axs[0, 1].plot(x, VELOCITY_RECORDS, marker='o')  # 在第一个子图上绘制曲线  
axs[0, 1].set_title('Curve Plot of Velocities')  
axs[0, 1].set_xlabel('Time (Sec)')  
axs[0, 1].set_ylabel('Velocity (m/s)')
axs[0, 1].axhline(y=average(VELOCITY_RECORDS), color='g', linestyle='--')  

# 第三个子图：重力图
x = list(range(len(GRAVITY_RECORDS)))  
axs[1, 0].plot(x, GRAVITY_RECORDS, marker='o')  # 在第一个子图上绘制曲线  
axs[1, 0].set_title('Curve Plot of Gravities')  
axs[1, 0].set_xlabel('Time (Sec)')  
axs[1, 0].set_ylabel('Gravity (N)')
axs[1, 0].axhline(y=average(GRAVITY_RECORDS), color='g', linestyle='--')  
  
# 第四个子图：轨迹图  
datas = [[], []]  
for i in path:  
    datas[0].append(i[0])  
    datas[1].append(i[1])  
axs[1, 1].scatter(datas[0], datas[1])  
axs[1, 1].set_title('Spacecraft Orbit Trajectory')  # 设置第二个子图的标题  
axs[1, 1].grid(True)  # 在第二个子图上显示网格  
circle = patches.Circle((0, 0), PLANET_RADIUS, edgecolor='red', facecolor='none')  # 创建一个圆形补丁  
axs[1, 1].add_patch(circle)  # 将圆形补丁添加到第二个子图上  
  
# 调整子图之间的距离  
plt.tight_layout()  

logout('正在渲染图表', 1)
# 显示整个图形窗口  
plt.show()

logout('模拟完成', 2)