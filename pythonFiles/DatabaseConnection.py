import pymysql


def getResults(query):
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="ifootball")
    myCursor = conn.cursor()
    # query = "INSERT INTO `me`(name) VALUES('mohamed');"
    myCursor.execute(query)

    rows = myCursor.fetchall()
    # print(rows)
    conn.commit()
    conn.close()
    return rows

def addRow(query):
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="ifootball")
    myCursor = conn.cursor()
    myCursor.execute(query)
    # print("myCursor.lastrowid",myCursor.lastrowid)
    conn.commit()
    conn.close()
    return myCursor

def signup(query,email):
    if isEMailRepeated(email):
        return -1
    else:
        cursor = addRow(query)
        id = cursor.lastrowid if cursor.rowcount == 1 else 0
        return id



def isEMailRepeated(email):
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="ifootball")
    myCursor = conn.cursor()
    query = f"SELECT COUNT(*) From `user` WHERE `email` = '{email}'"
    myCursor.execute(query)
    result = myCursor.fetchone()
    conn.commit()
    conn.close()
    return False if result[0]==0 else True

# query = "INSERT INTO `teamperformance`(`teamId`,`totalCorrectMoves`, `totalWrongMoves`, `year`, `performancePercentage`) VALUES (1,10, 10, 2020, 50)"
# months = list(range(1, 13))
# weeks = list(range(1, 5))
# days = list(range(1, 6))
#
# from random import randint
#
# for month in months:
#     for week in weeks:
#         for day in days:
#             totalCorrectMoves = randint(0, 100)
#             totalwrongMoves = randint(0, 100)
#             total = totalCorrectMoves + totalwrongMoves
#             if (totalwrongMoves == 0):
#                 performancePercentage = 100
#             else:
#                 performancePercentage = (totalCorrectMoves * 100) / (totalwrongMoves + totalCorrectMoves)
#                 performancePercentage = round(performancePercentage, 1)
#             query = "INSERT INTO `teamperformancedetails`(`moveId`, `totalCorrectMoves`, `totalwrongMoves`, `totalDuration`, `performancePercentage`, `teamPerformanceId`) " \
#                     f"VALUES (1,{totalCorrectMoves},{totalwrongMoves},5,{performancePercentage},1)"
#             addRow(query)






# totalCorrectMoves = 23457
# totalwrongMoves = 23717
# total = totalCorrectMoves + totalwrongMoves
# performancePercentage = (totalCorrectMoves * 100) / (totalwrongMoves + totalCorrectMoves)
# print(performancePercentage)
#
# totalDuration = 1920























