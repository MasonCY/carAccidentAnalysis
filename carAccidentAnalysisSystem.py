import wx
import wx.adv
from numpy import arange, sin, pi
from datetime import datetime
import matplotlib.pyplot as plt
from wx.grid import Grid
import sqlite3

"""
#calculate the differences between two days
"""
def daysCal(sDate,eDate):
    date_format = "%Y/%m/%d"
    a = datetime.strptime(sDate, date_format)
    b = datetime.strptime(eDate, date_format)
    delta = b - a
    return delta.days
"""connect to the server """
def connect():
    cnn = sqlite3.connect("carCrash.sqlite")

    return cnn

""" get the column name in the table"""
def getColNameList():
    cnn = connect()
    cur = cnn.cursor()
    cur.execute("SELECT * FROM crash")
    names = [description[0] for description in cur.description]
    return names
"""calculate the total number of records"""
def data_rows_count(rows):
       i=0
       for r in rows:
           i+=1
       return i
class MyApp(wx.App):
    def __init__(self):
        super(MyApp, self).__init__(clearSigInt=True)
        self.InitFrame()
    def InitFrame(self):
        frame = MyFrame(parent=None,title="Car accident data analysis system",pos=(20,40),size=(1240,700),)
        frame.setFrame(frame)
class MyFrame(wx.Frame):
    def __init__(self,parent, title, pos,size):
        super().__init__(parent = parent, title=title,pos=pos,size=size)
        self.OnInit()
    def setFrame(self,frame):
        self.frame = frame

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
        self.sDate = datetime.today().strftime('%Y/%m/%d')
        self.eDate = datetime.today().strftime('%Y/%m/%d')
        self.imageCtrl = None

    def initiatePicture(self, imgName):
        image_name = imgName
        img = wx.Image(image_name, wx.BITMAP_TYPE_PNG)
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.imageCtrl.Refresh()
        self.Refresh()
    def OnStartDateChanged(self, evt):
        sel_date = evt.GetDate()
        self.sDate = sel_date.Format("%Y/%m/%d")

    def OnEndDateChanged(self, evt):
        sel_date = evt.GetDate()
        self.eDate = sel_date.Format("%Y/%m/%d")
        print(self.eDate)
    def onSearch(self, event):
        self.dbSelect()
        print(self.sDate, self.eDate)
    def InitForm(self,hasType,titleT):
        title = wx.StaticText(parent=self, id=wx.ID_ANY, label=titleT)
        startLable = wx.StaticText(parent=self, id=wx.ID_ANY, label="start date: ")
        endLable = wx.StaticText(parent=self, id=wx.ID_ANY, label="end date: ")
        self.startDate = wx.adv.DatePickerCtrl(parent=self, id=wx.ID_ANY)
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnStartDateChanged, self.startDate)
        self.endDate = wx.adv.DatePickerCtrl(parent=self, id=wx.ID_ANY)
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

        self.grid_1 = Grid(self)
        self.grid_1.CreateGrid(0, 65)
        self.grid_1.EnableEditing(False)
        nameList = getColNameList()
        i = 0
        for name in nameList:
            self.grid_1.SetColLabelValue(i, name)
            self.grid_1.SetColSize(i, 150)
            i+=1

        self.mainSizer.Add(self.grid_1,proportion=0, flag=wx.ALL, border=2)
        self.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self)
        self.Layout()
        self.refresh_data()
    def searchDataAccordingToDate(self):
        cnn = connect()
        cur = cnn.cursor()
        cur.execute("SELECT * FROM crash where accident_date between ? and ?",(self.sDate,self.eDate))

        rows = cur.fetchall()
        r = data_rows_count(rows)
        self.grid_1.AppendRows(r)

        for i in range(0, len(rows)):

            for j in range(0, 63):
                cell = rows[i]
                self.grid_1.SetCellValue(i, j, str(cell[j]))

    def refresh_data(self):
        cnn = connect()
        cur = cnn.cursor()
        cur.execute("SELECT * FROM crash")

        rows = cur.fetchall()
        r = data_rows_count(rows)
        self.grid_1.AppendRows(r)

        for i in range(0, len(rows)):

            for j in range(0, 63):
              cell = rows[i]
              self.grid_1.SetCellValue(i, j, str(cell[j]))
    def draw(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        plt.plot(t, s)
        plt.ylabel('co2')
        plt.xlabel('year')

    def onSearch(self, event):
        testRows = self.grid_1.GetNumberRows()
        if testRows > 0:
            self.grid_1.DeleteRows(numRows=testRows)
        if self.type.Value== '':
            self.searchDataAccordingToDate()
            return False
        cnn = connect()
        cursor = cnn.cursor()
        cursor.execute("SELECT * FROM crash WHERE ACCIDENT_TYPE LIKE '%"
                       + self.type.Value + "%' and ACCIDENT_DATE >=" + "'" + self.sDate + "' and ACCIDENT_DATE <=" + "'" + self.eDate + "'" )

        rows = cursor.fetchall()
        r = data_rows_count(rows)
        self.grid_1.AppendRows(r)

        for i in range(len(rows)):
            for j in range(0, 63):
                cell = rows[i]
                self.grid_1.SetCellValue(i, j, str(cell[j]))
        cnn.close()
        self.type.SetFocus()
        event.Skip()

class AccidentPanel(mainPanel):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.InitForm(False,"The amount of accidents per hour of the day(on average)")

        img = wx.EmptyImage(1200, 500)
        img.Replace(0, 0, 0, 255, 255, 255)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))
        self.mainSizer.Add(self.imageCtrl, 0, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self)

        self.initiatePicture('1.png')
        self.Layout()

    def onSearch(self, event):
        connection = connect()
        cursor = connection.cursor()
        dateDict = {'00':0,'01':0,'02':0,'03':0,
                    '04':0,'05':0,'06':0,'07':0,
                    '08':0,'09':0,'10':0,'11':0,
                    '12':0,'13':0,'14':0,'15':0,
                    '16':0,'17':0,'18':0,'19':0,
                    '20':0,'21':0,'22':0,'23':0}
        cursor.execute("SELECT count(*) as numberOfAccidents, hour FROM crash where accident_date between ? and ? group by hour",(self.sDate,self.eDate))
        result = cursor.fetchall()
        rowNumbers = data_rows_count(result)
        print(rowNumbers)
        x_pos = []
        y_pos = []
        a = 1
        b = 2
        for i in range(12):

            x_pos.append(a)
            a += 4
            y_pos.append(b)
            b += 4


        days=daysCal(self.sDate,self.eDate) + 1
        print(days)
        for r in result:
            dateDict[r[1]] = round(r[0]/days,2)
            # dateDict[r[1]] = dateDict.get(r[1], 0) + 1
        connection.close()
        yVlues = list(dateDict.values())
        amValues = yVlues[0:12]
        pmValues = yVlues[12:25]

        xVlues = ['0-1', '1-2','2-3','3-4',
                  '4-5','5-6','6-7', '7-8',
                  '8-9','9-10', '10-11','11-12'
                  ]
        plt.figure(figsize=(20,6))
        plt.bar(x_pos,height=amValues,color='green',width=2,label='am')
        plt.bar(y_pos,height=pmValues,color='yellow',width=2,label='pm')

        plt.xticks(x_pos,xVlues)
        plt.legend()
        plt.xlabel("Hours-AM/PM [" + self.sDate +'-----'+ self.eDate+']')
        plt.ylabel("Average accident data")

        figure = plt.gcf()
        figure.set_size_inches(12, 5)

        plt.savefig('accident.png', dpi=100)
        self.initiatePicture('accident.png')

