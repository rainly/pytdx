#!/usr/bin/python
#-*- encoding: gbk -*- 
import ctypes
import win32gui
import win32con
import macro,SendKeys
import os,time,re,sys,glob
import zipfile,datetime
import getopt,ConfigParser


#############################################################
# zipfiles 将export下的文件压缩为 zip文件
# 
#############################################################
def zipfiles(exp_dir , deltxt = False):
    txtfiles = glob.glob(os.path.join(exp_dir,'*-*.TXT'))
    stkids = set(map(lambda x:os.path.splitext(os.path.split(x)[1])[0].split('-')[1],txtfiles))
    stkids = list(stkids)
    stkids.sort()
    #stkids = ['000002','000099']
    for i in stkids:
        print 'build '+i+'.zip,please wait......'
        fout = os.path.join(exp_dir,i+'.zip')
        #zipfile 的bug:文件不存在时，a 去追加时，报错！
        if os.path.exists(fout):
            fzip  = zipfile.ZipFile(fout,'a' ,zipfile.ZIP_DEFLATED)
        else:
            fzip  = zipfile.ZipFile(fout,'w' ,zipfile.ZIP_DEFLATED)
        zipednames = fzip.namelist()
        zipedFiles = {}
        for ff in zipednames:
            zipedFiles[ff] = 1
        thisfiles = filter(lambda x: '-'+i+'.TXT' in x,txtfiles)
        thisfiles.sort()
        b_succ = True
        try :
            for j in thisfiles:
                shortname = os.path.split(j)[1]
                #if shortname in zipednames:
                if zipedFiles.has_key(shortname):
                    print '\t',shortname,'had ziped,pass'
                else:
                    fzip.write(j,shortname)
            fzip.close()
        except IOError:
            b_succ = False

        if deltxt and b_succ:
            for j in thisfiles:
                    try :
                        os.unlink(j)
                    except IOError :
                        pass

############################################################
#获取当前窗口Title
############################################################
def GetForegroundWindowName():
    hwnd = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(hwnd)

def get_zipedFileList(zipname):
    try :
        fzip = zipfile.ZipFile(zipname)
    except IOError,e:
        return []
    else:
        return fzip.namelist()

def get_lastDayCan():
    """获取最后一个可下载日期 """
    today = datetime.date.today()
    wkd = today.weekday()
    if wkd == 5 : # 周六
        return today - datetime.timedelta(days=2)
    elif wkd == 6 : # 周日
        return today - datetime.timedelta(days=3)
    elif wkd == 0 : # 周一
        return today - datetime.timedelta(days=3)
    else:
        return today - datetime.timedelta(days=1)

