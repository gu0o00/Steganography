#coding:utf-8
__author__ = 'guojian'
import wx
from StegTab1 import StegTab1
from StegTab2 import StegTab2
from StegTab3 import StegTab3
from StegTab4 import StegTab4
#from StegTab5 import StegTab5

class NotebookPanel(wx.Notebook):
    """
    构造整体标签页
    """
    def __init__(self,parent):
        wx.Notebook.__init__(self,parent,id=wx.ID_ANY,style=wx.BK_BOTTOM)

        tab1 = StegTab1(self)
        #tabOne.SetBackgroundColour("gray")
        self.AddPage(tab1,u"尾部追加")

        tab2 = StegTab2(self)
        self.AddPage(tab2,u"LSB替换")

        tab3 = StegTab3(self)
        self.AddPage(tab3,u"LSB-PM1")

        tab4 = StegTab4(self)
        self.AddPage(tab4,u"LSB水印")

        #tab5 = StegTab5(self)
        #self.AddPage(tab5,u"BPCS(位平面复杂度分割)")


class MainFrame(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,None,wx.ID_ANY,"Steganograpy",pos=(30,40),size=(700,650))
        panel = wx.Panel(self)

        notebook = NotebookPanel(panel)
        """
        定位标签页的位置，方便编程
        """
        #notebook.SetSelection(3)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook,1,wx.ALL|wx.EXPAND,5)
        panel.SetSizer(sizer)
        self.Layout()

        self.Show()

if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(None)
    app.MainLoop()