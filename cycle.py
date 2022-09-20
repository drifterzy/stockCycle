from email_send import mail
from signal import signal, signal2
from datetime import date


close_list_today=[]
close_list_startday = []
profit_list = []
today = date.today().strftime("%Y-%m-%d")
startDay = signal2(today,22)
stock_list = ["sh511010", "sh510050", "sz159915"]
stock_dict = {'sh511010': '国债ETF:511010', 'sh510050': '上证50ETF:510050', 'sz159915': '创业板ETF:159915'}
for stock in stock_dict.keys():
    #结束日期收盘价
    close = signal(today,stock)
    close_list_today.append(close)
    # 起始日期收盘价
    close_startDay = signal(startDay,stock)
    close_list_startday.append(close_startDay)
    # 涨跌幅
    profit = (close-close_startDay)/close_startDay
    profit_list.append(profit)

# 计算涨跌幅情况
maxIndex = profit_list.index(max(profit_list))
buySignal = list(stock_dict.items())[maxIndex][1]
if(max(profit_list)>0):
    signalStr = today+"应该买入"+buySignal
else:
    signalStr = today+"应该空仓"

# 发送邮件
mail(signalStr,"1074725704@qq.com")
mail(signalStr,"223540840@qq.com")