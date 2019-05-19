# coding: utf-8
"""
排序
python 默认sort用的是TimSort
"""


def quick_sort(sort_list):
    """
    快速排序，最坏O(n2)，不稳定，尝试用TimSort替代
    """
    if not sort_list:
        return sort_list

    length = len(sort_list)
    if length == 1:
        return sort_list

    low = 0
    high = length - 1

    def _quick_sort(sort_list, low, high):
        if low < high:
            # 基准值
            pivot = sort_list[low]
            i, j = low, high
            while (i < j):
                while (i < j and sort_list[j] >= pivot):
                    j -= 1
                sort_list[i] = sort_list[j]
                while (i < j and sort_list[i] <= pivot):
                    i += 1
                sort_list[j] = sort_list[i]

            sort_list[i] = pivot

            _quick_sort(sort_list, low, i - 1)
            _quick_sort(sort_list, i + 1, high)

    _quick_sort(sort_list, low, high)


def tim_sort():
    """
    最坏O(nlogn)
    todo: 实现TimSort
    """
    pass
