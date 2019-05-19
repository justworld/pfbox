# coding: utf-8
from collections import defaultdict


def json_unpack(ori_data):
    """
    unpack json
    'test' > 'test'
    [1, 2, 3] > [1, 2, 3]
    {'a':1, 'b':1} > {'a':1, 'b':1}
    [{'a':1, 'b':1},{'a':2, 'b':2}] > {'a':[1,2],'b':[1,2]}
    {'data':[{'a':1, 'b':1},{'a':2, 'b':2}]} > {'a':[1,2],'b':[1,2]}

    拆分数据, 将多维的dict或list拆分成一维dict或list
    可能有性能问题
    """
    if isinstance(ori_data, dict):
        return dict_unpack(ori_data)

    if isinstance(ori_data, list):
        return list_unpack(ori_data)

    return ori_data


def dict_unpack(dict_data):
    """
    unpack dict
    {'a':1, 'b':1} > {'a':1, 'b':1}
    {'data':[{'a':1, 'b':1},{'a':2, 'b':2}]} > {'a':[1,2],'b':[1,2]}
    {'data': [{'a': 1, 'b': 1}, {'a': 2, 'b': 2}], 'data1': {'a': 1, 'b': 1}} > {'a':[1,2,1], 'b':[1,2,1]}
    {'data': {'a': {'a':{'test':1}}, 'b': 1}} > {'test':1, 'b':1}
    将多维的dict类型数据拆包成一维dict
    """
    res_data = dict()
    is_loop = True
    if isinstance(dict_data, dict):
        while is_loop:
            is_loop = False
            for k, v in dict_data.items():
                if isinstance(v, list):
                    # 如果是list类型，先unpack
                    # 递归，这之后是一维dict或list
                    v = list_unpack(v)
                if isinstance(v, dict):
                    # 如果是dict类型，要重新循环一遍
                    is_loop = True
                    if isinstance(v, dict):
                        for kk, vv in v.items():
                            res_data[kk] = vv
                else:
                    res_data[k] = v

            dict_data = res_data

        return res_data

    return None


def list_unpack(list_data):
    """
    unpack list
    [1, 2, 3] > [1, 2, 3]
    [{'a':1, 'b':1},{'a':2, 'b':2}] > {'a':[1,2],'b':[1,2]}
    [{'a': [1,2], 'b': 1}, {'a': 2, 'b': 2}] > {'a':[1,2 ,2], 'b':[1,2]}
    将多维的list类型数据拆包成一维dict或list
    """

    if isinstance(list_data, list):
        if len(list_data) > 1:
            first = list_data[0]
            if isinstance(first, dict):
                # 递归，这之后是一维dict
                res_data = defaultdict(list)
                for i in list_data:
                    dict_data = dict_unpack(i)
                    for k, v in dict_data.items():
                        if isinstance(v, list):
                            for vv in v:
                                res_data[k].append(vv)
                        else:
                            res_data[k].append(v)

                return dict(res_data)

            else:
                return list_data

    return None
