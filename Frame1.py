#Boa:Frame:Frame1
#-*-encoding:utf8-*-
# Todo 增加从Sqlite3 中获取数据

import os,sys,ConfigParser
import wx
import Dialog1
import MinPanel
import YahooPanel
from tdx_tool import *

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1CT_OUT, wxID_FRAME1NOTEBOOK1, wxID_FRAME1PANEL1, 
 wxID_FRAME1PANEL2, wxID_FRAME1PANEL3, wxID_FRAME1PANEL4, 
 wxID_FRAME1SPLITTERWINDOW1, 
] = [wx.NewId() for _init_ctrls in range(8)]

[wxID_FRAME1MENU2ITEMS0, wxID_FRAME1MENU2ITEMS1, 
] = [wx.NewId() for _init_coll_menu2_Items in range(2)]

[wxID_FRAME1MENU1ITEMS0] = [wx.NewId() for _init_coll_menu1_Items in range(1)]

[wxID_FRAME1MENU3ITEMS0] = [wx.NewId() for _init_coll_menu3_Items in range(1)]

class Frame1(wx.Frame):
    def _init_coll_menu3_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAME1MENU3ITEMS0, kind=wx.ITEM_NORMAL,
              text=u'About')
        self.Bind(wx.EVT_MENU, self.OnMenu3Items0Menu,
              id=wxID_FRAME1MENU3ITEMS0)

    def _init_coll_menuBar1_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.menu1, title=u'File')
        parent.Append(menu=self.menu2, title=u'Option')
        parent.Append(menu=self.menu3, title=u'About')

    def _init_coll_menu1_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAME1MENU1ITEMS0, kind=wx.ITEM_NORMAL,
              text=u'Exit')
        self.Bind(wx.EVT_MENU, self.OnMenu1Items0Menu,
              id=wxID_FRAME1MENU1ITEMS0)

    def _init_coll_menu2_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAME1MENU2ITEMS0, kind=wx.ITEM_NORMAL,
              text=u'Set path')
        parent.Append(help='', id=wxID_FRAME1MENU2ITEMS1, kind=wx.ITEM_NORMAL,
              text=u'Console')
        self.Bind(wx.EVT_MENU, self.OnMenu2Items0Menu,
              id=wxID_FRAME1MENU2ITEMS0)
        self.Bind(wx.EVT_MENU, self.OnMenu2Items1Menu,
              id=wxID_FRAME1MENU2ITEMS1)

    def _init_coll_notebook1_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panel1, select=True,
              text=u'Gen Min Data')
        parent.AddPage(imageId=-1, page=self.panel2, select=False,
              text=u'Block')
        parent.AddPage(imageId=-1, page=self.panel3, select=False,
              text=u'Copy Lines')
        parent.AddPage(imageId=-1, page=self.panel4, select=False,
              text=u'Copy Files')

    def _init_utils(self):
        # generated method, don't edit
        self.menuBar1 = wx.MenuBar()

        self.menu1 = wx.Menu(title='')

        self.menu2 = wx.Menu(title='')

        self.menu3 = wx.Menu(title='')

        self._init_coll_menuBar1_Menus(self.menuBar1)
        self._init_coll_menu1_Items(self.menu1)
        self._init_coll_menu2_Items(self.menu2)
        self._init_coll_menu3_Items(self.menu3)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(486, 261), size=wx.Size(611, 317),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame1')
        self._init_utils()
        self.SetClientSize(wx.Size(603, 283))
        self.SetMenuBar(self.menuBar1)

        self.splitterWindow1 = wx.SplitterWindow(id=wxID_FRAME1SPLITTERWINDOW1,
              name='splitterWindow1', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(603, 283), style=wx.SP_3D)

        self.notebook1 = wx.Notebook(id=wxID_FRAME1NOTEBOOK1, name='notebook1',
              parent=self.splitterWindow1, pos=wx.Point(0, 0), size=wx.Size(603,
              214), style=0)

        self.ct_out = wx.TextCtrl(id=wxID_FRAME1CT_OUT, name=u'ct_out',
              parent=self.splitterWindow1, pos=wx.Point(0, 218),
              size=wx.Size(603, 65), style=wx.TE_AUTO_SCROLL | wx.TE_MULTILINE,
              value=u'')
        self.ct_out.SetMinSize(wx.Size(493, -1))
        self.ct_out.SetMaxSize(wx.Size(-1, 50))
        self.splitterWindow1.SplitHorizontally(self.notebook1, self.ct_out, 200)

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(595, 187),
              style=wx.DOUBLE_BORDER)
        self.panel1.SetMinSize(wx.Size(485, 193))

        self.panel2 = wx.Panel(id=wxID_FRAME1PANEL2, name='panel2',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(595, 187),
              style=wx.TAB_TRAVERSAL)

        self.panel3 = wx.Panel(id=wxID_FRAME1PANEL3, name='panel3',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(595, 187),
              style=wx.TAB_TRAVERSAL)

        self.panel4 = wx.Panel(id=wxID_FRAME1PANEL4, name='panel4',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(595, 187),
              style=wx.TAB_TRAVERSAL)

        self._init_coll_notebook1_Pages(self.notebook1)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self._User_init()

    def _User_init(self):
        #__init__(self, parent, id, pos, size, style, name)
        wx.EVT_CLOSE(self,self.OnQuit)
        self.cfg_file = os.path.join(os.path.dirname(__file__),'tdx_conf.ini')
        self.cfg = ConfigParser.ConfigParser()
        self.OfflinePath = ''
        self.ExportPath = ''
        self.OnlinePath = ''

        try :
            self.cfg.read(self.cfg_file)
            self.OfflinePath = self.cfg.get('path','Offline')
            #self.ExportPath = self.cfg.get('path','Export')
            self.OnlinePath = self.cfg.get('path','Online')            
        except :
            pass
        if self.OfflinePath  == '' or self.OnlinePath == '' :
            self.OfflinePath = os.path.dirname(__file__)
            self.OnlinePath  = os.path.dirname(__file__)
            wx.MessageBox(u'请在Option中设置路径!')
        self.OfflineTdxNames = TdxNames(self.OfflinePath) 
        self.OnlineTdxNames  = TdxNames(self.OnlinePath) 
        # ----------------------- 自定义Panel 设置-------
        self.minpanel = MinPanel.MinPanel(self.panel1,wx.ID_ANY , (0,0) , 
                                 (0,0),wx.TAB_TRAVERSAL,'',
                                 self.cfg,self.ct_out,
                                 self.OfflineTdxNames,self.OnlineTdxNames)
        self.minpanel.SetClientSize(self.panel1.GetClientSize())
        
        #self.sdkpanel = SdkPanel.SdkPanel(self.panel2,wx.ID_ANY , (0,0) , 
        #                         (0,0),wx.TAB_TRAVERSAL,'',
        #                         self.cfg,self.ct_out)
        #self.sdkpanel.SetClientSize(self.panel2.GetClientSize())        
        #self.panel1.SetBackgroundColour(wx.BLUE) 
        #self.yahoopanel = YahooPanel.YahooPanel(self.panel2,wx.ID_ANY , (0,0) , 
        #                         (0,0),wx.TAB_TRAVERSAL,'',
        #                         self.cfg,self.ct_out,
        #                         self.OfflineTdxNames,self.OnlineTdxNames)
        #self.yahoopanel.SetClientSize(self.panel2.GetClientSize())                                
        # ----------------------- -----------------------
               
       
    def OnQuit(self,event):
        #Save option before close.
        self.Before_Close()
        self.Destroy()     

    def Before_Close(self):
        if not self.cfg.has_section('hist'):
            self.cfg.add_section('hist')
        # 各字段历史存入cfg先
        try:
            self.cfg.write(open(self.cfg_file,'w'))
        except IOError,e:
            pass
        
    def OnMenu1Items0Menu(self, event):
        """退出按钮 """
        self.OnQuit(event)

    def OnMenu2Items0Menu(self, event):
        """Option 按钮 """
        dlg = Dialog1.create(self)
        dlg.ShowModal()
        dlg.Destroy()
        try :
            self.cfg.read(self.cfg_file)   ## 重读设置  
            self.OfflinePath = self.cfg.get('path','Offline')
            #self.ExportPath = self.cfg.get('path','Export')
            self.OnlinePath = self.cfg.get('path','Online')
            #self.OfflineTdx._setpath(self.OfflinePath)
            #self.OnlineTdxMin._setpath(self.OnlinePath)
        except :
            pass

    def OnMenu3Items0Menu(self, event):
        """About 按钮 """    
        wx.MessageBox("tdx tools","About")   

    def OnMenu2Items1Menu(self, event):
        """cmd.exe """
        curdir = os.getcwd()
        os.system("start cmd.exe /k python autofbnew.py --help" )
        
