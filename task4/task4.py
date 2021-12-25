fh = input('Введите имя файла:')
f = open(fh)
nums = list()
for i in f:
    nums.append(int(i))


summ = 0
for i in range(0,len(nums)):
    summ = summ + nums[i]
sred = summ / len(nums)
x = int(sred)


l = list()
count = 0
for i in nums:
    if i == x:
        l.append(i)
    elif i < x:
        while i != x:
            i += 1
            count +=1
        l.append(i)
    elif i > x:
        while i != x:
            i -=1
            count +=1
        l.append(i)
print(count)
