array = [666,45,5,452,1,3,6,6,6,858,63,52,525,252,22]
print(f"Исходный массив:{array}")
lst =[]

#функция непосредственно сортировки и слияния, средняя сложность О(n*log(n))
def merge_sort(left_part, rigth_part):
    lst =[]
    i = 0
    j = 0
    while (len(left_part) + len(rigth_part) != len(lst)):
        if i == len(left_part):          #если в левой части кончились элементы, то переносим всю правую часть в результирующий список
            for b in rigth_part[j:]:
                lst.append(b)
        elif j == len(rigth_part):       #для правой аналогично
            for b in left_part[i:]:
                lst.append(b)
        elif left_part[i] < rigth_part[j]:
            lst.append(left_part[i])
            i+=1
        elif left_part[i] > rigth_part[j]:
            lst.append(rigth_part[j])
            j+=1
        elif left_part[i] == rigth_part[j]: # работаем с равными числами
            lst.append(left_part[i])
            lst.append(rigth_part[j])
            i+=1
            j+=1
    return lst

# функция для разделения массива вплоть до одного элемента, рекурсивная
def separation (array):
    if len(array) == 1:
        return array

    mid = len(array) // 2

    left_part = separation(array[:mid])
    rigth_part = separation(array[mid:])

    return merge_sort(left_part, rigth_part)

result = separation(array)
print(f"Отсортированный массив:{result}")
