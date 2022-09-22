import math
import pickle
import pandas as pd
from signal import getClosePrice2, nDayBefore, getOpenPrice


# 功能：生成交易日期和产品名的字典
# 输入：产品数组、开始、结束日期、日期差额
# 输出：字典变量
def get_signal(stock_dict, start_day, end_day, n):
    tradeDay = pd.read_csv('./tradeDay/tradeDay.csv')
    signal_dict_ori = {}
    signal_dict = {}
    day_storage = ""
    for dayRow in tradeDay.iterrows():
        today = dayRow[1]['calendar_date']
        # 从22天之后开始执行，跳过创业板2月8号无数据以及"22"天后的3月17号异常日期
        if today < start_day or today > end_day or today == '2021-02-08' or today == '2021-03-17':
            continue
        n_day_before = nDayBefore(today, n)
        close_list_today = []
        close_list_startday = []
        profit_list = []
        for stock in stock_dict.keys():
            # 结束日期收盘价
            close = getClosePrice2(today, stock)
            close_list_today.append(close)
            # 起始日期收盘价
            close_startDay = getClosePrice2(n_day_before, stock)
            close_list_startday.append(close_startDay)
            # 涨跌幅
            profit = (close - close_startDay) / close_startDay
            profit_list.append(profit)
        # 计算当日买入信号
        maxIndex = profit_list.index(max(profit_list))
        buySignal = list(stock_dict.items())[maxIndex][0]
        tmp_dict = {}
        if max(profit_list) > 0:
            tmp_dict[today] = buySignal
        else:
            buySignal = "空仓"
            tmp_dict[today] = buySignal
        # print(tmp_dict)
        signal_dict_ori.update(tmp_dict)
        # 去重
        if len(signal_dict) == 0:
            signal_dict.update(tmp_dict)
            day_storage = today
        else:
            if buySignal == signal_dict.get(day_storage):
                continue
            else:
                signal_dict.update(tmp_dict)
                day_storage = today
    # 保存去重信号df
    df = pd.DataFrame.from_dict(signal_dict,orient='index',columns=['product'])
    df = df.reset_index().rename(columns = {"index": "date"})
    df.to_csv('./signal/DistinctSignal' + str(n) + '.csv',index=False)
    # 保存原始信号df2
    df2 = pd.DataFrame.from_dict(signal_dict_ori, orient='index', columns=['product'])
    df2 = df2.reset_index().rename(columns = {"index": "date"})
    df2.to_csv('./signal/OriSignal' + str(n) + '.csv',index=False)
    print('生成信号文件成功，日期间隔为'+str(n))
    return df2

# 功能：获取交易数量
# 输入：投入总价和产品单价
# 输出：每次交易>=总价的数量
def get_num(total_price,close):
    num = total_price / close // 100
    plus = (total_price / close) % 100
    if plus == 0:
        buy_num = num * 100
    else:
        buy_num = (num + 1) * 100
    return buy_num


# 功能：获取结果
# 输入：交易日期和产品的dict，投入总价
# 输出：每次交易产生的盈利亏损情况
def get_result(trade_df,total_price):
    profit_list = []
    # total_profit = total_price
    total_profit_rate = 0
    for i in range(0, len(trade_df)-1):
        firstDate = trade_df.iloc[i]['date']
        firstProduct = trade_df.loc[trade_df['date'] == firstDate, 'product'].values[0]
        secondDate = trade_df.iloc[i + 1]['date']
        tmp_list = []
        if firstProduct=='空仓':
            tmp_list.append(firstDate)
            tmp_list.append(firstProduct)
            tmp_list.append(0)
            tmp_list.append(0)
            tmp_list.append(0)
            tmp_list.append(0)
            tmp_list.append(0)
            tmp_list.append(0)
            tmp_list.append(0)
            tmp_list.append(total_profit_rate)
        else:
            close = getClosePrice2(firstDate,firstProduct)
            close2 = getClosePrice2(secondDate, firstProduct)
            if i==0:
                # 计算买入数量
                buy_num = get_num(total_price,close)
                storage_num = buy_num
                buy_total = close * buy_num * 1.0001
                sell_total = close2 * buy_num * 0.9999
            else:
                beforeDate = trade_df.iloc[i - 1]['date']
                beforeProduct = trade_df.loc[trade_df['date'] == beforeDate, 'product'].values[0]
                if firstProduct==beforeProduct:
                    buy_num = storage_num
                    buy_total = close * buy_num
                    sell_total = close2 * buy_num
                else:
                    buy_num = get_num(total_price, close)
                    storage_num = buy_num
                    buy_total = close * buy_num * 1.0001
                    sell_total = close2 * buy_num * 0.9999

            # 信号日期
            tmp_list.append(firstDate)
            # 股票名称
            tmp_list.append(firstProduct)
            # 计划买入数量
            tmp_list.append(buy_num)
            # 计划买入单价：第二天以昨天的收盘价买入
            tmp_list.append(close)
            # 买入总价（含手续费）
            tmp_list.append(buy_total)
            # 计划卖出单价：第二天以昨天的收盘价卖出
            tmp_list.append(close2)
            # 卖出总价（含手续费）
            tmp_list.append(sell_total)
            # 此次交易的利润
            tmp_profit = sell_total-buy_total
            tmp_list.append(tmp_profit)
            # 此次交易的利润率
            tmp_profit_rate = tmp_profit/buy_total
            tmp_list.append(tmp_profit_rate)
            # 累计总金额
            # total_profit = total_profit+tmp_profit
            # 累计利润率
            total_profit_rate = total_profit_rate+tmp_profit_rate
            tmp_list.append(total_profit_rate)
        profit_list.append(tmp_list)
    return profit_list