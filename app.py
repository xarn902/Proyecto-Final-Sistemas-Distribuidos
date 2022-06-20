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
  
@app.route('/teacher/<id>', methods=['PUT'])
def update_teacher(id):
  repository = Repository()
  json_data = request.get_json(force=True)
  _name = json_data['name']
  _lastName = json_data['lastName']
  sql = "UPDATE teacher SET teacher_name = %s , teacher_last_name = %s WHERE teacher_code = %s"
  data = (_name, _lastName, id)
  repository.executeQuery(sql,data) 
  return "teacher updated successfully"

@app.route('/teacher', methods=['GET'])
def get_teacher():
  repository = Repository()
  results, row_headers= repository.executeSelectQuery("SELECT * FROM teacher") 
  print(results)
  json_data= []
  for result in results:
    print(result)
    json_data.append(dict(zip(row_headers,result)))
  return json.dumps(json_data)

@app.route('/teacher/<id>', methods=['GET'])
def find_teacher(id):
  repository = Repository()
  results, row_headers= repository.executeSelectQuery("SELECT * FROM teacher WHERE teacher_code={}".format(id)) 
  print(results)
  json_data= []
  for result in results:
    print(result)
    json_data.append(dict(zip(row_headers,result)))
  return json.dumps(json_data)

@app.route('/synchronize', methods=['GET'])
def synchronizeDB():
  repository = Repository()
  repository.synchronizeDB()
  return "Database synchronized successfully"

@app.route('/initdb')
def db_init():
  DB_Inited = InitDB()
  DB_Inited.initDB1()
  DB_Inited.initDB2()

  return 'init database'

if __name__ == "__main__":
  app.run(host ='0.0.0.0')