import datetime
import pandas as pd
import os
import time
import tushare as ts

#unicode error
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

#发送邮件
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  

def main():
    print("pd version:%s" %pd.__version__)
    print("tushare version:%s" %ts.__version__)
    '''
    data = ts.get_today_all()
    data['Profit yield'] = None

    for i in range(0, len(data.index)):
        if data.at[i, 'per'] == 0:  #可能停牌的股票
            continue

        #if 'ST' in data.at[i, 'name']:
        #    continue

        data.at[i, 'Profit yield'] = 1 / data.at[i, 'per']

    data.to_csv("./get_today_all.csv")
    '''
    databasic = ts.get_stock_basics()
    #databasic.sort_values(by = 'pb').to_csv("./get_today_all.csv")

    dta8_1 = ts.get_report_data(2018, 1)
    dta7_4 = ts.get_report_data(2017, 4)
    dta7_3 = ts.get_report_data(2017, 3)
    dta7_2 = ts.get_report_data(2017, 2)
    dta7_1 = ts.get_report_data(2017, 1)
    dta6_4 = ts.get_report_data(2016, 4)
    dta6_3 = ts.get_report_data(2016, 3)
    dta6_2 = ts.get_report_data(2016, 2)
    dta6_1 = ts.get_report_data(2016, 1)

    dtaROE = (dta8_1['roe'] + dta7_4['roe'] + dta7_3['roe'] + dta7_2['roe'] + dta7_1['roe']
               + dta6_4['roe'] + dta6_3['roe'] + dta6_2['roe'] + dta6_1['roe']) / 9

    print(dtaROE)

    



    
        

    

            

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
