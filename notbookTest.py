import wx
import wx.adv
from numpy import arange, sin, pi
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.pyplot as plt

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
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)
        tab_one=HomePanel(notebook)
        notebook.AddPage(tab_one,'Home')
        tab_two=AccidentPanel(notebook)
        notebook.AddPage(tab_two,'Accident')
        tab_three = AlcoholPanel(notebook)
        notebook.AddPage(tab_three, 'Alcohol')
        tab_four = TypePanel(notebook)
        notebook.AddPage(tab_four, 'Type')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook,1,wx.ALL|wx.EXPAND,5)
        panel.SetSizer(sizer)
        self.Show()
class mainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.sDate = datetime.today().strftime('%Y-%m-%d')
        self.eDate = datetime.today().strftime('%Y-%m-%d')


    def OnStartDateChanged(self, evt):
        sel_date = evt.GetDate()
        self.sDate = sel_date.Format("%Y-%m-%d")

    def OnEndDateChanged(self, evt):
        sel_date = evt.GetDate()
        self.eDate = sel_date.Format("%Y-%m-%d")

    def onSearch(self, event):
        print(self.sDate, self.eDate)
    def InitForm(self,hasType,titleT):
        title = wx.StaticText(parent=self, id=wx.ID_ANY, label=titleT)
        startLable = wx.StaticText(parent=self, id=wx.ID_ANY, label="start date: ")
        endLable = wx.StaticText(parent=self, id=wx.ID_ANY, label="end date: ")
        self.startDate = wx.adv.DatePickerCtrlGeneric(parent=self, id=wx.ID_ANY)
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnStartDateChanged, self.startDate)
        self.endDate = wx.adv.DatePickerCtrlGeneric(parent=self, id=wx.ID_ANY)
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnEndDateChanged, self.endDate)
        self.searchBtn = wx.Button(self, label='search')
        self.searchBtn.Bind(event=wx.EVT_BUTTON, handler=self.onSearch)
        if hasType:
            self.typeLable = wx.StaticText(parent=self, id=wx.ID_ANY, label="accident type: ")
            self.type = wx.TextCtrl(parent=self)
        self.SetBackgroundColour("#A8DADC")
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        menuSizer = wx.BoxSizer(wx.HORIZONTAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        titleSizer.Add(title, proportion=0, flag=wx.ALL, border=5)

        firstRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        firstRowSizer.Add(startLable, proportion=0, flag=wx.ALL, border=5)
        firstRowSizer.Add(self.startDate, proportion=0, flag=wx.ALL, border=5)
        if hasType:
            firstRowSizer.Add(self.typeLable, proportion=0, flag=wx.ALL, border=5)
            firstRowSizer.Add(self.type, proportion=0, flag=wx.ALL, border=5)

        secondRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        secondRowSizer.Add(endLable, proportion=0, flag=wx.ALL, border=5)
        secondRowSizer.Add(self.endDate, proportion=0, flag=wx.ALL, border=5)
        secondRowSizer.Add(self.searchBtn, proportion=0, flag=wx.ALL, border=5)

        self.mainSizer.Add(menuSizer, proportion=0, flag=wx.ALL, border=2)
        self.mainSizer.Add(titleSizer, proportion=0, flag=wx.ALL | wx.CENTER, border=2)
        self.mainSizer.Add(firstRowSizer, proportion=0, flag=wx.ALL, border=2)
        self.mainSizer.Add(secondRowSizer, proportion=0, flag=wx.ALL, border=2)


class HomePanel(mainPanel):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.InitForm(True,"All accidents related to the accident type")
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self,-1,self.figure)
        self.mainSizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self)
        self.Layout()

    def draw(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        plt.plot(t, s)
        plt.ylabel('co2')
        plt.xlabel('year')
        plt.show()

    def onSearch(self, event):
        self.draw()
        print(self.sDate)
class AccidentPanel(mainPanel):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.InitForm(False,"The amount of accidents per hour of the day(on average)")

        self.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self)
        self.Layout()

    def onSearch(self, event):


        print(self.sDate)
class AlcoholPanel(mainPanel):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.InitForm(True,"The trends of the number of alcohol-related accidents throughout the time ")

        self.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self)
        self.Layout()
    def onSearch(self, event):


        print(self.sDate)
class TypePanel(mainPanel):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.InitForm(False,"Overall number of accidents for each accident type")

        self.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self)
        self.Layout()
    def onSearch(self, event):

        print(self.sDate)

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()