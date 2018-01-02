import urllib.request

import re

import datetime

import pandas as pd

import os

import time

##def downback(a,b,c):

##    ''''

##    a:已经下载的数据块

##    b:数据块的大小

##    c:远程文件的大小

##   '''

##    per = 100.0 * a * b / c

##    if per > 100 :

##        per = 100

##    print('%.2f%%' % per)

stock_CodeUrl = 'http://quote.eastmoney.com/stocklist.html'

#获取股票代码列表

def urlTolist(url):

    allCodeList = []

    html = urllib.request.urlopen(url).read()

    html = html.decode('gbk')

    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'

    pat = re.compile(s)

    code = pat.findall(html)

    for item in code:

        if item[0]=='6' or item[0]=='3' or item[0]=='0':

            allCodeList.append(item)

    return allCodeList

def get_page(url):  #获取页面数据
    req=urllib.request.Request(url,headers={
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    })
    opener=urllib.request.urlopen(req)
    page=opener.read()
    return page

def checkM2andM5(m2, m5, code):
    for i in range(m2.size):
        if m2[i] != 0 and m5[i] != 0:
            if m2[i] == m5[i]:
                print("股票:%s" %code)
                return 1
    return 0

def main():
    print("pd version:%s" %pd.__version__)
    start = datetime.datetime.now() - datetime.timedelta(days=30)
    end = datetime.datetime.now()
    strStart = start.strftime('%Y%m%d')
    strEnd = end.strftime('%Y%m%d')
    
    allCodelist = urlTolist(stock_CodeUrl)

    #获取工作目录
	#os.getcwd()
    mcodes = []
#    names = []
#    count = 0
    for code in allCodelist:

        print('正在获取%s股票数据...'%code)
        
        if code[0]=='6':

            url = 'http://quotes.money.163.com/service/chddata.html?code=0' + code + \
                '&start=' + strStart + '&end=' + strEnd + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        else:
            url = 'http://quotes.money.163.com/service/chddata.html?code=1' + code + \
                '&start=' + strStart + '&end=' + strEnd + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        urllib.request.urlretrieve(url,'./ll_stock_data/' + code + '.csv')
        time.sleep(1)
        #把数据放入工作目录当中，并读取
#        try:
        stock_data = pd.read_csv('./ll_stock_data/' + code + '.csv', parse_dates=[1],encoding='gb2312')
#        except:
#            continue
        
        stock_data.head()
        #把数据从远到近排列
        stock_data.sort_values('日期', inplace=True)
        stock_data.head()
        m2 = pd.rolling_mean(stock_data['收盘价'], 2)
        m5 = pd.rolling_mean(stock_data['收盘价'], 5)
        ret = checkM2andM5(m2, m5, code)

        if ret == 1:
            mcodes.append(code)
#            names.append(stock_data[1]['名称'])
    
    save = pd.DataFrame({'股票:': mcodes})
    save.to_csv('./result.csv', index=False)


if __name__ == '__main__':
	main()

