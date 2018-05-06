# -- coding: utf-8 --
#在第一行加上上面这句才能注释中文
"""
pip install lxml
pip install sqlalchemy
pip install tushare
pip install tushare --upgrade
pip install pandas
pip install requests
pip install bs4
pip install mysql -python
"""
#上面是需要安装的包
from sqlalchemy import create_engine
import tushare as ts
import datetime
import pandas as pd
today = datetime.date.today()
#连接数据库mysql
，
数据库用户名root密码1234
，
数据库为new_schema
，
以utf8编码方式
engine = create_engine('mysql://root:1234@127.0.0.1/new_schema?charset=utf8')
#基本情况
df=ts.get_stock_basics()

#df.to_sql('stock_basics',engine,if_exists='replace')
df.to_sql('stock_basics',engine,if_exists='append')
#需要运行第二次后才行
，
对于基本情况的获取
df=ts.get_report_data(today.year-2,4)
df.to_sql('report_data0',engine)
df=ts.get_report_data(today.year-3,4)
df.to_sql('report_data1',engine)
df=ts.get_report_data(today.year-4,4)
df.to_sql('report_data2',engine)
df=ts.get_report_data(today.year-5,4)
df.to_sql('report_data3',engine)
df=ts.get_report_data(today.year-6,4)
df.to_sql('report_data4',engine)

#当前股价
df=ts.get_today_all()
df.to_sql('stock_price',engine)
#股权质押
df=ts.stock_pledged()

df.to_sql("stock_pledged",engine)
"""
#业绩报告
df=ts.get_report_data(today.year,1)
df.to_sql('report_data0',engine)

df=ts.get_report_data(today.year-1,4)
df.to_sql('report_data_1',engine)
df=ts.get_report_data(today.year-2,4)
df.to_sql('report_data_2',engine)
df=ts.get_report_data(today.year-3,4)
df.to_sql('report_data_3',engine)
df=ts.get_report_data(today.year-4,4)
df.to_sql('report_data_4',engine)
df=ts.get_report_data(today.year-5,4)
df.to_sql('report_data_5',engine)
"""
"""
#盈利能力
df=ts.get_profit_data(2014,3)
df.to_sql('profit_data',engine,if_exists='append')
#营运能力
df=ts.get_operation_data(2014,3)
df.to_sql('operation_data',engine,if_exists='append')
#成长能力
df=ts.get_growth_data(2014,3)
df.to_sql('growth_data',engine,if_exists='append')
#偿债能力
df=ts.get_debtpaying_data(2014,3)
df.to_sql('debtpaying_data',engine,if_exists='append')
#现金流量
df=ts.get_cashflow_data(2014,3)
df.to_sql('cashflow_data',engine,if_exists='append')
"""
#调用mysql存储过程实现对原始数据的加工处理

#美股
#http://python.tedu.cn/know/291043.html

二
、
MYSQL筛选分析

drop table new_schema.stock_basics,new_schema.stock_price,new_schema.report_data0,new_schema.report_data1,new_schema.report_data2,new_schema.report_data3,new_schema.report_data4,new_schema.report_data5,new_schema.report_data6,,new_schema.report_data7,new_schema.report_data8,new_schema.stock_pledged

SELECT distinct a.code as 代码,a.name as 名称,a.industry as 行业,a.area as 地域,a.pe as 静态市盈率,a.totalAssets as 总资产,

a.liquidAssets as 流动资产,a.fixedAssets as 固定资产,a.reservedPerShare,a.esp,a.bvps,a.pb as 市净率,a.timeToMarket as 上市时间,a.perundp

,b.roe as 净资产收益率, (b.roe+d.roe+e.roe+f.roe+g.roe)/5 as 近5年平均净资产收益率,(b.roe+d.roe+e.roe+f.roe+g.roe)/5/a.pb as 近5年平均除以市净率, c.trade as 交易价格,c.per as 动态市盈率

FROM new_schema.stock_basics a left join new_schema.report_data0 b

on a.code=b.code left join new_schema.stock_price c

on a.code=c.code left join new_schema.report_data1 d

on a.code=d.code left join new_schema.report_data2 e

on a.code=e.code left join new_schema.report_data3 f

on a.code=f.code left join new_schema.report_data4 g

on a.code=g.code

where

((a.pe>0 and a.pe<7 and a.pb>0 and a.pb<1 ) #低市盈率低市净率

)

and a.code in(

#股权质押率小于10

select d.code from

new_schema.stock_pledged d

where d.p_ratio <30)

SELECT distinct a.code as 代码,a.name as 名称,a.industry as 行业,a.area as 地域,a.pe as 静态市盈率,a.totalAssets as 总资产,

a.liquidAssets as 流动资产,a.fixedAssets as 固定资产,a.reservedPerShare,a.esp,a.bvps,a.pb as 市净率,a.timeToMarket as 上市时间,a.perundp

,b.roe as 净资产收益率, (b.roe+d.roe+e.roe+f.roe+g.roe)/5 as 近5年平均净资产收益率,,(b.roe+d.roe+e.roe+f.roe+g.roe)/5/a.pb as 近5年平均除以市净率, c.trade as 交易价格,c.per as 动态市盈率

