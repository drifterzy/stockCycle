from datetime import date
import akshare as ak
import pandas as pd
# 功能：获取当日收盘价
# 输入：日期、股票名称
# 输出：当日收盘价
def getClosePrice(date_string,stock_string):
    df = ak.fund_etf_hist_sina(symbol=stock_string)[['date','close']]
    try:
        now = date(*map(int, date_string.split('-')))
        close = df[df['date'] == now]['close'].values[0]
        return close
    except IndexError:
        print(date_string+" 今天不是交易日，好好休息吧～")
    except AttributeError:
        print(" 起始日期不是交易日哦，好好休息吧～")

# 功能：获取当日收盘价2
# 输入：日期、股票名称
# 输出：当日收盘价
def getClosePrice2(date_string,stock_string):
    df = pd.read_csv('./stock_price/'+stock_string+'.csv')
    try:
        close = df[df['date'] == date_string]['close'].values[0]
        return close
    except IndexError:
        print(date_string+" 今天不是交易日，好好休息吧～")
    except AttributeError:
        print(" 起始日期不是交易日哦，好好休息吧～")
# 功能：获取n天前的指定交易日
# 输入：日期、时间差
# 输出：交易日
def nDayBefore(date_string,n):
    tradeDay = pd.read_csv('./tradeDay/tradeDay.csv')
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