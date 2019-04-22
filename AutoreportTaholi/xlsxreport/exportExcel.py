# -*- coding: utf-8 -*-
"""
Spyder Editor
生成报表
每日汇总报表，保存在ExcelReport目录
2019-01-08
LiuXuanchao

This is a temporary script file.
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


ip = "172.23.110.16";
#ip = "223.71.105.241";

def getweather(detester):
    db = pymysql.connect(ip,"shaclo","1984Konami","azuz",charset='utf8' );
    cursor = db.cursor();
    cursor.execute("SELECT * from weather where txdate = '"+detester+"'");
    data = cursor.fetchone();
    db.close();
    result = "%s %s℃ %s风 风力%s 湿度%s%% "%(str(data[1]),str(data[2]),str(data[3]),str(data[4]),str(data[5]))
    return result;
def connectmysql(ip):
    db = pymysql.connect(ip,"shaclo","1984Konami","azuz",charset='utf8' );
    cursor = db.cursor();
    cursor.execute("SELECT * from users limit 0,4");
    data = cursor.fetchall();
    return data;

def getcategoryname():
    db = pymysql.connect(ip,"shaclo","1984Konami","azuz",charset='utf8' );
    cursor = db.cursor();
    cursor.execute("SELECT distinct category FROM `users` WHERE 1");
    data = cursor.fetchall();
    return data;

def getfilename(detester = '',name="DailySalesSummaryReport"):
    #filepath = "ExcelReport/";
    filepath = "";
    path = os.getcwd()
    currdate = datetime.datetime.now().strftime('%Y%m%d_%H%M%S');
    #filename = currdate+name+".xlsx";
    filename = detester+name+currdate+".xlsx";
    return filepath+filename,filename,path;


def switch_weekday_item(item):
    switcher = {
        "1": "周一",
        "2": "周二",
        "3": "周三",
        "4": "周四",
        "5": "周五",
        "6": "周六",
        "0": "周日",
    }
    return switcher.get(item,"未知")

def tusumquery(detester,dtype='',info=''):
    query =  "SELECT sum(amtsold),sum(passflow),sum(transtrades) from daliyamt WHERE `txdate`= '"+detester+"'";
    switcher = {
        "contract": " and contract = '"+info+"'",
        "category": " and category = '"+info+"'",
    }
    add = switcher.get(dtype," ")
    query = query+add;
    
    db = pymysql.connect(ip,"shaclo","1984Konami","azuz",charset='utf8' );
    cursor = db.cursor();
    cursor.execute(query);
    data = cursor.fetchone();
    return(data[0],data[1],data[2])

def tusumquery2(detester,dtype='',info=''):
    f = datetime.datetime.strptime(detester,'%Y-%m-%d')
    fristday= f.strftime('%Y-%m-01');
    query =  "SELECT sum(amtsold),sum(passflow),sum(transtrades) FROM `daliyamt` WHERE `txdate` between '"+fristday+"' and '"+detester+"'";
    db = pymysql.connect(ip,"shaclo","1984Konami","azuz",charset='utf8' );
    cursor = db.cursor();
    cursor.execute(query);
    data = cursor.fetchone();
    return(data[0],data[1],data[2])
    #return(sumsales,sumpf)

def sumyearsales(d1,d2,dtype='',info=''):
    query =  "SELECT sum(amtsold),sum(passflow),sum(transtrades) FROM `daliyamt` WHERE `txdate` between '"+d1+"' and '"+d2+"'";
    db = pymysql.connect(ip,"shaclo","1984Konami","azuz",charset='utf8' );
    cursor = db.cursor();
    cursor.execute(query);
    data = cursor.fetchone();
    return(data[0],data[1],data[2])

def tusumcategoryquery(detester,info=''):
    query =  "SELECT sum(a.amtsold),sum(a.passflow),sum(a.transtrades) from daliyamt as a ,users as b WHERE a.contract = b.contract and a.txdate= '"+detester+"'";
    add = " and category = '"+info+"'";
    query = query+add;
    db = pymysql.connect(ip,"shaclo","1984Konami","azuz",charset='utf8' );
    cursor = db.cursor();
    cursor.execute(query);
    data = cursor.fetchone();
    return(data[0],data[1],data[2])

def tusumcategoryquery2(detester,info=''):
    f = datetime.datetime.strptime(detester,'%Y-%m-%d')
    fristday= f.strftime('%Y-%m-01');
    query =  "SELECT sum(a.amtsold),sum(a.passflow),sum(a.transtrades) from daliyamt as a ,users as b WHERE a.contract = b.contract and txdate between '"+fristday+"' and '"+detester+"'";
    add = " and category = '"+info+"'";
    query = query+add;
    
    db = pymysql.connect(ip,"shaclo","1984Konami","azuz",charset='utf8' );
    cursor = db.cursor();
    cursor.execute(query);
    data = cursor.fetchone();
    return(data[0],data[1],data[2])

def getyearbudget(detester):
    fy = datetime.datetime.strptime(detester,'%Y-%m-%d')
    curryear= fy.strftime('%Y');
    querybugget = "SELECT * FROM `yearbudget` where year = '"+curryear+"'";
    
    db = pymysql.connect(ip,"shaclo","1984Konami","azuz",charset='utf8' );
    cursor = db.cursor();
    cursor.execute(querybugget);
    ybudget = cursor.fetchone();
    return(ybudget[1]);
    
def saleschampioneachcategory(detester,category):
    query =  "SELECT b.brand,a.amtsold,a.passflow,a.transtrades from daliyamt as a ,users as b WHERE a.contract = b.contract and a.txdate= '"+detester+"'";
    add = " and category = '"+category+"' order by a.amtsold desc limit 1";
    query = query+add;
    db = pymysql.connect(ip,"shaclo","1984Konami","azuz",charset='utf8' );
    cursor = db.cursor();
    cursor.execute(query);
    data = cursor.fetchone();
    return(data[0],data[1],data[2],data[3])

def getimportantamtsold(detester):
    query =  "SELECT c.brand,b.amtsold FROM importantbrand as a,daliyamt as b,users as c where b.txdate = '"+detester+"' and a.contract = b.contract and a.contract = c.contract order by c.brand";
    db = pymysql.connect(ip,"shaclo","1984Konami","azuz",charset='utf8' );
    cursor = db.cursor();
    cursor.execute(query);
    data = cursor.fetchall();
    return data;

def top20brand(detester):
    query =  "SELECT c.brand,c.category,b.amtsold FROM daliyamt as b,users as c where b.txdate = '"+detester+"' and c.contract = b.contract order by b.amtsold desc limit 0,20";
    db = pymysql.connect(ip,"shaclo","1984Konami","azuz",charset='utf8' );
    cursor = db.cursor();
    cursor.execute(query);
    data = cursor.fetchall();
    return data;

def exportexcel(detester,db):
    fullname,filename,path = getfilename(detester);
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(fullname)     #创建工作簿
    worksheet = workbook.add_worksheet("日销售汇总报表")            #创建工作表
    
    # Add a bold format to use to highlight cells.
    #在工作表中创建一个新的格式对象来格式化单元格，实现加粗   
    format_title = workbook.add_format({
            'border':   1,
            'align':    'center',#水平居中
            'valign':   'vcenter',#垂直居中
            'font_size':20,
            'bold':1,
    });
    format1 = workbook.add_format({
            'num_format': '#,##0.00',
            'border':   1,
            'align':    'center',#水平居中
            'valign':   'vcenter',#垂直居中
    });
    format1_1 = workbook.add_format({
            'num_format': '#,##0.00',
            'border':   1,
            'align':    'center',#水平居中
            'valign':   'vcenter',#垂直居中
            'font_color':'#DF2A2A',#红色
    });
    format2 = workbook.add_format({
            'num_format': '#,##0',
            'border':   1,
            'align':    'center',#水平居中
            'valign':   'vcenter',#垂直居中
    });
    format2_1 = workbook.add_format({
            'num_format': '#,##0',
            'border':   1,
            'align':    'center',#水平居中
            'valign':   'vcenter',#垂直居中
            'font_color':'#DF2A2A',#红色
    });
    format3 = workbook.add_format({
            'num_format': '###0.00%',
            'border':   1,
            'align':    'center',#水平居中
            'valign':   'vcenter',#垂直居中
    });
    format3_1 = workbook.add_format({
            'num_format': '###0.00%',
            'border':   1,
            'align':    'center',#水平居中
            'valign':   'vcenter',#垂直居中
            'font_color':'#DF2A2A',#红色
    });
    format3_3 = workbook.add_format({
            'num_format': '###0.00%',
            'border':   1,
            'align':    'right',#水平居中
            'valign':   'vcenter',#垂直居中
    });
    format3_4 = workbook.add_format({
            'num_format': '###0.00%',
            'border':   1,
            'align':    'right',#水平居中
            'valign':   'vcenter',#垂直居中
            'font_color':'#DF2A2A',#红色
    });
    format4 = workbook.add_format({
            'num_format': '#,##0.00',
            'border':   1,
            'align':    'right',#水平居中
            'valign':   'vcenter',#垂直居中
    });
    merge_format1 = workbook.add_format({
        'bold':     True,
        'border':   1,
        'align':    'center',#水平居中
        'valign':   'vcenter',#垂直居中
        'fg_color': '#FFCC99',#颜色填充
    })
    merge_format2 = workbook.add_format({
        'num_format': '#,##0',
        'bold':     True,
        'border':   1,
        'align':    'center',#水平居中
        'valign':   'vcenter',#垂直居中
        'fg_color': '#FFFFCC',#颜色填充
    })
    merge_format2_1 = workbook.add_format({
        'bold':     False,
        'border':   1,
        'align':    'center',#水平居中
        'valign':   'vcenter',#垂直居中
        'font_size':10,
        'fg_color': '#FFCC99',#颜色填充
    })
    merge_format2_2 = workbook.add_format({
        'num_format': '###0.00%',
        'bold':     True,
        'border':   1,
        'align':    'center',#水平居中
        'valign':   'vcenter',#垂直居中
        'fg_color': '#FFFFCC',#颜色填充
    })
    merge_format3 = workbook.add_format({
        'bold':     False,
        'border':   1,
        'align':    'center',#水平居中
        'valign':   'vcenter',#垂直居中
    })
    
    #出表的日期、星期
    #detester将获取传入值
    #detester = '2019-01-08';
    currdate = datetime.datetime.strptime(detester,'%Y-%m-%d')
    tw = currdate.strftime('%w');
    weekday = switch_weekday_item(tw);
    
    #上周同期
    delta = relativedelta(weeks=-1);
    n_days = currdate + delta;
    beforeweekday = n_days.strftime('%Y-%m-%d');
    
    #上月同期
    delta2 = relativedelta(weeks=-5);
    n_days2 = currdate + delta2;
    beforemonthday = n_days2.strftime('%Y-%m-%d');
    print("detester","beforeweekday","beforemonthday","weekday");
    print(detester,beforeweekday,beforemonthday,weekday);
    
    nowt = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S');
    init = str(detester+" "+beforeweekday+" "+beforemonthday+" "+weekday)
    f = open('D:\\TahoeLi_Auto\\AutoreportTaholi\\xlsxreport\\log.txt','a+');
    init = "%s:Report Dates %s\n"%(str(nowt),str(init))
    f.write(init)
    f.close();
    
    worksheet.merge_range('A1:I1',"日销售汇总表",format_title);
    worksheet.write('A2', '大兴泰禾里',merge_format1)       #工总表写入简单文本
    worksheet.write('C2', weekday);
    worksheet.write('A3', "类目",merge_format2);
    worksheet.merge_range('B2:C2',"报表日期："+detester,merge_format1);
    worksheet.merge_range('D2:E2',weekday,merge_format1);
    worksheet.merge_range('F2:G2',"天气",merge_format1);
    
    #获取天气
    weatherdata = getweather(detester);
    worksheet.merge_range('H2:I2',weatherdata,merge_format2_1);
    worksheet.merge_range('B3:C3',"当前日",merge_format2);
    worksheet.merge_range('D3:E3',"上周同日: "+beforeweekday,merge_format2);
    worksheet.merge_range('F3:G3',"上月同日: "+beforemonthday,merge_format2);
    worksheet.merge_range('H4:I8',"",format1);
    worksheet.merge_range('H3:I3',"",merge_format2);
    worksheet.write('A6',"",merge_format2);
    

    #当日销售和对比
    worksheet.write('A4', "销售额",merge_format3);
    worksheet.write('A5', "进店客流",merge_format3);
    #
    worksheet.write('A6', "交易笔数",merge_format3);
    worksheet.write('A7', "成交率",merge_format3);
    worksheet.write('A8', "客单价",merge_format3);

    currsale,pf,tr = tusumquery(detester);
    worksheet.merge_range('B4:C4',currsale,format1);
    worksheet.merge_range('B5:C5',pf,format2);
    worksheet.merge_range('B6:C6',tr,format2);
    worksheet.merge_range('B7:C7',tr/pf,format3);
    worksheet.merge_range('B8:C8',currsale/tr,format1);
    
    #上周同期
    currsale1,pf1,tr1 = tusumquery(beforeweekday);
    worksheet.write('D4',currsale1,format1);
    worksheet.write('D5',pf1,format2);
    worksheet.write('D6',tr1,format2);
    worksheet.write('D7',tr1/pf1,format3);
    worksheet.write('D8',currsale1/tr1,format1);
    if currsale/currsale1-1>0:
        f = format3;
    else:
        f = format3_1;
    worksheet.write('E4', currsale/currsale1-1,f) 
    if pf/pf1-1>0:
        f = format3;
    else:
        f = format3_1;
    worksheet.write('E5', pf/pf1-1,f) 
    if tr/tr1-1>0:
        f = format3;
    else:
        f = format3_1;
    worksheet.write('E6', tr/tr1-1,f) 
    #成交率对比绝对值
    if tr/pf-tr1/pf1>0:
        f = format3;
    else:
        f = format3_1;
    worksheet.write('E7', tr/pf-tr1/pf1,f) 
    #客单价对比绝对值
    if currsale/tr-currsale1/tr1>0:
        f = format1;
    else:
        f = format1_1;
    worksheet.write('E8', currsale/tr-currsale1/tr1,f) 
    
    #上月同期
    currsale2,pf2,tr2 = tusumquery(beforemonthday);
    worksheet.write('F4',currsale2,format1);
    worksheet.write('F5',pf2,format2);
    worksheet.write('F6',tr2,format2);
    if currsale2:
        worksheet.write('F7',tr2/pf2,format3);
        worksheet.write('F8',currsale2/tr2,format1);
        if currsale/currsale2-1>0:
            f = format3;
        else:
            f = format3_1;
        worksheet.write('G4', currsale/currsale2-1,f) 
        if pf/pf2-1>0:
            f = format3;
        else:
            f = format3_1;
        worksheet.write('G5', pf/pf2-1,f) 
        if tr/tr2-1>0:
            f = format3;
        else:
            f = format3_1;
        worksheet.write('G6', tr/tr2-1,f) 
        #成交率对比绝对值
        if tr/pf-tr2/pf2>0:
            f = format3;
        else:
            f = format3_1;
        worksheet.write('G7', tr/pf-tr2/pf2,f) 
        #客单价对比绝对值
        if currsale/tr-currsale2/tr2>0:
            f = format1;
        else:
            f = format1_1;
        worksheet.write('G8', currsale/tr-currsale2/tr2,f) 
    
    
    worksheet.write('A9', "",merge_format2);
    worksheet.merge_range('B9:C9',"本月累计",merge_format2);
    worksheet.merge_range('D9:E9',"本年累计",merge_format2);
    worksheet.merge_range('F9:G9',"上月同期累计",merge_format2);
    worksheet.merge_range('H9:I9',"",merge_format2);
    
    #累计项目
    s1,p1,t1=tusumquery2(detester);
    worksheet.write('A10', "累计销售",merge_format3);
    worksheet.write('A11', "累计客流",merge_format3);
    worksheet.write('A12', "累计交易笔数",merge_format3);
    worksheet.write('A13', "月均成交率",merge_format3);
    worksheet.write('A14', "月均客单价",merge_format3);
    worksheet.merge_range('B10:C10', s1,format1);
    worksheet.merge_range('B11:C11', p1,format2);
    worksheet.merge_range('B12:C12', t1,format2);
    worksheet.merge_range('B13:C13', t1/p1,format3);
    worksheet.merge_range('B14:C14', s1/t1,format1);
    
    
    
    #上月累计
    delta3 = relativedelta(days=-20);
    n_days3 = currdate + delta3;
    d = currdate.strftime("%d")
    beforemonth = n_days3.strftime('%Y-%m')+'-'+d;
    s2,p2,t2=tusumquery2(beforemonth);
    worksheet.write('F10', s2,format1);
    worksheet.write('F11', p2,format2);
    worksheet.write('F12', t2,format2);
    worksheet.write('F13', t2/p2,format3);
    worksheet.write('F14', s2/t2,format1);
    if s1/s2-1>0:
        f = format3;
    else:
        f = format3_1;
    worksheet.write('G10', s1/s2-1,f) 
    if p1/p2-1>0:
        f = format3;
    else:
        f = format3_1;
    worksheet.write('G11', p1/p2-1,f) 
    if t1/t2-1>0:
        f = format3;
    else:
        f = format3_1;
    worksheet.write('G12', t1/t2-1,f) 
    
    worksheet.merge_range('H10:I14',"",format1);
    
    #累计本年度
    thisyear = currdate.strftime('%Y-01-01');
    ys1,yp1,yt1 = sumyearsales(thisyear,detester)
    
    worksheet.merge_range('D10:E10', ys1,format1);
    worksheet.merge_range('D11:E11', yp1,format2);
    worksheet.merge_range('D12:E12', yt1,format2);
    worksheet.merge_range('D13:E13', yt1/yp1,format3);
    worksheet.merge_range('D14:E14', ys1/yt1,format1);
    
    #成交率对比绝对值
    if t2/p2-yt1/yp1>0:
        f = format3;
    else:
        f = format3_1;
    worksheet.write('G13', t2/p2-yt1/yp1,f) 
    #客单价对比绝对值
    if s2/t2-ys1/yt1>0:
        f = format1;
    else:
        f = format1_1;
    worksheet.write('G14', s2/t2-ys1/yt1,f) 
    
    
    totelyearbudget = getyearbudget(detester);
    
    #totelyearbudget = 10580000.00
    worksheet.write('A15', "全年销售预算",merge_format2);
    worksheet.write('A16', "全年完成率",merge_format2);
    
    worksheet.merge_range('B15:C15',totelyearbudget,merge_format2);
    yp = float(ys1)/float(totelyearbudget);
    worksheet.merge_range('B16:C16',yp,merge_format2_2);
    
    worksheet.merge_range('D15:I15',"",merge_format2);
    worksheet.merge_range('D16:I16',"",merge_format2);
    
    
    
    #业态销售汇总
    worksheet.merge_range('A17:I17', "",merge_format1);
    worksheet.set_row(1,26) 
    worksheet.set_row(16,8) 
    r = 17;
    c = 0;
    worksheet.write(r,c, "",merge_format2);
    c=c+1;
    worksheet.write(r,c, "业态",merge_format2);
    c=c+1;
    worksheet.write(r,c, "本日销售",merge_format2);
    c=c+1;
    worksheet.write(r,c, "上周同日",merge_format2);
    c=c+1;
    worksheet.write(r,c, "上月同日",merge_format2);                    
    c=c+1;
    worksheet.write(r,c, "本月累计",merge_format2);
    c=c+1;
    worksheet.write(r,c, "上月累计同比",merge_format2);
    c = c+1;
    c2=c+1;
    worksheet.merge_range(r,c,r,c2, "业态销售冠军",merge_format2); 
    
    r2 = r+1;
    c = 1;
    categoryname = getcategoryname();
    for i in categoryname:
        worksheet.write(r2,c, i[0],format2);
        cs1,cp1,ct1 = tusumcategoryquery(detester,i[0]);
        cs2,cp2,ct2 = tusumcategoryquery(beforeweekday,i[0]);
        cs3,cp3,ct3 = tusumcategoryquery(beforemonthday,i[0]);
        cs4,cp4,ct4 = tusumcategoryquery2(detester,i[0]);
        cs5,cp5,ct5 = tusumcategoryquery2(beforemonth,i[0]);
        worksheet.write(r2,2,cs1,format4);
        if cs2!=0:
            csf1 = cs1/cs2-1;
            if cs1/cs2-1>0:
                f = format3_3;
            else:
                f = format3_4;
        else:
            f = format3_4;
            csf1 = 0;
        worksheet.write(r2,3,csf1,f);
        
        if cs3!=0:
            csf2 = cs1/cs3-1;
            if cs1/cs3-1>0:
                f = format3_3;
            else:
                f = format3_4;
        else:
            f = format3_4;
            csf2 = 0;
        worksheet.write(r2,4,csf2,f);
        worksheet.write(r2,5,cs4,format4);
        
        if cs5!=0:
            csf3 = cs4/cs5-1;
            if csf3>0:
                f = format3_3;
            else:
                f = format3_4;
        else:
            f = format3_4;
            csf3 = 0;
        worksheet.write(r2,6,csf3,f);
        
        name,re1,re2,re3 = saleschampioneachcategory(detester,i[0]);
        worksheet.write(r2,7,name,format2);
        worksheet.write(r2,8,re1,format4);
        r2 = r2+1;
    worksheet.merge_range(r,0,r2-1,0, "业态销售",merge_format2); 
    worksheet.merge_range(r2,1,r2,2, "重点店铺",merge_format2)
    worksheet.merge_range(r2,3,r2,8, "本日销售前20名",merge_format2);
    worksheet.merge_range(r2,0,r2+11,0, "销售排名",merge_format2);
    worksheet.set_row(r2,22);
    r2=r2+1;
    worksheet.write(r2,1, "店铺名称",merge_format2);
    worksheet.write(r2,2, "销售",merge_format2);
    worksheet.write(r2,3, "店铺",merge_format2);
    worksheet.write(r2,4, "业态",merge_format2);
    worksheet.write(r2,5, "销售",merge_format2);
    worksheet.write(r2,6, "店铺",merge_format2);
    worksheet.write(r2,7, "业态",merge_format2);
    worksheet.write(r2,8, "销售",merge_format2);
    worksheet.set_row(r2,22);
    datasales = getimportantamtsold(detester);
    r = r2+1;
    for i in datasales:
        print(i[0],i[1])
        worksheet.write(r,1,i[0],format2)
        worksheet.write(r,2,i[1],format4)
        r=r+1
        
    for i in range(10-len(datasales)):
        worksheet.write(r,1,'',format2)
        worksheet.write(r,2,'',format4)
        r=r+1

    #top 20
    top20 = top20brand(detester);
    r = r2+1;
    n=0;c1 = 3;c2 = 4;c3 = 5;
    for i in top20:
        if(n>9):
            c1 = c1+3;c2 = c2+3;c3 =c3+3; 
            r = r2+1;
            n=-10;
        worksheet.write(r,c1,i[0],format2)
        worksheet.write(r,c2,i[1],format2)
        worksheet.write(r,c3,i[2],format4)
        r=r+1;
        n=n+1
    worksheet.merge_range(r,0,r,8,"备注：1.环比和同比采自日期为前一周相同星期，以及上个月同星期的日期; 2.成交率、客单价成长率使用绝对值")

    #设置行高
    worksheet.set_row(1,30);
    worksheet.set_row(2,22);
    worksheet.set_row(8,22);
    worksheet.set_row(17,22);
    
    # Insert an image.
    #worksheet.insert_image('B5', 'logo.png')   #插入图片
    
    #设置列宽
    worksheet.set_column('A:I', 15); 
    workbook.close()    #关闭工作薄
    return filename,path;
#获取当前日期的前一天
currdate = datetime.datetime.now().strftime('%Y-%m-%d');
y = datetime.datetime.now()+relativedelta(days=-1)
y = y.strftime("%Y-%m-%d");

nowt = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S');
f = open('D:\\TahoeLi_Auto\\AutoreportTaholi\\xlsxreport\\log.txt','a+');
init = """
##########################################
%s:.........Start..........
"""%str(nowt)
f.write(init)
f.close();

db = connectmysql(ip);    
filename,path =exportexcel(y,db); 

nowt = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S');
f = open('D:\\TahoeLi_Auto\\AutoreportTaholi\\xlsxreport\\log.txt','a+');
init = "%s:%s\n"%(str(nowt),str(filename))
f.write(init)
f.close();


#发送邮件
def activesendmail(emailfrom,emailto,port,smtp_server,password,ir):
    print(emailto)
    nowt = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S');
    f = open('D:\\TahoeLi_Auto\\AutoreportTaholi\\xlsxreport\\log.txt','a+');
    init = "%s:Send mail %s "%(str(nowt),str(emailto))
    f.write(init)
    f.close();
    context = ssl.create_default_context()
    fileToSend = filename

    
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = ",".join(emailto)
    ff = filename.split('D')[0];
    msg["Subject"] = ff+"大兴泰禾里日销售汇总报表";
    message = """
    Dear All,
        附件中名为 %s 的报表，请阅。
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
        f = open('D:\\TahoeLi_Auto\\AutoreportTaholi\\xlsxreport\\log.txt','a+');
        init = ",%s Send mail sccuess.\n "%(str(nowt))
        f.write(init)
        f.close();
        
        return True;
    except:
        nowt = datetime.datetime.now().strftime('%H:%M:%S');
        f = open('D:\\TahoeLi_Auto\\AutoreportTaholi\\xlsxreport\\log.txt','a+');
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
    '''
    smtp_server = "smtp.tahoecn.com"
    emailfrom = "liuxuanchao@tahoecn.com"  # Enter your address
    password = "1984Konami";
    '''
    
    query =  "select email from maillist where priority>0 order by priority DESC";
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
    

t = sendmail(filename,path);
if t:
    dpath = "D:\\TahoeLi_Auto\\AutoreportTaholi\\xlsxreport\\ExcelReport";
    #发送完邮件后移动文件到ExcelReport
    shutil.move(path+"\\"+filename,dpath)
    f = open('D:\\TahoeLi_Auto\\AutoreportTaholi\\xlsxreport\\log.txt','a+');
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
    print("Send Mail Error!");
    