FROM new_schema.stock_basics a left join new_schema.report_data0 b

on a.code=b.code left join new_schema.stock_price c

on a.code=c.code left join new_schema.report_data1 d

on a.code=d.code left join new_schema.report_data2 e

on a.code=e.code left join new_schema.report_data3 f

on a.code=f.code left join new_schema.report_data4 g

on a.code=g.code

where

(

(a.pe>0 and a.pb>0 and a.pb<0.8) #低市净率

)

and a.code in(

#股权质押率小于10

select d.code from

new_schema.stock_pledged d

where d.p_ratio <30)

SELECT distinct a.code as 代码,a.name as 名称,a.industry as 行业,a.area as 地域,a.pe as 静态市盈率,a.totalAssets as 总资产,

a.liquidAssets as 流动资产,a.fixedAssets as 固定资产,a.reservedPerShare,a.esp,a.bvps,a.pb as 市净率,a.timeToMarket as 上市时间,a.perundp

,b.roe as 净资产收益率, (b.roe+d.roe+e.roe+f.roe+g.roe)/5 as 近5年平均净资产收益率,(b.roe+d.roe+e.roe+f.roe+g.roe)/5/a.pb as 近5年平均除以市净率, c.trade as 交易价格,c.per as 动态市盈率

FROM new_schema.stock_basics a left join new_schema.report_data0 b

on a.code=b.code left join new_schema.stock_price c

on a.code=c.code left join new_schema.report_data1 d

on a.code=d.code left join new_schema.report_data2 e

on a.code=e.code left join new_schema.report_data3 f

on a.code=f.code left join new_schema.report_data4 g

on a.code=g.code

where

(

(a.pe>0 and a.pe<6 and b.roe>6 and (b.roe+d.roe+e.roe+f.roe+g.roe)/5>7) #较低市净率

) and a.timeToMarket<'20130101'

and a.code in(

#股权质押率小于10

select d.code from

new_schema.stock_pledged d

where d.p_ratio <30)

order by (b.roe+d.roe+e.roe+f.roe+g.roe)/5/a.pb

SELECT distinct a.code as 代码,a.name as 名称,a.industry as 行业,a.area as 地域,a.pe as 静态市盈率,a.totalAssets as 总资产,

a.liquidAssets as 流动资产,a.fixedAssets as 固定资产,a.reservedPerShare,a.esp,a.bvps,a.pb as 市净率,a.timeToMarket as 上市时间,a.perundp

,b.roe as 净资产收益率, (b.roe+d.roe+e.roe+f.roe+g.roe)/5 as 近5年平均净资产收益率,(b.roe+d.roe+e.roe+f.roe+g.roe)/5/a.pb as 近5年平均除以市净率, c.trade as 交易价格,c.per as 动态市盈率

FROM new_schema.stock_basics a left join new_schema.report_data0 b

on a.code=b.code left join new_schema.stock_price c

on a.code=c.code left join new_schema.report_data1 d

on a.code=d.code left join new_schema.report_data2 e

on a.code=e.code left join new_schema.report_data3 f

on a.code=f.code left join new_schema.report_data4 g

on a.code=g.code

where a.timeToMarket<'20130101' and a.name like '%茅%'

#and a.pb<2

and (b.roe+d.roe+e.roe+f.roe+g.roe)/5>15

and (b.roe+d.roe+e.roe+f.roe+g.roe)/5/a.pb>15 and a.fixedAssets/a.totalAssets<0.3

order by (b.roe+d.roe+e.roe+f.roe+g.roe)/5/a.pb desc

#下一步加入黑名单排除

#期望回报率＝增长率+股息率=ROE×留存率＋ROE×股息支付率÷PB

#过去9年达到R15的企业

SELECT distinct a.code as 代码,a.name as 名称,a.industry as 行业,a.area as 地域,a.pe as 静态市盈率,a.totalAssets as 总资产,

a.liquidAssets as 流动资产,a.fixedAssets as 固定资产,a.reservedPerShare,a.esp,a.bvps,a.timeToMarket as 上市时间,a.perundp

, (b.roe+ifnull(d.roe,b.roe)+ifnull(e.roe,b.roe)+ifnull(f.roe,b.roe)+ifnull(g.roe,b.roe)+ifnull(h.roe,b.roe)+ifnull(i.roe,b.roe)+ifnull(j.roe,b.roe)+ifnull(k.roe,b.roe))/9 as 近9年平均净资产收益率,

(b.roe+ifnull(d.roe,b.roe)+ifnull(e.roe,b.roe)+ifnull(f.roe,b.roe)+ifnull(g.roe,b.roe)+ifnull(h.roe,b.roe)+ifnull(i.roe,b.roe)+ifnull(j.roe,b.roe)+ifnull(k.roe,b.roe))/9/a.pb as 近9年平均除以市净率,

a.pb as 市净率,

