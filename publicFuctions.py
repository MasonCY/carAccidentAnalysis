import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
errorMsg = []
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
    cnn = sqlite3.connect("carCrash.sqlite")

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
    names.pop()
    return names

"""calculate the total number of records"""
def data_rows_count(rows):
       i=0
       for r in rows:
           i+=1
       return i

