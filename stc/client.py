import requests
import json

def table_chek():
    table_number = input("Выберите таблицу( 1 - employees, 2 - tasks): ")
    if table_number == "1":
        table = "employees"
        return table
    elif table_number == "2":
        table = "tasks"
        return table
    else:
        print("Указано неверное значение")


while True:
    choice = input('Выберите действие: 1 - read, 2 - update, 3 - delete, 4 - busy_employees, 5 - important_tasks, 6 - exit: ')

    if choice == "1":
        table = table_chek()
        if table == None:
            continue
        URL = "http://127.0.0.1:5000/read/" + table
        response = requests.get(URL)
        print(response.text)


    elif choice == "2":
        table = table_chek()
        if table == None:
            continue
        URL = "http://127.0.0.1:5000/update/" + table
        # добавление новых строк в таблицу
        move =input("Выберите действие: 1 - добавить строку, 2 - обновить строку: ")
        if move == "1":
            if table == "employees":
                fio = input("Введите fio: ")
                position = input("Введите position: ")
                params = {
                "fio" : fio,
                "position" : position
                }
            elif table == "tasks":
                description = input("Введите description: ")
                parent_task_id = input("Введите parent_task_id: ")
                if parent_task_id == "":
                    parent_task_id = None
                specialist_id = input("Введите specialist_id: ")
                if specialist_id == "":
                    specialist_id= None
                deadline = input("Введите deadline (YYYY-MM-DD): ")
                status = input("Введите status(в работе, решено, специалист не назначен): ")
                params = {
                "description" : description,
                "parent_task_id" : parent_task_id,
                "specialist_id" : specialist_id,
                "deadline" : deadline,
                "status" : status
                }

        # изменение существующих строк в таблице
        elif move == "2":
            id = input(f"Работа с таблицей {table}.Укажите id строки: ")
            try:
                int_id = int(id)
            except:
                print('Значение не int')
                continue
            if table == "employees":
                field = input("Какое поле нужно обновить: fio, position: ")
                if field == "fio":
                    value = input("Введите fio:")
                elif field == "position":
                    value = input("Введите position:")
                else:
                    print("Неверная команда")
                    continue

            elif table == "tasks":
                field = input("Укажите, какое поле нужно обновить: description, parent_task_id, specialist_id, deadline, status: ")
                if field == "description":
                    value = input("Введите description:")
                elif field == "parent_task_id":
                    value = input("Введите parent_task_id:")
                    try:
                        int_value = int(value)
                    except:
                        print('Значение не int')
                        continue
                elif field == "specialist_id":
                    value = input("Введите specialist_id:")
                    try:
                        int_value = int(value)
                    except:
                        print('Значение не int')
                        continue
                elif field == "deadline":
                    value = input("Введите deadline:")
                elif field == "status":
                    value = input("Введите status:")
                else:
                    print("Неверная команда")
                    continue
            params = {
            'id' : int_id,
            'field' : field,
            'value' : value
            }
        else:
            print("Неверная команда")
            continue

        response = requests.post(URL, json = params)
        data = response.text
        print(data)


    elif choice == "3":
        table = table_chek()
        if table == None:
            continue
        URL = "http://127.0.0.1:5000/delete/" + table
        if table == "employees":
            id = input("Введите id: ")
            params = {
            "id" : id,
            }
        elif table == "tasks":
            id = input("Введите id: ")
            params = {
            "id" : id,
            }
        response = requests.post(URL, json = params)
        data = response.text
        print(data)

    elif choice == "4":
        URL = "http://127.0.0.1:5000/busy_employees/"
        response = requests.get(URL)
        print(response.text)

    elif choice == "5":
        URL = "http://127.0.0.1:5000/important_tasks"
        response = requests.get(URL)
        print(response.text)

    elif choice == "6":
        exit()

    else:
        print("Неверная команда")
        continue
