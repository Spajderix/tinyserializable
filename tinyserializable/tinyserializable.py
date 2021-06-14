import json
import typing
import logging

_log = logging.getLogger(__name__)

class BaseModel(dict):
    def __init__(self, data_dict=None, **kwargs):
        super().__init__()
        self.__construct_default_values()

        if isinstance(data_dict, dict):
            construct_data = data_dict
        else:
            construct_data = kwargs

        for k,v in construct_data.items():
            self.__construct_field(k, v)

    def __repr__(self):
        return f'{type(self).__name__}<{super().__repr__()}>'

    def __dir__(self):
        if _log.getEffectiveLevel() == logging.DEBUG:
            return super().__dir__() + list(typing.get_type_hints(self.__class__).keys())
        else:
            return list(typing.get_type_hints(self.__class__).keys())

    def __construct_default_values(self):
        for k, v in self.__class__.__dict__.items():
            if k in typing.get_type_hints(self.__class__).keys():
                self.__construct_field(k, v)

    def __construct_field(self, k, v):
        if self.__is_serializable_object_field(k) and isinstance(v, dict):
            field_type = self.__get_field_class(k)
            self.__setattr__(k,field_type(v))
        else:
            self.__setattr__(k,v)

    def __is_serializable_object_field(self, key):
        field_type = typing.get_type_hints(self).get(key, None)
        if field_type is None: return False
        try:
            if issubclass(field_type, BaseModel): return True
        except TypeError:
            pass
        return False

    def __get_field_class(self, key):
        return typing.get_type_hints(self.__class__).get(key, dict)

    def __setattr__(self, key, val):
        if not key in typing.get_type_hints(self.__class__).keys():
            raise AttributeError(f'Not a valid attribute: {key}')
        self.__setitem__(key,val)

    def __getattr__(self, key):
        if key not in typing.get_type_hints(self.__class__).keys():
            raise AttributeError(f'Not a valid attribute: {key}')
        return self.get(key, self.__class__.__dict__.get(key, None))