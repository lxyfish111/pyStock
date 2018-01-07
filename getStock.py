import urllib.request
import re
import datetime
import os
import time

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

def makedir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
 
        print(path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
        return False

def main():
    makedir("./ll_stock_data/") 

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

if __name__ == '__main__':
	main()
