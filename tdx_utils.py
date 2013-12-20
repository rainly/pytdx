#!/usr/bin/python
#-*- encoding: gbk -*- 
from __future__ import division
import struct   
import os,time ,datetime,string,sys,math,re,shutil,glob
from tdx_const import *
import ctypes as ct

#############################################################
# read 通达信分笔数据
# example readfbtxt(readlines(),'20100831-600000.TXT')
# 返回的data格式为
# list of dict [{'ID':'stock id','DT':datetime.datetime(),
#  'CLOSE':Price,'VOL':vol,'AMT':amout}] 
# vol 为股而不是手！
#############################################################
def readfbtxt(p_lines,p_name):
        """读通达信分笔数据 """
        shortname = os.path.basename(p_name)
        shortname = os.path.splitext(shortname)[0]
        sDay,stkid = shortname.split('-')
        if len(sDay) != 8 : return []
        stky = int(sDay[0:4])
        stkm = int(sDay[4:6])
        stkd = int(sDay[6:8])    
        line_no = 0
        data = []
        for l in p_lines:
            line_no += 1
            if line_no <=3: continue 
            l = l.strip()
            t = re.split('\s+',l)
            if len(t) < 4 : continue
            k = None
            try:
                k =  datetime.datetime(stky,stkm,stkd,int(t[0][0:2]),int(t[0][3:5]))
            except ValueError ,e :
                if DEBUG :
                    print e,p_name
                continue
            p = float(t[1])      #price
            vol = int(t[2])*100  #股数
            amt = p * vol        #成交量
            bscnt = 0            #笔数
            bstag = ''           #buy or sale
            try:
                bscnt = int(t[3])    #笔数
                bstag = t[4]         #buy or sale
            except IndexError,e:
                pass
            data.append({M_ID:stkid,
                        M_DT:k,
                        M_CLOSE:p,
                        M_VOL:vol,
                        M_AMT:amt,
                        'BSCNT':bscnt,
                        'BSTAG':bstag})               
        return data

#############################################################
# 将分笔数据转化为分笔数据
# p_data:传入参数 为readfbtxt所返回
# data:  返回的数据格式为
# 返回的data格式为
# list of dict [{'ID':'stock id','DT':datetime.datetime(),
#  'OPEN':OpenPrice,'HIGH':HighPrice,'LOW':LowPrice,'CLOSE':Price,
#  'VOL':vol,'AMT':amout}] 
# vol 为股而不是手！
#############################################################
def fbtxt2lc0(p_data):
    """分笔数据转化为分笔数据的OHLC"""
    data = []
    for i in p_data:
        data.append({ M_ID: i[M_ID] ,
                      M_DT: i[M_DT] ,
                      M_OPEN : i[M_CLOSE] ,
                      M_HIGH : i[M_CLOSE] ,
                      M_LOW  : i[M_CLOSE] ,
                      M_CLOSE: i[M_CLOSE],
                      M_VOL  : i[M_VOL]  ,
                      M_AMT  : i[M_AMT]
            })
    return data



