from ast import Try
import mysql.connector
import constant

class Repository:

    def executeQuery(self , query, data = None):
        isConnectionDB1 = False
        isConnectionDB2 = False
        cursor1 = None
        cursor2 = None
        mydb = None
        mydb2 = None

        try:
            mydb = mysql.connector.connect(
                host= constant.HOST_DB1,
                user=constant.USER_DB,
                password=constant.PASSWORD_DB,
                database=constant.DB1_NAME
            )
            cursor1 = mydb.cursor()
            isConnectionDB1 = True
        except:
            print("couldn't connect to DB1")

        try:
            mydb2 = mysql.connector.connect(
                host= constant.HOST_DB2,
                user=constant.USER_DB,
                password=constant.PASSWORD_DB,
                database=constant.DB2_NAME
            )
            cursor2 = mydb2.cursor()
            isConnectionDB2 = True
        except:
            print("couldn't connect to DB1")

        if isConnectionDB1:
            cursor1.execute(query, data)
            mydb.commit()
            cursor1.close() 
            mydb.close()
        
        if isConnectionDB2:
            cursor2.execute(query, data)
            mydb2.commit()
            cursor2.close() 
            mydb2.close()

