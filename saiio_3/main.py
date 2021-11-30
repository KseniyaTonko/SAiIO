from copy import deepcopy as dc
import numpy as np
from colorama import Fore, Style


def read_data(num='1') -> tuple:
    file = open('input'+num+'.txt', 'r')
    file.readline()
    A = []
    for line in file:
        A.append([float(i) for i in line.split()])
    n, Q = len(A), len(A[0]) - 1
    return n, Q, A


def get_OPT(n, Q, A) -> tuple:
    opt = [dc(A[0])]
    x = [[i for i in range(Q+1)]]
    for k in range(1, n):
        opt.append([])
        x.append([])
        for q in range(Q+1):
            cur_max, cur_x = - np.inf, None
            for xk in range(0, q+1):
                if cur_max < opt[k-1][q-xk] + A[k][xk]:
                    cur_x = xk
                cur_max = max(cur_max, opt[k-1][q-xk] + A[k][xk])
            opt[-1].append(cur_max)
            x[-1].append(cur_x)
    return opt, x


def print_opt(OPT, x) -> None:
    print(Fore.MAGENTA + 'OPT(k, q):' + Style.RESET_ALL)
    print(str(np.array(OPT)) + "\n")
    print(Fore.MAGENTA + "x:" + Style.RESET_ALL)
    print(str(np.array(x)))


def get_x_values(n, Q, x) -> list:
    answer, x_sum = [x[-1][-1]], x[-1][-1]
    for k in range(n-2, -1, -1):
        answer.append(x[k][Q-x_sum])
        x_sum += answer[-1]
    return answer


def print_answer(x, profit) -> None:
    print("\n" + Fore.GREEN + "Максимальная прибыль =\t" + Style.RESET_ALL + str(profit))
    print(Fore.GREEN + "Оптимальный план x =\t" + Style.RESET_ALL + str(x[::-1]))


if __name__ == '__main__':
    n, Q, A = read_data()
    OPT, x = get_OPT(n, Q, A)
    print_opt(OPT, x)
    answer = get_x_values(n, Q, x)
    print_answer(answer, OPT[-1][-1])