#############################################################
# 将分笔数据转化为1分钟数据
# p_data:传入参数 为readfbtxt所返回
# p_convfq 为复权处理列表[(日期,比率)]
# data:  返回的数据格式为
# list of dict [{'ID':'stock id','DT':datetime.datetime(),
#  'OPEN':OpenPrice,'HIGH':HighPrice,'LOW':LowPrice,'CLOSE':Price,
#  'VOL':vol,'AMT':amout}] 
# vol 为股而不是手！
#############################################################
def fbtxt2lc1(p_data,p_convfq = None):
    """分笔数据转化为1分钟数据"""
    data = []
    for i in p_data:
        t = i[M_DT]     #datetime
        p = i[M_CLOSE]     #price
        lend = len(data)
        j = lend - 1
        while j >= 0:
            if data[j][M_DT] == t:break
            j -= 1
        if j < 0:  #没有找到该时间
            data.append({ M_ID: i[M_ID] ,
                      M_DT: i[M_DT] ,
                      M_OPEN : i[M_CLOSE] ,
                      M_HIGH : i[M_CLOSE] ,
                      M_LOW  : i[M_CLOSE] ,
                      M_CLOSE: i[M_CLOSE],
                      M_VOL  : i[M_VOL]  ,
                      M_AMT  : i[M_AMT] })
        else:          #找到该时间
            if p > data[j][M_HIGH]:  #high
                data[j][M_HIGH] = p
            if p < data[j][M_LOW]:  #low
                data[j][M_LOW] = p
            data[j][M_CLOSE] = p      #close
            data[j][M_AMT] += i[M_AMT]  #amout
            data[j][M_VOL] += i[M_VOL]  #vol
    #data.sort(key = lambda x:x[1])  #以datetime 排序

    #目前的版本暂时只处理一个复权的问题吧
    #复权的时候只处理了价格，并未处理股数！！
    #if p_convfq and len(p_convfq ) > 0 :
        #l_fq = p_convfq[0]
        #for i,dd in enumerate(data):
            #if dd[M_DT].date()   <= l_fq[0] : # 前复权 
                #data[i][M_OPEN]  /= l_fq[1] 
                #data[i][M_HIGH]  /= l_fq[1] 
                #data[i][M_LOW]   /= l_fq[1] 
                #data[i][M_CLOSE] /= l_fq[1] 

    return data


#############################################################
# 将1分钟数据转为5分钟数据
# p_data:传入参数 为fbtxt2lc1所返回
# data:  返回的数据格式为
# list of dict [{'ID':'stock id','DT':datetime.datetime(),
#  'OPEN':OpenPrice,'HIGH':HighPrice,'LOW':LowPrice,'CLOSE':Price,
#  'VOL':vol,'AMT':amout}] 
# vol 为股而不是手！
#############################################################
def lc1tolc5(p_data):
    """1分钟数据转化为5分钟数据 """
    if len(p_data) <= 0: return []
    data = []
    for i in p_data:
        t = which5min(i[M_DT])   #找对应5分钟的区段
        if t == None:
            raise ValueError,'time out of range: %s' % i[M_DT]
        lend = len(data)
        j = lend - 1
        while j >= 0:
            if data[j][M_DT] == t:break
            j -= 1
        if j < 0:  #没有找到该时间
            data.append({ M_ID: i[M_ID] ,
                      M_DT: t ,
                      M_OPEN : i[M_OPEN] ,
                      M_HIGH : i[M_HIGH] ,
                      M_LOW  : i[M_LOW] ,
                      M_CLOSE: i[M_CLOSE],
                      M_VOL  : i[M_VOL]  ,
                      M_AMT  : i[M_AMT] })
        else:         #找到该时间
            if i[M_HIGH] > data[j][M_HIGH]:  #high
                data[j][M_HIGH] = i[M_HIGH]
            if i[M_LOW] < data[j][M_LOW]:  #low
                data[j][M_LOW] = i[M_LOW]
            data[j][M_CLOSE] = i[M_CLOSE]      #close
            data[j][M_AMT] += i[M_AMT]     #amout
            data[j][M_VOL] += i[M_VOL]     #vol
    #data.sort(key = lambda x:x[1])  #以datetime 排序
    return data




