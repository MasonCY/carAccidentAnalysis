import unittest
import accidentPanelFunctions
import alcoholPanelFunctions
import publicFuctions
import homePanelFunctions
import typePanelFunctions
class carAccidentFunctionTest(unittest.TestCase):
    #################################################################
    ####### test all public functions #####################
    def test_importCsvIntoSqlite(self):
        with self.assertRaises(FileNotFoundError): publicFuctions.importCsvIntoSqlite('111')

    def test_convertDateFormat(self):
        fomatedDate = publicFuctions.convertDateFormat('1/2/2013')
        self.assertEqual(fomatedDate,'2013/02/01')
    def test_extractHour(self):
        hour = publicFuctions.extractHour('09:20:21')
        self.assertEqual(hour,'09')
    def test_getAllData(self):
        self.assertNotEqual(publicFuctions.getAllData(), [])
    def test_getMaxDate(self):
        maxDate = publicFuctions.getMaxDate()

        self.assertEqual(maxDate,'2019/03/21')
    def test_getMinDate(self):
        minDate = publicFuctions.getMinDate()
        self.assertEqual(minDate, '2013/07/01')

    def test_dasCal(self):
        days1 = publicFuctions.daysCal('2018/01/01','2018/01/05')
        self.assertEqual(days1,4)

    def test_connect(self):
        cnn = publicFuctions.connect()
        self.assertIsNotNone(cnn)

    def test_dateCheck(self):
        errorLen1 = len(publicFuctions.dateCheck('2018/01/01','2018/01/05'))
        errorLen2 = len(publicFuctions.dateCheck('2018/01/05','2018/01/01'))
        errorLen3 = len(publicFuctions.dateCheck('2013/06/29','2018/01/01'))
        errorLen4 = len(publicFuctions.dateCheck('2018/01/05','2018/01/01'))
        self.assertEqual(errorLen1,0)
        self.assertNotEqual(errorLen2,0)
        self.assertNotEqual(errorLen3,0)
        self.assertNotEqual(errorLen4,0)


        # self.assertFalse(publicFuctions.dateCheck('2018/01/05','2018/01/01'))

    def test_getColNameList(self):
        clist = publicFuctions.getColNameList()
        print(clist)
        self.assertEqual(len(clist),63)
    def test_data_rows_count(self):
        rows1 = publicFuctions.data_rows_count([1,2,3])
        rows2 = publicFuctions.data_rows_count([[1,2,3],[2,3,4]])
        self.assertEqual(rows1,3)
        self.assertEqual(rows2,2)

    #################################################################
    ####### test all homePanel functions #####################

    def test_getDataWithinPeriod(self):
        result = homePanelFunctions.getDataWithinPeriod('2018/01/01', '2018/01/05')
        self.assertNotEqual(result,[])


    def test_getDataByAccidentType(self):
        result1 = homePanelFunctions.getDataByAccidentType('Other', '2018/01/01', '2018/01/01')
        self.assertListEqual(result1,[])



  #################################################################
  ####### test all accidentPanel functions #####################
    def test_getNumberOfAccidentsPerHour(self):
        result = accidentPanelFunctions.getNumberOfAccidentsPerHour('2018/01/01','2018/01/05')
        self.assertEqual(len(result),24)
    def test_hoursDictGenerate(self):
        hourDict1 = {'00' : 0, '01' : 0}
        hourDict2 = {'00': 0, '01': 0, '02': 0}
        hourDict3 = {'00': 0, '01': 0, '02': 0, '03':0 }
        print(accidentPanelFunctions.hoursDictGenerate(24))
        self.assertDictEqual(accidentPanelFunctions.hoursDictGenerate(2),hourDict1)
        self.assertDictEqual(accidentPanelFunctions.hoursDictGenerate(3),hourDict2)
        self.assertDictEqual(accidentPanelFunctions.hoursDictGenerate(4),hourDict3)

    def test_getXYPostion(self):
        x_pos,y_pos = accidentPanelFunctions.getXYPostion()
        self.assertIsNotNone(x_pos)
        self.assertIsNotNone(y_pos)
        self.assertEqual(len(x_pos),len(y_pos))

    def test_getXvalues(self):
        xValues = accidentPanelFunctions.getXvalues()
        self.assertEqual(len(xValues),12)

    #################################################################
    ####### test all alcoholPanel functions #####################
    def test_dayList(self):
        dayList1 = alcoholPanelFunctions.dayList('2018/01/01', '2018/01/01')
        dayList2 = alcoholPanelFunctions.dayList('2018/01/01', '2018/01/02')
        dayList3 = alcoholPanelFunctions.dayList('2018/01/01', '2018/01/03')
        self.assertListEqual(dayList1, [1])
        self.assertListEqual(dayList2, [1,2])
        self.assertListEqual(dayList3, [1,2,3])


    def test_yesAcholData(self):
        yesDict = alcoholPanelFunctions.yesAcholData('2013/07/01','2013/07/01')
        self.assertDictEqual(yesDict,{'2013/07/01':16})

    def test_noAcholData(self):
        noDict = alcoholPanelFunctions.noAcholData('2019/03/17', '2019/03/20')
        self.assertDictEqual(noDict, {'2019/03/17': 0, '2019/03/18': 0,'2019/03/19': 0, '2019/03/20': 0 })

    def test_combineYesAndNoDict(self):
        yesDict = alcoholPanelFunctions.yesAcholData('2019/03/17', '2019/03/20')
        noDict = alcoholPanelFunctions.noAcholData('2019/03/17', '2019/03/20')
        combineDict = alcoholPanelFunctions.combineYesAndNoDict(yesDict,noDict)
        self.assertDictEqual(combineDict,{'2019/03/17': 0, '2019/03/18': 1,'2019/03/19': 0, '2019/03/20': 0 })

    def test_sortDateDict(self):
        originDict = {'2019/03/18':0,'2019/03/17':1}
        sortedDict = {'2019/03/17':1,'2019/03/18':0}
        self.assertDictEqual(alcoholPanelFunctions.sortDateDict(originDict),sortedDict)


    def test_valueDict(self):
        testDict = {'1':2,'2':3}
        self.assertListEqual(alcoholPanelFunctions.valueDict(testDict),[2,3])
    #################################################################
    ####### test all typePanel functions #####################

    def test_getAllType(self):
        self.assertEqual(len(typePanelFunctions.getAllType()),9)
    def test_getAllResult(self):
        self.assertTrue(typePanelFunctions.getAllResult('2019/03/17', '2019/03/20'))



if __name__ == '__main__':
    unittest.main()