import datetime
import pandas as pd
import os
import time

#发送邮件
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  

def checkM2andM5(m2, m5, code):
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

def main():
    print("pd version:%s" %pd.__version__)

    rootdir = './ll_stock_data/'
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    mcodes = []

    htmlp = ""

    for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i])
        if os.path.isfile(path):
            print("股票:%s" %list[i])
            stock_data = pd.read_csv(path, parse_dates=[1],encoding='gbk')
            
            stock_data.head()

            #把数据从远到近排列
            stock_data.sort_values('日期', inplace=True)
            stock_data.head()
            m2 = pd.rolling_mean(stock_data['收盘价'], 2)
            m5 = pd.rolling_mean(stock_data['收盘价'], 5)
            m10 = pd.rolling_mean(stock_data['收盘价'], 10)
            m20 = pd.rolling_mean(stock_data['收盘价'], 20)
            m30 = pd.rolling_mean(stock_data['收盘价'], 30)
            ret = checkM2andM5(m5, m10, list[i])

            if ret == 1:
                mcodes.append(stock_data['名称'][1])
                htmlp += "<p>" + stock_data['名称'][1] + "</p>" 
 
    save = pd.DataFrame({'股票:': mcodes})
    save.to_csv('./result.csv', index=False) 

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

if __name__ == '__main__':
	main()