#############################################################
# 一个时间对应的5分钟区间段
# dt 传入参数 为一个datetime.datetime or datetime.time
# 返回datetime 或time 
#############################################################
def which5min(dt):
    """5 分钟时间划分 """
    if type(dt) != datetime.datetime and  type(dt) != datetime.time:
        return None
    t = dt
    ret = None
    if type(dt) == datetime.datetime:
        t = datetime.time(dt.hour,dt.minute,dt.second)

    if t < datetime.time(9,30) : return None 
    if   t < datetime.time(9,35): ret = datetime.time(9,35)
    elif t < datetime.time(9,40): ret = datetime.time(9,40)
    elif t < datetime.time(9,45): ret = datetime.time(9,45)
    elif t < datetime.time(9,50): ret = datetime.time(9,50)
    elif t < datetime.time(9,55): ret = datetime.time(9,55)
    elif t < datetime.time(10,0): ret = datetime.time(10,0)
    elif t < datetime.time(10,5): ret = datetime.time(10,5)
    elif t < datetime.time(10,10): ret = datetime.time(10,10)
    elif t < datetime.time(10,15): ret = datetime.time(10,15)
    elif t < datetime.time(10,20): ret = datetime.time(10,20)
    elif t < datetime.time(10,25): ret = datetime.time(10,25)
    elif t < datetime.time(10,30): ret = datetime.time(10,30)
    elif t < datetime.time(10,35): ret = datetime.time(10,35)
    elif t < datetime.time(10,40): ret = datetime.time(10,40)
    elif t < datetime.time(10,45): ret = datetime.time(10,45)
    elif t < datetime.time(10,50): ret = datetime.time(10,50)
    elif t < datetime.time(10,55): ret = datetime.time(10,55)
    elif t < datetime.time(11,0): ret = datetime.time(11,0)
    elif t < datetime.time(11,5): ret = datetime.time(11,5)
    elif t < datetime.time(11,10): ret = datetime.time(11,10)
    elif t < datetime.time(11,15): ret = datetime.time(11,15)
    elif t < datetime.time(11,20): ret = datetime.time(11,20)
    elif t < datetime.time(11,25): ret = datetime.time(11,25)
    elif t <= datetime.time(11,30): ret = datetime.time(11,30)
    #elif t < datetime.time(13,0): ret = datetime.time(13,0)
    elif t < datetime.time(13,5): ret = datetime.time(13,5)
    elif t < datetime.time(13,10): ret = datetime.time(13,10)
    elif t < datetime.time(13,15): ret = datetime.time(13,15)
    elif t < datetime.time(13,20): ret = datetime.time(13,20)
    elif t < datetime.time(13,25): ret = datetime.time(13,25)
    elif t < datetime.time(13,30): ret = datetime.time(13,30)
    elif t < datetime.time(13,35): ret = datetime.time(13,35)
    elif t < datetime.time(13,40): ret = datetime.time(13,40)
    elif t < datetime.time(13,45): ret = datetime.time(13,45)
    elif t < datetime.time(13,50): ret = datetime.time(13,50)
    elif t < datetime.time(13,55): ret = datetime.time(13,55)
    elif t < datetime.time(14,0): ret = datetime.time(14,0)
    elif t < datetime.time(14,5): ret = datetime.time(14,5)
    elif t < datetime.time(14,10): ret = datetime.time(14,10)
    elif t < datetime.time(14,15): ret = datetime.time(14,15)
    elif t < datetime.time(14,20): ret = datetime.time(14,20)
    elif t < datetime.time(14,25): ret = datetime.time(14,25)
    elif t < datetime.time(14,30): ret = datetime.time(14,30)
    elif t < datetime.time(14,35): ret = datetime.time(14,35)
    elif t < datetime.time(14,40): ret = datetime.time(14,40)
    elif t < datetime.time(14,45): ret = datetime.time(14,45)
    elif t < datetime.time(14,50): ret = datetime.time(14,50)
    elif t < datetime.time(14,55): ret = datetime.time(14,55)
    elif t <= datetime.time(15,0):  ret = datetime.time(15,0)
    else : return None
    if type(dt) == datetime.datetime:
        return datetime.datetime(dt.year,dt.month,dt.day,ret.hour,ret.minute,ret.second)
    else: return ret 

def which5min_all(dt):
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
    

