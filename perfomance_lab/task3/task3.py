import json

fhand_tests = input('Введите имя файла, макет:')
fhand_values = input('Введите имя файла, значения:')
fh_tests = open(fhand_tests)
fh_values = open(fhand_values)
fdata_tests = fh_tests.read()
fdata_values = fh_values.read()
data_tests = json.loads(fdata_tests)
data_values = json.loads(fdata_values)


def func(id, value, list):
    for i in range(0,len(list)):
        if list[i]['id'] == id:
            list[i]['value'] = value
            return
        elif list[i].get('values') != None:
            if func(id, value, list[i]['values']):
                return

r = open('report.json', 'w')
for i in range(0, len(data_values['values'])):
    id = data_values["values"][i]['id']
    value = data_values["values"][i]['value']
    list = data_tests['tests']
    func(id, value, list)

json.dump(data_tests, r, sort_keys=True, indent=2)
