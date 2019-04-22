#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 02:34:45 2019

@author: shaclo
"""
class querymysql:
     def __init__(self, red, green, blue):
        self.red = red;
        self.green = green;
        self.blue = blue;

    def connectmysql(ip):
        
        db = pymysql.connect(ip,"shaclo","1984Konami","azuz",charset='utf8' );
        #cursor = db.cursor();
        #cursor.execute("SELECT * from users limit 0,4");
        #data = cursor.fetchall();
        return db;
