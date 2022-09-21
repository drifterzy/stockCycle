import pickle
import akshare as ak
import pandas as pd
from process import get_signal, get_result


# 功能：ETF轮动回测代码
# 输入：产品数组、开始、结束日期、投入总额、日期差额
# 输出：日期、买入节点、此次交易的盈利亏损额、总盈利亏损额
def etf_cycle(stock_dict, start_day, end_day, total_price, n):
    # trade_df = get_signal(stock_dict, start_day, end_day, n)
    trade_df = pd.read_csv('./signal/OriSignal22.csv')
    profit_list = get_result(trade_df, total_price)
    df = pd.DataFrame(profit_list,columns=['date','product','buy_num','budget','profit'])
    df.to_csv('./result/profit'+str(n)+'.csv',index=False)


if __name__ == '__main__':
    stock_dict = {'sh511010': '国债ETF:511010', 'sh510050': '上证50ETF:510050', 'sz159915': '创业板ETF:159915'}
    start_day = '2015-01-01'
    end_day = '2022-09-19'
    n = 22
    total_price = 10000
    # 保存最新的数据文件，加速读写速度
    for stock in stock_dict.keys():
        df = ak.fund_etf_hist_sina(symbol=stock)[['date', 'open', 'close']]
        df.to_csv('./stock_price/'+stock+'.csv',index=False)
    # 执行策略
    etf_cycle(stock_dict, start_day, end_day, total_price, n)
    print("etf轮动完成")
    # 分析结果：文字、表格、图片
