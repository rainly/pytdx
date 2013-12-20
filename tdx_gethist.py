#!/usr/bin/python
#-*- encoding: gbk -*- 
# 从网站获取历史数据
from __future__ import division
import struct   
import os,time ,datetime,string,sys,math,re,shutil,glob
from tdx_utils import *
import ctypes as ct
import urllib
import ystockquote
    

def rawlines2data(lines,skip=1,fuquan = False):
    """data 是按照writeDayBin的格式 """
    #Date,Open,High,Low,Close,Volume,Adj Close
    data = []
    vol_max = None
    for i,line in enumerate(lines):
        if i < skip : continue
        line = line.strip()
        tt = line.split(',')
        p = {M_DT : datetime.datetime.strptime(tt[0],'%Y-%m-%d').date() ,
             M_OPEN : float(tt[1]) , 
             M_HIGH : float(tt[2]),
             M_LOW : float(tt[3]),
             M_CLOSE : float(tt[4]),
             M_AMT : 0,
             M_VOL : float(tt[5]),
             'adjc': float(tt[6])  
        }
        if vol_max == None :
            vol_max = p[M_VOL]
        elif p[M_VOL] > vol_max :
            vol_max = p[M_VOL]
        if fuquan and p[M_CLOSE] != 0 and p['adjc'] != p[M_CLOSE]:
            p[M_OPEN] = p['adjc'] * p[M_OPEN] / p[M_CLOSE] 
            p[M_HIGH] = p['adjc'] * p[M_HIGH] / p[M_CLOSE] 
            p[M_LOW] = p['adjc'] * p[M_LOW] / p[M_CLOSE] 
            p[M_CLOSE] = p['adjc']
        data.append(p)
    # endfor
    # 对成交量进行修正
    div = 1
    while vol_max > 0xffffffff:
        #print 'vol_max = %s to big!' % vol_max
        vol_max /= 10
        div *= 10
    if div != 1 and div != 0:
        for i,item in enumerate(data):
            data[i][M_VOL] /= div
   
    return (data,div )


def save_to_dir(symbol,cache,start_date = None,end_date=None,stat = 'a'):
    """ start_date 为空表示取cache 文件夹的日期,如果文件不存在则用'19000101'
        end_date   为空表示取当前日期
        stat = a 表示追加; w表示复写
    """
    if not os.path.isdir(cache):
        raise IOError , '%s is not a dir.' % cache

    shortname = symbol + '.txt'
    if shortname.startswith('^') : 
        shortname = shortname[1:]
    fname = os.path.join(cache,shortname)
    if stat == 'a':
        try : 
            lines = file(fname).readlines()
            line  = lines[-1].strip()
            tstr  = line.split(',')[0]
            t = datetime.datetime.strptime(tstr,'%Y-%m-%d').date()
            t = t + datetime.timedelta(days = 1)
            start_date = t.strftime('%Y%m%d')
        except IOError,e:
            pass
    if start_date == None :
        start_date = '19000101'
    if end_date == None:
        end_date = datetime.date.today().strftime('%Y%m%d')
    
    # 文件不存在用head 
    # 文件存在复写时用head
    with_head = True
    if os.path.exists(fname):
        if stat == 'a' :
            with_head = False
        else:
            with_head = True
    else:
        with_head = True
    lines = ystockquote.get_hist_lines(symbol, start_date, end_date,with_head,b_sort=True) 
    f = open(fname,stat)
    f.writelines(lines)
    f.close()
    return (len(lines),start_date,end_date)


def myFormat(dd):
    """strftime当年度<1900时出错 """
    return'%04d-%02d-%02d' % (dd.year,dd.month,dd.day)


def manydowns(symbols,p_dir):
    """symbols [symbol,] """
    logh = open('histlog.txt','a')
    for i in symbols :
        print 'will down ',i
        ret = save_to_dir(i,p_dir)
        if ret[0] == 0 :
            msg = '%s\t Fail\n' % i
        else:
            msg = '%s\t OK\t%s\t%s\n' % (i,ret[1],ret[2])
        logh.write(msg)
        logh.flush()
    # endfor
    logh.close()    

def manywrite(idsym,globpat,to_dir,fuquan):
    """idsym [(id,symbol),]"""
    symdict = {}
    for i in idsym:
        if symdict.has_key(i[1]):
            print 'symbol %s double!!' % i[1]
            continue
        symdict[i[1]] = i[0]
    for fname in glob.glob(globpat):
        s = os.path.splitext(os.path.basename(fname))[0]
        stkid = symdict.get(s,'')
        if stkid == '' :
            stkid = symdict.get('^' + s,'')
        print fname , '*****' ,s, '****', stkid
        if stkid == '':
            print s,' please specify ID!'
            continue
        to_file = os.path.join(to_dir,stkid+'.day')
        data,div = rawlines2data(file(fname).readlines(),skip=1,fuquan=fuquan)
        writeDayBin(data,to_file)




if __name__ == '__main__':
    import pprint    
    #lines = file('DJI.txt').readlines()
    #data,div = rawlines2data(lines)
    #sys.stderr.write(str(div))
    #data.sort(key = lambda x:x[M_DT])
    #print 'Date,Open,High,Low,Close,Volume,Adj Close'
    #for i in data:
        #print  "%s,%s,%s,%s,%s,%s,%s"  % \
                #(myFormat(i[M_DT]) , i[M_OPEN] ,i[M_HIGH] ,i[M_LOW] ,i[M_CLOSE] ,i[M_VOL] ,i['adjc'])
    #lines = file('us_america.txt').readlines()
    #symbols = []
    #for ll in lines:
        #if ll.startswith('#'):
            #continue
        #tt = ll.strip().split('\t')
        #if len(tt) <3 : 
            #continue
        #symbols.append(tt[1])
    ## endfor
    symbols = ['^GSPC','MSFT','GOOG']
    #manydowns(symbols,r'E:\cwork\python\pytdx_new\cache')
    idsym = [('SH710001','MSFT'),
            ('SH710002','GOOG'),
            ('SH710003','GSPC')
            ]
    globpat = r'E:\cwork\python\pytdx_new\cache\MSFT.txt'
    to_dir   = r'E:\cwork\python\pytdx_new\cache'
    manywrite(idsym,globpat,to_dir,True)
    data = readDayBin(os.path.join(to_dir,'SH710001.day'))
    #for i in data:
        #print i[M_DT],i[M_OPEN],i[M_HIGH],i[M_LOW],i[M_CLOSE]



