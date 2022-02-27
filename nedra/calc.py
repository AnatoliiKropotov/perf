from typing import Optional
from fastapi import FastAPI

app = FastAPI()
lst = list()
error = "ошибка"

@app.get("/calc/{viragenie_s_probelami}")
def calc(viragenie_s_probelami: str):
    number_1_str = ""
    number_2_str = ""
    number_3_str = ""
    operation_1 = ""
    operation_2 = ""
    operation_3 = ""
    start_number_2 = False
    start_number_3 = False
    status = "success"
    dct = {"request": "", "response": "", "status": ""}

    # сохранение в память списка запросов с заданным лимитом
    def memory(viragenie, result, status):
        dct = {"request": viragenie, "response": result, "status": status}
        print(f"Создали словарь {dct}")
        if len(lst) < 30:
            lst.append(dct)
            return
        elif len(lst) >= 30:
            for i in range(len(lst)):
                if i+1 == len(lst):
                    lst[i] = dct
                    print("Последний элемент списка изменён")
                    return
                lst[i] = lst[i+1]
        else:
            print("что-то пошло не так")
            return error

    # умножение в конце выражения
    def multiplication(vichislenie):
        vichislenie_with_multiplication = vichislenie * float(number_3_str)
        result = round(vichislenie_with_multiplication, 3)
        print(result)
        return result

    # парсинг входного арифметического выражения
    viragenie = viragenie_s_probelami.replace(" ", "")
    for i in range(len(viragenie)):
        print(f"Длина ввода {len(viragenie)}")
        try:
            if start_number_3 == True:
                if viragenie[i] == "." or viragenie[i] == "0" or int(viragenie[i]):
                    number_3_str += viragenie[i]
                    print(viragenie[i])
            elif start_number_2 == True:
                if viragenie[i] == "." or viragenie[i] == "0" or int(viragenie[i]):
                    number_2_str += viragenie[i]
                    print(viragenie[i])
            else:
                if viragenie[i] == "." or viragenie[i] == "0" or int(viragenie[i]):
                    number_1_str += viragenie[i]
                    print(viragenie[i])
        except:
            print(f"{viragenie[i]} не число")
            if operation_1 == "" and viragenie[i] == viragenie[0]:
                if viragenie[i] == "-" or viragenie[i] == "+":
                    operation_1 = viragenie[i]
                    print(f"operation_1 = {operation_1}")
                    continue
                else:
                    status = "fail"
                    result = ""
                    memory(viragenie, result, status)
                    return error
            elif operation_2 == "" and (viragenie[i] == "+" or viragenie[i] == "-" or viragenie[i] == "*" or viragenie[i] == "\\"):
                operation_2 = viragenie[i]
                print(f"operation_2 = {operation_2}")
                if viragenie[i-1] == operation_1:
                    status = "fail"
                    result = ""
                    memory(viragenie, result, status)
                    return error
                start_number_2 = True
                continue
            elif operation_3 == "" and viragenie[i] == "*":
                operation_3 = viragenie[i]
                print(f"operation_3 = {operation_3}")
                if viragenie[i-1] == operation_2:
                    status = "fail"
                    result = ""
                    memory(viragenie, result, status)
                    return error
                start_number_3 = True
            else:
                status = "fail"
                result = ""
                memory(viragenie, result, status)
                return error

    print(f" Число 1 строкой: {number_1_str}")
    print(f" Число 2 строкой: {number_2_str}")
    print(f" Число 3 строкой: {number_3_str}")
    print(operation_1,  number_1_str, operation_2, number_2_str, operation_3, number_3_str )

    # математические операции с выражением
    if operation_1 == "+" or operation_1 == "":
        if operation_2 == "-":
            vichislenie = float(number_1_str) - float(number_2_str)
            if number_3_str != "":
                result = multiplication(vichislenie)
                memory(viragenie, result, status)
                return result
            result = round(vichislenie, 3)
            print(result)
            memory(viragenie, result, status)
            return result
        elif operation_2 == "+":
            vichislenie = float(number_1_str) + float(number_2_str)
            if number_3_str != "":
                result = multiplication(vichislenie)
                memory(viragenie, result, status)
                return result
            result = round(vichislenie, 3)
            print(result)
            memory(viragenie, result, status)
            return result
        elif operation_2 == "*":
            vichislenie = float(number_1_str) * float(number_2_str)
            if number_3_str != "":
                result = multiplication(vichislenie)
                memory(viragenie, result, status)
                return result
            result = round(vichislenie, 3)
            print(result)
            memory(viragenie, result, status)
            return result
        elif operation_2 == "\\":
            vichislenie = float(number_1_str) / float(number_2_str)
            if number_3_str != "":
                result = multiplication(vichislenie)
                memory(viragenie, result, status)
                return result
            result = round(vichislenie, 3)
            print(result)
            memory(viragenie, result, status)
            return result
        elif operation_2 == "":
            vichislenie = float(number_1_str)
            result = round(vichislenie, 3)
            print(result)
            memory(viragenie, result, status)
            return result
        else:
            status = "fail"
            result = ""
            memory(viragenie, result, status)
            return error
    elif operation_1 == "-":
        if operation_2 == "-":
            vichislenie = - float(number_1_str) - float(number_2_str)
            if number_3_str != "":
                result = multiplication(vichislenie)
                memory(viragenie, result, status)
                return result
            result = round(vichislenie, 3)
            memory(viragenie, result, status)
            print(result)
            return result
        elif operation_2 == "+":
            vichislenie=  - float(number_1_str) + float(number_2_str)
            if number_3_str != "":
                result = multiplication(vichislenie)
                memory(viragenie, result, status)
                return result
            result = round(vichislenie, 3)
            memory(viragenie, result, status)
            print(result)
            return result
        elif operation_2 == "*":
            vichislenie =  - float(number_1_str) * float(number_2_str)
            if number_3_str != "":
                result = multiplication(vichislenie)
                memory(viragenie, result, status)
                return result
            result = round(vichislenie, 3)
            memory(viragenie, result, status)
            print(result)
            return result
        elif operation_2 == "\\":
            vichislenie = - float(number_1_str) / float(number_2_str)
            if number_3_str != "":
                result = multiplication(vichislenie)
                memory(viragenie, result, status)
                return result
            result = round(vichislenie, 3)
            memory(viragenie, result, status)
            print(result)
            return result
        elif operation_2 == "":
            result = -round(float(number_1_str) , 3)
            memory(viragenie, result, status)
            print(result)
            return result
        else:
            status = "fail"
            result = ""
            memory(viragenie, result, status)
            return error

@app.get("/history")
def history(limit: Optional[int] = None, status: Optional[str] = None):
    lst_1 = list()

    # выводим заданное количество последних запросов
    if limit != None and status == None:
        if limit >= 1 and limit <= 30:
            if len(lst) <= limit:
                return lst
            return lst[len(lst)-limit:]
        else:
            return error

    # фильтруем запросы по значению ключа status
    elif limit == None and status != None:
        if status == "success" or status == "fail":
            for i in lst:
                if i["status"] == status:
                    lst_1.append(i)
            return lst_1
        else:
            return error

    # делаем всё вместе
    elif limit != None and status != None:
        if limit >= 1 and limit <= 30:
            if status == "success" or status == "fail":
                for i in lst:
                    if i["status"] == status:
                        lst_1.append(i)
                if len(lst_1) <= limit:
                    return lst_1
                return lst_1[len(lst_1)-limit:]
            else:
                return error
        else:
            return error
    else:
        return lst
