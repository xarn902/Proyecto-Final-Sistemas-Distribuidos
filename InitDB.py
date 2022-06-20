import mysql.connector
import constant

class InitDB:
  
  def initDB1(self):
    mydb = mysql.connector.connect(
      host= constant.HOST_DB1,
      user=constant.USER_DB,
      password=constant.PASSWORD_DB
    )
    cursor = mydb.cursor()

    cursor.execute(constant.QUERY_CREATE_DB1)
    cursor.close()

    mydb = mysql.connector.connect(
      host= constant.HOST_DB1,
      user=constant.USER_DB,
      password=constant.PASSWORD_DB,
      database=constant.DB1_NAME
    )
    cursor = mydb.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS teacher (teacher_code BIGINT NOT NULL ,teacher_name VARCHAR(255), teacher_last_name VARCHAR(255), PRIMARY KEY (teacher_code))")
    cursor.execute("CREATE TABLE IF NOT EXISTS student (student_code BIGINT NOT NULL ,student_name VARCHAR(255), lstudent_ast_name VARCHAR(255), PRIMARY KEY (student_code))")
    cursor.execute("CREATE TABLE IF NOT EXISTS course (course_code BIGINT NOT NULL ,course_name VARCHAR(255), PRIMARY KEY (course_code))")
    cursor.execute("CREATE TABLE IF NOT EXISTS class (class_code BIGINT NOT NULL , class_course_code BIGINT NOT NULL , class_teacher_code BIGINT NOT NULL , year VARCHAR(255) , period VARCHAR(255) , PRIMARY KEY (class_code), FOREIGN KEY (class_course_code) REFERENCES course(course_code) , FOREIGN KEY (class_teacher_code) REFERENCES teacher(teacher_code))")
    cursor.execute("CREATE TABLE IF NOT EXISTS class_stundent_note (class_code BIGINT NOT NULL , student_code BIGINT NOT NULL , note DECIMAL(1,1) ,  PRIMARY KEY (class_code,student_code), FOREIGN KEY (class_code) REFERENCES class(class_code) , FOREIGN KEY (student_code) REFERENCES student(student_code))")
    cursor.execute("CREATE TABLE IF NOT EXISTS backup (query TEXT(255), data TEXT(255))")
    mydb.commit()

    cursor.close()
    mydb.close()

  def initDB2(self):
    mydb = mysql.connector.connect(
      host= constant.HOST_DB2,
      user=constant.USER_DB,
      password=constant.PASSWORD_DB
    )
    cursor = mydb.cursor()

    cursor.execute(constant.QUERY_CREATE_DB2)
    cursor.close()

    mydb = mysql.connector.connect(
      host= constant.HOST_DB2,
      user=constant.USER_DB,
      password=constant.PASSWORD_DB,
      database=constant.DB2_NAME
    )
    cursor = mydb.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS teacher (teacher_code BIGINT NOT NULL ,teacher_name VARCHAR(255), teacher_last_name VARCHAR(255), PRIMARY KEY (teacher_code))")
    cursor.execute("CREATE TABLE IF NOT EXISTS student (student_code BIGINT NOT NULL ,student_name VARCHAR(255), lstudent_ast_name VARCHAR(255), PRIMARY KEY (student_code))")
    cursor.execute("CREATE TABLE IF NOT EXISTS course (course_code BIGINT NOT NULL ,course_name VARCHAR(255), PRIMARY KEY (course_code))")
    cursor.execute("CREATE TABLE IF NOT EXISTS class (class_code BIGINT NOT NULL , class_course_code BIGINT NOT NULL , class_teacher_code BIGINT NOT NULL , year VARCHAR(255) , period VARCHAR(255) , PRIMARY KEY (class_code), FOREIGN KEY (class_course_code) REFERENCES course(course_code) , FOREIGN KEY (class_teacher_code) REFERENCES teacher(teacher_code))")
    cursor.execute("CREATE TABLE IF NOT EXISTS class_stundent_note (class_code BIGINT NOT NULL , student_code BIGINT NOT NULL , note DECIMAL(1,1) ,  PRIMARY KEY (class_code,student_code), FOREIGN KEY (class_code) REFERENCES class(class_code) , FOREIGN KEY (student_code) REFERENCES student(student_code))")
    cursor.execute("CREATE TABLE IF NOT EXISTS backup (query TEXT(255) , data TEXT(255))")
    mydb.commit()

    cursor.close()
    mydb.close()