from datetime import datetime
from operator import attrgetter
from unittest import TestCase

from attr import Factory
from xsdata.formats.dataclass.compat import class_types

from tests.fixtures import TypeC
from xsdata_attrs.bindings import XmlContext
from xsdata_attrs.compat import AnyElement
from xsdata_attrs.compat import Attrs
from xsdata_attrs.compat import DerivedElement


class AttrsTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.class_type = class_types.get_type("attrs")

    def test_class_type(self):
        self.assertIsInstance(self.class_type, Attrs)

    def test_property_any_element(self):
        self.assertIs(self.class_type.any_element, AnyElement)

    def test_property_derived_element(self):
        self.assertIs(self.class_type.derived_element, DerivedElement)

    def test_is_model(self):
        obj = AnyElement()
        self.assertTrue(self.class_type.is_model(obj))
        self.assertTrue(self.class_type.is_model(AnyElement))
        self.assertFalse(self.class_type.is_model(XmlContext))

    def test_get_fields(self):
        obj = TypeC(one="a", two=1.1, three=False, four=datetime.now())
        expected = ("one", "two", "three", "four", "any")
        get_name = attrgetter("name")

        from_obj = self.class_type.get_fields(obj)
        self.assertEqual(expected, tuple(map(get_name, from_obj)))

        from_type = self.class_type.get_fields(TypeC)
        self.assertEqual(expected, tuple(map(get_name, from_type)))

    def test_default_value(self):
        fields = self.class_type.get_fields(TypeC)

        self.assertIsNone(self.class_type.default_value(fields[0]))
        self.assertIsNone(self.class_type.default_value(fields[1]))
        self.assertTrue(self.class_type.default_value(fields[2]))
        self.assertEqual(Factory(list), self.class_type.default_value(fields[3]))
