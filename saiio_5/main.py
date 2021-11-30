import numpy as np
from colorama import Fore, Back, Style
from copy import deepcopy


def read_data(file_num='1') -> tuple:
    file = open('input'+file_num+'.txt', 'r')
    s, t = [int(num) - 1 for num in file.readline().split()]
    n = int(file.readline())
    G = [{} for _ in range(n)]
    for line in file:
        x, y, z = [int(num) for num in line.split()]
        x -= 1
        y -= 1
        G[x][y] = [0, z]
        G[y][x] = [0, 0]
    return s, t, G


# вычисление первоначального Gf
def get_Gf(G) -> list:
    Gf = [{} for _ in range(len(G))]
    for i, item in enumerate(G):
        for key in item.keys():
            cf = G[i][key][1] - G[i][key][0] + G[key][i][0]
            Gf[i][key] = cf
    return Gf


# изменение значений в Gf на пути P
def change_Gf(G, Gf, P) -> list:
    if len(Gf) == 0:
        return get_Gf(G)
    else:
        for i, j in P:
            Gf[i][j] = G[i][j][1] - G[i][j][0] + G[j][i][0]
            Gf[j][i] = G[j][i][1] - G[j][i][0] + G[i][j][0]
        return Gf


# нахождение пути из s в t
def find_path(s, t, Gf):
    Q = [s]
    l = [None] * len(Gf)
    l[s] = np.inf

    while len(Q) > 0 and l[t] is None:
        cur_v = Q.pop(0)
        for next_v in Gf[cur_v].keys():
            if l[next_v] is None and Gf[cur_v][next_v] != 0:
                Q.append(next_v)
                l[next_v] = cur_v

    l[s] = None

    return l


# tetta = min(cf(a)), a принадлежит пути P
def get_tetta(s, t, l, Gf) -> int:
    i, tetta = t, np.inf
    while i != s:
        tetta = min(tetta, Gf[l[i]][i])
        i = l[i]
    return tetta


# создание пути P
def make_P(s, t, l) -> list:
    i = t
    P = []
    while i != s:
        P.append([l[i], i])
        i = l[i]
    return P


# прибавление в исходному потоку f вспомогательного потока fp
def make_new_f(tetta, P, G) -> None:
    for i, item in enumerate(G):
        for key in item.keys():
            value = G[i][key][0] - G[key][i][0]
            if [i, key] in P:
                value += tetta
            G[i][key][0] = max(0, value)


def print_variables(i, Gf, l) -> None:
    if i < 5:
        print('\n' + Back.MAGENTA + Fore.BLACK + f'Итерация {i+1}' + Style.RESET_ALL)
        print(Fore.MAGENTA + 'Gf:\t' + Style.RESET_ALL)
        for i, item in enumerate(Gf):
            print(str(i + 1) + Fore.CYAN + ' --> ' + Style.RESET_ALL, {key + 1: item[key] for key in item.keys()})
        l_copy = deepcopy(l)
        for i in range(len(l_copy)):
            if l_copy[i] is not None:
                l_copy[i] += 1
        print(Fore.MAGENTA + 'l =\t' + Style.RESET_ALL, l_copy)


def print_variables_end(i, tetta, P, G):
    if i < 5:
        print(Fore.MAGENTA + 'tetta =\t' + Style.RESET_ALL, tetta)
        print(Fore.MAGENTA + 'P =\t' + Style.RESET_ALL, [[i+1, j+1] for i, j in P][::-1])
        print(Fore.MAGENTA + 'G:\t' + Style.RESET_ALL)
        for i, item in enumerate(G):
            print(str(i + 1) + Fore.CYAN + ' --> ' + Style.RESET_ALL, {key + 1: item[key] for key in item.keys()})


def iterations(s, t, G):
    Gf, P, i = [], [], 0

    while True:
        Gf = change_Gf(G, Gf, P)
        l = find_path(s, t, Gf)

        print_variables(i, Gf, l)

        if l[t] is None:
            print('\n' + Fore.MAGENTA + f'Нет пути в t -> текущий поток - максимальной мощности!\nЧисто итераций: {i+1}'
                  + Style.RESET_ALL)
            return G

        tetta = get_tetta(s, t, l, Gf)
        P = make_P(s, t, l)
        make_new_f(tetta, P, G)

        print_variables_end(i, tetta, P, G)
        i += 1


def print_G(G):
    print(Fore.BLACK + Back.MAGENTA + 'G:\t' + Style.RESET_ALL)
    for i, item in enumerate(G):
        print(str(i+1) + Fore.CYAN + ' --> ' + Style.RESET_ALL, {key+1: item[key][0] for key in item.keys()})


# мощность потока
def get_M(s, G) -> int:
    m = sum([G[s][key][0] for key in G[s].keys()])
    m -= sum([G[i][key][0] for i, item in enumerate(G) for key in item.keys() if key == s])
    return m


if __name__ == '__main__':
    s, t, G = read_data('1')

    G = iterations(s, t, G)
    print('\n' + Back.GREEN + Fore.BLACK + '~~~ Ответ ~~~' + Style.RESET_ALL)
    print_G(G)

    m = get_M(s, G)
    print(Back.MAGENTA + Fore.BLACK + 'Мощность потока M(s) =\t' + Style.RESET_ALL, m)
