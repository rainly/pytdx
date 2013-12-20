#Boa:Dialog:Dialog1
#-*-encoding:utf8-*-

import wx
import os,sys,ConfigParser

def create(parent):
    return Dialog1(parent)

[wxID_DIALOG1, wxID_DIALOG1BUTTON1, wxID_DIALOG1BUTTON2, 
 wxID_DIALOG1STATICTEXT1, wxID_DIALOG1STATICTEXT2, wxID_DIALOG1STATICTEXT3, 
 wxID_DIALOG1TEXTCTRL1, wxID_DIALOG1TEXTCTRL2, wxID_DIALOG1TEXTCTRL3, 
] = [wx.NewId() for _init_ctrls in range(9)]

class Dialog1(wx.Dialog):
    def _init_coll_gridSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticText1, 0, border=0, flag=wx.ALIGN_CENTER)
        parent.AddWindow(self.textCtrl1, 0, border=0, flag=wx.ALIGN_CENTER)
        parent.AddWindow(self.staticText3, 0, border=0, flag=wx.ALIGN_CENTER)
        parent.AddWindow(self.textCtrl3, 0, border=0, flag=wx.ALIGN_CENTER)
        parent.AddWindow(self.staticText2, 0, border=0, flag=wx.ALIGN_CENTER)
        parent.AddWindow(self.textCtrl2, 0, border=0, flag=wx.ALIGN_CENTER)
        parent.AddWindow(self.button1, 0, border=0, flag=wx.ALIGN_CENTER)
        parent.AddWindow(self.button2, 0, border=0, flag=wx.ALIGN_CENTER)

    def _init_sizers(self):
        # generated method, don't edit
        self.gridSizer1 = wx.GridSizer(cols=2, hgap=0, rows=4, vgap=0)

        self._init_coll_gridSizer1_Items(self.gridSizer1)

        self.SetSizer(self.gridSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              pos=wx.Point(511, 493), size=wx.Size(400, 250),
              style=wx.DEFAULT_DIALOG_STYLE, title='Dialog1')
        self.SetClientSize(wx.Size(392, 216))

        self.staticText1 = wx.StaticText(id=wxID_DIALOG1STATICTEXT1,
              label=u'TDX\u5b66\u4e60\u76ee\u5f55', name='staticText1',
              parent=self, pos=wx.Point(62, 20), size=wx.Size(71, 14), style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL1, name='textCtrl1',
              parent=self, pos=wx.Point(200, 16), size=wx.Size(188, 22),
              style=0, value=u'')

        self.staticText3 = wx.StaticText(id=wxID_DIALOG1STATICTEXT3,
              label=u'\u5728\u7ebf\u6570\u636e\u5206\u6790\u76ee\u5f55',
              name='staticText3', parent=self, pos=wx.Point(30, 74),
              size=wx.Size(136, 14), style=0)

        self.textCtrl3 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL3, name='textCtrl3',
              parent=self, pos=wx.Point(200, 70), size=wx.Size(188, 22),
              style=0, value=u'')
        self.textCtrl3.Bind(wx.EVT_SET_FOCUS, self.OnTextCtrl3SetFocus)

        self.button1 = wx.Button(id=wxID_DIALOG1BUTTON1, label=u'OK',
              name='button1', parent=self, pos=wx.Point(60, 177),
              size=wx.Size(75, 24), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_DIALOG1BUTTON1)

        self.button2 = wx.Button(id=wxID_DIALOG1BUTTON2, label=u'Cancel',
              name='button2', parent=self, pos=wx.Point(256, 177),
              size=wx.Size(75, 24), style=0)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button,
              id=wxID_DIALOG1BUTTON2)

        self.textCtrl2 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL2, name='textCtrl2',
              parent=self, pos=wx.Point(201, 124), size=wx.Size(186, 22),
              style=0, value=u'')

        self.staticText2 = wx.StaticText(id=wxID_DIALOG1STATICTEXT2,
              label=u'Sqlite3', name='staticText2', parent=self,
              pos=wx.Point(67, 128), size=wx.Size(62, 14), style=0)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        self._User_init()
        
    def _User_init(self):
        self.cfg_file = os.path.join(os.path.dirname(__file__),'tdx_conf.ini')
        self.cfg = ConfigParser.ConfigParser()
                
        try :
            self.cfg.read(self.cfg_file)
            self.textCtrl1.SetValue(self.cfg.get('path','Offline'))
            #self.textCtrl2.SetValue(self.cfg.get('path','Export'))
            self.textCtrl3.SetValue(self.cfg.get('path','Online'))
        except :
            pass    

    def OnButton1Button(self, event):
        #wx.MessageBox(str(wxID_DIALOG1BUTTON1))
        if not self.cfg.has_section('path'):
            self.cfg.add_section('path')
        self.cfg.set('path','Offline',self.textCtrl1.GetValue())
        #self.cfg.set('path','Export', self.textCtrl2.GetValue())
        self.cfg.set('path','Online', self.textCtrl3.GetValue())
        try:
            f = open(self.cfg_file,'w')
            self.cfg.write(f)
            f.close()
        except IOError,e:
            wx.MessageBox("can not write file " + self.cfg_file + "\n","ERROR") 
        else:
            wx.MessageBox(u"设置保存成功！重启生效！")                             
        self.Destroy()

    def OnButton2Button(self, event):
        self.Destroy()


    def OnTextCtrl3SetFocus(self, event):
        if self.textCtrl3.GetValue() == "" :
            self.textCtrl3.SetValue(self.textCtrl1.GetValue())
