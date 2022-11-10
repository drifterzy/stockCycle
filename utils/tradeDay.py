import baostock as bs
import pandas as pd
import akshare as ak

def getTradeDay(begin,end):
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    #### 获取交易日信息 ####
    rs = bs.query_trade_dates(start_date=begin, end_date=end)
    print('query_trade_dates respond error_code:'+rs.error_code)
    print('query_trade_dates respond  error_msg:'+rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    res = result[result['is_trading_day']=='1']
    res = res.drop(['is_trading_day'],axis=1)
    res['calendar_date'] = res['calendar_date'].astype(str)
    res = res.reset_index(drop=True)
    #### 结果集输出到csv文件 ####
    res.to_csv("./tradeDay/tradeDay.csv", encoding="gbk", index=False)

    #### 登出系统 ####
    bs.logout()

# 功能：获取n天前的指定交易日
# 输入：日期、时间差
# 输出：交易日
def getNDayBefore(date_string,n):
    tradeDay = pd.read_csv('/Users/leo/Documents/project/stockCycle/tradeDay/tradeDay.csv')
    try:
        endIndex = tradeDay[tradeDay['calendar_date'] == date_string].index.tolist()[0]
        beginIndex = endIndex-n
        beginDay = tradeDay.iloc[beginIndex,0]
        return beginDay
    except IndexError:
        print(date_string+" 今天不是交易日，好好休息吧～")

# 功能：获取股票开始日期
# 输入：股票名称
# 输出：返回开始日期
def getIpoDay(stock_string):
    df = ak.fund_etf_hist_sina(symbol=stock_string)[['date','close']]
    beginDay = df.iloc[0,0]
    str = beginDay.strftime('%Y-%m-%d')
    return str