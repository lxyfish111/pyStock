import datetime
import pandas as pd
import os
import time

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
                    return 1
                
    return 0

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
def getBuyPt(diff, dea, macd, m5, m10, m20):
 
    indexMax = len(diff) -1
    for i in range(0, len(diff)):
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
 
#Trend line
def getTrendLine(openPrice, closePrice):
   trend = []
   size = len(openPrice)
   
   mean_openPrice = sum(openPrice) / size
   maxClosePrice = max(closePrice)
   minClosePrice = min(closePrice)

   rangeVal = maxClosePrice - minClosePrice
   upper = mean_openPrice + rangeVal
   lower = mean_openPrice + rangeVal

   trend.append(upper)
   trend.append(lower)

   return


def main():
    print("pd version:%s" %pd.__version__)

    rootdir = './ll_stock_data/'
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    mcodes = []

    htmlp = ""

    for i in range(0, len(list)):
        path = os.path.join(rootdir,list[i])
        if os.path.isfile(path):
            print("股票:%s" %list[i])
            stock_data = pd.read_csv(path, parse_dates=[1],encoding='gbk')
            
            stock_data.head()

            #把数据从远到近排列
            stock_data.sort_values('日期', inplace=True)
            stock_data.head()

            #m2 = stock_data['收盘价'].rolling(window = 2, center = False).mean()
            m5 = stock_data['收盘价'].rolling(window = 5, center = False).mean()
            m10 = stock_data['收盘价'].rolling(window = 10, center = False).mean()
            m20 = stock_data['收盘价'].rolling(window = 20, center = False).mean()
            m30 = stock_data['收盘价'].rolling(window = 30, center = False).mean()

            diff = calcDIFF(stock_data['收盘价'])
            dea = calcDEA(diff)
            macd = calcMACD(diff, dea)

            ret = getBuyPt(diff, dea, macd, m5, m10, m20)
            #ret = checkRule(m5, m10)
            
            if ret == True:
                mcodes.append(stock_data['名称'][1])
                #htmlp += "<p>" + stock_data['名称'][1] + "</p>" 
            

            
    save = pd.DataFrame({'股票:': mcodes})
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
