import numpy as np
from colorama import Fore, Back, Style


def read_data(file_num='1'):
    file = open('input'+file_num+'.txt', 'r')
    s, t = [int(num) - 1 for num in file.readline().split()]
    n = int(file.readline())
    G = [{} for _ in range(n)]
    for line in file:
        x, y, z = [int(num) for num in line.split()]
        x -= 1
        y -= 1
        G[x][y] = max(G[x].setdefault(y, - np.inf), z)
    return s, t, G


def topological_sort(s, G):
    answer, visited = [], [False] * len(G)

    def dfs(v):
        visited[v] = True
        for next_v in G[v].keys():
            if not visited[next_v]:
                dfs(next_v)
        answer.append(v)

    dfs(s)

    return answer[::-1]


def find_path(s, sorted_list, G):
    n = len(sorted_list)
    l, prev = [-np.inf] * n, [0] * n
    l[sorted_list.index(s)], prev[sorted_list.index(s)] = 0, None

    for i in range(1, n):
        cur_v = sorted_list[i]
        for v in G[cur_v].keys():
            if v in sorted_list:
                prev_v = sorted_list.index(v)
                if G[cur_v][v] + l[prev_v] > l[i]:
                    l[i], prev[i] = G[cur_v][v] + l[prev_v], v

    return l, prev


def print_path(l, prev, s, t, sorted_list):
    print('\n' + Back.GREEN + Fore.BLACK + 'Длина пути:\t' + str(l[sorted_list.index(t)]) + Style.RESET_ALL)
    path = [t+1]
    while t != s:
        t = prev[sorted_list.index(t)]
        path.append(t+1)
    print('\n' + Back.GREEN + Fore.BLACK + 'Путь:\t' + str(path[::-1]) + Style.RESET_ALL)


def print_l_prev(l, prev):
    prev_printed = []
    for num in prev:
        if num is not None:
            prev_printed.append(num + 1)
        else:
            prev_printed.append(num)
    print(Fore.MAGENTA + '\nl =\t' + Style.RESET_ALL, l, '\n' + Fore.MAGENTA + 'prev =\t' + Style.RESET_ALL,
          prev_printed)


def get_G_rev(sorted_list, G):
    G_rev = [{} for _ in range(len(G))]
    for i in range(len(G)):
        for v in G[i].keys():
            if i in sorted_list and v in sorted_list:
                G_rev[v][i] = max(G_rev[v].setdefault(i, - np.inf), G[i][v])
    # print(G_rev)
    return G_rev


if __name__ == '__main__':
    s, t, G = read_data('1')

    sorted_list = topological_sort(s, G)
    print(Fore.MAGENTA + 'Топологически отсортированные вершины:\n' + Style.RESET_ALL, [num+1 for num in sorted_list])

    if t not in sorted_list:
        print(Fore.RED + f'\nВершина {t + 1} недостижима из вершины {s + 1}!' + Style.RESET_ALL)
    else:
        i = sorted_list.index(t) + 1
        print('\n' + Fore.MAGENTA + 'Удаляем вершины, расположенные после t:' + Style.RESET_ALL + '\n',
              [num+1 for num in sorted_list[:i]])
        l, prev = find_path(s, sorted_list[:i], get_G_rev(sorted_list, G))
        print_l_prev(l, prev)
        print_path(l, prev, s, t, sorted_list)
