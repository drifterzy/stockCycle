import pickle
import akshare as ak
from analysis import get_signal, get_result


# 功能：ETF轮动回测代码
# 输入：产品数组、开始、结束日期、投入总额、日期差额
# 输出：日期、买入节点、此次交易的盈利亏损额、总盈利亏损额
def etf_cycle(stock_dict, start_day, end_day, total_price, n):
    trade_dict = get_signal(stock_dict, start_day, end_day, n)
    profit_dict = get_result(trade_dict, total_price)
    f_save = open('./result/profit' + str(n) + '.pkl', 'wb')
    pickle.dump(profit_dict, f_save)
    f_save.close()


if __name__ == '__main__':
    stock_dict = {'sh511010': '国债ETF:511010', 'sh510050': '上证50ETF:510050', 'sz159915': '创业板ETF:159915'}
    start_day = '2015-01-01'
    end_day = '2022-09-19'
    n = 22
    total_price = 10000
    # 保存最新的数据文件，加速读写速度
    for stock in stock_dict.keys():
        df = ak.fund_etf_hist_sina(symbol=stock)[['date', 'close']]
        df.to_csv('./stock_price/'+stock+'.csv',index=False)
    # 执行策略
    etf_cycle(stock_dict, start_day, end_day, total_price, n)
    print("etf轮动完成")
    # 分析结果：文字、表格、图片
