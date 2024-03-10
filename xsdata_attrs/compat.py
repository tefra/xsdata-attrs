from typing import Any
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar

import attr
from xsdata.exceptions import XmlContextError
from xsdata.formats.dataclass.compat import ClassType
from xsdata.formats.dataclass.models.elements import XmlType

T = TypeVar("T", bound=object)


@attr.s
class AnyElement:
    """Generic model to bind xml document data to wildcard fields.

    Args:
        qname: The element's qualified name
        text: The element's text content
        tail: The element's tail content
        children: The element's list of child elements.
        attributes: The element's key-value attribute mappings.
    """

    qname: Optional[str] = attr.ib(default=None)
    text: Optional[str] = attr.ib(default=None)
    tail: Optional[str] = attr.ib(default=None)
    children: List[object] = attr.ib(factory=list, metadata={"type": XmlType.WILDCARD})
    attributes: Dict[str, str] = attr.ib(
        factory=dict, metadata={"type": XmlType.ATTRIBUTES}
    )


@attr.s
class DerivedElement(Generic[T]):
    """Generic model wrapper for type substituted elements.

    Example: eg. <b xsi:type="a">...</b>

    Args:
        qname: The element's qualified name
        value: The wrapped value
        type: The real xsi:type
    """

    qname: str = attr.ib()
    value: T = attr.ib()
    type: Optional[str] = attr.ib(default=None)


class Attrs(ClassType):
    """The attrs class type."""

    @property
    def any_element(self) -> Type:
        """Return the AnyElement used to bind wildcard element nodes."""
        return AnyElement

    @property
    def derived_element(self) -> Type:
        """Return the DerivedElement used to bind ambiguous element nodes."""
        return DerivedElement

    def is_model(self, obj: Any) -> bool:
        """Return whether the given value is binding model."""
        return attr.has(obj if isinstance(obj, type) else type(obj))

    def verify_model(self, obj: Any):
        """Verify the given value is a binding model.

        Args:
            obj: The input model instance

        Raises:
            XmlContextError: if not supported
        """
        if not self.is_model(obj):
            raise XmlContextError(f"Type '{obj}' is not an attrs model.")

    def get_fields(self, obj: Any) -> Tuple[Any, ...]:
        """Return the models fields in the correct mro ordering."""
        if not isinstance(obj, type):
            return self.get_fields(type(obj))

        # Emulate dataclasses fields ordering
        fields = {}
        for b in obj.__mro__[-1:0:-1]:
            if self.is_model(b):
                for f in self.get_fields(b):
                    fields[f.name] = f

        for f in attr.fields(obj):
            fields[f.name] = f

        return tuple(fields.values())

    def default_value(
        self, field: attr.Attribute, default: Optional[Any] = None
    ) -> Any:
        """Return the default value or factory of the given model field."""
        res = field.default
        if res is attr.NOTHING:
            return default

        if isinstance(res, attr.Factory):  # type: ignore
            return res.factory  # type: ignore

        return res

    def default_choice_value(self, choice: Dict) -> Any:
        """Return the default value or factory of the given model field choice."""
        factory = choice.get("factory")
        if callable(factory):
            return factory

        return choice.get("default")
