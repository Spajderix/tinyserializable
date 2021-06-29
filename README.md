# Purpose

The library is designed to serve as a baseline for serializable data structures. For complex data structures it is advised to write custom handlers, as the library is limited in capability, but for some simple structures, it should provide a nice building block to speed up development/serialization of data.

# Quick start

Simply define a class that inherits from `BaseModel`, and annotate any attributes with their appropriate types. It supports all base types like `str`, `int`, `float` as well as nested `BaseModel` based structures. It will forbid from setting an attribute that is not defined, but it will not validate types of values assigned to it. It's based on `dict`, so you can also operate on it just as it would've been a regular dictionary. This has an added bonus of being able to pass directly to functions like `json.dumps`. Examples listed below should make it easy to understand and follow

# Examples

## Basic Class

```python
from tinyserializable import BaseModel
import json

class Test(BaseModel):
    id: int,
    name: str

t1 = Test(id = 5, name="foo")

t1
# Test<{'id': 1, 'name': 'foo'}>
json.dumps(t1)
# {"id": 1, "name": "foo"}
```

## Nested structures

```python
class SubTest(BaseModel):
    sub_type: str

class Test(BaseModel):
    id: int
    name: str
    sub: SubTest
    
t1 = Test(id = 1, name = "foo", sub = SubTest(sub_type = "bar"))

t1.sub.sub_type
# bar
json.dumps(t1)
# {"id": 1, "name": "foo", "sub": {"sub_type": "bar"}}
```

## Inheritance

```python
class SubTest(BaseModel):
    sub_type: str
    
class ChildSubTest(SubTest):
    value: float

class Test(BaseModel):
    id: int
    name: str
    sub: ChildSubTest
    
t1 = Test(id = 1, name = "foo", sub = ChildSubTest(sub_type = "bar", value = 30))

t1.sub.value
# 30
json.dumps(t1)
# {"id": 1, "name": "foo", "sub": {"sub_type": "bar", "value": 30}}
```

## De-serializing

```python
raw_json = '{"id": 1, "name": "foo", "sub": {"sub_type": "bar", "value": 30}}'
t1 = Test(json.loads(raw_json))

t1.name
# foo
t1
# Test<{'id': 1, 'name': 'foo', 'sub': ChildSubTest<{'sub_type': 'bar', 'value': 30}>}>
```

## Properties

It's allowed to define property getters and setters, but those will not be externalized when serializing

```python
class SubTest(BaseModel):
    sub_type: str
    
    @property
    def SubType(self) -> str:
        return self.sub_type.upper()
    @SubType.setter
    def SubType(self, newvalue: str):
        self.sub_type = newvalue.lower()

class Test(BaseModel):
    id: int
    name: str
    sub: SubTest
    
t1 = Test(id = 1, name = "foo", sub = SubTest(sub_type = "bar"))

t1.sub.sub_type
# bar
t1.sub.SubType 
# BAR
t1.sub.SubType = "BaZ"
t1.sub.sub_type
# baz
t1.sub.SubType
# BAZ
json.dumps(t1)
# {"id": 1, "name": "foo", "sub": {"sub_type": "baz"}}
```
