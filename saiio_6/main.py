import numpy as np
from heapq import heapify, heappop, _siftdown
from colorama import Fore, Back, Style


def read_data(file_num='') -> tuple:
    file = open('input'+file_num+'.txt', 'r')
    n = int(file.readline())
    s = int(file.readline()) - 1
    G = [[] for _ in range(n)]
    for line in file:
        x, y, z = [int(num) for num in line.split()]
        G[x-1].append([y-1, z])
    return n, s, G


def renew_dist(heap, prev, l, G, value) -> None:
    for i, length in G[value[1]]:
        if (l[i], i) in heap and l[i] > value[0] + length:
            index = heap.index((l[i], i))
            prev[i], l[i] = value[1], value[0] + length
            heap[index] = (value[0] + length, i)
            _siftdown(heap, 0, index)


def deikstra(n, s, G) -> tuple:
    prev, l = [None] * n, [np.inf] * n
    l[s] = 0
    heap = [(np.inf, i) for i in range(n)]
    heap[s] = (0, s)
    heapify(heap)

    while len(heap) > 0:
        value = heappop(heap)
        if value[1] == np.inf:
            break
        renew_dist(heap, prev, l, G, value)

    return prev, l


def print_result(prev, l):
    for i, num in enumerate(prev):
        if num is not None:
            prev[i] += 1
    print(Back.MAGENTA + Fore.BLACK + "prev =" + Style.RESET_ALL + "\t", prev, '\n')
    print(Back.GREEN + Fore.BLACK + "Длины путей из s: " + Style.RESET_ALL + "\t", l)


if __name__ == '__main__':
    n, s, G = read_data('1')
    prev, l = deikstra(n, s, G)

    print_result(prev, l)
