#Boa:FramePanel:YahooPanel
#-*-encoding:utf8-*-

import wx
import os,sys,ConfigParser
from tdx_tool import *
from tdx_gethist import *
import ystockquote

[wxID_YAHOOPANEL, wxID_YAHOOPANELBUTTON1, wxID_YAHOOPANELCC_FUQUAN, 
 wxID_YAHOOPANELCC_REDOWN, wxID_YAHOOPANELCD_DATEFROM, 
 wxID_YAHOOPANELCD_DATETO, wxID_YAHOOPANELCR_CONV, wxID_YAHOOPANELCR_DOWN, 
 wxID_YAHOOPANELCR_RUN, wxID_YAHOOPANELCR_USAIND, wxID_YAHOOPANELCR_USAOTHER, 
 wxID_YAHOOPANELCR_USASTK, wxID_YAHOOPANELCT_STKID, wxID_YAHOOPANELCT_STKNAME, 
 wxID_YAHOOPANELCT_SYMBNAME, wxID_YAHOOPANELCT_SYMBOL, 
 wxID_YAHOOPANELSTATICBOX1, wxID_YAHOOPANELSTATICBOX2, 
 wxID_YAHOOPANELSTATICBOX3, wxID_YAHOOPANELSTATICTEXT1, 
 wxID_YAHOOPANELSTATICTEXT2, wxID_YAHOOPANELSTATICTEXT2, 
] = [wx.NewId() for _init_ctrls in range(22)]