#############################################################
# read 日线数据文件
# example readDayBin(r'E:\new_gxzq_v6\Vipdoc\sh\lday\sh600000.day')
# return data 格式
# list of dict [{'ID':'stock id','DT':datetime.date,
#  'OPEN':OpenPrice,'HIGH':HighPrice,'LOW':LowPrice,'CLOSE':Price,
#  'VOL':vol,'AMT':amout}] 
# vol 为股而不是手！
#############################################################
def readDayBin(p_name):
    """读日线二进制文件"""
    f = open(p_name,'rb')
    stkid = os.path.split(p_name)[1]
    stkid = os.path.splitext(stkid)[0]
    if string.lower(stkid[0:2]) == 'sh' or string.lower(stkid[0:2]) == 'sz':
        stkid = stkid[2:]
    icnt = 0
    data = []
    while 1:
        raw = f.read(4*8)
        if len(raw) <= 0 : break
        tmp = struct.unpack('IIIIIfII',raw)
        y = tmp[0] // 10000
        m = (tmp[0] - y*10000 ) // 100
        d = tmp[0] % 100
        data.append({M_ID:stkid,
                     M_DT:datetime.date(y,m,d),
                     M_OPEN:tmp[1] / 100.0,
                     M_HIGH:tmp[2] / 100.0,
                     M_LOW:tmp[3] / 100.0,
                     M_CLOSE:tmp[4] / 100.0,
                     M_AMT:tmp[5] ,
                     M_VOL:tmp[6] ,
                     'UNKOWN':tmp[7]
            
            })
    #end while
    return data


#############################################################
# write 日线数据文件
# example writeDayBin(p_data,r'E:\new_gxzq_v6\Vipdoc\sh\lday\sh600000.day')
# p_data格式
# list of dict [{'ID':'stock id','DT':datetime.date,
#  'OPEN':OpenPrice,'HIGH':HighPrice,'LOW':LowPrice,'CLOSE':Price,
#  'VOL':vol,'AMT':amout}] 
# vol 为股而不是手！
#############################################################
def writeDayBin(p_data,p_name):
    """写日线二进制文件"""
    f = open(p_name,'wb')
    for i in p_data:
        t = i[M_DT].year * 10000 + i[M_DT].month * 100 + i[M_DT].day
        raw = struct.pack('IIIIIfII',t, round(i[M_OPEN]*100,0),
                                        round(i[M_HIGH]*100,0),
                                        round(i[M_LOW]*100,0),
                                        round(i[M_CLOSE]*100,0),
                                        float(i[M_AMT]),
                                        i[M_VOL],
                                        i.get('UNKOWN',0))
        f.write(raw)    
    # end for
    f.close()





#############################################################
# read 分钟数据文件
# example readlc5(r'E:\new_gxzq_v6\Vipdoc\sh\fzline\sh600000.lc5')
# return data 格式
# list of dict [{'ID':'stock id','DT':(月,日,时,分),
#  'OPEN':OpenPrice,'HIGH':HighPrice,'LOW':LowPrice,'CLOSE':Price,
#  'VOL':vol,'AMT':amout}] 
# vol 为股而不是手！lc5根本就没有记录年！
#############################################################
def readMinBin(p_name):
        """tdx 5min 数据 
           日期上低16位表示月日，高16位表示分钟
           这个结构个人感觉就不如同花顺做的巧妙
               在一个4字节中把 年 月 日 时 分 都记录下来了
        """
        f = open(p_name,'rb')
        stkid = os.path.split(p_name)[1]
        stkid = os.path.splitext(stkid)[0]
        if string.lower(stkid[0:2]) == 'sh' or string.lower(stkid[0:2]) == 'sz':
            stkid = stkid[2:]
        icnt = 0
        data = []
        while 1:
            raw = f.read(4*8)
            if len(raw) <= 0 : break
            t = struct.unpack('IfffffII',raw)
            mins = (t[0] >> 16) & 0xffff
            mds  = t[0] & 0xffff
            month = int(mds / 100)
            day   = mds % 100
            hour = int(mins / 60)
            minute = mins % 60
            data.append({M_ID:stkid,
                         M_DT:(month,day,hour,minute),
                         M_OPEN:t[1],
                         M_HIGH:t[2],
                         M_LOW:t[3],
                         M_CLOSE:t[4],
                         M_AMT:t[5],
                         M_VOL:t[6],
                         'UNKOWN':t[7]})
            icnt += 1
        ## end while
        f.close()
        return data

