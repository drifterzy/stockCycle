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


# 功能：获取结果
# 输入：交易日期和产品的dict，投入总价
# 输出：每次交易产生的盈利亏损情况
def get_result(trade_df,total_price):
    profit_list = []
    for i in range(0, len(trade_df)-1):
        firstDate = trade_df.iloc[i]['date']
        date = trade_df.iloc[i+1]['date']
        # test = trade_df.loc[trade_df['date'] == date, 'product'].values[0]
        firstProduct = trade_df.loc[trade_df['date'] == date, 'product'].values[0]
        tmp_list = []
        if firstProduct=='空仓':
            tmp_list.append(firstDate)
            tmp_list.append(firstProduct)
            tmp_list.append(0)
            tmp_list.append(0)
            tmp_list.append(0)
        else:
            close = getClosePrice2(firstDate,firstProduct)
            num = total_price/close//100
            buy_num = (num+1)*100
            close2 = getClosePrice2(date,firstProduct)
            margin = close2-close
            tmp_list.append(firstDate)
            tmp_list.append(firstProduct)
            tmp_list.append(buy_num)
            tmp_list.append(close*buy_num)
            tmp_list.append(margin*buy_num-close*buy_num*0.0001-close2*buy_num*0.0001)
        profit_list.append(tmp_list)
    return profit_list