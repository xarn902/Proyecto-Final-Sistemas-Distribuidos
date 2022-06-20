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
        comparationDBVersion = 0

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
            cursor1.execute("INSERT INTO backup (query,data) VALUES(%s,%s)", (query,str(data)))
            mydb.commit()
            cursor1.close() 
            mydb.close()
        
        if isConnectionDB2 and (comparationDBVersion == 0 or comparationDBVersion == 2):
            cursor2.execute(query, data)
            cursor2.execute("INSERT INTO backup (query,data) VALUES(%s,%s)", (query,str(data)))
            mydb2.commit()
            cursor2.close() 
            mydb2.close()

    def executeSelectQuery(self , query):
        isConnectionDB1 = False
        isConnectionDB2 = False
        cursor1 = None
        cursor2 = None
        mydb = None
        mydb2 = None
        comparationDBVersion = 0
        resultQuery = None
        resultHeaders= None

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
            cursor1.execute(query)
            resultHeaders = [x[0] for x in cursor1.description] 
            resultQuery = cursor1.fetchall()
            cursor1.close() 
            mydb.close()
        
        if isConnectionDB2 and (comparationDBVersion == 0 or comparationDBVersion == 2):
            cursor2.execute(query)
            resultHeaders = [x[0] for x in cursor2.description] 
            resultQuery = cursor2.fetchall()
            cursor2.close() 
            mydb2.close()

        return resultQuery,resultHeaders


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
            if comparationDBVersion == 1 :
                diff = resultsDB1[len(resultsDB2):]
                for sql in diff:
                    cursor2.execute(sql[0], self.stringToTuple(sql[1]))
                    cursor2.execute("INSERT INTO backup (query,data) VALUES(%s,%s)", sql)
            if comparationDBVersion == 2 :
                diff = resultsDB2[len(resultsDB1):]
                for sql in diff:
                    cursor1.execute(sql[0], self.stringToTuple(sql[1]))
                    cursor1.execute("INSERT INTO backup (query,data) VALUES(%s,%s)", sql)
            
            mydb.commit()
            cursor1.close() 
            mydb.close()
            mydb2.commit()
            cursor2.close() 
            mydb2.close()
        else:
            logging.info("couldn't synchronize DBs")

    def stringToTuple(self, stringTuple):
        stringTuple = stringTuple.replace("(","")
        stringTuple = stringTuple.replace(")","")
        stringTuple = stringTuple.replace("'","")
        stringSplited = stringTuple.split(",")
        stringSplited = [s.strip() for s in stringSplited ]
        sortedTuple = tuple(stringSplited)
        return sortedTuple

            