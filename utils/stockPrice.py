import akshare as ak
from datetime import date
import pandas as pd


def getStockPrice(stock):
    df = ak.fund_etf_hist_sina(symbol=stock)[['date', 'open', 'close']]
    df.to_csv('./stockPrice/' + stock + '.csv', index=False)

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
    df = pd.read_csv('./stockPrice/'+stock_string+'.csv')
    try:
        close = df[df['date'] == date_string]['close'].values[0]
        return close
    except IndexError:
        print(date_string+" 今天不是交易日，好好休息吧～")
    except AttributeError:
        print(" 起始日期不是交易日哦，好好休息吧～")

# 功能：获取当日开盘价
# 输入：日期、股票名称
# 输出：当日收盘价
def getOpenPrice(date_string,stock_string):
    df = pd.read_csv('./stockPrice/'+stock_string+'.csv')
    try:
        close = df[df['date'] == date_string]['open'].values[0]
        return close
    except IndexError:
        print(date_string+" 今天不是交易日，好好休息吧～")
    except AttributeError:
        print(" 起始日期不是交易日哦，好好休息吧～")