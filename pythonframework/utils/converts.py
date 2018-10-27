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
                    v = list_unpack(v)
                if isinstance(v, dict):
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
    [{'a': [1,2], 'b': 1}, {'a': 2, 'b': 2}] > {'a':[1,2,1], 'b':[1,2]}
    [{'a': {'c':[1,2], 'b':2}, 'b': 1}, {'a': 2, 'b': 2}] > {'a':2, 'b':[1,2], 'c':[1,2]}
    将多维的list类型数据拆包成一维dict或list
    """
    res_data = defaultdict(list)
    if isinstance(list_data, list):
        for i in list_data:
            if isinstance(i, dict):
                dict_data = dict_unpack(i)
                for k, v in dict_data.items():
                    if isinstance(v, list):
                        for vv in v:
                            res_data[k].append(vv)
                    else:
                        res_data[k].append(v)
            else:
                return list_data

        return dict(res_data)

    return None
