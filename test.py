import wx
import webbrowser
class MyApp(wx.App):
    def __init__(self):
        super(MyApp, self).__init__(clearSigInt=True)
        self.InitFrame()
    def InitFrame(self):
        frame = MyFrame(parent=None,title="My Frame",pos=(100,100))
        frame.Show()
class TabPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour('blue')
class MyFrame(wx.Frame):
    def __init__(self,parent, title, pos):
        super().__init__(parent = parent, title=title,pos=pos)
        self.OnInit()
    def OnInit(self):
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)
        tab_one = TabPanel(notebook)
        notebook.AddPage(tab_one,'Home')
        tab_two = TabPanel(notebook)
        notebook.AddPage(tab_two,'Other')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook,-1,wx.ALL|wx.EXPAND,-5)
        panel.SetSizer(sizer)
if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()