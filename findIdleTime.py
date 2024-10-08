def find_idle_time(used_time_slots, start_time, end_time):
    # 首先按开始时间对时间段排序
    used_time_slots.sort(key=lambda x: x[0])

    # 合并重叠的时间段
    merged_slots = []
    for slot in used_time_slots:
        if not merged_slots or merged_slots[-1][1] < slot[0]:
            merged_slots.append(slot)
        else:
            # 如果有重叠，更新结束时间
            merged_slots[-1][1] = max(merged_slots[-1][1], slot[1])

    idle_time_list = []

    # 计算最开始的空闲时间段
    if merged_slots[0][0] > start_time:
        idle_time_list.append([start_time, merged_slots[0][0]])

    # 计算中间的空闲时间段
    for i in range(1, len(merged_slots)):
        previous_end_time = merged_slots[i - 1][1]
        current_start_time = merged_slots[i][0]
        if current_start_time > previous_end_time:
            idle_time_list.append([previous_end_time, current_start_time])

    # 计算最后的空闲时间段
    if merged_slots[-1][1] < end_time:
        idle_time_list.append([merged_slots[-1][1], end_time])

    return idle_time_list


# 该算法的时间复杂度可以分为两个部分来分析：
#
# 排序阶段：在代码的第一步中，我们对 used_time_slots 进行了排序，时间复杂度为 O(nlogn)，其中 n 是时间段的数量。
#
# 合并重叠时间段阶段：在合并时间段的过程中，我们对每个时间段进行一次遍历，合并时会比较时间段的起止时间。这个阶段的时间复杂度是 O(n)。
#
# 计算空闲时间段阶段：在合并后的时间段中，我们再次遍历一次已合并的时间段，来计算每两个相邻时间段之间的空闲时间。因此，这部分的时间复杂度也是 O(n)。
#
# 总体时间复杂度：
# 排序： O(nlogn)
# 合并和计算空闲时间段： O(n)
# 因此，算法的总时间复杂度为 O(nlogn)，其中 n 是输入的时间段数量。
#
# 排序的步骤是整个算法的主导部分，因此该算法的主要复杂度是由排序的复杂度 (nlogn) 决定的。


# 示例：假设有多个已占用时间段
used_time_slots = [[12, 13], [15, 16], [18, 19], [3, 4], [40, 60], [45, 55], [15, 23]]
start_time = 0
end_time = 70

idle_time_list = find_idle_time(used_time_slots, start_time, end_time)
print(idle_time_list)

# 示例：假设有多个已占用时间段
used_time_slots = [[12, 13], [15, 16], [18, 19], [3, 4], [5, 8], [11, 12], [40, 60], [45, 55], [15, 23]]
start_time = 0
end_time = 70

idle_time_list = find_idle_time(used_time_slots, start_time, end_time)
print(idle_time_list)

def find_idle_time_via_tags(used_time_slots, start_time, end_time):
    events = []

    # 给所有开始和结束时间打上 tag，并放入 events
    for slot in used_time_slots:
        events.append((slot[0], 'start'))  # 开始时间
        events.append((slot[1], 'end'))  # 结束时间

    # 对 events 按时间排序。如果时间相同，优先处理 'end'，保证先结束再开始
    events.sort(key=lambda x: (x[0], x[1] == 'start'))

    idle_time_list = []
    c = 0  # 活跃状态计数
    prev_time = start_time

    # 遍历所有事件
    for time, tag in events:
        if c == 0 and time > prev_time:  # 如果当前没有任务占用，则计算空闲时间
            idle_time_list.append([prev_time, time])

        # 更新活跃状态计数
        if tag == 'start':
            c += 1
        elif tag == 'end':
            c -= 1

        # 更新前一个时间点
        prev_time = time

    # 处理最后一段空闲时间
    if prev_time < end_time:
        idle_time_list.append([prev_time, end_time])

    return idle_time_list

# 解释：
# 打 tag：将所有的开始时间和结束时间加上标签，然后放到 events 列表中。每个元素是一个元组 (时间, 标签)，其中标签可以是 'start' 或 'end'。
#
# 排序：对 events 列表按时间进行排序。如果两个事件的时间相同，优先处理 end 标签（即先结束再开始，这样可以防止同一时间点既结束又开始的情况）。
#
# 遍历并更新计数：通过遍历 events，当 c 为 0 时，表示之前一段时间是空闲时间段。我们记录这些空闲时间。
#
# 处理最后的空闲时间段：如果遍历结束后，prev_time 小于 end_time，还要处理从最后一个结束时间到总时间结束的空闲时间段。
#
# 时间复杂度分析：
# 打标签阶段：将每个时间段的开始和结束打标签，需要遍历所有时间段，因此这部分时间复杂度为 O(n)。
#
# 排序阶段：我们将 2n 个标签进行排序，时间复杂度为 O(nlogn)。
#
# 遍历阶段：遍历所有事件并更新计数，同样需要 O(n) 的时间。
#
# 总时间复杂度：
# 由于排序操作的主导作用，整个算法的时间复杂度为 O(nlogn)。

# 示例：
used_time_slots = [[12, 13], [15, 16], [18, 19], [3, 4], [40, 60], [45, 55], [15, 23]]
start_time = 0
end_time = 70

idle_time_list = find_idle_time_via_tags(used_time_slots, start_time, end_time)
print(idle_time_list)