class AlcoholPanel(mainPanel):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.InitForm(False,"The trends of the number of alcohol-related accidents throughout the time ")
        img = wx.EmptyImage(1200,500)
        img.Replace(0, 0, 0, 255, 255, 255)
        self.imageCtrl = wx.StaticBitmap(self,wx.ID_ANY,wx.BitmapFromImage(img))
        self.mainSizer.Add(self.imageCtrl,0,wx.LEFT | wx.TOP | wx.GROW)

        self.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self)
        self.initiatePicture('2.png')
        self.Layout()
    ###search for alcoholtime == Yes group by accident_date store it in the datedict
    ###search for alcoholtime == No group by accident_date store it in noDatedict
    ###check if key in date dict or not merger these two dicts
    ###sort dict by keys
    def onSearch(self, event):
        connection = connect()
        cursor = connection.cursor()
        dateDict = dict()
        cursor.execute(
            " select accident_date,count(*) from crash  where alcoholtime='Yes' and accident_date between ? and ? group by accident_date",
            (self.sDate, self.eDate))
        yesResult = cursor.fetchall()
        if self.eDate > '2019/03/21':
            days = daysCal(self.sDate,'2019/03/21')
        else:
            days = daysCal(self.sDate, self.eDate)
        dList=[]
        a = 1
        for i in range(1,days+2):
            dList.append(a)
            a = a +1
        for r in yesResult:
            dateDict[r[0]] = r[1]
        cursor.execute(
            " select accident_date  from crash  where alcoholtime='No' and accident_date between ? and ? group by accident_date",
            (self.sDate, self.eDate))
        noResult = cursor.fetchall()
        noAchDateDict = dict()
        for r in noResult:
            noAchDateDict[r[0]] = 0

        print(noAchDateDict)
        for key in noAchDateDict.keys():
            if key not in dateDict.keys():
                dateDict[key] = 0

        sortedDict = dict()
        for key in sorted(dateDict.keys()):
            sortedDict[key] = dateDict[key]



        connection.close()

        xValues = dList
        print(xValues)
        yValues = list(sortedDict.values())
        plt.figure(figsize=(20, 6))
        plt.plot(xValues, yValues)
        plt.plot(xValues, yValues,'yo')
        plt.xticks(xValues,xValues)
        plt.xlabel("alcohol related accident [" + self.sDate + '-----' + self.eDate + ']')
        figure = plt.gcf()
        figure.set_size_inches(12, 5)

        plt.savefig('alcohol.png',dpi=100)
        self.initiatePicture('alcohol.png')

