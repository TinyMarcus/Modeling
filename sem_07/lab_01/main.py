from datetime import datetime
import random
from scipy.stats import chi2

global first

def table_method(first):
    time = datetime.now()
    current_hour = time.hour
    current_minute = time.minute
    current_microsecond = time.microsecond % 60

    digit = ''
    file = ''

    if current_hour % 2 == 0:
        file = 'even_table.txt'
    else:
        file = 'odd_table.txt'

    i = 0
    with open(file) as table:
        for row in table:
            i += 1
            if i == current_minute:
                digit = row[current_microsecond]
            if first == True and digit == '0':
                current_microsecond = datetime.now().microsecond % 60
                digit = row[current_microsecond]
                first = False

    return digit


def get_table_number(digit_count):
    num = ''
    first = True

    for _ in range(digit_count):
        digit = table_method(first)
        num += digit
    # num = num * 10 + int(digit)
    num = int(num)
    return num


def middle_square_method():
    one_digit = random.randint(0, 9)
    two_digit = random.randint(10, 99)
    three_digit = random.randint(100, 999)

    len_num_one_digit = len(str(one_digit))
    str_num_one_digit = str(one_digit)
    seed_num_one_digit = one_digit**2
    str_seed_one_digit = str(seed_num_one_digit)

    len_num_two_digit = len(str(two_digit))
    str_num_two_digit = str(two_digit)
    seed_num_two_digit = two_digit**2
    str_seed_two_digit = str(seed_num_two_digit)

    len_num_three_digit = len(str(three_digit))
    str_num_three_digit = str(three_digit)
    seed_num_three_digit = three_digit**2
    str_seed_three_digit = str(seed_num_three_digit)

    str_seed_one_digit.zfill(2 * len_num_one_digit)
    middle_one_digit = (len(str_seed_one_digit) - len_num_one_digit) / 2
    middle_one_digit = round(middle_one_digit)

    str_seed_two_digit.zfill(2 * len_num_two_digit)
    middle_two_digit = (len(str_seed_two_digit) - len_num_two_digit) / 2
    middle_two_digit = round(middle_two_digit)

    str_seed_three_digit.zfill(2 * len_num_three_digit)
    middle_three_digit = (len(str_seed_three_digit) - len_num_three_digit) / 2
    middle_three_digit = round(middle_three_digit)

    str_res_one_digit = str_seed_one_digit[middle_one_digit:middle_one_digit+len_num_one_digit]

    if str_seed_two_digit[middle_two_digit] == '0':
        str_res_two_digit = str_seed_two_digit[middle_two_digit+1:middle_two_digit+len_num_two_digit+1]
    else:
        str_res_two_digit = str_seed_two_digit[middle_two_digit:middle_two_digit+len_num_two_digit]

    if str_seed_three_digit[middle_three_digit] == '0':
        str_res_three_digit = str_seed_three_digit[middle_three_digit+1:middle_three_digit+len_num_three_digit+1]
    else:
        str_res_three_digit = str_seed_three_digit[middle_three_digit:middle_three_digit+len_num_three_digit]

    return str_res_one_digit, str_res_two_digit, str_res_three_digit


def uniformity_criterion(seq, d=1000):
    n = len(seq)

    cnt = [0 for _ in range(d)]
    for i in range(n):
        if int(seq[i]) < d:
            cnt[int(seq[i])] += 1

    k = d
    p = 1 / d
    e = n * p

    chi2_stat = 0
    for j in range(k):
        chi2_stat += (cnt[j] - e)**2 / e

    pvalue = chi2.cdf(chi2_stat, k - 1)

    return pvalue


def output_middle_square():
    first = []
    second = []
    third = []

    cnt = 50

    for i in range(cnt):
        one, two, three = middle_square_method()
        first.append(one)
        second.append(two)
        third.append(three)

    first_crit = uniformity_criterion(first[0:15], 10)
    second_crit = uniformity_criterion(second[0:15], 100)
    third_crit = uniformity_criterion(third[0:15], 1000)

    print("┏━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓")
    print("┃    №    ┃     0 - 9     ┃   10 - 99     ┃   100 - 999   ┃")
    print("┣━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━┫")
    for i in range(0, 15):
        print("┃{:^9d}┃{:^15d}┃{:^15d}┃{:^15d}┃".format(i+1, int(first[i]), int(second[i]), int(third[i])))
    print("┣━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━┫")
    print("┃   ...   ┃      ...      ┃      ...      ┃      ...      ┃".format(cnt, cnt, cnt))
    print("┣━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━┫")
    print("┃  Чисел  ┃{:^15d}┃{:^15d}┃{:^15d}┃".format(cnt, cnt, cnt))
    print("┃Оценка(%)┃{:^15.2f}┃{:^15.2f}┃{:^15.2f}┃".format(first_crit * 100, second_crit * 100, third_crit * 100))
    print("┗━━━━━━━━━┻━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┛")


def output_table_method():
    first = []
    second = []
    third = []

    cnt = 50

    for i in range(cnt):
        first.append(get_table_number(1))
        second.append(get_table_number(2))
        third.append(get_table_number(3))

    first_crit = uniformity_criterion(first[0:20], 10)
    second_crit = uniformity_criterion(second[0:20], 100)
    third_crit = uniformity_criterion(third[0:20], 1000)

    print("┏━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓")
    print("┃    №    ┃     0 - 9     ┃   10 - 99     ┃   100 - 999   ┃")
    print("┣━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━┫")
    for i in range(0, 15):
        print("┃{:^9d}┃{:^15d}┃{:^15d}┃{:^15d}┃".format(i+1, int(first[i]), int(second[i]), int(third[i])))
    print("┣━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━┫")
    print("┃   ...   ┃      ...      ┃      ...      ┃      ...      ┃".format(cnt, cnt, cnt))
    print("┣━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━┫")
    print("┃  Чисел  ┃{:^15d}┃{:^15d}┃{:^15d}┃".format(cnt, cnt, cnt))
    print("┃Оценка(%)┃{:^15.2f}┃{:^15.2f}┃{:^15.2f}┃".format(first_crit * 100, second_crit * 100, third_crit * 100))
    print("┗━━━━━━━━━┻━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┛")


def main():
    # output_middle_square()
    output_table_method()


if __name__ == "__main__":
    main()