#############################################################
# write通达信5min数据文件
# 传入p_data 结构 如readMinBin 所返回的结构 
#   M_DT 或者为datetime.datetime
#############################################################
def writeMinBin(p_data,p_name):
    fout = open(p_name,'wb')
    for i in p_data:
        if type(i[M_DT]) == datetime.datetime:
            t = i[M_DT].month*100 + i[M_DT].day + ( (i[M_DT].hour * 60 + i[M_DT].minute) << 16)
        else:
            t = i[M_DT][0]*100+i[M_DT][1] + ( (i[M_DT][2] * 60 + i[M_DT][3]) << 16)
        raw = struct.pack('IfffffII',t,i[M_OPEN],i[M_HIGH],i[M_LOW],i[M_CLOSE],i[M_AMT],i[M_VOL],i.get('UNKOWN',0))
        fout.write(raw)
    ## end for
    fout.close()


#############################################################
# read 分钟数据文件
# example readlc5(r'E:\new_gxzq_v6\Vipdoc\sh\fzline\sh600000.lc5')
# return data 格式
# list of dict [{'ID':'stock id','DT':datetime.datetime,
#  'OPEN':OpenPrice,'HIGH':HighPrice,'LOW':LowPrice,'CLOSE':Price,
#  'VOL':vol,'AMT':amout}] 
# vol 为股而不是手！新版本的lc5文件有记录年
#############################################################
def readMinBin_new(p_name):
        """tdx 5min 数据 
           日期上低16位表示年月日，高16位表示分钟
        """
        f = open(p_name,'rb')
        stkid = os.path.split(p_name)[1]
        stkid = os.path.splitext(stkid)[0]
        if string.lower(stkid[0:2]) == 'sh' or string.lower(stkid[0:2]) == 'sz':
            stkid = stkid[2:]
        icnt = 0
        data = []
        while 1:
            raw = f.read(4*8)
            if len(raw) <= 0 : break
            t = struct.unpack('IfffffII',raw)
            data.append({M_ID:stkid,
                         M_DT:int2datetime_new(t[0]),
                         M_OPEN:t[1],
                         M_HIGH:t[2],
                         M_LOW:t[3],
                         M_CLOSE:t[4],
                         M_AMT:t[5],
                         M_VOL:t[6],
                         'UNKOWN':t[7]})
            icnt += 1
        ## end while
        f.close()
        return data


#############################################################
# write通达信5min数据文件
# 传入p_data 结构 如readMinBin 所返回的结构 
#   M_DT 或者为datetime.datetime
#############################################################
def writeMinBin_new(p_data,p_name):
    fout = open(p_name,'wb')
    for i in p_data:
        raw = struct.pack('IfffffII',datetime2int_new(i[M_DT]),i[M_OPEN],i[M_HIGH],i[M_LOW],i[M_CLOSE],i[M_AMT],i[M_VOL],i.get('UNKOWN',0))
        fout.write(raw)
    #endfor
    fout.close()



###################################
## 整数转化为日期
###################################
def int2date(p_int):
    y = p_int // 10000
    m = (p_int - y*10000 ) // 100
    d = p_int % 100
    return datetime.date(y,m,d)

###################################
## 日期转化为整数
###################################
def date2int(p_date):
    return p_date.year * 10000 + p_date.month * 100 + p_date.day

###################################
## 整数转化为日期时间(没有年的tuple)
###################################
def int2datetime(p_int):
    """高十六位为时间，低十六位为日期 """
    mins = (p_int >> 16) & 0xffff
    mds  = p_int & 0xffff
    month = int(mds / 100)
    day   = mds % 100
    hour = int(mins / 60)
    minute = mins % 60
    return (month,day,hour,minute)

###################################
## 整数转化为日期时间有年，
## 而且这个数据结构也不同
## 在低16位中用5为表示年(要加2004才是真实的)
## 在低16位的其他11位表示月日
###################################
def int2datetime_new(p_int):
    mask = 0xFFF - (1 << 11)  # 11位的1
    mins = (p_int >> 16) & 0xffff
    ymds  = p_int & 0xffff
    tmpdd = ymds & mask
    month = int( tmpdd / 100 )
    day   = tmpdd % 100
    year =  ( ymds >> 11 ) + 2004
    hour = int(mins / 60)
    minute = mins % 60            
    return datetime.datetime(year,month,day,hour,minute)

