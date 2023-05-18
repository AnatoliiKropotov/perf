lst = [1,2,4,6,24,24,30,32,53,56,64,66,67,80,100]

print(f"массив для поиска: {lst}")
number = int(input("Введите число дял происка:"))

# сложность O(log(n))
def binary_search(lst, number):
    if len(lst) == 1:
        if lst[0] == number:
            print(f"Число {number} найдено! ")
            return
        else:
            print(f"Число {number} не найдено в списке ")
            return
    middle = len(lst) // 2
    if lst[middle] == number:
        print(f"Число {number} найдено!")
        return
    elif lst[middle] < number:
        lst = lst[middle + 1:]
        binary_search(lst, number)
    elif lst[middle] > number:
        lst = lst[:middle]
        binary_search(lst, number)

binary_search(lst, number)
