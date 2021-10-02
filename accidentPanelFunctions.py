from publicFuctions import *
def getNumberOfAccidentsPerHour(sDate,eDate):
    connection = connect()
    cursor = connection.cursor()
    # hourDict = hoursDictGenerate(24)
    cursor.execute(
        "SELECT count(*) as numberOfAccidents, hour FROM crash where accident_date between ? and ? group by hour",
        (sDate, eDate))
    result = cursor.fetchall()
    return result
def hoursDictGenerate(number):
    hoursDict={}
    for key in range(number):
        if key < 10:
            key = '0' + str(key)
        else:
            key = str(key)
        hoursDict[key] = 0
    return hoursDict
def getXYPostion():
    x_pos = []
    y_pos = []
    a = 1
    b = 2
    for i in range(12):
        x_pos.append(a)
        a += 4
        y_pos.append(b)
        b += 4
    return x_pos,y_pos
def getXvalues():
    xVlues = ['0-1', '1-2', '2-3', '3-4',
              '4-5', '5-6', '6-7', '7-8',
              '8-9', '9-10', '10-11', '11-12'
              ]
    return xVlues

def plotAccident(yValues,sDate,eDate):
    amValues = yValues[0:12]
    pmValues = yValues[12:24]
    print(amValues)
    print(pmValues)
    xVlues = getXvalues()
    x_pos,y_pos = getXYPostion()

    days = daysCal(sDate, eDate) + 1
    plt.figure(figsize=(20, 6))
    plt.bar(x_pos, height=amValues, color='green', width=2, label='am')
    plt.bar(y_pos, height=pmValues, color='yellow', width=2, label='pm')

    plt.xticks(x_pos, xVlues)
    plt.legend()
    plt.xlabel("Hours-AM/PM [" + sDate + '-----' + eDate + ']' + '     Total days:' + str(days))
    plt.ylabel("Average accident data")

    figure = plt.gcf()
    figure.set_size_inches(12, 5)

    plt.savefig('accident.png', dpi=100)