class YahooPanel(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_YAHOOPANEL, name=u'YahooPanel',
              parent=prnt, pos=wx.Point(448, 364), size=wx.Size(547, 291),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(539, 257))

        self.staticText1 = wx.StaticText(id=wxID_YAHOOPANELSTATICTEXT1,
              label=u'symbol', name=u'staticText1', parent=self,
              pos=wx.Point(48, 8), size=wx.Size(37, 14), style=0)

        self.ct_symbol = wx.TextCtrl(id=wxID_YAHOOPANELCT_SYMBOL,
              name=u'ct_symbol', parent=self, pos=wx.Point(120, 8),
              size=wx.Size(100, 22), style=0, value=u'')
        self.ct_symbol.Bind(wx.EVT_KILL_FOCUS, self.OnCt_symbolKillFocus)

        self.ct_symbname = wx.StaticText(id=wxID_YAHOOPANELCT_SYMBNAME,
              label=u'', name=u'ct_symbname', parent=self, pos=wx.Point(272, 8),
              size=wx.Size(88, 24), style=0)

        self.StaticText2 = wx.StaticText(id=wxID_YAHOOPANELSTATICTEXT2,
              label=u'stkid', name=u'StaticText2', parent=self, pos=wx.Point(56,
              80), size=wx.Size(40, 14), style=0)

        self.ct_stkid = wx.TextCtrl(id=wxID_YAHOOPANELCT_STKID,
              name=u'ct_stkid', parent=self, pos=wx.Point(120, 80),
              size=wx.Size(100, 22), style=0, value=u'')

        self.cr_usastk = wx.RadioButton(id=wxID_YAHOOPANELCR_USASTK,
              label=u'\u7f8e\u80a1', name=u'cr_usastk', parent=self,
              pos=wx.Point(40, 128), size=wx.Size(91, 14), style=wx.RB_GROUP)
        self.cr_usastk.SetValue(True)

        self.cr_usaind = wx.RadioButton(id=wxID_YAHOOPANELCR_USAIND,
              label=u'\u7f8e\u6307', name=u'cr_usaind', parent=self,
              pos=wx.Point(40, 144), size=wx.Size(91, 14), style=0)
        self.cr_usaind.SetValue(False)

        self.cr_usaother = wx.RadioButton(id=wxID_YAHOOPANELCR_USAOTHER,
              label=u'\u5176\u4ed6', name=u'cr_usaother', parent=self,
              pos=wx.Point(40, 160), size=wx.Size(91, 14), style=0)
        self.cr_usaother.SetValue(False)

        self.cc_redown = wx.CheckBox(id=wxID_YAHOOPANELCC_REDOWN,
              label=u'\u91cd\u65b0\u4e0b\u8f7d', name=u'cc_redown', parent=self,
              pos=wx.Point(280, 160), size=wx.Size(79, 14), style=0)
        self.cc_redown.SetValue(False)

        self.button1 = wx.Button(id=wxID_YAHOOPANELBUTTON1, label=u'Run',
              name='button1', parent=self, pos=wx.Point(392, 120),
              size=wx.Size(96, 40), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_YAHOOPANELBUTTON1)

        self.cc_fuquan = wx.CheckBox(id=wxID_YAHOOPANELCC_FUQUAN,
              label=u'\u590d\u6743', name=u'cc_fuquan', parent=self,
              pos=wx.Point(280, 136), size=wx.Size(79, 16), style=0)
        self.cc_fuquan.SetValue(False)

        self.cd_datefrom = wx.DatePickerCtrl(id=wxID_YAHOOPANELCD_DATEFROM,
              name=u'cd_datefrom', parent=self, pos=wx.Point(120, 48),
              size=wx.Size(104, 22), style=wx.DP_SHOWCENTURY)

        self.cd_dateto = wx.DatePickerCtrl(id=wxID_YAHOOPANELCD_DATETO,
              name=u'cd_dateto', parent=self, pos=wx.Point(272, 48),
              size=wx.Size(104, 22), style=wx.DP_SHOWCENTURY)

        self.staticText2 = wx.StaticText(id=wxID_YAHOOPANELSTATICTEXT2,
              label=u'Date Between', name='staticText2', parent=self,
              pos=wx.Point(8, 48), size=wx.Size(80, 14), style=0)

        self.ct_stkname = wx.TextCtrl(id=wxID_YAHOOPANELCT_STKNAME,
              name=u'ct_stkname', parent=self, pos=wx.Point(272, 80),
              size=wx.Size(100, 22), style=0, value=u'')

        self.staticBox1 = wx.StaticBox(id=wxID_YAHOOPANELSTATICBOX1,
              label=u'\u7c7b\u522b', name='staticBox1', parent=self,
              pos=wx.Point(32, 104), size=wx.Size(96, 80), style=0)

        self.staticBox2 = wx.StaticBox(id=wxID_YAHOOPANELSTATICBOX2,
              label=u'\u529f\u80fd', name='staticBox2', parent=self,
              pos=wx.Point(136, 104), size=wx.Size(112, 80), style=0)

        self.staticBox3 = wx.StaticBox(id=wxID_YAHOOPANELSTATICBOX3,
              label=u'\u9009\u9879', name='staticBox3', parent=self,
              pos=wx.Point(264, 104), size=wx.Size(104, 80), style=0)

        self.cr_run = wx.RadioButton(id=wxID_YAHOOPANELCR_RUN, label=u'Run',
              name=u'cr_run', parent=self, pos=wx.Point(144, 128),
              size=wx.Size(91, 14), style=wx.RB_GROUP)
        self.cr_run.SetValue(True)

        self.cr_down = wx.RadioButton(id=wxID_YAHOOPANELCR_DOWN,
              label=u'Only down', name=u'cr_down', parent=self,
              pos=wx.Point(144, 144), size=wx.Size(91, 14), style=0)
        self.cr_down.SetValue(False)

        self.cr_conv = wx.RadioButton(id=wxID_YAHOOPANELCR_CONV,
              label=u'Only conv', name=u'cr_conv', parent=self,
              pos=wx.Point(144, 160), size=wx.Size(91, 14), style=0)
        self.cr_conv.SetValue(False)

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
        self.OfflinePath = ''  
        self.OnlinePath = ''
        self.namelist = []
        try:
            self.OnlinePath = self.cfg.get('path','Online')
            self.OfflinePath = self.cfg.get('path','Offline')
            self.namelist = self.offlineNames.get_id_like_list('SH7')
        except ConfigParser.NoSectionError ,e :
            self.puts('Please set the path')        
        self.YahooTemp = os.path.join(self.OfflinePath,'yahoo')

    def puts(self,ss):
        if self.tdxout == None:
            print str(ss)
        else:
            self.tdxout.AppendText(ss)
            self.tdxout.AppendText('\n')
            
    def befor_run(self):
        """check """
        self.symbol = self.ct_symbol.GetValue()
        if self.cr_usaind.GetValue() and not self.symbol.startswith('^'):
            self.symbol  =  '^' + self.symbol

        try:
            symbolName = ystockquote.get_name(self.symbol)
            self.ct_symbname.SetLabel(symbolName)
        except :
            pass
        if not os.path.isdir(self.YahooTemp):
            try:
                os.mkdir(self.YahooTemp)
            except IOError :
                self.puts('can not make dir %s' % self.YahooTemp)
                return False

        self.stkid = self.ct_stkid.GetValue()
        self.stkname = self.ct_stkname.GetValue()
        if self.stkid == '' :
            wx.puts('please specify the stock id')
            return False
        if self.stkname == '':
            wx.puts('please specify the stock name')
        return True
        
    def after_ct_symbol(self):
        """输入symbol 之后 """
        self.ct_symbname.SetLabel('')
        self.symbol = string.upper(self.ct_symbol.GetValue())
        tmp = self.symbol 
        if tmp.startswith('^') :
            tmp = tmp[1:]
        self.ct_symbol.SetValue(tmp)
        b_found = False
        self.stkid = ''
        self.stkname = ''
        for ii in self.namelist:
            if ii[2] == tmp:
                b_found = True
                self.stkid = ii[0]
                self.stkname = ii [1]                
                break
        if not b_found:
            if len(self.namelist) ==0 :
                self.stkid = 'SH770001'
            else:
                lastid = self.namelist[-1][0]
                self.stkid = 'SH' + str(int(lastid[2:]) +1)

        if self.stkname == '' :
            try:
                self.stkname = ystockquote.get_name(self.symbol)
            except :
                pass
        self.ct_stkid.SetValue(self.stkid)
        self.ct_stkname.SetValue(self.stkname)
        
    def download(self):
        """down load the content to the tmp file """
        # 注意是否重新下载
        datefrom = self.cd_datefrom.GetValue()
        dateto   = self.cd_dateto.GetValue()
        rawlines = ystockquote.get_hist_lines(self.symbol,datefrom.Format("%Y%m%d") ,dateto.Format("%Y%m%d"))
        txtname = os.path.join(self.YahooTemp,self.symbol)
        try:
            txtout = open(txtname,'w')
            txtout.writelines(rawlines)
            txtout.close()
        except   IOError :
                self.puts("warnning :can not write file %s " % txtname)
        fuquan = self.cc_fuquan.GetValue()
        data,div = rawlines2data(rawlines,1,fuquan)
        if div> 1 :
            self.puts('注意：本处成交量有缩小%s倍，因为大于了% ' % (div,0xffffffff))

    
    def convert(self):
        """convert the tmp file to bin """
        # 注意是否复权
        pass
        
    def OnButton1Button(self, event):
        if not self.befor_run():
            wx.MessageBox("Error , Please see the text below","ERROR")
            return 
        wx.MessageBox('Now do it')

    def OnCt_symbolKillFocus(self, event):
        self.after_ct_symbol()
