# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 14:27:43 2019

@author: Administrator
"""

import os;
import xlsxwriter;
import shutil
import datetime;
import pymysql
#import numpy as np
from dateutil.relativedelta import relativedelta
import smtplib,ssl
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from dateutil.relativedelta import relativedelta

nowt = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S');
f = open('D:\\TahoeLi_Auto\\AutoreportTaholi\\api\\log.txt','a+');
init = """
##########################################
%s:GET CRE sales Start..........
"""%str(nowt)
f.write(init)
f.close();

ip = "172.23.110.16";
#ip = "223.71.105.241";
currdate = datetime.datetime.now().strftime('%Y-%m-%d');
y = datetime.datetime.now()+relativedelta(days=-1)
detester = y.strftime("%Y-%m-%d");
f = datetime.datetime.strptime(detester,'%Y-%m-%d')
fristday= f.strftime('%Y-%m-01');

query = "SELECT b.cont2,DATE_FORMAT(a.txdate,'%Y-%m-%d'),a.amtsold,a.transtrades FROM daliyamt as a,users as b WHERE a.contract = b.contract and a.txdate between '"+fristday+"' and  '"+detester+"' and b.sdate <='"+detester+"' and b.cont2 <> '-' order by a.txdate";
db = pymysql.connect(ip,"shaclo","1984Konami","azuz",charset='utf8' );
cursor = db.cursor();
cursor.execute(query);
data = cursor.fetchall();



def getfilename(detester,fristday,name="SalesInputBatch"):
    #filepath = "ExcelReport/";
    filepath = "";
    path = os.getcwd()
    #filename = currdate+name+".xlsx";
    currdate = datetime.datetime.now().strftime('%Y%m%d_%H%M%S');
    filename = name+fristday+'~'+detester+"["+currdate+"].xlsx";
    return filepath+filename,filename,path;

def exportexcel(detester,fristday,data):
    fullname,filename,path = getfilename(detester,fristday);
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(fullname)     #创建工作簿
    worksheet = workbook.add_worksheet("SalesInputBatch")
    worksheet.write(0,0,'收款方')
    worksheet.write(0,1,'合同')
    worksheet.write(0,2,'商品')
    worksheet.write(0,3,'起始日期')
    worksheet.write(0,4,'截止日期')
    worksheet.write(0,5,'数量')
    worksheet.write(0,6,'销售额')
    worksheet.write(0,7,'付款方式')
    worksheet.write(0,8,'付款金额')
    worksheet.write(0,9,'银行')
    worksheet.write(0,10,'说明')
    n = 1;
    for i in data:
        worksheet.write(n,1,i[0]) #合同
        worksheet.write(n,3,i[1]) #起始日期
        worksheet.write(n,4,i[1]) #截止日期
        worksheet.write(n,5,i[3]) #数量，交易笔数
        worksheet.write(n,6,float(i[2])) #销售额
        worksheet.write(n,7,'01') #付款方式
        worksheet.write(n,8,float(i[2])) #付款金额
        n = n+1;
    workbook.close()
    return filename,path;
    
#发送邮件
def activesendmail(emailfrom,emailto,port,smtp_server,password,ir):
    print(emailto)
    nowt = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S');
    f = open('D:\\TahoeLi_Auto\\AutoreportTaholi\\api\\log.txt','a+');
    init = "%s:Send mail %s "%(str(nowt),str(emailto))
    f.write(init)
    f.close();
    context = ssl.create_default_context()
    fileToSend = filename

    
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = ",".join(emailto)
    ff = filename.split('S')[0];
    msg["Subject"] = "大兴泰禾里CRE销售日导入模板"+ff;
    message = """
    Dear All,
        附件中名为 %s 的CRE销售导入数据，由于CRE无法获取xlsx文本，因此下载附件后，请在Excel中另存为 97-2003格式（xls)后上传。
        
        如有任何意见，请及时联系我。
        这是一封自动发送的邮件，请勿直接回复
    
    Regards,
    刘烜超
    """%(filename)
    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    
    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    
    maintype, subtype = ctype.split("/", 1)
    
    if maintype == "text":
        #print ('text')
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        #print ('image')
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        #print ('audio')
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        #print ('else filetype.')
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)
    try:
        server = smtplib.SMTP_SSL(smtp_server, port, context=context)
        server.login(emailfrom, password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
        nowt = datetime.datetime.now().strftime('%H:%M:%S');
        f = open('D:\\TahoeLi_Auto\\AutoreportTaholi\\api\\log.txt','a+');
        init = ",%s Send mail sccuess.\n "%(str(nowt))
        f.write(init)
        f.close();
        
        return True;
    except:
        nowt = datetime.datetime.now().strftime('%H:%M:%S');
        f = open('D:\\TahoeLi_Auto\\AutoreportTaholi\\api\\log.txt','a+');
        init = ",%s Send failed. \n"%(str(nowt))
        f.write(init)
        f.close();
        ir = ir+1;
        if ir<=5:
            activesendmail(emailfrom,emailto,port,smtp_server,password,ir)
        else:
            pass
        return False;    

def sendmail(filename,path):
    port = 465  # For SSL
    smtp_server = "smtp.139.com"
    emailfrom = "13911870014@139.com"  # Enter your address
    password = "1984Konami010884";
    query =  "select email from maillist where priority between 1 and 50 order by priority DESC";
    db = pymysql.connect(ip,"shaclo","1984Konami","azuz",charset='utf8' );
    cursor = db.cursor();
    cursor.execute(query);
    data = cursor.fetchall();
    #emaillist = [];
    for i in data:
        ir=0;
        emailto = list([i[0]])
        activesendmail(emailfrom,emailto,port,smtp_server,password,ir)
    #emailto = list(emaillist);
    #print("Send Mail to：")
   # emailto = ["liuxuanchao@tahoecn.com","shaclo@139.com"]  # Enter receiver address
    #activesendmail(emailfrom,emailto,port,smtp_server,password)
    return True
    

filename,path = exportexcel(detester,fristday,data)
t = sendmail(filename,path);
if t:
    dpath = "D:\\TahoeLi_Auto\\AutoreportTaholi\\api\\dailysalesmodel";
    #发送完邮件后移动文件到ExcelReport
    shutil.move(path+"\\"+filename,dpath)
    f = open('D:\\TahoeLi_Auto\\AutoreportTaholi\\api\\log.txt','a+');
    nowt = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S');
    msg = str("GET %s"%(path))
    init = "%s:%s\n"%(str(nowt),msg)
    f.write(init)
    nowt = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S');
    msg = str("%s:TO %s\n"%(str(nowt),dpath))
    f.write(msg)
    nowt = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S');
    init = "%s:.........Complate.........."%str(nowt)
    f.write(init)
    f.close();
else:
    print("Send Mail Error!")