import math

fh_circle = input('Введите файл с параметрами окружности: ')
f_circle = open(fh_circle)
circle_params = f_circle.read().split()
x_circle = float(circle_params[0])
y_circle = float(circle_params[1])
r_circle = float(circle_params[2])

fh_points = input('Введите файл с координатами точек: ')
f_points = open(fh_points)
points = f_points.read().split()


def func(point, circle):
    if point > 0 and circle > 0:
        if point > circle:
            result = math.fabs(point) - math.fabs(circle)
        elif point < y_circle:
            result = math.fabs(circle) - math.fabs(point)
    elif point < 0 and circle > 0:
        result = math.fabs(point) + math.fabs(circle)
    elif point < 0 and circle < 0:
        if point > circle:
            result = math.fabs(circle) - math.fabs(point)
        elif point < y_circle:
            result = math.fabs(point) - math.fabs(circle)
    elif point > 0 and y_circle < 0:
        result = math.fabs(point) + math.fabs(circle)
    elif point != 0 and circle == 0:
        result = math.fabs(point)
    elif point == 0 and circle == 0:
        result = 0
    elif point == 0 and circle != 0:
        result = math.fabs(circle)
    return result


def func2(parameter):
    if parameter < r_circle:
        print(1) #точка внутри
    elif parameter > r_circle:
        print(2) #точка снаружи
    else:
        print(0) #точка лежит на окружности


count = 0
for i in range(0, int((len(points)/ 2))):
    x_point = float(points[count])
    y_point = float(points[count+1])

    if x_point == x_circle and y_point == y_circle:
        print(1) #точка внутри
        count = count + 2

    elif x_point == x_circle and y_point != y_circle:
        distance = func(y_point, y_circle)
        func2(distance)
        count = count + 2

    elif y_point == y_circle and x_point != x_circle:
        distance = func(x_point, x_circle)
        func2(distance)
        count = count + 2

    else:
        a = func(x_point, x_circle)
        b = func(y_point, y_circle)
        hypotenuse = math.sqrt(a ** 2 + b ** 2)
        func2(hypotenuse)
        count = count + 2
