import sqlite3
import json
from database import Database_main
from flask import Flask, request

app = Flask(__name__)
db = Database_main()


#endpoint read
@app.route("/read/<table>", methods = ['GET'])
def read(table):
    # выводим информацию о запрашиваемой таблице
    lst=[]
    if table == 'employees':
        for i in db.read(table):
            result = {"id": i[0], "fio": i[1], "position": i[2]}
            lst.append(result)

    elif table == 'tasks':
        for i in db.read(table):
            result = {"id": i[0], "description": i[1], "parent_task_id": i[2], "specialist_id": i[3], "deadline": i[4], "status": i[5]}
            lst.append(result)

    return json.dumps(lst ,indent=4, ensure_ascii=False)

#endpoint update
@app.route("/update/<table>", methods = ['POST'])
def update(table):
    if not request.is_json:
        return {"status": "error", "message":"this not json"}
    data = json.loads(request.data)
    db.update(table, data)
    return {"status":"ok"}


#endpoint delete
@app.route("/delete/<table>/", methods = ['POST'])
def delete(table):
    if not request.is_json:
        return {"status": "error", "message":"this not json"}
    data = json.loads(request.data)
    print(data)
    db.delete(table, int(data["id"]))
    return {"status":"ok"}


#endpoint busy_employees
@app.route("/busy_employees/", methods = ['GET'])
def busy_employees():
    lst=[]
    for i in db.busy():
        result = {"id": i[0], "fio": i[1], "count_tasks": i[2]}
        lst.append(result)
    print(json.dumps(lst ,indent=4, ensure_ascii=False))
    return json.dumps(lst ,indent=4, ensure_ascii=False)


#endpoint important_tasks
@app.route("/important_tasks/", methods = ['GET'])
def important_tasks():
    # подбираем сотрудника под важные задачи
    list_of_candidants=[]
    count = 0
    count_free_specialist = len(db.free_specialist())
    for i in db.tasks_not_in_work():
        specialist_with_parent_task = db.parent_task_information(i[0])
        # исключаем перебор свободных сотрудников, если их меньше, чем нераспределённых задач
        if count < len(db.free_specialist()):
            free_specialist = db.free_specialist()[count]
        # сравниваем количество задач сотрудников с родительской задачей и с наименьшей загрузкой
        if specialist_with_parent_task[0][2] <= int(free_specialist[1]) + 2:
            list_of_candidants.append({"id_important_task":i[0], "deadline": i[4],"fio_specialist":[specialist_with_parent_task[0][1]]})
            count+=1
        else:
            list_of_candidants.append({"id_important_task":i[0], "deadline": i[4],"fio_specialist":[free_specialist[0]]})
            count+=1
    print(json.dumps(list_of_candidants ,indent=4, ensure_ascii=False))
    return json.dumps(list_of_candidants ,indent=4, ensure_ascii=False)


if __name__ == "__main__":
    app.run()
