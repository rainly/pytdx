#Boa:FramePanel:MinPanel
#-*-encoding:utf8-*-
# 注意self.SetPosition(wx.Point(0,0))

import wx
import os,sys,ConfigParser
from tdx_tool import *


[wxID_MINPANEL, wxID_MINPANELBUTTON1, wxID_MINPANELCC_MIN1, 
 wxID_MINPANELCC_MIN5, wxID_MINPANELCD_DATEFROM, wxID_MINPANELCD_DATETO, 
 wxID_MINPANELCT_STKID, wxID_MINPANELCT_STKNAME, wxID_MINPANELSTATICTEXT1, 
 wxID_MINPANELSTATICTEXT2, 
] = [wx.NewId() for _init_ctrls in range(10)]

class MinPanel(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_MINPANEL, name=u'MinPanel', parent=prnt,
              pos=wx.Point(457, 360), size=wx.Size(360, 215),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(352, 181))

        self.staticText1 = wx.StaticText(id=wxID_MINPANELSTATICTEXT1,
              label=u'stkid', name='staticText1', parent=self, pos=wx.Point(30,
              30), size=wx.Size(80, 14), style=0)

        self.ct_stkid = wx.TextCtrl(id=wxID_MINPANELCT_STKID, name=u'ct_stkid',
              parent=self, pos=wx.Point(128, 24), size=wx.Size(100, 22),
              style=0, value=u'SH999999')
        self.ct_stkid.Bind(wx.EVT_KILL_FOCUS, self.OnCt_stkidKillFocus)

        self.staticText2 = wx.StaticText(id=wxID_MINPANELSTATICTEXT2,
              label=u'date between', name='staticText2', parent=self,
              pos=wx.Point(32, 64), size=wx.Size(79, 14), style=0)

        self.cd_datefrom = wx.DatePickerCtrl(id=wxID_MINPANELCD_DATEFROM,
              name=u'cd_datefrom', parent=self, pos=wx.Point(128, 64),
              size=wx.Size(104, 22), style=wx.DP_SHOWCENTURY)

        self.cd_dateto = wx.DatePickerCtrl(id=wxID_MINPANELCD_DATETO,
              name=u'cd_dateto', parent=self, pos=wx.Point(240, 64),
              size=wx.Size(104, 22), style=wx.DP_SHOWCENTURY)

        self.button1 = wx.Button(id=wxID_MINPANELBUTTON1, label=u'Convert',
              name='button1', parent=self, pos=wx.Point(136, 144),
              size=wx.Size(75, 24), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_MINPANELBUTTON1)

        self.cc_min1 = wx.CheckBox(id=wxID_MINPANELCC_MIN1, label=u'min1 data',
              name=u'cc_min1', parent=self, pos=wx.Point(32, 112),
              size=wx.Size(79, 14), style=0)
        self.cc_min1.SetValue(True)

        self.cc_min5 = wx.CheckBox(id=wxID_MINPANELCC_MIN5, label=u'min5 data',
              name=u'cc_min5', parent=self, pos=wx.Point(136, 112),
              size=wx.Size(79, 14), style=0)
        self.cc_min5.SetValue(True)

        self.ct_stkname = wx.StaticText(id=wxID_MINPANELCT_STKNAME, label=u'',
              name=u'ct_stkname', parent=self, pos=wx.Point(240, 24),
              size=wx.Size(104, 24), style=0)

    def __init__(self, parent, id, pos, size, style, name,cfg,tdxout,offlineNames,onlineNames):
        self._init_ctrls(parent)
        self.cfg = cfg 
        self.tdxout = tdxout
        self.SetPosition(wx.Point(0,0))
        self.namedict = {}
        self.offlineNames = offlineNames
        self.onlineNames = onlineNames
        self._UserInit()
        
    def _UserInit(self):
        self.OnlinePath = ''
        self.OfflinePath = ''
        try:
            self.OnlinePath = self.cfg.get('path','Online')
            self.OfflinePath = self.cfg.get('path','Offline')
            self.namedict = self.offlineNames.get_id_mostuse()
        except ConfigParser.NoSectionError ,e :
            self.puts('Please set the path')
        
        self.OnlineTdxMin = TdxMin(self.OnlinePath,self.tdxout)
        self.OfflineTdx = Tdx(self.OfflinePath)  
        # 获取字段历史
        try:
            self.ct_stkid.SetValue(self.cfg.get('hist','stkid'))
            s1 = self.cfg.get('hist','datefrom')
            s2 = self.cfg.get('hist','dateto')
            dt1 = wx.DateTime()
            dt2 = wx.DateTime()
            dt1.Set(int(s1[6:8]),int(s1[4:6])-1,int(s1[0:4]))
            dt2.Set(int(s2[6:8]),int(s2[4:6])-1,int(s2[0:4]))            
            self.cd_datefrom.SetValue(dt1)
            self.cd_dateto.SetValue(dt2)      
        except :
            pass
        self.ct_stkname.SetLabel(self.namedict.get(self.ct_stkid.GetValue(),''))   
              
        
    def puts(self,ss):
        if self.tdxout == None:
            print str(ss)
        else:
            self.tdxout.AppendText(ss)
            self.tdxout.AppendText('\n')

    def convert(self):
        mktid = self.ct_stkid.GetValue()
        mkt = string.upper(mktid[0:2])
        stkid = mktid[2:]
        if mkt != 'SH' and mkt != 'SZ' :
            wx.MessageBox(u'仅支持市场代码SH SZ',"Error ")
        self.tdxout.Clear()
        if not self.cc_min1.GetValue() and not self.cc_min5.GetValue():
            wx.MessageBox(u'请至少选择min1 or min5',"Error ")
            return 
        OnlineTdxMin = self.OnlineTdxMin
        OfflineTdx   = self.OfflineTdx
        OnlineTdxMin.setID(mkt,stkid)
        date1 = self.cd_datefrom.GetValue()
        date2 = self.cd_dateto.GetValue()
        cnt = OnlineTdxMin.readFromText(dt1 = date1.Format("%Y%m%d"),dt2 = date2.Format("%Y%m%d"))
        if self.cc_min1.GetValue():
            fname = os.path.join(OfflineTdx.Min1BinPaths[OnlineTdxMin.mkt],OnlineTdxMin.mkt + OnlineTdxMin.stkid + '.lc1')
            OnlineTdxMin.writeMin1ToBin(fname)
        
        if self.cc_min5.GetValue():
            fname = os.path.join(OfflineTdx.Min5BinPaths[OnlineTdxMin.mkt],OnlineTdxMin.mkt + OnlineTdxMin.stkid + '.lc5')
            OnlineTdxMin.writeMin5ToBin(fname)
            
        #wx.MessageBox(str(cnt)+ " 天数据转换完毕！","OK")
        self.puts(str(cnt)+ u" days date convert OK!")
        self.puts("=" * 50 )  
        
        # 将字段历史存入cfg变量
        if not self.cfg.has_section('hist'):
            self.cfg.add_section('hist')   
        self.cfg.set('hist','stkid',self.ct_stkid.GetValue())
        self.cfg.set('hist','datefrom', date1.Format("%Y%m%d"))
        self.cfg.set('hist','dateto'  , date2.Format("%Y%m%d"))        

    def after_ct_stkid (self):
        stkid = self.ct_stkid.GetValue()
        if len(stkid) == 6 and not stkid.startswith('SH') and not stkid.startswith('SZ'):
                if self.namedict.has_key('SH' + stkid):
                    stkid = 'SH' + stkid
                elif self.namedict.has_key('SZ' + stkid):
                    stkid = 'SZ' + stkid
        self.ct_stkid.SetValue(stkid)
        self.ct_stkname.SetLabel(self.namedict.get(self.ct_stkid.GetValue(),''))           
    
    def OnButton1Button(self, event):
        self.convert()

    def OnCt_stkidKillFocus(self, event):
        self.after_ct_stkid()
        event.Skip()
        
        
