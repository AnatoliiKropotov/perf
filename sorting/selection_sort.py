lst = [8,5,1,6,63,525,6,2,4,55,255]
print(f"начальный массив: {lst}")
count = 0

# функция сортировки выбором (в среднем О(n^2))
def selection_sort(lst, count):
    if count == len(lst):
        print(f"Отсортированный массив: {lst}")
        return lst

    smallest_element_index = None
    for i in range(count,len(lst)):
        if smallest_element_index is None:
            smallest_element_index = i
        elif lst[i] < lst[smallest_element_index]:
                smallest_element_index = i
    lst[count], lst[smallest_element_index] = lst[smallest_element_index], lst[count] # наименьший элемент ставим в начало неотсортированного списка (меняем местами)

    count +=1
    selection_sort(lst, count)

selection_sort(lst, count)
