import sqlite3
import json

class Database_main:
    def __init__(self):
        with sqlite3.connect('employees.sqlite') as connection:
            cursor = connection.cursor()

            # cursor.execute("""DROP TABLE IF EXISTS employees; """)

            cursor.execute( """CREATE TABLE IF NOT EXISTS employees(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            fio TEXT NOT NULL,
            position TEXT NOT NULL
            );""")
            connection.commit()

            # cursor.execute("""DROP TABLE IF EXISTS tasks; """)

            # подразумеваеся что есть 3 типа статусов задач: 'в работе', 'решено', 'специалист не назначен'.
            cursor.execute( """CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            parent_task_id INTEGER,
            specialist_id INTEGER,
            deadline TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (specialist_id)  REFERENCES employees (id) ON DELETE SET NULL
            );""")
            connection.commit()

    def read(self, table):
        with sqlite3.connect('employees.sqlite') as connection:
            cursor = connection.cursor()
            if table == 'employees':
                result = cursor.execute("""SELECT * FROM employees""")
            elif table == 'tasks':
                result = cursor.execute("""SELECT * FROM tasks""")
        return result.fetchall()


    def update(self,table, data):
        with sqlite3.connect('employees.sqlite') as connection:
            cursor = connection.cursor()
            if table == 'employees':
                # если в параметрах запроса есть ключ "id", обновляем значения в таблице
                if 'id' in data:
                    if data['field'] == 'fio':
                        cursor.execute('''UPDATE employees
                        SET fio = ?
                        WHERE id = ?''', (data['value'], data['id'] ))
                    elif data['field'] == 'position':
                        cursor.execute('''UPDATE employees
                        SET position = ?
                        WHERE id = ?''', (data['value'], data['id'] ))
                # если нет, добавляем новую строку
                else:
                    result = cursor.execute("""INSERT INTO employees(fio, position)
                    VALUES(?,?)""", (data['fio'], data['position']))

            elif table == 'tasks':
                if 'id' in data:
                    if data['field'] == 'description':
                        cursor.execute('''UPDATE tasks
                        SET description = ?
                        WHERE id = ?''', (data['value'], data['id'] ))
                    elif data['field'] == 'parent_task_id':
                        cursor.execute('''UPDATE tasks
                        SET parent_task_id = ?
                        WHERE id = ?''', (data['value'], data['id'] ))
                    elif data['field'] == 'specialist_id':
                        cursor.execute('''UPDATE tasks
                        SET specialist_id = ?
                        WHERE id = ?''', (data['value'], data['id'] ))
                    elif data['field'] == 'deadline':
                        cursor.execute('''UPDATE tasks
                        SET deadline = ?
                        WHERE id = ?''', (data['value'], data['id'] ))
                    elif data['field'] == 'status':
                        cursor.execute('''UPDATE tasks
                        SET status = ?
                        WHERE id = ?''', (data['value'], data['id'] ))
                else:
                    result = cursor.execute("""INSERT INTO tasks(description, parent_task_id, specialist_id, deadline, status)
                    VALUES(?,?,?,?,?)""", (data['description'], data['parent_task_id'], data['specialist_id'], data['deadline'], data['status']))



    def delete(self, table, id):
        with sqlite3.connect('employees.sqlite') as connection:
            cursor = connection.cursor()
            if table == "employees":
                cursor.execute("""DELETE FROM employees WHERE id = ?; """, (id,))
            elif table == "tasks":
                cursor.execute("""DELETE FROM tasks WHERE id = ?; """, (id,))


    # "Занятые сотрудники": Запрашивает из БД список сотрудников и их задачи, отсортированный по количеству активных задач.
    def busy(self):
        with sqlite3.connect('employees.sqlite') as connection:
            cursor = connection.cursor()
            result = cursor.execute("""
            SELECT employees.id, employees.fio, COUNT(x.status) as task_count FROM employees
            LEFT JOIN
            (SELECT * FROM tasks
            WHERE status != 'решено') AS x
            ON employees.id = x.specialist_id
            GROUP BY employees.fio
            ORDER BY  COUNT(x.status) DESC, employees.fio ASC""")
        return result.fetchall()

    # Задачи не взятые в работу, и от которых зависят другие задачи, взятые в работу
    def tasks_not_in_work(self):
        with sqlite3.connect('employees.sqlite') as connection:
            cursor = connection.cursor()
            result = cursor.execute("""
            SELECt * FROM tasks
            WHERE status = 'специалист не назначен'
            and id in (
            select parent_task_id FROM tasks
            where status = 'в работе')""")
        return result.fetchall()

    # наименее загруженный сотрудник
    def free_specialist(self):
        with sqlite3.connect('employees.sqlite') as connection:
            cursor = connection.cursor()
            result = cursor.execute("""
            WITH data AS
            (SELECT employees.fio, COUNT(x.status) as task_count FROM employees
            LEFT JOIN
            (SELECT * FROM tasks
            WHERE status != 'решено') AS x
            ON employees.id = x.specialist_id
            GROUP BY employees.fio
            ORDER BY  COUNT(x.status) DESC, employees.fio ASC)

            SELECT * FROM data
            WHERE task_count  =
            (SELECT MIN(task_count ) FROM data);""")
        return result.fetchall()

    # количество активных задач у сотрудника, который выполняет родительскую задачу
    def parent_task_information(self, parent_task_id):
        with sqlite3.connect('employees.sqlite') as connection:
            cursor = connection.cursor()
            result = cursor.execute("""
            WITH data as
            (Select employees.id, employees.fio, count(tasks.description) as 'Количество активных задач' FROM employees
            LEFT JOIN tasks
            ON employees.id = tasks.specialist_id
            WHERE tasks.status = 'в работе'
            GROUP BY employees.fio)

            SELECT * FROM data
            WHERE id =
            (SELECT id FROM employees
            WHERE id  =
            (SELECT specialist_id FROM tasks
            WHERE parent_task_id = ? ))""", (parent_task_id,) )
        return result.fetchall()
