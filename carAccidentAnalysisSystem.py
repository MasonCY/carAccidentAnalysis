import wx
import wx.adv
from wx.grid import Grid
from alcoholPanelFunctions import *
import typePanelFunctions
import accidentPanelFunctions
import homePanelFunctions
class MyApp(wx.App):
    def __init__(self):
        super(MyApp, self).__init__(clearSigInt=True)
        ### loading data
        initialData()
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
        self.maxDate = getMaxDate()
        self.minDate = getMinDate()
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
        # self.startDate = wx.adv.DatePickerCtrl(parent=self, id=wx.ID_ANY,style=wx.adv.DP_DROPDOWN)
        self.startDate = wx.adv.DatePickerCtrlGeneric(parent=self, id=wx.ID_ANY,style=wx.adv.DP_DROPDOWN|wx.adv.DP_SHOWCENTURY)
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnStartDateChanged, self.startDate)
        # self.endDate = wx.adv.DatePickerCtrl(parent=self, id=wx.ID_ANY,style=wx.adv.DP_DROPDOWN)
        self.endDate = wx.adv.DatePickerCtrlGeneric(parent=self, id=wx.ID_ANY,style=wx.adv.DP_DROPDOWN|wx.adv.DP_SHOWCENTURY)
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
        self.InitForm(True,"All accidents related to the accident type between [" + self.minDate + '----'+ self.maxDate + ']' )

        self.grid_1 = Grid(self)
        self.grid_1.CreateGrid(0, 63)
        # self.grid_1.EnableEditing(False)
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
        rows = homePanelFunctions.getDataWithinPeriod(self.sDate, self.eDate)
        r = data_rows_count(rows)
        self.grid_1.AppendRows(r)
        for i in range(0, len(rows)):
            for j in range(0, 63):
                cell = rows[i]
                self.grid_1.SetCellValue(i, j, str(cell[j]))
    def refresh_data(self):
        rows = getAllData()
        r = data_rows_count(rows)
        self.grid_1.AppendRows(r)
        for i in range(0, len(rows)):
            for j in range(0, 63):
              cell = rows[i]
              self.grid_1.SetCellValue(i, j, str(cell[j]))
    def onSearch(self, event):
        errorMsg = dateCheck(self.sDate,self.eDate)
        if len(errorMsg) == 0:
            testRows = self.grid_1.GetNumberRows()
            if testRows > 0:
                self.grid_1.DeleteRows(numRows=testRows)
            if self.type.Value== '':
                self.searchDataAccordingToDate()
                return False
            rows = homePanelFunctions.getDataByAccidentType(self.type.Value, self.sDate, self.eDate)
            r = data_rows_count(rows)
            self.grid_1.AppendRows(r)

            for i in range(len(rows)):
                for j in range(0, 63):
                    cell = rows[i]
                    self.grid_1.SetCellValue(i, j, str(cell[j]))
            self.type.SetFocus()
            event.Skip()
        else:
            error = combineErrorMsgs(errorMsg)
            wx.MessageBox(error)


class AccidentPanel(mainPanel):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.InitForm(False,"The amount of accidents per hour of the day(on average) between [" + self.minDate + '----'+ self.maxDate + ']')

        img = wx.EmptyImage(1200, 500)
        img.Replace(0, 0, 0, 255, 255, 255)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))
        self.mainSizer.Add(self.imageCtrl, 0, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self)

        self.initiatePicture('1.png')
        self.Layout()

    def onSearch(self, event):
        errorMsg = dateCheck(self.sDate, self.eDate)
        if len(errorMsg) == 0:
            result = accidentPanelFunctions.getNumberOfAccidentsPerHour(self.sDate,self.eDate)
            hourDict = accidentPanelFunctions.hoursDictGenerate(24)
            rowNumbers = data_rows_count(result)
            days = daysCal(self.sDate, self.eDate) + 1
            print(days)
            for r in result:
                hourDict[r[1]] = round(r[0]/days,2)
                # dateDict[r[1]] = dateDict.get(r[1], 0) + 1
            yValues = list(hourDict.values())
            print(yValues)

            accidentPanelFunctions.plotAccident(yValues,self.sDate,self.eDate)
            self.initiatePicture('accident.png')
        else:
            error = combineErrorMsgs(errorMsg)
            wx.MessageBox(error)


class AlcoholPanel(mainPanel):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.InitForm(False,"The trends of the number of alcohol-related accidents throughout the time  between [" + self.minDate + '----'+ self.maxDate + ']')
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
        errorMsg = dateCheck(self.sDate, self.eDate)
        if len(errorMsg) == 0:
            yesDateDict = yesAcholData(self.sDate,self.eDate)
            noDateDict = noAcholData(self.sDate,self.eDate)
            dateDict = combineYesAndNoDict(yesDateDict,noDateDict)
            sortedDict = sortDateDict(dateDict)
            xValues = dayList(self.sDate,self.eDate)
            # yValues = list(sortedDict.values())
            yValues = valueDict(sortedDict)
            plotAlcohol(xValues,yValues,self.sDate,self.eDate)
            self.initiatePicture('alcohol.png')
        else:
            error = combineErrorMsgs(errorMsg)
            wx.MessageBox(error)

class TypePanel(mainPanel):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.InitForm(False,"Overall number of accidents for each accident type between [" + self.minDate + '----'+ self.maxDate + ']')
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
        result = typePanelFunctions.getAllType()
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
        errorMsg = dateCheck(self.sDate, self.eDate)
        if len(errorMsg) == 0:
            allResult = typePanelFunctions.getAllResult(self.sDate,self.eDate)
            xypList = typePanelFunctions.getXYAndXposion(allResult,self.typeDict)
            xValue = xypList[0]
            yValue = xypList[1]
            x_pos = xypList[2]
            typePanelFunctions.plotType(xValue,yValue,x_pos,self.sDate,self.eDate)
            self.initiatePicture('type.png')
        else:
            error = combineErrorMsgs(errorMsg)
            wx.MessageBox(error)

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()