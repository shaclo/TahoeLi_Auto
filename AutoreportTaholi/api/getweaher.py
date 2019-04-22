# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 12:39:29 2019

@author: Administrator
"""
import requests
import datetime;
import pymysql

nowt = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S');
f = open('D:\\TahoeLi_Auto\\AutoreportTaholi\\api\\log.txt','a+');
init = """
*****************************************
%s:GET weather Start..........
"""%str(nowt)
f.write(init)
f.close();

ip = "172.23.110.16";
#ip = "223.71.105.241";
def get_data_json():
    #url = 'https://restapi.amap.com/v3/weather/weatherInfo?city=110115&key=0dc399515782167f251a531fa9844a03'
    url = 'https://restapi.amap.com/v3/weather/weatherInfo?key=6b8fb80788824d27765cdd1a9e0a8ad0&city=110115'

    r = requests.get(url)
    return r.json()
    
       
    
#if __name__ == '__main__':
r = get_data_json()
lives = r['lives'][0]
"""
{'province': '北京',
 'city': '大兴区',
 'adcode': '110115',
 'weather': '多云',
 'temperature': '0',
 'winddirection': '西',
 'windpower': '≤3',
 'humidity': '22',
 'reporttime': '2019-01-09 13:20:01'}
"""
db = pymysql.connect(ip,"shaclo","1984Konami","azuz",charset='utf8' );

txdate = datetime.datetime.now().strftime('%Y-%m-%d');
query = "INSERT INTO weather VALUES ('"+str(txdate)+"','"+lives['weather']+"','"+lives['temperature']+"','"+lives['winddirection']+"','"+lives['windpower']+"','"+lives['humidity']+"')";

ip = "172.23.110.16";
#ip = "223.71.105.241";

nowt = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S');
f = open('D:\\TahoeLi_Auto\\AutoreportTaholi\\api\\log.txt','a+');
print(query)

try:
    cursor = db.cursor();
    cursor.execute(query);
    db.commit()
    init = "%s:Weather#Query Sucess,%s\n"%(str(nowt),str(query))
except:
    init = "%s:Weather#Query Fail,%s\n"%(str(nowt),str(query))
    pass
f.write(init)
f.close();
db.close()
