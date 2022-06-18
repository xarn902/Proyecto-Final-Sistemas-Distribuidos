from ast import Try
import mysql.connector
import constant
import logging


class Repository:

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    def executeQuery(self , query, data = None):
        isConnectionDB1 = False
        isConnectionDB2 = False
        cursor1 = None
        cursor2 = None
        mydb = None
        mydb2 = None
        comparationDBVersion = None

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
            logging.info("couldn't connect to DB1")

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
            logging.info("couldn't connect to DB2")

        
        if isConnectionDB1 and isConnectionDB2 :
            comparationDBVersion = self.validateDBVersion(cursor1,cursor2)
            logging.info("Validation of the dataBase Version: %s" , comparationDBVersion)

        if isConnectionDB1 and (comparationDBVersion == 0 or comparationDBVersion == 1):
            cursor1.execute(query, data)
            cursor1.execute("INSERT INTO backup (query) VALUES(%s)", (query,))
            mydb.commit()
            cursor1.close() 
            mydb.close()
        
        if isConnectionDB2 and (comparationDBVersion == 0 or comparationDBVersion == 2):
            cursor2.execute(query, data)
            cursor2.execute("INSERT INTO backup (query) VALUES(%s)", (query,))
            mydb2.commit()
            cursor2.close() 
            mydb2.close()


    def validateDBVersion(self, cursorBD1 , cursorDB2 ):

        cursorBD1.execute("SELECT COUNT(*) FROM backup")
        resultDB1 = cursorBD1.fetchone()

        logging.info("result DB 1 ")
        logging.info(resultDB1)

        cursorDB2.execute("SELECT COUNT(*) FROM backup")
        resultDB2 = cursorDB2.fetchone()

        logging.info("result DB 2 ")
        logging.info(resultDB2)

        if resultDB1[0] == resultDB2[0] :
            return 0
        elif resultDB1[0] > resultDB2[0]:
            return 1
        elif resultDB1[0] < resultDB2[0]:
            return 2

        

    def synchronizeDB(self):
        isConnectionDB1 = False
        isConnectionDB2 = False
        cursor1 = None
        cursor2 = None
        mydb = None
        mydb2 = None
        comparationDBVersion = None

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
            logging.info("couldn't connect to DB1")

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
            logging.info("couldn't connect to DB2")

        if isConnectionDB1 and isConnectionDB2 :
            comparationDBVersion = self.validateDBVersion(cursor1,cursor2)
            cursor1.execute("SELECT * FROM backup")
            resultsDB1 = cursor1.fetchall()
            cursor2.execute("SELECT * FROM backup")
            resultsDB2 = cursor2.fetchall()
            listResultStringDB1 = []
            listResultStringDB2 = []
            for result in resultsDB1:
                listResultStringDB1.append(result[0])
            for result in resultsDB2:
                listResultStringDB2.append(result[0])
            if comparationDBVersion == 1 :
                diff = list(set(listResultStringDB1) - set(listResultStringDB2))
                for sql in diff:
                    cursor2.execute(sql)
                    cursor2.execute("INSERT INTO backup (query) VALUES(%s)", (sql,))
            if comparationDBVersion == 2 :
                diff = list(set(listResultStringDB2) - set(listResultStringDB1))
                for sql in diff:
                    cursor1.execute(sql)
                    cursor1.execute("INSERT INTO backup (query) VALUES(%s)", (sql,))




        else:
            logging.info("couldn't synchronize DBs")


strinset = strinset.replace("(","")
strinset = strinset.replace(")","")
strinset = strinset.replace("'","")
stringSplited = strinset.split(",")
stringSplited = [s.strip() for s in stringSplited ]
sortedset = sorted(set(stringSplited), key=stringSplited.index)