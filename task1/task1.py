import numpy as np
n = int(input('Введите n:'))
m = int(input('Введите m:'))

l = list()
while len(l) < 10000:
    for i in range(1,n+1):
        l.append(i)

x = 0
y = m

while True:
    l1 = list()
    for i in l[x:y]:
        l1.append(i)
        if len(l1)==m:
            if l1[m-1] == 1:
                print(l1[0])
                quit()
            x, y= y-1,y+m-1
            print(l1[0], end='')