class TypePanel(mainPanel):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.InitForm(False,"Overall number of accidents for each accident type")
        img = wx.EmptyImage(940, 500)
        img.Replace(0, 0, 0, 255, 255, 255)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))

        self.imageSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.imageSizer.Add(self.imageCtrl)
        self.grid_1 = Grid(self)
        self.grid_1.CreateGrid(0, 2)
        self.grid_1.EnableEditing(False)
        self.grid_1.SetColLabelValue(0, 'Type_ID')
        self.grid_1.SetColSize(0, 50)
        self.grid_1.SetColLabelValue(1, 'Accident Type')
        self.grid_1.SetColSize(1, 220)
        self.grid_1.SetInitialSize((500,500))
        self.grid_1.HideRowLabels()
        self.drawTable()

        self.imageSizer.Add(self.grid_1)
        self.mainSizer.Add(self.imageSizer, 0, wx.LEFT | wx.TOP | wx.GROW)

        self.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self)
        self.initiatePicture('3.png')
        self.Layout()
    def drawTable(self):
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("select accident_type from crash group by accident_type")
        result = cursor.fetchall()
        typeID = 1
        self.typeDict = dict()
        for r in result:
            self.typeDict[r[0]] = typeID
            typeID += 1
        r = data_rows_count(result)
        self.grid_1.AppendRows(r)

        for i in range(0, r):
            cell = result[i]
            a = i+1
            self.grid_1.SetCellValue(i, 0, str(a))
            self.grid_1.SetCellValue(i, 1, str(cell[0]))
    def onSearch(self, event):

        connection = connect()
        cursor = connection.cursor()
        cursor.execute(
            " select accident_type,count(*) from crash  where accident_date between ? and ? group by accident_type",
            (self.sDate, self.eDate))

        allResult = cursor.fetchall()
        xValue = []
        yValue = []

        a = 1
        x_pos = []
        for r in allResult:
            xValue.append(self.typeDict[r[0]])
            yValue.append(r[1])
            x_pos.append(a)
            a += 4

        plt.figure(figsize=(20, 6))
        plt.bar(x_pos, height=yValue, color='green', width=2, label='accident type')
        plt.xticks(x_pos, xValue)
        plt.legend()
        plt.xlabel("Accident type ID [" + self.sDate + '-----' + self.eDate + ']')
        plt.ylabel("number of accidents")

        figure = plt.gcf()
        figure.set_size_inches(9.4, 5)

        plt.savefig('type.png', dpi=100)

        self.initiatePicture('type.png')
if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()