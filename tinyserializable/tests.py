import json
import unittest
import typing
from tinyserializable import BaseModel

class TestTinySerializable(unittest.TestCase):
    
    def test_base_attrs(self):
        "BaseModel, when setting attributes at constructor, sets proper defined properties"
        class TestModel(BaseModel):
            field_int: int
            field_string: str
            field_list: typing.List[str]
            
        expected_int = 12
        expected_string = "test"
        expected_list = ["t", "e", "s", "t"]
            
        t1 = TestModel(
            field_int = expected_int,
            field_string = expected_string,
            field_list = expected_list
        )
        
        self.assertEqual(t1.field_int, expected_int)
        self.assertEqual(t1.field_string, expected_string)
        self.assertEqual(t1.field_list, expected_list)
        
    def test_no_forced_types(self):
        "BaseModel, when setting attributes, does not enforce hinted types"
        class TestModel(BaseModel):
            field_int: int
            
        t1 = TestModel()
        
        t1.field_int = "test"
        t1.field_int = 0.2
        t1.field_int = {"test_key": "test_val"}
        
    def test_unset_property_nulls(self):
        "BaseModel, when property not set, does not initialize it, and always returns null"
        class TestModel(BaseModel):
            field_int: int
            
        t1 = TestModel()
        
        self.assertEqual(t1.field_int, None)
        
    def test_properties_available_through_underlying_dict(self):
        "BaseModel properties can be accessed like regular dictionary"
        class TestModel(BaseModel):
            field_int: int
            field_string: str
            field_list: typing.List[str]
            
        expected_int = 12
        expected_string = "test"
        expected_list = ["t", "e", "s", "t"]
            
        t1 = TestModel(
            field_int = expected_int,
            field_string = expected_string,
            field_list = expected_list
        )
        
        self.assertEqual(t1['field_int'], expected_int)
        self.assertEqual(t1['field_string'], expected_string)
        self.assertEqual(t1['field_list'], expected_list)
        
    def test_use_default_value(self):
        "BaseModel, when initialized withour property value, uses default value, if set"
        class TestModel(BaseModel):
            field_int: int
            field_string: str = "default"
            field_list: typing.List[str]
            
        t1 = TestModel()
        
        self.assertEqual(t1.field_int, None)
        self.assertEqual(t1.field_string, "default")
        self.assertEqual(t1.field_list, None)
        
    def test_construct_overrides_default_value(self):
        "BaseModel, init arguments override default values"
        class TestModel(BaseModel):
            field_int: int
            field_string: str = "default"
            field_list: typing.List[str]
            
        t1 = TestModel({'field_string': "override"})
        
        self.assertEqual(t1.field_int, None)
        self.assertEqual(t1['field_string'], "override")
        self.assertEqual(t1.field_string, "override")
        self.assertEqual(t1.field_list, None)
        
    def test_ignores_undefined_fields(self):
        "BaseModel, when provided with undefined field, will ignore and load"
        class TestModel(BaseModel):
            field_int: int

        t1 = TestModel({"field_int": 1, "field_string": "abcdef"})

        self.assertEqual(t1.field_int, 1)

    def test_nested_objects_properly_loaded_from_dict(self):
        "BaseModel, when loading from dict on construct, properly loads nested BaseModel objects"
        class TestNestedModel(BaseModel):
            nested_string: str

        class TestModel(BaseModel):
            field_int: int
            field_string: str
            field_list: typing.List[str]
            field_nested: TestNestedModel
            
        initial_data = {
            "field_int": 12,
            "field_string": "test",
            "field_list": ["t", "e", "s", "t"],
            "field_nested": {
                "nested_string": "nested"
                }
            }
        
        loaded_object = TestModel(**initial_data)
        
        self.assertIsInstance(loaded_object.field_nested, TestNestedModel)
        
    def test_nested_objects_properly_loaded_from_list(self):
        "BaseModel, when loading from dict on construct, properly loads nested list of BaseModel objects"
        class TestNestedModel(BaseModel):
            nested_string: str

        class TestModel(BaseModel):
            field_int: int
            field_nested: typing.List[TestNestedModel]

        initial_data = {
            "field_int": 12,
            "field_nested": [
                {
                    "nested_string": "nested"
                },
                {
                    "nested_string": "second nested"
                }
            ]
        }

        loaded_object = TestModel(**initial_data)

        expected_loaded_object_nested_list = [
            TestNestedModel(nested_string = "nested"),
            TestNestedModel(nested_string = "second nested")
        ]

        self.assertIsInstance(loaded_object.field_nested, list)
        self.assertListEqual(loaded_object.field_nested, expected_loaded_object_nested_list)

    def test_nested_objects_not_regenerated_from_list(self):
        "BaseModel, when loading dict on construct, does not regenerate BaseModel on nested list of BaseModel objects, if not needed"
        class TestNestedBaseModel(BaseModel):
            pass

        class TestNestedModel(BaseModel):
            nested_string: str

        class TestModel(BaseModel):
            field_int: int
            field_nested: typing.List[TestNestedBaseModel]

        initial_object = TestModel(
            field_int = 12,
            field_nested = [
                TestNestedModel(nested_string = "nested"),
                TestNestedModel(nested_string = "nested")
            ]
        )

        self.assertIsInstance(initial_object.field_nested[0], TestNestedModel)
        self.assertIsInstance(initial_object.field_nested[1], TestNestedModel)

    def test_allow_property_getter(self):
        "BaseModel allows defining property getters"
        class TestModel(BaseModel):
            field_int: int
            
            @property
            def FieldInt(self) -> int:
                return self.field_int + 3
        
        t1 = TestModel(field_int = 12)
        
        self.assertEqual(t1['field_int'], 12)
        self.assertEqual(t1.FieldInt, 15)
        
    def test_allow_property_setter(self):
        "BaseModel allows defining property setters"
        class TestModel(BaseModel):
            field_int: int
            
            @property
            def FieldInt(self) -> int:
                return self.field_int + 3
            @FieldInt.setter
            def FieldInt(self, newvalue: int):
                self.field_int = newvalue - 3
        
        t1 = TestModel(field_int = 12)
        t1.FieldInt = 8
        
        self.assertEqual(t1.field_int, 5)
        
    def test_serializes_to_json(self):
        "BaseModel correctly serializes to json string"
        class TestNestedModel(BaseModel):
            nested_string: str

        class TestModel(BaseModel):
            field_int: int
            field_string: str
            field_list: typing.List[str]
            field_nested: TestNestedModel
            
        t1 = TestModel(
            field_int = 12,
            field_string = "test",
            field_list = ["t", "e", "s", "t"],
            field_nested = TestNestedModel(
                nested_string = "nested"
            )
        )
        
        expected_json_string = """{"field_int": 12, "field_string": "test", "field_list": ["t", "e", "s", "t"], "field_nested": {"nested_string": "nested"}}""".strip()
        
        serialized = json.dumps(t1)
        
        self.assertEqual(serialized, expected_json_string)
        
    def test_deserializes_from_json(self):
        "BaseModel correctly deserializes from json string"
        class TestNestedModel(BaseModel):
            nested_string: str

        class TestModel(BaseModel):
            field_int: int
            field_string: str
            field_list: typing.List[str]
            field_nested: TestNestedModel
        
        json_string = """{"field_int": 12, "field_string": "test", "field_list": ["t", "e", "s", "t"], "field_nested": {"nested_string": "nested"}}""".strip()
        
        t1 = TestModel(json.loads(json_string))
        
        self.assertIsInstance(t1, TestModel)
        self.assertIsInstance(t1.field_nested, TestNestedModel)
        
        self.assertEqual(t1.field_int, 12)
        self.assertEqual(t1.field_string, "test")
        self.assertEqual(t1.field_list, ["t", "e", "s", "t"])
        self.assertEqual(t1.field_nested.nested_string, "nested")