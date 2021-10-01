from publicFuctions import *
def getDataWithinPeriod(sDate,eDate):
    cnn = connect()
    cur = cnn.cursor()
    cur.execute("SELECT * FROM crash where accident_date between ? and ?", (sDate, eDate))

    rows = cur.fetchall()
    return rows

def getDataByAccidentType(typeValue,sDate,eDate):
    cnn = connect()
    cur = cnn.cursor()
    # cursor.execute("SELECT * FROM crash WHERE ACCIDENT_TYPE LIKE '%"
    #                + typeValue + "%' and ACCIDENT_DATE >=" + "'" + sDate + "' and ACCIDENT_DATE <=" + "'" + eDate + "'")
    cur.execute("SELECT * FROM crash where accident_date between ? and ? and accident_type like ?", (sDate, eDate,'%'+typeValue +'%'))
    rows = cur.fetchall()
    return rows