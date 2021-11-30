from math import ceil
import numpy as np
from colorama import Fore, Back, Style
from simplex import SimplexMethod


MAX_COUNT = 15


def read_data() -> tuple:
    file = open('input1.txt', 'r')
    c = [float(i) for i in file.readline().split()]
    b = [float(i) for i in file.readline().split()]
    A = [[float(i) for i in line.split()] for line in file.readlines()]
    print(c, b, A)
    return c, b, A


def all_int(x) -> tuple:
    b, i_res = True, None
    for i, xi in enumerate(x):
        if round(xi, MAX_COUNT) % 1 > 0:
            b, i_res = False, i
    return b, i_res


def make_Ab(A, Jb) -> list:
    Ab = []
    for j in sorted(Jb):
        Ab.append([A[i][j] for i in range(len(A))])
    return np.transpose(Ab)


def make_An(A, Jb) -> list:
    An = []
    for j in range(len(A[0])):
        if j not in Jb:
            An.append([A[i][j] for i in range(len(A))])
    return np.transpose(An)


def get_part(num) -> float:
    if num >= 0:
        return - num + int(num)
    return ceil(num) - num - 1


def add_line_to_A(A, line, Jb) -> None:
    for i in range(len(A)):
        A[i].append(0)
    A.append([0] * len(A[0]))
    line = list(line)
    for i in range(len(A[0]) - 1):
        if i not in Jb:
            A[-1][i] = get_part(line.pop(0))
    A[-1][-1] = 1


def homory(c, b, A) -> tuple:
    end = False

    count = 1

    while not end:
        print(Fore.CYAN + "\nИтерация " + str(count) + Style.RESET_ALL)
        count += 1

        model1 = SimplexMethod(np.array(c), np.array(A), np.array(b))
        x, Jb = model1.solve()

        print("x=", list(x), "Jb=", Jb)
        end, i = all_int(x)
        if end:
            return x

        Ab = make_Ab(A, Jb)
        print("Ab:\n", Ab)

        Ab_inv = np.linalg.inv(Ab)
        print("Ab^-1:\n", Ab_inv)

        An = make_An(A, Jb)
        print("An:\n", An)

        M = np.dot(Ab_inv, An)
        print("Ab^-1 * An:\n", M)

        j = Jb.index(i)

        print("i-ая строка:\t", M[j])

        add_line_to_A(A, M[j], Jb)

        print("new A:\n", np.array(A))
        c.append(0)
        print("x[i] =\t", x[i])
        b.append(get_part(x[i]))
        print("new b:\t", b)
        print("new c:\t", c)


if __name__ == '__main__':
    c, b, A = read_data()

    n = len(c)

    answer = homory(c, b, A)
    print('\n' + Back.GREEN + Fore.BLACK + "Ответ: x =\t", list(round(i, MAX_COUNT) for i in answer[:n]), Style.RESET_ALL)