###################################
## 日期时间转化为整数
###################################
def datetime2int(p_dt):
    if type(p_dt) == datetime.datetime:
        return p_dt.month*100 + p_dt.day + ( (p_dt.hour * 60 + p_dt.minute) << 16)
    else:
        return p_dt[0]*100 + p_dt[1] + ( (p_dt[2] * 60 + p_dt[3]) << 16)

###################################
## 日期时间转化为整数
###################################
def datetime2int_new(p_dt):
    return ((p_dt.year-2004) << 11 ) + p_dt.month*100 + p_dt.day + ( (p_dt.hour * 60 + p_dt.minute) << 16)



##################################
### struct 结构操作###############
##################################
def struct2stream(s):
    length  = ct.sizeof(s)
    p       = ct.cast(ct.pointer(s), ct.POINTER(ct.c_char * length))
    return p.contents.raw

def stream2struct(string, stype):
    if not issubclass(stype, ct.Structure):
        raise ValueError('The type of the struct is not a ctypes.Structure')
    length      = ct.sizeof(stype)
    stream      = (ct.c_char * length)()
    stream.raw  = string
    p           = ct.cast(stream, ct.POINTER(stype))
    return p.contents

#############################################################
#TODO:
#画线文件的读写增删 使用union也可以
#名称文件的读写增删
#复权文件的解读
#zip TXTFile and
#auto download
#############################################################
## 名称文件的解析
#############################################################
NAME_FILE_HEAD_LEN = 50
class T_TdxNames(ct.Structure):
    _pack_      = 1
    _fields_ = [
                ("stkid", ct.c_char * 9),  # stkid
                ("un1", ct.c_byte ),
                ("un2", ct.c_char*2), 
                ("un3", ct.c_float), # 未知
                ("un4", ct.c_int), # 
                ("un5", ct.c_int), # 
                ("stkname", ct.c_char * 18), # name
                ("un6", ct.c_int), # 
                ("un7", ct.c_char * 186),
                ("lastclose", ct.c_float), # 前日收盘
                ("un8", ct.c_byte),
                ("un9", ct.c_int),
                ("shortname", ct.c_char*9)   #缩写
                ]       

def get_tdxNames(fname,Bsimple = True):
    data = []
    try:
        f = open(fname,'rb')
    except IOError,e:
        return data
    else:
        f.seek(NAME_FILE_HEAD_LEN)
        itemlen = ct.sizeof(T_TdxNames)
        while True:
            raw = f.read(itemlen)
            if len(raw) <= 0 : break
            nn = stream2struct(raw,T_TdxNames)
            if Bsimple:
                data.append((nn.stkid,nn.stkname,nn.shortname))
            else:
                data.append((nn.stkid,nn.un1,nn.un2,nn.un3,nn.un4,nn.un5,
                    nn.un6,nn.un7,nn.lastclose,nn.stkname,nn.un8,nn.un9,nn.shortname))

        f.close()
        return data


class NamesFile():
    def __init__(self,fname):
        self.fname = fname
        self.head = ''
        self.items_raw = []
        self.count = 0
        self.items_index = {}
        self.sample_raw = ''
        self.read()

    def read(self):
        try:
            f = open(self.fname,'rb')
        except IOerror,e:
            pass
        else:
            self.head = f.read(NAME_FILE_HEAD_LEN)
            itemlen = ct.sizeof(T_TdxNames)
            icnt = 0
            while True:
                raw = f.read(itemlen)
                if len(raw) <= 0 : break
                nn = stream2struct(raw,T_TdxNames)
                self.items_raw.append(raw)
                self.items_index[nn.stkid] = icnt
                icnt += 1
            f.close()
            self.count = icnt
            if self.count > 0 :
                tmp_stru = stream2struct(self.items_raw[0],T_TdxNames)
                tmp_stru.un3 = 0.0
                tmp_stru.lastclose = 0.0
                self.sample_raw = struct2stream(tmp_stru)

    def update(self,idnames):
        """idnames[(stkid,stkname,shortname),(...)] """
        f = open(self.fname,'r+b')
        itemlen = ct.sizeof(T_TdxNames)
        for ii in idnames:
            if len(ii) >=3 :
                (stkid,stkname,shortname) = ii
                if self.items_index.has_key(stkid) :
                    pos = NAME_FILE_HEAD_LEN + itemlen * self.items_index[stkid]
                    raw = self.items_raw[self.items_index[stkid]]
                    nn = stream2struct(raw,T_TdxNames)
                    nn.stkname = stkname
                    nn.shortname = shortname
                    raw = struct2stream(nn)
                    f.seek(pos)
                    f.write(raw)
                    nn = None
                else:
                    ## 在最后加一行，并且让self.count +1
                    raw = self.sample_raw
                    tt = stream2struct(raw,T_TdxNames) ## 注意这里是指针
                    tt.stkid = stkid
                    tt.stkname = stkname
                    tt.shortname = shortname
                    raw = struct2stream(tt)
                    f.seek(0,os.SEEK_END)
                    f.write(raw)
                    self.items_index[stkid] = self.count
                    self.count += 1
                    tt = None
        f.close()

    def write(self,fname,stkids):
        """生成新的文件"""
        f = open(fname,'wb')
        f.write(self.head)
        for stkid in stkids:
            ind = self.items_index.get(stkid,None)
            if ind == None:
                continue
            f.write(self.items_raw[ind])
        f.close()

