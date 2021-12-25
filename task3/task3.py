import json

fhand_tests = input('Введите имя файла, макет:')
fhand_values = input('Введите имя файла, значения:')
fh_tests = open(fhand_tests)
fh_values = open(fhand_values)
fdata_tests = fh_tests.read()
fdata_values = fh_values.read()
data_tests = json.loads(fdata_tests)
data_values = json.loads(fdata_values)


# здесь должна быть рекурсивная функция,к этому я пришёл, но написать её не успел :(
def func4(id, value, list):
    print('переход в func4')
    for i in range(0,len(list)):
        if list[i]['id'] == id:
            list[i]['value'] = value
            print('выход из func4')
            return

def func3(id, value, list):
    print('переход в func3')
    for i in range(0,len(list)):
        if list[i]['id'] == id:
            list[i]['value'] = value
            print('выход из func3')
            return
    for i in range(0,len(list)):
        if list[i].get('values') != None:
            func4(id, value, list = list[i]['values'])
            return

def func2(id, value, list):
    print('переход в func2')
    for i in range(0,len(list)):
        if list[i]['id'] == id:
            list[i]['value'] = value
            print('выход из func2')
            return True
        elif list[i].get('values') != None:
            if func3(id, value, list = list[i]['values']) == True:
                return

def func(id, value, list):
    for a in range(0,len(list)):
        if list[a]['id'] == id:
            list[a]['value'] = value
            return
        elif list[a].get('values') != None:
            if func2(id, value, list[a]['values']) == True:
                return

r = open('report.json', 'w')
for i in range(0, len(data_values['values'])):
    print('start')
    id = data_values["values"][i]['id']
    value = data_values["values"][i]['value']
    list = data_tests['tests']
    func(id, value, list)

json.dump(data_tests, r, sort_keys=True, indent=2)
