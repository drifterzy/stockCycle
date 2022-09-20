import baostock as bs
import pandas as pd

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

#### 获取交易日信息 ####
rs = bs.query_trade_dates(start_date="2015-01-01", end_date="2022-12-31")
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
# count = 22
# for index, row in res.iterrows():
#   print(index, row)
#### 结果集输出到csv文件 ####
res.to_csv("./tradeDay/2015To2022.csv", encoding="gbk", index=False)
print(res)

#### 登出系统 ####
bs.logout()