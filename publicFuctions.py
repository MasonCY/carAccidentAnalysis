import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import csv
import os
errorMsg = []
#### file loading if database exits load directly from database,
#### other wise we have to creat the database base on the csv file
def initialData():
    if os.path.isfile('crash_car.sqlite'):
        pass
    else:
        importCsvIntoSqlite('Crash.csv')
        updateDateFormat()
        updateHour()
"""import the csv into the sqlite and add hour column"""
def importCsvIntoSqlite(filename):
    if os.path.isfile(filename) == False:
        raise FileNotFoundError('can not find the file')
    cnn = connect()
    cur = cnn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS CRASH(OBJECTID INTEGER,ACCIDENT_NO STRING,ABS_CODE STRING,
                        ACCIDENT_STATUS STRING,ACCIDENT_DATE STRING, ACCIDENT_TIME STRING,ALCOHOLTIME STRING,
                        ACCIDENT_TYPE STRING,DAY_OF_WEEK STRING, DCA_CODE STRING,HIT_RUN_FLAG STRING,
                        LIGHT_CONDITION STRING,POLICE_ATTEND STRING, ROAD_GEOMETRY STRING, SEVERITY STRING, 
                        SPEED_ZONE STRING, RUN_OFFROAD STRING,NODE_ID STRING,LONGITUDE STRING, LATITUDE STRING,
                        NODE_TYPE STRING, LGA_NAME STRING,REGION_NAME STRING, VICGRID_X STRING, VICGRID_Y STRING,
                        TOTAL_PERSONS INTEGER,INJ_OR_FATAL INTEGER,FATALITY INTEGER,  SERIOUSINJURY INTEGER,
                        OTHERINJURY INTEGER,NONINJURED INTEGER,MALES INTEGER, FEMALES INTEGER,BICYCLIST INTEGER,
                        PASSENGER INTEGER, DRIVER INTEGER, PEDESTRIAN INTEGER,PILLION INTEGER,MOTORIST INTEGER,
                        UNKNOWN INTEGER, PED_CYCLIST_5_12 INTEGER,PED_CYCLIST_13_18 INTEGER, OLD_PEDESTRIAN INTEGER,
                        OLD_DRIVER INTEGER,YOUNG_DRIVER INTEGER, ALCOHOL_RELATED STRING, UNLICENCSED INTEGER,
                        NO_OF_VEHICLES INTEGER, HEAVYVEHICLE INTEGER, PASSENGERVEHICLE INTEGER, MOTORCYCLE INTEGER,
                        PUBLICVEHICLE INTEGER, DEG_URBAN_NAME STRING, DEG_URBAN_ALL STRING,LGA_NAME_ALL STRING, 
                        REGION_NAME_ALL STRING,SRNS STRING, SRNS_ALL STRING, RMA STRING, RMA_ALL STRING, DIVIDED STRING,
                        DIVIDED_ALL STRING,STAT_DIV_NAME STRING)""")
    filename.encode('utf-8')
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader, None)
        for field in reader:
            cur.execute(
                    "INSERT INTO CRASH VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                    field)
    cur.execute("alter table crash add hour char(2);")
    cnn.commit()
    cnn.close()


""" convert date into YYYY/MM/DD from D/m/YYYY format"""
def convertDateFormat(dateString):
    day = ''
    month = ''
    year = ''
    _day=''
    _month=''
    slashTimes = 0
    for i in dateString:
        if i != '/':
            if slashTimes == 0:
                day += i
            elif slashTimes ==1:
                month +=i
            else:
                year +=i
        else:
            slashTimes += 1
    if len(day) < 2:
        _day = '0' + day
    else:
        _day = day
    if len(month) <2:
        _month = '0' + month
    else:
        _month = month
    return year + '/' + _month + '/' + _day
"""update the date in sqlite into the YYYY/MM/DD format by using convertDateFormat()"""
def updateDateFormat():
    cnn = connect()
    cur = cnn.cursor()

    # List full details of all hotels in Brisbane.
    cur.execute("SELECT accident_date FROM crash")
    print("fetchall:")
    result = cur.fetchall()
    dateList = []
    for r in result:
        date = convertDateFormat(r[0])
        dateList.append(date)
    id = 1
    for d in dateList:
        cur.execute("update crash set accident_date = ? where rowid = ?", (d, id))
        id += 1
    print('finished')
    cnn.commit()
    cnn.close()
"""extract hour from time """
def extractHour(timeString):
    hour = ''
    sTimes = 0
    for i in timeString:
        if sTimes < 2:
            hour += i
            sTimes += 1
        else:
            break
    return hour
"""update the hour column with the extracted hour from the accident_time"""
def updateHour():
    cnn = connect()
    cur = cnn.cursor()

    # List full details of all hotels in Brisbane.
    cur.execute("SELECT accident_time FROM crash order by rowid asc")
    print("fetchall:")
    result = cur.fetchall()
    dateList = []
    for r in result:
        date = extractHour(r[0])
        dateList.append(date)
    id = 1
    for d in dateList:
        cur.execute("update crash set hour = ? where rowid = ?", (d, id))
        id += 1
    cnn.commit()
    cnn.close()


"""get all data from database"""
def getAllData():
    cnn = connect()
    cur = cnn.cursor()
    cur.execute("SELECT * FROM crash")
    rows = cur.fetchall()
    return rows

def getMaxDate():
    cnn = connect()
    cur = cnn.cursor()
    cur.execute("SELECT accident_date FROM crash order by accident_date desc limit 0,1 ")
    rows = cur.fetchall()
    maxDate = rows[0][0]
    return maxDate

def getMinDate():
    cnn = connect()
    cur = cnn.cursor()
    cur.execute("SELECT accident_date FROM crash order by accident_date asc limit 0,1 ")
    rows = cur.fetchall()
    minDate = rows[0][0]
    return minDate

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
    cnn = sqlite3.connect("crash_car.sqlite")

    return cnn
"""check the start date and end date"""
def dateCheck(sDate,eDate):
    errorMsg = []
    maxDate = getMaxDate()
    minDate = getMinDate()
    if sDate > eDate:
        errorMsg.append("End date must larger than start date")
    if sDate < minDate:
        newError = 'Start date must larger than ' + minDate + '.'
        errorMsg.append(newError)
    if eDate > maxDate:
        newError = 'End date must less than ' + maxDate + '.'
        errorMsg.append(newError)
    return errorMsg
def combineErrorMsgs(errorMsg):
    error = ''
    for msg in errorMsg:
        error = error + msg + '\n'
    return error
""" get the column name in the table"""
def getColNameList():
    cnn = connect()
    cur = cnn.cursor()
    cur.execute("SELECT * FROM crash")
    names = [description[0] for description in cur.description]
    names.pop()
    return names

"""calculate the total number of records"""
def data_rows_count(rows):
       i=0
       for r in rows:
           i+=1
       return i