## 名称文件的解析
#############################################################

#------------------------------
#-- i2bin 整数转为 2进制字符串
#------------------------------
def i2bin(x):
        result = ''
        x = int(x)
        while x > 0:
               mod = x & 0x01 # 取2的余数
               x = x >> 0x01  # 右移一位
               result = str(mod) + result
        return result

#------------------------------
#-- bin2i 2进制字符串 转为正数
#------------------------------
def bin2i(bin):
    result = 0
    for s in bin:
        if s != '0' and s != '1':
            raise ValueError,'bad bin string:'+bin
        result = 2*result + int(s)
    return result

def GBK(str):
    return str.decode('utf8').encode('gbk')


def __update_names():
    root = r'D:\tdx_global'
    fname = os.path.join(root,r'T0002\hq_cache\shex.tnf')
    nn = NamesFile(fname)
    names1 = []
    for ll in file('us_names.txt').readlines():
        ll = ll.strip()
        if ll.startswith('#'): continue
        tt = ll.split('\t')
        if len(tt) >= 3:
            if tt[2].startswith('^'):
                tt[2] = tt[2][1:]
            if len(tt[2]) > 9 :
                tt[2] = tt[2][:9]
            names1.append(tt)
    names1.sort()
    #for i in names1:
        #print i[0],i[1],i[2]
    nn.update(names1)



if __name__ == '__main__':
    print 'test begin '
    import pprint
    #aa = TdxData([r'E:\cwork\guosen\T0002\export\20120529-600499.TXT',r'E:\cwork\guosen\T0002\export\20120529-399001.TXT'])
    #aa = TdxData([r'20120529-600499.TXT',r'20120529-999999.TXT'],'ZIP',r'E:\cwork\guosen\T0002\export\999999.zip')
    #data = readfbtxt(file(r'E:\cwork\guosen\T0002\export\20120529-600499.TXT').readlines(),'20120529-600499.TXT')
    #data2 = fbtxt2lc1(data)
    #data5 = lc1tolc5(data2)
    #data = readMinBin(r'E:\cwork\guosen\Vipdoc\sh\fzline\sh600000.lc5')
    #writeMinBin(data,'out.lc5')
    #data = readMinBin('out.lc5')
    #for i in data :
        #pprint.pprint(i)
    #print len(data)
    #root = r'D:\tdx_global'
    #fname = os.path.join(root,r'T0002\hq_cache\shex.tnf')
    #nn = NamesFile(fname)
    #nn.update([('999999','上证的指','SZ11'),('880011','test','TST'),('1A0001','道琼斯指数','DJIA')])
    #stkids = nn.items_index.keys()
    #stkids = filter(lambda x : x.startswith('9'),stkids)
    #stkids = ['399001','399005']
    #stkids.sort()
    #for i in stkids :
        #print i
    #nn.write('szex.tnf',stkids)
    # 直接判断分钟不就完了吗？



