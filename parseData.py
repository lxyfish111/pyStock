import datetime
import pandas as pd
import os
import time

#unicode error
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

#发送邮件
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  

def checkmean(m2, m5, code):
    for i in range(m2.size):
        if m2[i] != 0 and m5[i] != 0:

            slopM2 = 0
            if m2[i] == m5[i]:
                if i != 0:
                    slopM2 = m2[i] - m2[i - 1]
                else:
                    slopM2 = m2[i + 1] - m2[i]
                
                if slopM2 > 0:
                    return True
                
    return False

#Calc EMA
def calcEMA(closeValueList, n):
    ema = []

    for i in range(0, len(closeValueList)):
        if i == 0:
            ema.append(closeValueList[i])
        elif i > 0:
            ema.append((2 * closeValueList[i] + (n - 1) * ema[i - 1]) / (n + 1))
        
    return ema

#Calc DIFF
def calcDIFF(closeValueList, shortD = 12, longD = 26):
    shortEMA = calcEMA(closeValueList, shortD)
    longEMA = calcEMA(closeValueList, longD)
    diff = pd.Series(shortEMA) - pd.Series(longEMA)
    return diff

#calc DEA
def calcDEA(diff, m = 9):
    dea = []

    for i in range(0, len(diff)):
        if i == 0:
            dea.append(diff[i])
        elif i > 0:
            dea.append((2 * diff[i] + (m - 1) * dea[i - 1]) / (m + 1))

    return dea

#Calc MACD
def calcMACD(diff, dea):
    macd = 2 * (diff - dea)
    return macd   

#Get buy point
<<<<<<< HEAD
def getBuyPt(diff, macd, m5, m10, m15):
    ret = False
    for i in range(1, len(diff)):
        if diff[i] == macd[i] and diff[i - 1] < macd[i - 1]:
            ret = ret or True
            break
    
    nlen = len(m5)
    for n in range(0, len(m5)):
        if m5[n] == m10[n] == m15[n] and m5[n - 1] < m10[n- 1] < m15[n-1]:
            if m5[nlen - 1] > m10[nlen - 1] > m15[nlen - 1]:
                ret = ret or True
                break
    
    return ret
=======
def getBuyPt(diff, dea, macd, m5, m10, m20):
 
    indexMax = len(diff) -1
    for i in range(1, len(diff)):
        if i == 0:
            continue
        if (diff[i] > 0) and (dea[i] > 0) and (diff[i] == dea[i]):
            k = diff[indexMax] - diff[i]
            if k < 0:
                return False
        
        if macd[i - 1] > 0 and macd[i] <= 0:
            return False

    return True


#m5 m10
def checkRule(mS, mL):
    maxlen = len(mS)
    for i in range(0, maxlen):
       if i == 0:
          continue

       if mS[i] == mL[i] and (mS[i] - mS[i - 1]) > 0 and (mS[maxlen - 1] - mS[i]) > 0:
          return True

    return False
>>>>>>> 910eb93671053be3014d3c8872fb76bccadd7e47

#Get the Cross Stars
def getCrossStars(openPriceList, maxPriceList, minPriceList, closePriceList, exponential):
    for i in range(0, len(closePriceList)):
        if i == 0:
            continue

        rs = closePriceList[i] / closePriceList[i - 1] - 1
        ri = exponential[i] / exponential[i - 1] - 1
        re = rs - ri
        oprice = re * openPriceList[i]
        maxprice = re * maxPriceList[i]
        minprice = re * minPriceList[i]
        cprice = re * closePriceList[i]

        h = abs(cprice - oprice)
        upshadowlen = maxprice - max(oprice, cprice)
        downshadowlen = min(oprice, cprice) - minprice
        
        if h < 0.001 * oprice and upshadowlen > (3 * h) and downshadowlen > (3 * h):
            return True
            
    return False

#Trend line
def getTrendLine(openPrice, closePrice):
    trend = []
    size = len(openPrice)

    if size == 0:
        trend.append(0)
        trend.append(0)
        return trend
   
    mean_openPrice = sum(openPrice) / size
    maxClosePrice = max(closePrice)
    minClosePrice = min(closePrice)

    rangeVal = maxClosePrice - minClosePrice
    upper = mean_openPrice + rangeVal
    lower = mean_openPrice + rangeVal

    trend.append(upper)
    trend.append(lower)

    return trend

#Check the trend line
def checkTrendline(openPriceList, closePriceList):
    trend = getTrendLine(openPriceList, closePriceList)
    if trend[0] == 0 and trend[1] == 0:
        return False

    size = len(openPriceList)
    print (trend[0])
    print (trend[1])

    if closePriceList[size - 1] > trend[0] > closePriceList[size - 2] or closePriceList[size - 1] > trend[1]  > closePriceList[size - 2]:
        return True

    return False

def checkVolume(RaF, Volume):
    up = 0.0
    down = 0.0
    for i in range(0, len(RaF)):
        if RaF[i] == 'None':
            continue

        if float(RaF[i]) > 0:
            up = up + Volume[i]
        else:
            down = down + Volume[i]

    tmp = 8 * (up + down) / 10

    if up > tmp:
        return True

    return False

