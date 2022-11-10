import pickle
import akshare as ak
import pandas as pd
from process import get_signal, get_result
from utils.stockPrice import getStockPrice
from utils.tradeDay import getTradeDay

# 功能：ETF轮动回测代码
# 输入：产品数组、开始、结束日期、投入总额、日期差额
# 输出：日期、买入节点、此次交易的盈利亏损额、总盈利亏损额



def etf_cycle(stock_dict, start_day, end_day, total_price, n):
    distinctSignal,allSignal = get_signal(stock_dict, start_day, end_day, n)
    profit_list = get_result(allSignal, total_price)
    df = pd.DataFrame(profit_list,columns=['信号日期','股票名称','股票数量','买入单价','买入总价','卖出单价','卖出总价','单次利润','单次利润率','累计利润率'])
    df.to_csv('./result/result'+str(n)+'day.csv',index=False)


if __name__ == '__main__':
    stock_dict = {'sh511010': '国债ETF:511010', 'sh510050': '上证50ETF:510050', 'sz159915': '创业板ETF:159915'}
    start_day = '2015-01-01'
    end_day = '2022-11-10'
    n = 22
    total_price = 10000
    # 获取交易日
    getTradeDay(start_day, end_day)
    # 获取股票价格
    print("获取股票价格开始")
    for stock in stock_dict.keys():
        getStockPrice(stock)
    print("获取股票价格结束")
    # 执行策略
    print("etf轮动开始")
    etf_cycle(stock_dict, start_day, end_day, total_price, n)
    print("etf轮动结束")
    # 分析结果：文字、表格、图片
