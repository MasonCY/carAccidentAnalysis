from publicFuctions import *
def dayList(sDate,eDate):
    if eDate > '2019/03/21':
        days = daysCal(sDate, '2019/03/21')
    else:
        days = daysCal(sDate, eDate)
    dList = []
    a = 1
    for i in range(1, days + 2):
        dList.append(a)
        a = a + 1
    return dList
""" accidents related to the alcohol """
def yesAcholData(sDate,eDate):
    connection = connect()
    cursor = connection.cursor()
    dateDict = dict()
    cursor.execute(
        " select accident_date,count(*) from crash  where alcoholtime='Yes' and accident_date between ? and ? group by accident_date",
        (sDate, eDate))
    yesResult = cursor.fetchall()

    for r in yesResult:
        dateDict[r[0]] = r[1]
    return dateDict
"""accidents not related to the alcohol"""
def noAcholData(sDate,eDate):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        " select accident_date  from crash  where alcoholtime='No' and accident_date between ? and ? group by accident_date",
        (sDate, eDate))
    noResult = cursor.fetchall()
    noAchDateDict = dict()
    for r in noResult:
        noAchDateDict[r[0]] = 0
    # for key in noAchDateDict.keys():
    #     if key not in dateDict.keys():
    #         dateDict[key] = 0
    # return dateDict
    return noAchDateDict

def combineYesAndNoDict(yesDateDict,noDateDict):
    for key in noDateDict.keys():
        if key not in yesDateDict.keys():
            yesDateDict[key] = 0
    return yesDateDict

def sortDateDict(dateDict):
    sortedDict = dict()
    for key in sorted(dateDict.keys()):
        sortedDict[key] = dateDict[key]
    return sortedDict
def valueDict(dateDict):
    return list(dateDict.values())

def plotAlcohol(xValues,yValues,sDate,eDate):
    plt.figure(figsize=(20, 6))
    plt.plot(xValues, yValues)
    plt.plot(xValues, yValues, 'yo')
    plt.xticks(xValues, xValues)
    plt.xlabel("alcohol related accident [" + sDate + '-----' + eDate + ']')
    figure = plt.gcf()
    figure.set_size_inches(12, 5)
    plt.savefig('alcohol.png', dpi=100)