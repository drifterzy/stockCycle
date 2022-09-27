import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('./result/profit22.csv')
array = np.array(df['累计利润率'])
profit_list = array.tolist()

# 净值曲线
# plt.style.use("seaborn")
# plt.figure(figsize=(10,6))
# plt.plot(df['累计利润率'])
# plt.show()
# 最大回撤
def _withdraw_with_high_low(arr):
    """ 传入一个数组，返回最大回撤和对应的最高点索引、最低点索引 """
    _dp = 0  # 使用 _dp 表示 i 点的最大回撤
    i_high = 0  # 遍历时，0 ~ i - 1 中最高的点的索引，注意是索引

    # 全局最大回撤和对应的最高点和最低点的索引，注意是索引
    g_withdraw, g_high, g_low = float('-inf'), -1, -1

    for i in range(1, len(arr)):
        # 注意：此处求的是
        if arr[i_high] < arr[i-1]:  # 若 0 ~ i - 1 中最高的点小于当前点
            i_high = i-1  # 0 ~ i - 1 中最高的点的索引

        _dp = arr[i_high] - arr[i]  # _dp 表示 i 点的最大回撤
        if _dp > g_withdraw:  # 找到新的最大回撤，更新三个值
            g_withdraw = _dp
            g_high = i_high
            g_low = i

    return g_withdraw, g_high, g_low
# 最大回撤曲线
def draw_trend_and_withdraw(xs, ys, title, max_x, max_y, show_max_str, min_x, min_y, show_min_str,
                            withdraw=None, withdraw_x=None, withdraw_y=None):
    """ 根据数据绘制折线走势图 """
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(xs, ys)  # 根据数据绘制折线走势图
    plt.title(title)

    plt.scatter(min_x, min_y, color='r')  # 标记最低点
    plt.scatter(max_x, max_y, color='r')  # 标记最高点
    plt.annotate(show_min_str, xytext=(min_x, min_y), xy=(min_x, min_y))  # 标记提示
    plt.annotate(show_max_str, xytext=(max_x, max_y), xy=(max_x, max_y))  # 标记提示

    plt.plot([min_x, max_x], [min_y, max_y], color='b', linestyle='--')  # 连接最低净值点和最高净值点
    if withdraw_x is None or withdraw_y is None:
        plt.annotate(f'   {withdraw}', xytext=((max_x + min_x) / 2, (max_y + min_y) / 2), xy=((max_x + min_x) / 2, (max_y + min_y) / 2))  # 标记提示
    else:
        plt.annotate(f'   {withdraw}', xytext=(withdraw_x, withdraw_y), xy=(withdraw_x, withdraw_y))  # 标记提示

    plt.show()
# 每年的盈利金额
# 盈利次数，平均单次盈利额
# 亏损次数，平均单次亏损额

print(_withdraw_with_high_low(profit_list))
max_withdraw, _max, _min = _withdraw_with_high_low(profit_list)
start_day = df.iloc[_max,0]
end_day = df.iloc[_min,0]
print(start_day)
print(end_day)
draw_trend_and_withdraw(list(range(0, len(profit_list))), profit_list, f'{profit_list}', _max, profit_list[_max], f'最高点索引:{_max}',
                            _min, profit_list[_min], f'最低点索引:{_min}', max_withdraw)