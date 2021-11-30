from scipy import optimize
import numpy as np
import math as ma
from copy import deepcopy
from colorama import Fore, Back, Style


MAX_COUNT = 10


def read_data() -> tuple:
    file = open('input1.txt', 'r')
    c = [int(i) for i in file.readline().split()]
    b = [int(i) for i in file.readline().split()]
    A = [[int(i) for i in line.split()] for line in file.readlines()]
    return c, b, A


def all_int(x) -> tuple:
    for i, xi in enumerate(x):
        if round(xi, 15) % 1 > 0:
            return False, i
    return True, None


def add_to_stack(stack, c, b, A, expr, i, xi, a=1) -> None:
    A_new = deepcopy(A)
    b_new = deepcopy(b)
    expr_new = deepcopy(expr)

    if expr_new[i] is None:
        expr_new[i] = len(A_new)
        A_new.append([0 for _ in range(len(c))])
        A_new[-1][i] = a
        b_new.append(xi)
    else:
        A_new[expr_new[i]][i] = a
        b_new[expr_new[i]] = xi

    stack.append({'c': c, 'b': b_new, 'A': A_new, 'expr': expr_new})


def print_text(count, text) -> None:
    if count < MAX_COUNT:
        print(text)


def iterations(stack):
    r = - np.inf
    answer = None
    count = 0
    while len(stack) > 0:
        last = stack.pop()
        c, b, A, expr = last['c'], last['b'], last['A'], last['expr']
        print_text(count, "\nc = " + str(c) + "\nb =" + str(b) + "\nA =\n" + str(np.array(A)))
        print_text(count, Fore.CYAN + "~ решение симплекс-методом ~" + Style.RESET_ALL)
        x_all = optimize.linprog(- np.array(c), A, b, method='simplex')
        print(x_all)
        if not x_all.get('success'):
            print_text(count, Fore.YELLOW + 'Текущая подзадача несовместна!' + Style.RESET_ALL)
            continue
        x = x_all.get('x')
        r_new = - x_all.get("fun")
        print_text(count, "x* = " + str(x) + "\nr* = " + str(r_new) + "\nr = " + str(r))
        is_int, i = all_int(x)

        if ma.floor(r_new) > r:
            if not is_int:
                print_text(count, Fore.MAGENTA + "~ ветвим ~" + Style.RESET_ALL)
                xi_floor = ma.floor(x[i])
                xi_ceil = ma.ceil(x[i])
                print_text(count, "i = " + str(i) + "\tfloor(xi) = " + str(xi_floor) + "\tceil(xi) = " + str(xi_ceil))
                add_to_stack(stack, c, b, A, expr, i, - xi_ceil, -1)
                add_to_stack(stack, c, b, A, expr, i, xi_floor)
            else:
                r = r_new
                answer = x
                print_text(count, Back.CYAN + Fore.BLACK + "обновлённые r = " + str(r) + ", x = " + str(answer) +
                           Style.RESET_ALL)

        count += 1
    return answer


if __name__ == '__main__':
    c, b, A = read_data()
    stack = [{'c': c, 'b': b, 'A': A, 'expr': [None for _ in range(len(c))]}]
    x = iterations(stack)

    if x is not None:
        print(Fore.GREEN + "\nОтвет: x = ", x)
    else:
        print(Fore.RED + '\nЗадача несовместна!')
