import baostock as bs
import pandas as pd
import akshare as ak

# 获取交易日期，pandas对应列名为trade_date
def getTradeDay():
    tool_trade_date_hist_sina_df = ak.tool_trade_date_hist_sina()
    tool_trade_date_hist_sina_df.to_csv("./tradeDay/tradeDay.csv", encoding="gbk", index=False)


# 功能：获取n天前的指定交易日
# 输入：日期、时间差
# 输出：交易日
def getNDayBefore(date_string,n):
    tradeDay = pd.read_csv('/Users/leo/Documents/project/stockCycle/tradeDay/tradeDay.csv')
    try:
        endIndex = tradeDay[tradeDay['trade_date'] == date_string].index.tolist()[0]
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