used_time_slots = [[12, 13], [15, 16], [18, 19], [3, 4], [5, 8], [11, 12], [40, 60], [45, 55], [15, 23]]
start_time = 1
end_time = 70

idle_time_list = find_idle_time_via_tags(used_time_slots, start_time, end_time)
print(idle_time_list)


# ##########################################################################

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 定义处理的计算任务，每个任务的使用时间段
tasks = {
    'Task1': [[12, 13], [15, 16], [18, 19]],
    'Task2': [[3, 4], [5, 8], [11, 12]],
    'Task3': [[40, 60], [45, 55], [15, 23]],
}

# 颜色列表，为每个任务及闲置时间分配不同的颜色
colors = ['green', 'blue', 'purple', 'red']  # 最后一个颜色是闲置时间的颜色

def find_idle_time_via_tags(used_time_slots, start_time, end_time):
    events = []

    # 给所有开始和结束时间打上 tag，并放入 events
    for slot in used_time_slots:
        events.append((slot[0], 'start'))  # 开始时间
        events.append((slot[1], 'end'))  # 结束时间

    # 对 events 按时间排序。如果时间相同，优先处理 'end'，保证先结束再开始
    events.sort(key=lambda x: (x[0], x[1] == 'start'))

    idle_time_list = []
    c = 0  # 活跃状态计数
    prev_time = start_time

    # 遍历所有事件
    for time, tag in events:
        if c == 0 and time > prev_time:  # 如果当前没有任务占用，则计算空闲时间
            idle_time_list.append([prev_time, time])

        # 更新活跃状态计数
        if tag == 'start':
            c += 1
        elif tag == 'end':
            c -= 1

        # 更新前一个时间点
        prev_time = time

    # 处理最后一段空闲时间
    if prev_time < end_time:
        idle_time_list.append([prev_time, end_time])
    print(f"idle_time_list = {idle_time_list}")

    return idle_time_list

def visualize_tasks(tasks, start_time, end_time):
    fig, ax = plt.subplots(figsize=(10, 6))

    y_labels = []
    used_time_slots = []
    y_pos = 0
    color_idx = 0  # 颜色索引，用来给每个任务分配不同的颜色

    # 对每个任务进行可视化
    for task, time_slots in tasks.items():
        y_labels.append(task)
        for slot in time_slots:
            ax.broken_barh([(slot[0], slot[1] - slot[0])],
                           (y_pos - 0.4, 0.8),
                           facecolors=colors[color_idx],
                           alpha=0.8)  # 设置透明度为0.8
            used_time_slots.append(slot)
        y_pos += 1
        color_idx += 1

    # 设置图形的纵轴和横轴标签
    y_labels.append('Idle Time')  # 添加“闲置时间”的标签
    ax.set_yticks(range(len(tasks) + 1))
    ax.set_yticklabels(y_labels)
    ax.set_xlabel('Time')
    ax.set_ylabel('Tasks')

    # # 找出空闲时间并标记出来，分配最后一个颜色
    # idle_times = find_idle_time_via_tags(used_time_slots, start_time, end_time)
    # for idle in idle_times:
    #     ax.broken_barh([(idle[0], idle[1] - idle[0])],
    #                    (-1, len(tasks) + 1),
    #                    facecolors=colors[-1],
    #                    alpha=0.3)  # 设置透明度为0.3
    #
    # # 添加图例，每个任务和闲置时间都有一个图例
    # task_patches = [mpatches.Patch(color=colors[i], label=f'Task{i + 1}') for i in range(len(tasks))]
    # idle_patch = mpatches.Patch(color=colors[-1], label='Idle Time', alpha=0.3)
    # plt.legend(handles=task_patches + [idle_patch])
    #
    # plt.title('CPU Usage of Multiple Tasks')
    # plt.show()
    # 找出空闲时间并标记出来，分配最后一个颜色且仅限制在第一行
    idle_times = find_idle_time_via_tags(used_time_slots, start_time, end_time)
    for idle in idle_times:
        ax.broken_barh([(idle[0], idle[1] - idle[0])],
                       (y_pos - 0.4, 0.8),
                       facecolors=colors[-1],
                       alpha=0.3)  # 设置透明度为0.3

        # 绘制虚线，将粉色块的左右两侧向下延伸
        ax.vlines(x=idle[0], ymin=-0.4, ymax=y_pos - 0.4, colors='black', linestyles='dashed')
        ax.vlines(x=idle[1], ymin=-0.4, ymax=y_pos - 0.4, colors='black', linestyles='dashed')

    # 添加图例，每个任务和闲置时间都有一个图例
    task_patches = [mpatches.Patch(color=colors[i], label=f'Task{i + 1}') for i in range(len(tasks))]
    idle_patch = mpatches.Patch(color=colors[-1], label='Idle Time', alpha=0.3)

    # 通过 bbox_to_anchor 和 loc 参数，将图例放在图像外
    plt.legend(handles=task_patches + [idle_patch], bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.title('CPU Usage of Multiple Tasks')
    plt.tight_layout()  # 确保图像不被元素遮挡
    plt.show()

# 设置任务时间段和 CPU 可用的时间范围
start_time = 0
end_time = 70

# 可视化任务以及空闲时间
visualize_tasks(tasks, start_time, end_time)