<<<<<<< HEAD
=======
def checkMACD(diff, macd):
    for i in range(1, len(macd)):
        if diff[i] == macd[i]:
            break

    if i == len(macd):
        return False

    if diff[i] < 0 or macd[i] < 0:
        return False

    if diff[i - 1] < macd[i - 1]:
        return True
    else:
        return False




>>>>>>> 910eb93671053be3014d3c8872fb76bccadd7e47
def main():
    print("pd version:%s" %pd.__version__)

    rootdir = './ll_stock_data/'
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    mcodes = []
    mnames = []

    #htmlp = ""

    shExpoPath = './stock_exponent/000001.csv'
    shexpo = pd.read_csv(shExpoPath, parse_dates = True, encoding = 'gbk')

    szExpoPath = './stock_exponent/399001.csv'
    szexpo = pd.read_csv(szExpoPath, parse_dates = True, encoding = 'gbk')

    for i in range(0, len(list)):
        path = os.path.join(rootdir,list[i])
        if os.path.isfile(path):
            
            #if list[i] != '600181.csv':
            #    continue
            #print("股票:%s" %list[i])

            stock_data = pd.read_csv(path, parse_dates = True,encoding = 'gbk')
            if stock_data.empty:  #可能停牌的股票
                print("股票:%s is empty" %list[i])
                continue

            if 'ST' in stock_data['名称'][0]:
                print('股票:%s is ST股票' %stock_data['名称'][0])
                continue


            stock_data.head()

            #把数据从远到近排列
            stock_data.sort_values('日期', inplace=True)
            stock_data.head()

<<<<<<< HEAD
            m5 = stock_data['收盘价'].rolling(window = 5, center = False).mean()
            m10 = stock_data['收盘价'].rolling(window = 10, center = False).mean()
            m15 = stock_data['收盘价'].rolling(window = 20, center = False).mean()
=======
            #m2 = stock_data['收盘价'].rolling(window = 2, center = False).mean()
            m5 = stock_data['收盘价'].rolling(window = 5, center = False).mean()
            m10 = stock_data['收盘价'].rolling(window = 10, center = False).mean()
            m20 = stock_data['收盘价'].rolling(window = 20, center = False).mean()
            #m30 = stock_data['收盘价'].rolling(window = 30, center = False).mean()
>>>>>>> 910eb93671053be3014d3c8872fb76bccadd7e47

            diff = calcDIFF(stock_data['收盘价'])
            dea = calcDEA(diff)
            macd = calcMACD(diff, dea)

<<<<<<< HEAD
            ret = getBuyPt(diff, macd, m5, m10, m15)
            #ret = checkTrendline(stock_data['开盘价'], stock_data['收盘价'])

            #ret2 = checkVolume(stock_data['涨跌幅'], stock_data['成交量'])
=======
            ret3 = getBuyPt(diff, dea, macd, m5, m10, m20)
            #ret = checkRule(m5, m10)
            #ret = checkTrendline(stock_data['开盘价'], stock_data['收盘价'])

            #ret2 = checkVolume(stock_data['涨跌幅'], stock_data['成交量'])
            ret2 = checkMACD(diff, macd)
>>>>>>> 910eb93671053be3014d3c8872fb76bccadd7e47

            strCode = stock_data['股票代码'][0]

            if strCode[1] == '6':
                ret1 = getCrossStars(stock_data['开盘价'], stock_data['最高价'], stock_data['最低价'], stock_data['收盘价'], shexpo['收盘价'])
            else:
                ret1 = getCrossStars(stock_data['开盘价'], stock_data['最高价'], stock_data['最低价'], stock_data['收盘价'], szexpo['收盘价'])

            ret = ret1 and ret2 and ret3

            if ret == True:
                mnames.append(stock_data['名称'][0])
                mcodes.append(stock_data['股票代码'][0])
                #htmlp += "<p>" + stock_data['名称'][1] + "</p>" 
            
    save = pd.DataFrame({'股票:': mnames, '股票代码:': mcodes})
    save.to_csv('./result.csv', index=False) 

'''
    #发送邮件
    sender = 'lxy_fish_111@163.com'  
    receiver = 'lxy_fish_111@163.com'  
    subject = 'Mult Mean'  
    smtpserver = 'smtp.163.com'  
    username = 'lxy_fish_111'  
    password = '111!!!qaz'  

    htmlFont = """\
    <html> 
      <head></head> 
         <body> 
           <p>
    """

    htmlBack = """\
           </p> 
         </body> 
    </html> 
    """
    html = htmlFont + htmlp + htmlBack

    msg = MIMEText(html, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender

  
    smtp = smtplib.SMTP()  
    smtp.connect('smtp.163.com')  
    smtp.login(username, password)  
    smtp.sendmail(sender, receiver, msg.as_string())  
    smtp.quit()        
'''
if __name__ == '__main__':
	main()