def tdx_sendkeys(exp_dir,loghandle = sys.stderr,conf = None,lastday = None):
    """tdx send keys to download text files"""
    
    #                    名称     代码           年       月       日
    pymd = re.compile(r'^(.*)\((\d{3,9})\)\s+(\d{4})年(\d{2})月(\d{2})日')
    ## 默认的配置
    max_try = 3
    max_waitsecs = 10
    pos_caozuo = (457, 454)
    pos_daochu = (474, 618)    
    if lastday == None:
        lastday = get_lastDayCan()
    lastday_str = lastday.strftime('%Y%m%d')
    if conf != None:
        try :
            cfg = ConfigParser.ConfigParser()
            cfg.read(conf)
            max_try = int(cfg.get('sendkey','max_try'))
            max_waitsecs = int(cfg.get('sendkey','max_waitsecs'))
            pos_caozuo = eval(cfg.get('sendkey','pos_caozuo'))
            pos_daochu = eval(cfg.get('sendkey','pos_daochu'))
        except :
            pass

    l_try = 0
    zipedFiles = {}
    b_has_entered = False
    if not os.path.isdir(exp_dir):
        sys.stderr.write('%s is not a dir\n ' % exp_dir)
        return

    while 1:
        title = GetForegroundWindowName()
        mm = pymd.search(title)
        if mm == None :
            print title
            zipedFiles = {}
            l_try = 0
            if b_has_entered : break
            time.sleep(1)
        else: # 开始按键
            ##
            b_has_entered = True
            name1,stkid,stky,stkm,stkd=mm.groups()
            date_str = "%s%s%s" % (stky,stkm,stkd)
            if date_str > lastday_str:
                print '到指定日或最后一日了'
                return
            #20050523-999999.TXT
            ftxt = stky+stkm+stkd+'-'+stkid+'.TXT'
            longtxt = os.path.join(exp_dir,ftxt)
            if os.path.exists(longtxt):
               SendKeys.SendKeys("{PGDN}",0.8)  #pagedown 换到下一日 
               continue
            if len(zipedFiles) == 0:  ## 建立已有文件的ziplist
                zipname = os.path.join(exp_dir,stkid+'.zip')       
                for ff in get_zipedFileList(zipname):
                    zipedFiles[ff] = 1
            if zipedFiles.has_key(ftxt):
               SendKeys.SendKeys("{PGDN}",0.8)  #pagedown 换到下一日 
               continue
            ## 否则正式下载文件
            macro.move(pos_caozuo[0], pos_caozuo[1])         #移动到操作处           
            time.sleep(0.4)
            macro.click()                #单击打开菜单
            time.sleep(0.4)
            macro.move(pos_daochu[0], pos_daochu[1])         #移动到导出数据处
            time.sleep(0.3)
            SendKeys.SendKeys("{ENTER}") #回车 弹出导出对话框
            SendKeys.SendKeys("{ENTER}") #回车 开始导出        
            l_j = 0
            while l_j  < max_waitsecs * 10 :
                time.sleep(0.2)
                if os.path.exists(os.path.join(exp_dir,ftxt)) : break 
                l_j += 1
                if l_j % 10 == 0 and  l_j / 10.0 >=3 : print '\t',l_j / 10.0
            SendKeys.SendKeys("{ESC}",0.4)   #esc
            
            if os.path.exists(longtxt): # 下载成功
                SendKeys.SendKeys("{PGDN}",0.8)  #pagedown 换到下一日
                l_try = 0 #归0！
                #icnt +=1
            else:
                l_try += 1
                if l_try < max_try:
                    sys.stderr.write("尝试第 %d 次\n" % (l_try + 1 ))            
                else:
                    SendKeys.SendKeys("{PGDN}",0.4)   #pagedown 换到下一日
                    l_try = 0 #归0！
                    msg = "Fail: %s at %s%s%s can not download\n" % (stkid,stky,stkm,stkd)
                    loghandle.write(msg)
                    loghandle.flush()
                    if loghandle != sys.stderr:
                        sys.stderr.write(msg)

#############################################################
# usage 使用说明
# exec("1.12/12") exec 执行
#############################################################

def usage(p):
    print r"""
python %s
-z --zip        压缩text to zip
-d --deltxt     压缩后并删除
-r --root=RootDIR          设置root，默认为d:\new_gxzq_v6
-l --logfile=logfile       设置log文件
-c --configfile=configfile 设置按键的配置文件
-e --endday=YYYYmmdd       设置按键的最后截止日
    """ % p


if __name__ == '__main__':
    argv = sys.argv[1:]
    root = r'd:\new_gxzq_v6'  # default root
    try:
        loghandle = open('autolog.txt','a')
    except IOError:
        loghandle = sys.stderr

    conf = "tdx_conf.ini"
    endday = get_lastDayCan()
    try : 
        opts, args = getopt.getopt(argv, "hzdr:l:c:e:", ["help", "zip","deltxt","root=","logfile=","configfile=","endday="])
    except getopt.GetoptError:
        usage(sys.argv[0])
        sys.exit(0)    
    
    for opt, arg in opts:
        if opt in ('-r','--root'):
            root = arg
        elif opt in ('-l','--logfile'):
            try :
                loghandle = open(arg,'a')
            except IOError,e:
                pass
        elif opt in ('-c','--configfile'):
            conf = arg
        elif opt in ('-e','--endday'):
            try:
                endday = datetime.datetime.strptime(arg,"%Y%m%d").date()
            except :
                pass

    exp_dir = os.path.join(root,r'T0002\export')
    for opt, arg in opts:                
        if opt in ("-h", "--help"): 
            usage(sys.argv[0])
            sys.exit(0)
        elif opt in ('-z',"--zip"):
            # only 压缩
            zipfiles(exp_dir, False)
            sys.exit(0)
        elif opt in ('-d',"--deltxt"):
            # 压缩 删除
            zipfiles(exp_dir, True)
            sys.exit(0)
    try:
        if loghandle != sys.stderr:
            loghandle.write("=====================%s=====================\n" % str(datetime.datetime.now()))
        tdx_sendkeys(exp_dir,loghandle,conf,endday)
    except KeyboardInterrupt:
        print 'Stop by User. Now zip the text:'
        zipfiles(exp_dir, True)
        print '=' * 72
    finally :
        if loghandle != sys.stderr and not loghandle.closed:
            loghandle.close()