((b.roe+ifnull(d.roe,b.roe)+ifnull(e.roe,b.roe)+ifnull(f.roe,b.roe)+ifnull(g.roe,b.roe)+ifnull(h.roe,b.roe)+ifnull(i.roe,b.roe)+ifnull(j.roe,b.roe)+ifnull(k.roe,b.roe))/9)*(

least(b.roe,(b.roe+ifnull(d.roe,b.roe)+ifnull(e.roe,b.roe)+ifnull(f.roe,b.roe)+ifnull(g.roe,b.roe)+ifnull(h.roe,b.roe)+ifnull(i.roe,b.roe)+ifnull(j.roe,b.roe)+ifnull(k.roe,b.roe))/9)) /100 *0.1

+ least(b.roe,(b.roe+ifnull(d.roe,b.roe)+ifnull(e.roe,b.roe)+ifnull(f.roe,b.roe)+ifnull(g.roe,b.roe)+ifnull(h.roe,b.roe)+ifnull(i.roe,b.roe)+ifnull(j.roe,b.roe)+ifnull(k.roe,b.roe))/9) /10 *0.9 as 合理PB,

a.pb/(((b.roe+ifnull(d.roe,b.roe)+ifnull(e.roe,b.roe)+ifnull(f.roe,b.roe)+ifnull(g.roe,b.roe)+ifnull(h.roe,b.roe)+ifnull(i.roe,b.roe)+ifnull(j.roe,b.roe)+ifnull(k.roe,b.roe))/9)*(

least(b.roe,(b.roe+ifnull(d.roe,b.roe)+ifnull(e.roe,b.roe)+ifnull(f.roe,b.roe)+ifnull(g.roe,b.roe)+ifnull(h.roe,b.roe)+ifnull(i.roe,b.roe)+ifnull(j.roe,b.roe)+ifnull(k.roe,b.roe))/9)) /100 *0.1

+ least(b.roe,(b.roe+ifnull(d.roe,b.roe)+ifnull(e.roe,b.roe)+ifnull(f.roe,b.roe)+ifnull(g.roe,b.roe)+ifnull(h.roe,b.roe)+ifnull(i.roe,b.roe)+ifnull(j.roe,b.roe)+ifnull(k.roe,b.roe))/9) /10 *0.9) as 市净率合理PB比,

c.trade as 交易价格,c.per as 动态市盈率

,b.roe as 净资产收益率1年 ,d.roe as 净资产收益率2年,e.roe as 净资产收益率3年,f.roe as 净资产收益率4年,g.roe as 净资产收益率5年,

h.roe as 净资产收益率6年,i.roe as 净资产收益率7年,j.roe as 净资产收益率8年,k.roe as 净资产收益率9年

FROM new_schema.stock_basics a left join new_schema.report_data0 b

on a.code=b.code left join new_schema.stock_price c

on a.code=c.code left join new_schema.report_data1 d

on a.code=d.code left join new_schema.report_data2 e

on a.code=e.code left join new_schema.report_data3 f

on a.code=f.code left join new_schema.report_data4 g

on a.code=g.code left join new_schema.report_data5 h

on a.code=h.code left join new_schema.report_data6 i

on a.code=i.code left join new_schema.report_data7 j

on a.code=j.code left join new_schema.report_data8 k

on a.code=k.code

where a.timeToMarket<'20080101' and (b.roe+ifnull(d.roe,b.roe)+ifnull(e.roe,b.roe)+ifnull(f.roe,b.roe)+ifnull(g.roe,b.roe)+ifnull(h.roe,b.roe)+ifnull(i.roe,b.roe)+ifnull(j.roe,b.roe)+ifnull(k.roe,b.roe))/9>15

and b.roe>15 and a.fixedAssets/a.totalAssets<0.3

order by (b.roe+ifnull(d.roe,b.roe)+ifnull(e.roe,b.roe)+ifnull(f.roe,b.roe)+ifnull(g.roe,b.roe)+ifnull(h.roe,b.roe)+ifnull(i.roe,b.roe)+ifnull(j.roe,b.roe)+ifnull(k.roe,b.roe))/9/a.pb desc

SELECT distinct a.code as 代码,a.name as 名称,a.industry as 行业,a.area as 地域,a.pe as 静态市盈率,a.totalAssets as 总资产,

a.liquidAssets as 流动资产,a.fixedAssets as 固定资产,a.reservedPerShare,a.esp,a.bvps,a.pb as 市净率,a.timeToMarket as 上市时间,a.perundp

,b.roe as 净资产收益率, c.trade as 交易价格,c.per as 动态市盈率,b.roe,d.roe,e.roe,f.roe,g.roe,g.roe,h.roe,i.roe,j.roe,k.roe

FROM new_schema.stock_basics a left join new_schema.report_data0 b

on a.code=b.code left join new_schema.stock_price c

on a.code=c.code left join new_schema.report_data1 d

on a.code=d.code left join new_schema.report_data2 e

on a.code=e.code left join new_schema.report_data3 f

on a.code=f.code left join new_schema.report_data4 g

on a.code=g.code left join new_schema.report_data5 h

on a.code=h.code left join new_schema.report_data6 i

on a.code=i.code left join new_schema.report_data7 j

on a.code=j.code left join new_schema.report_data8 k

on a.code=k.code

where a.timeToMarket<'20080101' and a.name like '%茅%';


