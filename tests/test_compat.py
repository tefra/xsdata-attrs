from datetime import datetime
from operator import attrgetter
from unittest import TestCase

from xsdata.exceptions import XmlContextError
from xsdata.formats.dataclass.compat import class_types

from tests.fixtures.common import TypeC
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

    def test_verify_model(self):
        obj = AnyElement()
        self.class_type.verify_model(obj)

        with self.assertRaises(XmlContextError) as cm:
            self.class_type.verify_model(int)

        self.assertEqual(
            "Type '<class 'int'>' is not an attrs model.", str(cm.exception)
        )

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
        self.assertEqual(list, self.class_type.default_value(fields[3]))

    def test_default_choice_value(self):
        choice = {}
        self.assertIsNone(self.class_type.default_choice_value(choice))

        choice["factory"] = 1
        self.assertIsNone(self.class_type.default_choice_value(choice))

        choice["default"] = 1
        self.assertEqual(1, self.class_type.default_choice_value(choice))

        choice["factory"] = lambda: 2

        default = self.class_type.default_choice_value(choice)
        self.assertTrue(callable(default))
        self.assertEqual(2, default())
