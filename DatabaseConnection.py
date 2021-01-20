import pymysql

conn = pymysql.connect(host="localhost",user="root",passwd="", db="testt")
myCursor = conn.cursor()
query = "INSERT INTO `me`(name) VALUES('mohamed');"
myCursor.execute(query)
conn.commit()
conn.close()