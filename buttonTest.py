import wx
from numpy import arange, sin, pi

import matplotlib.pyplot as plt
import webbrowser
class MyApp(wx.App):
    def __init__(self):
        super(MyApp, self).__init__(clearSigInt=True)
        self.InitFrame()
    def InitFrame(self):
        frame = MyFrame(parent=None,title="My Frame",pos=(100,100))
        frame.Show()
class MyFrame(wx.Frame):
    def __init__(self,parent, title, pos):
        super().__init__(parent = parent, title=title,pos=pos)
        self.OnInit()
    def OnInit(self):
        panel = MyPanel(parent=self)
class MyPanel(wx.Panel):
    def __init__(self,parent):
        super().__init__(parent=parent)
        welcomeText = wx.StaticText(parent=self,id=wx.ID_ANY,label="hello world")
        button = wx.Button(parent=self,label="click here", pos=(20,80))
        button.Bind(event=wx.EVT_BUTTON,handler=self.onSubmit)
    def onSubmit(self,event):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        plt.plot(t, s)
        plt.ylabel('co2')
        plt.xlabel('year')
        plt.show()
if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()