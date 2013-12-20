#!/usr/bin/python
#-*- encoding: gbk -*- 

sqlscripts = """\
CREATE TABLE DAY_FILE 
(
    STKID   VARCHAR(10) NOT NULL,
    STKDATE DATE NOT NULL,
    OPEN    FLOAT,
    HIGH    FLOAT,
    LOW     FLOAT,
    CLOSE   FLOAT,
    VOL     INTEGER,
    AMOUT   FLOAT,
    ADJC    FLOAT,
PRIMARY KEY (STKID,STKDATE)
);

CREATE TABLE MIN1_FILE 
(
    STKID   VARCHAR(10) NOT NULL,
    STKDATE DATE NOT NULL,
    STKTIME TIME NOT NULL,
    OPEN    FLOAT,
    HIGH    FLOAT,
    LOW     FLOAT,
    CLOSE   FLOAT,
    VOL     INTEGER,
    AMOUT   FLOAT,
    ADJC    FLOAT,
PRIMARY KEY (STKID,STKDATE,STKTIME)
);

CREATE TABLE MIN5_FILE 
(
    STKID   VARCHAR(10) NOT NULL,
    STKDATE DATE NOT NULL,
    STKTIME TIME NOT NULL,
    OPEN    FLOAT,
    HIGH    FLOAT,
    LOW     FLOAT,
    CLOSE   FLOAT,
    VOL     INTEGER,
    AMOUT   FLOAT,
    ADJC    FLOAT,
PRIMARY KEY (STKID,STKDATE,STKTIME)
);
"""

import sqlite3,datetime
import os,sys

def adapt_datetime_time(val):
    return val.isoformat()

def convert_datetime_time(val):
    return datetime.time(*map(int, val.split(":")))

def convert_datetime_time(val):
    #datepart, timepart = val.split(" ")
    timepart = val 
    #year, month, day = map(int, datepart.split("-"))
    timepart_full = val.split(".")
    hours, minutes, seconds = map(int, timepart_full[0].split(":"))
    if len(timepart_full) == 2:
        microseconds = int('{:0<6.6}'.format(timepart_full[1].decode()))
    else:
        microseconds = 0

    val = datetime.time(hours, minutes, seconds, microseconds)
    return val

sqlite3.register_adapter(datetime.time, adapt_datetime_time)
sqlite3.register_converter("time", convert_datetime_time)

def exchange_insert(dbfile,txtfile,stkid,HaveTime=False,DateFormat = "%d.%m.%Y"):
    lines = file(txtfile).readlines()
    data = []
    for i,line in enumerate(lines):
        if i < 1 : continue
        line = line.strip()
        if line.startswith('#') :continue
        tt = line.split(',')
        if len(tt) < 6 : continue
        dtstr = tt[0].strip().split(' ')
        l_date = datetime.datetime.strptime(dtstr[0],DateFormat).date()
        if len(dtstr) > 1:
            l_time = convert_datetime_time(dtstr[1])
        else:
            l_time = datetime.time(0, 0, 0, 0)
        if HaveTime:
            data.append((stkid,l_date,l_time, #.strftime('%H:%M:%S'),
                float(tt[1]),float(tt[2]),float(tt[3]),float(tt[4]),float(tt[5]) ) )
        else:
            data.append((stkid,l_date, #.strftime('%H:%M:%S'),
                float(tt[1]),float(tt[2]),float(tt[3]),float(tt[4]),float(tt[5]) ) )

    #endfor
    conn = sqlite3.connect(dbfile,detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    curs = conn.cursor()
    try:
        #curs.execute("delete from MIN1_FILE")
        if HaveTime:
            curs.executemany("INSERT INTO MIN1_FILE(STKID,STKDATE,STKTIME,OPEN,HIGH,LOW,CLOSE,VOL) VALUES(?,?,?,?,?,?,?,?)",data)
        else:
            curs.executemany("INSERT INTO DAY_FILE(STKID,STKDATE,OPEN,HIGH,LOW,CLOSE,VOL) VALUES(?,?,?,?,?,?,?)",data)
    except sqlite3.IntegrityError,e:
        sys.stderr.write(e)
        sys.stderr.write('\n')
    conn.commit()
    for row in curs.execute("select * from min1_file where stkid = 'USDJPY' order by stkid, stkdate, stktime limit 100"):
        print row
    conn.close()


"""\
AUDUSD_Candlestick_1_D_BID_01.01.1986-28.11.2013.csv
EURUSD_Candlestick_1_D_BID_01.01.1972-28.11.2013.csv
GBPUSD_Candlestick_1_D_BID_01.01.1986-28.11.2013.csv
NZDUSD_Candlestick_1_D_BID_01.01.1991-28.11.2013.csv
USDCAD_Candlestick_1_D_BID_01.01.1986-28.11.2013.csv
USDCHF_Candlestick_1_D_BID_01.01.1986-28.11.2013.csv
USDJPY_Candlestick_1_D_BID_01.01.1986-28.11.2013.csv
USDNOK_Candlestick_1_D_BID_01.01.1991-28.11.2013.csv
USDSEK_Candlestick_1_D_BID_01.01.1991-28.11.2013.csv
USDSGD_Candlestick_1_D_BID_01.01.1991-28.11.2013.csv
"""        

def which5min_new(dt):
    """时间划分"""
    if type(dt) != datetime.datetime and  type(dt) != datetime.time:
        return None
    t = dt
    ret = None
    if type(dt) == datetime.datetime:
        t = datetime.time(dt.hour,dt.minute,dt.second)

    h = t.hour
    m = t.minute
    if h == 23 and m >=55 :
        min5 = 59
    elif h < 23 and m >= 55 :
        min5 = 0
        h += 1
    else:
        min5 = (int(m / 5) + 1) * 5
    if type(dt) == datetime.datetime:
        return datetime.datetime(dt.year,dt.month,dt.day,h,min5,0)
    else:
        return datetime.time(h,min5,0)



def testmin5_new():
    dbfile = r'e:\cwork\study\Stock\somedata\dbtest.sqlite'
    # conn的参数 决定是否启用类型适配器
    conn = sqlite3.connect(dbfile,detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    curs = conn.cursor()
    #for row in curs.execute("select * from min1_file where stkid = 'USDJPY' and stkdate = '2011-01-01' order by stkid, stkdate, stktime"):
    for row in curs.execute("select * from min1_file where stkid = 'USDJPY' and stkdate = '2011-01-01' order by stkid, stkdate, stktime limit 10000"):
        print row[2],which5min_new(row[2])
    conn.close()



if __name__ == '__main__':
    #exchange_insert(dbfile = r'e:\cwork\study\Stock\somedata\dbtest.sqlite',\
            #txtfile = r'E:\cwork\study\Stock\samedata\USDSGD_Candlestick_1_D_BID_01.01.1991-28.11.2013.csv',\
            #stkid = 'USDSGD',\
            #HaveTime = False ,\
            #DateFormat = "%d.%m.%Y")
    testmin5_new()         


