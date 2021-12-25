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
r = open('report.json', 'w')
for i in range(0, len(data_values['values'])):
    id = data_values["values"][i]['id']
    value = data_values["values"][i]['value']
    for a in range(0,len(data_tests['tests'])):
        if data_tests['tests'][a]['id'] == id:
            data_tests['tests'][a]['value'] = value
            break
        elif data_tests['tests'][a].get('values') != None:
            for b in range(0, len(data_tests['tests'][a]['values'])):
                if data_tests['tests'][a]['values'][b]['id'] == id:
                    data_tests['tests'][a]['values'][b]['value'] = value
                    break
                elif data_tests['tests'][a]['values'][b].get('values') != None:
                    for c in range(0, len(data_tests['tests'][a]['values'][b]['values'])):
                        if data_tests['tests'][a]['values'][b]['values'][c]['id'] == id:
                            data_tests['tests'][a]['values'][b]['values'][c]['value'] = value
                            break
                        elif data_tests['tests'][a]['values'][b]['values'][c].get('values') != None:
                            for d in range(0, len(data_tests['tests'][a]['values'][b]['values'][c]['values'])):
                                if data_tests['tests'][a]['values'][b]['values'][c]['values'][d]['id'] == id:
                                    data_tests['tests'][a]['values'][b]['values'][c]['values'][d]['value'] = value
                                    break

json.dump(data_tests, r, sort_keys=True, indent=2)
