# coding: utf-8
"""
配置相关
"""
from .import_util import import_object


class Configurable(object):
    """
    from tornado
    """
    __impl_class = None
    __impl_kwargs = None

    def __new__(cls, *args, **kwargs):
        base = cls.configurable_base()
        init_kwargs = {}
        if cls is base:
            impl = cls.configured_class()
            if base.__impl_kwargs:
                init_kwargs.update(base.__impl_kwargs)
        else:
            impl = cls
        init_kwargs.update(kwargs)
        if impl.configurable_base() is not base:
            return impl(*args, **init_kwargs)
        instance = super(Configurable, cls).__new__(impl)
        instance.initialize(*args, **init_kwargs)
        return instance

    @classmethod
    def configurable_base(cls):
        raise NotImplementedError()

    @classmethod
    def configurable_default(cls):
        raise NotImplementedError()

    def initialize(self):
        """
        """

    @classmethod
    def configure(cls, impl, **kwargs):
        base = cls.configurable_base()
        if isinstance(impl, (str, unicode)):
            impl = import_object(impl)
        if impl is not None and not issubclass(impl, cls):
            raise ValueError("Invalid subclass of %s" % cls)
        base.__impl_class = impl
        base.__impl_kwargs = kwargs

    @classmethod
    def configured_class(cls):
        base = cls.configurable_base()
        if base.__dict__.get('_Configurable__impl_class') is None:
            base.__impl_class = cls.configurable_default()
        return base.__impl_class

    @classmethod
    def _save_configuration(cls):
        base = cls.configurable_base()
        return (base.__impl_class, base.__impl_kwargs)

    @classmethod
    def _restore_configuration(cls, saved):
        base = cls.configurable_base()
        base.__impl_class = saved[0]
        base.__impl_kwargs = saved[1]
