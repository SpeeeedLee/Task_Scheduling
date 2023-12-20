import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch

# 提供的字典
data = {0: [0, 0, 0, 0, 0, 0, 0, 0, 12, 12, 12, 12, 12, 0, 0, 22, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 1: [0, 0, 0, 0, 0, 0, 42, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 23, 23, 23, 23, 0, 0, 0, 0, 0, 0, 0, 34, 34, 34, 34, 34], 2: [0, 41, 41, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 3: [0, 0, 0, 0, 0, 21, 21, 21, 21, 21, 21, 21, 0, 0, 0, 31, 31, 31, 31, 31, 31, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 4: [0, 0, 11, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 13, 13, 13, 13, 0, 0, 32, 32, 32, 32, 33, 33, 33, 33, 0, 0, 0, 0, 0, 0, 0]}
data_2 = {0: [0, 0, 0, 0, 0, 12, 12, 12, 0, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 1: [0, 0, 0, 0, 0, 42, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 23, 23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 34, 0, 0, 0, 0, 0], 2: [41, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 3: [21, 21, 21, 21, 21, 0, 0, 0, 0, 0, 0, 0, 31, 31, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 4: [11, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 13, 0, 0, 0, 0, 0, 0, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
data_3 = {(0, 1): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 23, 23, 23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (1, 0): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (0, 2): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (2, 0): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (0, 3): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (3, 0): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 22, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (0, 4): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 13, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (4, 0): [0, 0, 0, 0, 12, 12, 12, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (1, 2): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (2, 1): [0, 0, 0, 42, 42, 42, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (1, 3): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (3, 1): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (1, 4): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (4, 1): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 34, 34, 0, 0, 0, 0, 0], (2, 3): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (3, 2): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (2, 4): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (4, 2): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (3, 4): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (4, 3): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}


# 生成色彩映射，每个任务ID的首数字对应不同的颜色
colors = list(mcolors.TABLEAU_COLORS.keys())
color_map = {task_id: colors[int(str(task_id)[0]) % len(colors)] if task_id != 0 else 'white' for task_id in set(x for lst in data.values() for x in lst)}

# 为 data_2 使用统一的淡皮肤色
light_skin_color = mcolors.to_rgba('peachpuff', 0.6)

fig, ax = plt.subplots(figsize=(15, 10))  # 调整图表尺寸

# 绘制 data 中的数据
for computer_id, tasks in data.items():
    start_time = 0
    for i in range(1, len(tasks)):
        if tasks[i] != tasks[i-1]:
            ax.broken_barh([(start_time, i-start_time)], (computer_id-0.4, 0.8), facecolors=color_map[tasks[i-1]])
            if tasks[i-1] != 0:
                ax.text(start_time, computer_id, str(tasks[i-1]), va='center', ha='left', color='black')
            start_time = i
    ax.broken_barh([(start_time, len(tasks)-start_time)], (computer_id-0.4, 0.8), facecolors=color_map[tasks[-1]])

# 绘制 data_2 中的数据，使用较高的透明度
for computer_id, tasks in data_2.items():
    start_time = 0
    for i in range(1, len(tasks)):
        if tasks[i] != tasks[i-1]:
            ax.broken_barh([(start_time, i-start_time)], (computer_id-0.4, 0.8), facecolors=light_skin_color if tasks[i-1] != 0 else 'white', alpha=0.5)
            if tasks[i-1] != 0:
                ax.text(start_time, computer_id, str(tasks[i-1]), va='center', ha='left', color='black', alpha=0.5)
            start_time = i
    ax.broken_barh([(start_time, len(tasks)-start_time)], (computer_id-0.4, 0.8), facecolors=light_skin_color if tasks[-1] != 0 else 'white', alpha=0.5)

# 绘制 data_3 中的数据，对两台电脑各自画一条黑线
for (comp1, comp2), tasks in data_3.items():
    for i, task in enumerate(tasks):
        if task != 0:
            # 在每台电脑的时间区块中间画上水平黑线
            ax.plot([i, i+1], [comp1 , comp1 + 0.2], color='black')
            ax.plot([i, i+1], [comp2+0.2 , comp2], color='black')


# 设置图表格式
ax.set_xlabel('Time (s)')
ax.set_ylabel('Computer ID')
ax.set_yticks(range(len(data)))
ax.set_yticklabels(['Computer {}'.format(i) for i in range(len(data))])
ax.set_title('Gantt Chart of Tasks on Computers')

# 创建图例
unique_jobs = set(int(str(task_id)[0]) for task_id in color_map if task_id != 0)
legend_elements = [Patch(facecolor=colors[job % len(colors)], label='Job {}'.format(job)) for job in unique_jobs]
legend_elements.append(Patch(facecolor=light_skin_color, label='Set Up'))
ax.legend(handles=legend_elements)

plt.show()