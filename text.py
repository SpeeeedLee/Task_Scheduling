import random

# 给定的列表
lst = [77, 31, 32, 33, 21, 11, 12, 13, 41, 42, 34, 22, 23]

# 保留第一个元素
first_element = lst[0]

# 根据首位数字分组并排序每组
groups = {}
for num in lst[1:]:
    key = num // 10
    if key not in groups:
        groups[key] = []
    groups[key].append(num)
for key in groups:
    groups[key].sort()

# 随机化：随机调整组间顺序，以及组内部分元素位置
group_keys = list(groups.keys())
random.shuffle(group_keys)
new_lst = [first_element]
for key in group_keys:
    group = groups[key]
    # 可以在这里添加更多随机化逻辑，例如随机交换组内元素
    new_lst.extend(group)

print(new_lst)
