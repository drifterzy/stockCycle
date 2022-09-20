import pickle
import pandas as pd
from signal import getClosePrice2, nDayBefore


# 功能：生成交易日期和产品名的字典
# 输入：产品数组、开始、结束日期、日期差额
# 输出：字典变量
def get_signal(stock_dict, start_day, end_day, n):
    tradeDay = pd.read_csv('./tradeDay/tradeDay.csv')
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
        # 去重
        if len(signal_dict)==0:
            signal_dict.update(tmp_dict)
            day_storage = today
        else:
            if buySignal==signal_dict.get(day_storage):
                continue
            else:
                signal_dict.update(tmp_dict)
                day_storage = today

    f_save = open('./signal/cycle'+str(n)+'Signal.pkl', 'wb')
    pickle.dump(signal_dict, f_save)
    f_save.close()
    print('生成信号文件成功，日期间隔为'+str(n))
    return signal_dict

# 功能：去重交易日期和产品名的字典
# 输入：原始不去重的字典文件
# 输出：去重的字典变量
def get_distinct_signal(n):
    f_read = open('./signal/cycle'+n+'Signal.pkl', 'rb')
    signal_dict = pickle.load(f_read)
    f_read.close()

    date_list = list(signal_dict)

    target_list = []
    for i in range(len(date_list)-1):
        firstDate = date_list[i]
        date = date_list[i+1]
        firstProduct = signal_dict[firstDate]
        product = signal_dict[date]
        if product!=firstProduct:
            target_list.append(date)

    tmp_dict = {}
    target_dict = {}
    for i in range(len(target_list)):
        signal = signal_dict.get(target_list[i])
        tmp_dict[target_list[i]] = signal
        target_dict.update(tmp_dict)

    print("success")
    return target_dict


# 功能：获取结果
# 输入：交易日期和产品的dict，投入总价
# 输出：每次交易产生的盈利亏损情况
def get_result(trade_dict,total_price):
    date_list = list(trade_dict)
    # profit_dict = {}
    # tmp_dict = {}
    profit_list = []

    for i in range(len(date_list) - 1):
        firstDate = date_list[i]
        date = date_list[i + 1]
        firstProduct = trade_dict[firstDate]
        tmp_list = []
        if firstProduct=='空仓':
            tmp_list.append(firstDate)
            tmp_list.append(firstProduct)
            tmp_list.append(0)
            # tmp_dict[firstDate + " " + firstProduct] = 0
        else:
            close = getClosePrice2(firstDate,firstProduct)
            num = total_price/close
            close2 = getClosePrice2(date,firstProduct)
            margin = close2-close
            tmp_list.append(firstDate)
            tmp_list.append(firstProduct)
            tmp_list.append(margin*num)
            # tmp_dict[firstDate+" "+firstProduct] = margin*num
        # profit_dict.update(tmp_dict)
        profit_list.append(tmp_list)
    # print(sum(profit_dict.values()))
    # print("success")
    return profit_list