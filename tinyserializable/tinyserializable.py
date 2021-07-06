import json
import typing

class BaseModel(dict):
    def __init__(self, __data_dict=None, **kwargs):
        super().__init__()
        self.__construct_default_values()

        if isinstance(__data_dict, dict):
            construct_data = __data_dict
        else:
            construct_data = kwargs

        for k,v in construct_data.items():
            self.__construct_field(k, v)

    def __repr__(self):
        return f'{type(self).__name__}<{super().__repr__()}>'

    def __dir__(self):
        return set(super().__dir__() + list(typing.get_type_hints(self.__class__).keys()))

    def __construct_default_values(self):
        for k, v in self.__class__.__dict__.items():
            if k in typing.get_type_hints(self.__class__).keys():
                self.__construct_field(k, v)

    def __construct_field(self, k, v):
        if self.__is_serializable_object_field(k) and isinstance(v, dict):
            field_type = self.__get_field_class(k)
            self.__setattr__(k,field_type(v))
        elif self.__is_serializable_object_list_field and isinstance(v, list):
            field_component_type = self.__get_field_list_component_class(k)
            self.__setattr__(k, [field_component_type(element) for element in v])
        elif self.__is_defined_field(k):
            self.__setattr__(k,v)

    def __is_serializable_object_field(self, key):
        field_type = typing.get_type_hints(self).get(key, None)
        if field_type is None: return False
        try:
            if issubclass(field_type, BaseModel): return True
        except TypeError:
            pass
        return False

    def __is_serializable_object_list_field(self, key):
        field_type = typing.get_type_hints(self).get(key, None)
        if field_type is None: return False

        if (field_origin_type := typing.get_origin) is None: return False
        if not issubclass(field_origin_type, list): return False

        field_component_type = field_type.__args__[0]
        try:
            if issubclass(field_component_type, BaseModel): return True
        except TypeError:
            pass
        return False

    def __is_defined_field(self, key):
        return key in typing.get_type_hints(self.__class__).keys()

    def __get_field_class(self, key):
        return typing.get_type_hints(self.__class__).get(key, dict)

    def __get_field_list_component_class(self, key):
        return typing.get_type_hints(self.__class__)[key].__args__[0]

    def __is_property(self, key):
        try:
            return isinstance(object.__getattribute__(self.__class__, key), property)
        except AttributeError:
            return False

    def __setattr__(self, key, val):
        if key in typing.get_type_hints(self.__class__).keys():
            self.__setitem__(key,val)
        elif self.__is_property(key):
            object.__setattr__(self, key, val)
        else:
            raise AttributeError(f'Not a valid attribute: {key}')
    
    def __getattribute__(self, key):
        model_class = dict.__getattribute__(self, '__class__')
        if key in typing.get_type_hints(model_class).keys():
            return dict.get(self, key, model_class.__dict__.get(key, None))
        return dict.__getattribute__(self, key)