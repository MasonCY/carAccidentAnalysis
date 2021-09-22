import wx

import webbrowser
class MyApp(wx.App):
    def __init__(self):
        super(MyApp, self).__init__(clearSigInt=True)
        self.InitFrame()
    def InitFrame(self):
        frame = MyFrame(parent=None,title="Car accident data analysis system",pos=(20,40),size=(1240,700))
        frame.Show()
class MyFrame(wx.Frame):
    def __init__(self,parent, title, pos,size):
        super().__init__(parent = parent, title=title,pos=pos,size=size)
        self.OnInit()
    def OnInit(self):
        panel = MyPanel(parent=self)
class MyPanel(wx.Panel):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.InitForm()
    def InitForm(self):



        homeBtn = wx.Button(parent=self, label='Home')
        self.accidentBtn = wx.Button(parent=self, label='Accident')
        self.alcoholBtn = wx.Button(parent=self, label='Alcohol')
        self.typeBtn = wx.Button(parent=self, label='Type')

        title = wx.StaticText(parent=self,id=wx.ID_ANY,label="Home")
        startLable = wx.StaticText(parent=self,id=wx.ID_ANY,label="start date: ")
        # self.startDate= wx.DateTime(parent=self,id=wx.ID_ANY)
        self.startDate = wx.TextCtrl(parent=self, id=wx.ID_ANY)
        self.typeLable = wx.StaticText(parent=self, id=wx.ID_ANY, label="accident type: ")
        self.type = wx.TextCtrl(parent=self)

        self.SetBackgroundColour("#A8DADC")

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        menuSizer = wx.BoxSizer(wx.HORIZONTAL)
        menuSizer.Add(homeBtn, proportion=0, flag=wx.ALL, border=5)
        menuSizer.Add(self.accidentBtn, proportion=0, flag=wx.ALL, border=5)
        menuSizer.Add(self.alcoholBtn, proportion=0, flag=wx.ALL, border=5)
        menuSizer.Add(self.typeBtn, proportion=0, flag=wx.ALL, border=5)

        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        titleSizer.Add(title, proportion=0, flag=wx.ALL, border=5)

        firstRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        firstRowSizer.Add(startLable, proportion=0, flag=wx.ALL, border=5)
        firstRowSizer.Add(self.startDate, proportion=0, flag=wx.ALL, border=5)
        firstRowSizer.Add(self.typeLable, proportion=0, flag=wx.ALL, border=5)
        firstRowSizer.Add(self.type, proportion=0, flag=wx.ALL, border=5)

        mainSizer.Add(menuSizer, proportion=0, flag=wx.ALL, border=2)
        mainSizer.Add(titleSizer, proportion=0, flag=wx.ALL | wx.CENTER, border=2)
        mainSizer.Add(firstRowSizer, proportion=0, flag=wx.ALL, border=2)

        self.accidentBtn.SetBackgroundColour('red')
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        self.Layout()
if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()