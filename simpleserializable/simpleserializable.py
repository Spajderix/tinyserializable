import json
import typing

class SimpleSerializableObject(dict):
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
        return super().__dir__() + list(self.__annotations__.keys())

    def __construct_default_values(self):
        for k, v in self.__class__.__dict__.items():
            if k in typing.get_type_hints(self).keys():
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
            if issubclass(field_type, SimpleSerializableObject): return True
        except TypeError:
            pass
        return False

    def __get_field_class(self, key):
        return typing.get_type_hints(self).get(key, dict)

    def __setattr__(self, key, val):
        if not key in typing.get_type_hints(self).keys():
            raise AttributeError(f'Not a valid attribute: {key}')
        self.__setitem__(key,val)

    def __getattr__(self, key):
        if key not in self.__annotations__.keys():
            raise AttributeError(f'Not a valid attribute: {key}')
        return self.get(key, self.__class__.__dict__.get(key, None))



class Person(SimpleSerializableObject):
    name: str
    last_name: str
    sex: typing.Optional[str]
    employed: typing.Union[str, bool] = True
    job_history: typing.Dict


class Employee(SimpleSerializableObject):
    personal_info: Person
    active: bool



p1 = Person(name = 'ka', last_name = 'er')
e1 = Employee(active = True, personal_info = p1)

e2 = Employee(active = False, personal_info = {
    'name': 'Arturito',
    'employed': False
})


if __name__ == '__main__':
    print('t')
