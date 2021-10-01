from publicFuctions import *
def getAllType():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("select accident_type from crash group by accident_type")
    result = cursor.fetchall()
    return result
def getAllResult(sDate,eDate):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        " select accident_type,count(*) from crash  where accident_date between ? and ? group by accident_type",
        (sDate, eDate))

    allResult = cursor.fetchall()
    return allResult

def getXYAndXposion(allResult,typeDict):
    xValue = []
    yValue = []
    a = 1
    x_pos = []
    for r in allResult:
        xValue.append(typeDict[r[0]])
        yValue.append(r[1])
        x_pos.append(a)
        a += 4
    xypList =[xValue,yValue,x_pos]
    return xypList
def plotType(xValue,yValue,x_pos,sDate,eDate):
    plt.figure(figsize=(20, 6))
    plt.bar(x_pos, height=yValue, color='green', width=2, label='accident type')
    plt.xticks(x_pos, xValue)
    plt.legend()
    plt.xlabel("Accident type ID [" + sDate + '-----' + eDate + ']')
    plt.ylabel("number of accidents")

    figure = plt.gcf()
    figure.set_size_inches(9.4, 5)

    plt.savefig('type.png', dpi=100)