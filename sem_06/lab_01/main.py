from math import ceil, sqrt

def func(x, u):
    return x ** 2  + u ** 2

# Пикар
def picar_method(n, h, x, y0):
    def f1(t):
        return t ** 3 / 3
    def f2(t):
        return f1(t) + t ** 7 / 63
    def f3(t):
        return f2(t) +  (t ** 11) * (2 / 2079) + (t ** 15) / 59535
    def f4(t, f3):
        return f3 + (t ** 15)*(2 / 93555) + (t ** 19)*(2 / 3393495) + \
                    (t ** 19)*(2 / 2488563) + (t ** 23)*(2 / 86266215) + \
                    (t ** 23)*(1 / 99411543) + (t ** 27)*(2 / 3341878155) + \
                    (t ** 31)*(1 / 109876902975)

    y_out = [[y0, y0]]
    for i in range(n-1):
        x += h
        y_f3 = f3(x)
        y_out.append([y_f3, f4(x, y_f3)])
    return y_out

# Явный Эйлера
def explicit_euler_method(n, h, x, y):
    y_out = []
    for i in range(n):
        try:
            y += h * func(x, y)
            y_out.append(y)
            x += h
        except OverflowError:
            y_out.append('Overflow')
            for j in range(i, n - 1):
                y_out.append('────')
            break
    return y_out

# Неявный Эйлера
def implicit_euler_method(n, h, x, y):
    y_out = [y]
    for i in range(n):
        D = 1 - 4 * h * (y + h * ((x + h)**2))
        if D < 0:
            y_out.append('Neg discr')
            for j in range(i, n - 2):
                y_out.append('────')
            break
        y = (1 - sqrt(D)) / (2 * h) # берем корень с минусом
        # try:
        #     y += h * (func(x, y) + func(x + h, y + h * func(x,y))) / 2
        x += h
        y_out.append(y)
        # except OverflowError:
        #     y_out.append('overflow')
        #     for j in range(i, n-1):
        #         y_out.append('────')
        #     break
    return y_out
        
# Вывод
def output(s):
    if type(s) == float:
        if s > 1000000:
            return '{:.9e}'.format(s)
        return '{:.9f}'.format(s)
    elif type(s) == int:
        return str(s)
    else:
        return s

def main():
    
    
    x = float(input("Введите начальное значение x: "))
    y0 = 0
    end = float(input("Введите конечное значение x: "))
    h = float(input("Введите шаг: "))
    quan = int(input("Введите количество выводимых значений: "))

    n = ceil(abs(end - x)/h) + 1 # количество повторений

    x_arr = [x + h*i for i in range(n)]
    y1 = explicit_euler_method(n, h, x, y0)
    y2 = implicit_euler_method(n, h, x, y0)
    y3 = picar_method(n, h, x, y0)
    
    print("┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓")
    print("┃    x    ┃     Пикар 3      ┃      Пикар 4     ┃  Явный Эйлера  ┃  Неявный Эйлера  ┃")
    print("┣━━━━━━━━━╋━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━┫")
    output_step = int(n/quan) 
    for i in range(0, n, output_step):
        print("┃{:^9.5f}┃{:^18.8f}┃{:^18.8f}┃{:^16s}┃{:^18s}┃".format(x_arr[i], y3[i][0], \
                                                                      y3[i][1], output(y1[i]), \
                                                                      output(y2[i])))
    print("┗━━━━━━━━━┻━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━┛")


if __name__ == '__main__':
    main()


# from math import sqrt
# from prettytable import PrettyTable

# def num_explicit(x1, x2, h): 
#     y = [0]
#     x = x1
#     while x < x2:
#         y.append(y[-1] + h*(x*x + y[-1]*y[-1]))
#         x += h 
#     return y

# def num_implicit(x1, x2, h): 
#     y = [0]
#     x = x1
#     a=h 
#     b = -1
#     while x < x2:
#         try:
#             c = h*(x + h)*(x + h) + y[-1] 
#             D = b*b - 4*a*c
#             #print(D)
#             root1 = (-1*b - sqrt(D))/(2*a) 
#             root2 = (-1*b + sqrt(D))/(2*a)
#             y.append(round(root1, 7))
#         except: 
#             y.append(None)
#         x += h
#     return y

# def picard(x1, x2, h):
#     y1 = [0]
#     y2 = [0]
#     y3 = [0]
#     y4 = [0]
#     x = x1
#     while x < x2:
#         x += h
#         y1.append((x**3)/3)
#         y2.append((x**3)/3 + (x**7)/63)
#         y3.append((x**3)/3 + (x**7)/63 + (x**15)/59535 + 2*(x**11)/2079) 
#         y4.append((x**3)/3 + (x**7)/63 + 13*(x**15)/218395 + 2*(x**11)/2079 +
#                    82*(x**19)/37328445 + 662*(x**23)/10438212015 +
#                   4*(x**27)/3341878155 + (x**31)/109876902975)


#     return y1, y2, y3, y4

# def main():
#     x1 = float(input('    X от '))
#     x2 = float(input('    до '))
#     h1 = float(input('    с шагом '))
#     h2 = float(input('с шагом для вывода '))
#     expl = num_explicit(0, x2, h1) 
#     impl = num_implicit(0, x2, h1)
#     y1, y2, y3, y4 = picard(0, x2, h1)

#     table = PrettyTable()
#     table.field_names = ["x", "Пикар 1", "Пикар 2",
#                          "Пикар 3", "Пикар 4",
#                          "численный явный", "численный неявный"]

#     x=0

#     i=0
#     res_i = 0
#     n = round(h2/h1) 
#     mindif = 10 
#     while True:
#         if abs(x - x1) < mindif: 
#             mindif = abs(x - x1) 
#             res_i = i
#         if x > x2:
#             break
#         x += h2 
#         i += n
    
#     x = x1
#     i = res_i

#     while True:
#         table.add_row([round(x, 3), round(y1[i], 7), round(y2[i], 7), round(y3[i], 7),
#                        round(y4[i], 7) , round(expl[i], 7), impl[i]])
#         if x > x2:
#             break
#         x += h2
#         i += n
#     print(table)

# if __name__ == "__main__": 
#     main()
