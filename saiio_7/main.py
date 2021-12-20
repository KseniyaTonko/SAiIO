from colorama import Fore, Back, Style
import numpy as np
import networkx as nx


PLUS = '+'
MINUS = '-'


def read_data(file_num='1') -> tuple:
    file = open('input'+file_num+'.txt', 'r')
    n, m = [int(i) for i in file.readline().split()]
    G = {}
    for i in range(m):
        line = file.readline()
        i, j, x, c = [int(num) for num in line.split()]
        G[(i-1, j-1)] = {'x': x, 'c': c}
    Jb = []
    for line in file:
        Jb.append([int(i)-1 for i in line.split()])
    return n, G, Jb


# решение системы для нахождения значений потенциалов u
def get_u(n, G, Jb) -> list:
    A = np.zeros((n, n))
    b = [0]
    A[0][0] = 1
    for index, pair in enumerate(Jb):
        A[index+1][pair[0]] = 1
        A[index+1][pair[1]] = -1
        b.append(G[(pair[0], pair[1])]['c'])
    return np.linalg.solve(A, b)


# проверка условия для всех пар (i, j) не из Jb:
# ui - uj <= cij,
# если есть такая пара индексов, что условие не соблюдается, то план не оптимален, возвращаем эту пару индексов
def check_is_optimal(G, Jb, u) -> tuple:
    for i, j in G.keys():
        if (i, j) not in Jb:
            if u[i] - u[j] > G[(i, j)]['c']:
                return False, i, j
    return True, None, None


# пары индексов (i, j) и (j, i) из Jb
def make_Gb(Jb) -> list:
    Gb = []
    for i, j in Jb:
        Gb.append((i, j))
        Gb.append((j, i))
    return Gb


# нахожденеи цикла в Gb
def get_cycle(Gb, i, j) -> list:
    final_cycle = []
    for cycle in nx.simple_cycles(nx.DiGraph(Gb)):
        if len(cycle) > len(final_cycle):
            final_cycle = cycle

    k = final_cycle.index(i)
    n = len(final_cycle)
    if final_cycle[(k + 1) % n] != j:
        final_cycle.reverse()
    k = final_cycle.index(i)
    return final_cycle[k:] + final_cycle[:k]


# удаление из Gb рёбер, которые не входят в цикл
def delete_from_Gb_not_cycle(cycle) -> dict:
    Gb = {}
    n = len(cycle)
    for id, i in enumerate(cycle):
        j = cycle[(id + 1) % n]
        Gb.setdefault(i, {})
        Gb[i][j] = None
    return Gb


# расстановка для рёбер цикла '+' и '-'
def place_signs(n, Gb, Jb, pair) -> None:
    visited = [[False] * n for _ in range(n)]

    def dfs(i, prev) -> None:
        if visited[prev][i]:
            return
        visited[prev][i] = True
        if [prev, i] in Jb:
            Gb[prev][i] = PLUS
        else:
            Gb[prev][i] = MINUS
        for j in Gb[i].keys():
            dfs(j, i)

    dfs(pair[1], pair[0])


def get_pair(i, j, Jb) -> tuple:
    pair = (i, j)
    if [i, j] not in Jb:
        pair = (j, i)
    return pair


# tetta = min(xij) для (i, j) со знаком '-'
def get_tetta(G, Gb, Jb) -> int:
    tetta = np.inf
    for i in Gb.keys():
        for j in Gb[i]:
            if Gb[i][j] == MINUS:
                pair = get_pair(i, j, Jb)
                tetta = min(tetta, G[pair]['x'])
    return tetta


# изменение xij: если (i, j) со знаком '+', то +tetta, если со знаком '-', то -tetta
def change_G(G, Gb, Jb, tetta) -> None:
    for i in Gb.keys():
        for j in Gb[i]:
            pair = get_pair(i, j, Jb)
            if Gb[i][j] == PLUS:
                G[pair]['x'] += tetta
            else:
                G[pair]['x'] -= tetta


# удаление из Jb случайного ребра со значением потока, равным 0
def change_Jb(Jb, G) -> None:
    for i, j in Jb:
        if G[(i, j)]['x'] == 0:
            Jb.remove([i, j])
            return


def print_with_colorful_text(text, data, color=Fore.MAGENTA) -> None:
    print(color + text + Style.RESET_ALL, data)


def print_vals(i, j, cycle, Gb, tetta, G, Jb) -> None:
    print_with_colorful_text('Делаем базисным ребро', (i+1, j+1))
    print_with_colorful_text('Цикл =\t', [i+1 for i in cycle])
    print(Fore.MAGENTA + 'Gb:' + Style.RESET_ALL)
    for i in Gb.keys():
        for j in Gb[i]:
            print((i+1, j+1), Gb[i][j])
    print_with_colorful_text('tetta =\t', tetta)
    print(Fore.MAGENTA + 'G с обновлёнными значениями x:' + Style.RESET_ALL)
    for i in G.keys():
        print((i[0]+1, i[1]+1), '-',  G[i])
    print_with_colorful_text('Jb:\t', Jb)


# стоимость = сумме cij * xij для базисных (i, j)
def print_count(G, Jb) -> None:
    count = 0
    for i, j in Jb:
        count += G[(i, j)]['x'] * G[(i, j)]['c']
    print(Fore.LIGHTGREEN_EX + 'Стоимость:' + Style.RESET_ALL + '\t', count)


def iterations(n, G, Jb) -> None:
    iteration = 1
    while True:
        print('\n' + Back.LIGHTMAGENTA_EX + Fore.BLACK + f'Итерация: {iteration}' + Style.RESET_ALL)
        iteration += 1
        u = get_u(n, G, Jb)
        print_with_colorful_text('u =\t', u)

        is_optimal, i, j = check_is_optimal(G, Jb, u)
        if is_optimal:
            print('\n' + Fore.MAGENTA + 'Текущий план оптимальный!' + Style.RESET_ALL + '\n')
            return

        Jb.append([i, j])
        Gb = make_Gb(Jb)
        cycle = get_cycle(Gb, i, j)
        Gb = delete_from_Gb_not_cycle(cycle)
        place_signs(n, Gb, Jb, (i, j))
        tetta = get_tetta(G, Gb, Jb)
        change_G(G, Gb, Jb, tetta)
        change_Jb(Jb, G)
        print_vals(i, j, cycle, Gb, tetta, G, Jb)
        print_count(G, Jb)


def print_answer(G, Jb) -> None:
    print(Back.LIGHTGREEN_EX + Fore.BLACK + '~~~Ответ~~~' + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX + 'Оптимальный план:' + Style.RESET_ALL)
    for i, j in sorted(Jb):
        print((i+1, j+1), '-', G[(i, j)]['x'])
    print_count(G, Jb)


if __name__ == '__main__':
    n, G, Jb = read_data()
    iterations(n, G, Jb)
    print_answer(G, Jb)
