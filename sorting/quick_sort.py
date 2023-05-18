lst = [8,5,1,6,63,525,6,2,4,55,255]
print(f"начальный массив: {lst}")

# средняя сложность О(n*log(n))
def quick_sort(lst):
    left_part = []
    rigth_part= []
    opora=[]
    if len(lst) == 2:
        if lst[0] > lst[1]:
            lst[0], lst[1] = lst[1], lst[0]
            return lst
        else:
            return lst
    elif len(lst) < 2:
        return lst
    elif len(lst) > 2:
        opora.append(lst.pop(len(lst) // 2))
        for i in lst:
            if i < opora[0]:
                left_part.append(i)
            elif i >= opora[0]:
                rigth_part.append(i)
        left = quick_sort(left_part)
        rigth = quick_sort(rigth_part)
        return  left + opora + rigth

print(f"отсортированный массив: {quick_sort(lst)}")
