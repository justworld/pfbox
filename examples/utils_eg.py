# coding: utf-8
"""
工具框架使用示例
"""

#######  import example  ######
from pythonframework.utils.import_util import import_object

join = import_object('os.path.join')
print join('fold', 'file')
