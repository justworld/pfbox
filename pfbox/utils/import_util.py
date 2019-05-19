# coding: utf-8
"""
导入相关
"""


def import_object(name):
    """
    from tornado
    Imports an object by name.

    import_object('x') is equivalent to 'import x'.
    import_object('x.y.z') is equivalent to 'from x.y import z'.

    >>> import_object('os.path') is os.path
    True
    >>> import_object('os.path.join') is os.path.join
    True
    >>> import_object('os') is os
    True
    >>> import_object('os.missing_module')
    Traceback (most recent call last):
        ...
    ImportError: No module named missing_module
    """
    if not isinstance(name, str):
        name = name.encode('utf-8')
    if name.count('.') == 0:
        return __import__(name)

    parts = name.split('.')
    obj = __import__('.'.join(parts[:-1]), fromlist=[parts[-1]])
    try:
        return getattr(obj, parts[-1])
    except AttributeError:
        raise ImportError("No module named %s" % parts[-1])
