import json
from InitDB import InitDB
from Repository import Repository
from flask import Flask , request

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, Docker!'

@app.route('/teacher', methods=['POST'])
def add_teacher():
  repository = Repository()
  json_data = request.get_json(force=True)
  _code = json_data['code']
  _name = json_data['name']
  _lastName = json_data['lastName']
  sql = "INSERT INTO teacher (teacher_code, teacher_name, teacher_last_name)VALUES(%s, %s, %s)"
  data = (_code, _name, _lastName,)
  repository.executeQuery(sql,data) 
  return "teacher created successfully"

@app.route('/initdb')
def db_init():
  DB_Inited = InitDB()
  DB_Inited.initDB1()
  DB_Inited.initDB2()

  return 'init database'

if __name__ == "__main__":
  app.run(host ='0.0.0.0')