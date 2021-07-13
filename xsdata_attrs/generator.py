from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from xsdata.codegen.models import Attr
from xsdata.formats.dataclass.filters import Filters
from xsdata.formats.dataclass.generator import DataclassGenerator
from xsdata.models.config import GeneratorConfig
from xsdata.models.config import OutputFormat
from xsdata.models.mixins import attribute


class AttrsGenerator(DataclassGenerator):
    """Python attrs classes code generator."""

    @classmethod
    def init_filters(cls, config: GeneratorConfig) -> Filters:
        return AttrsFilters(config)


@dataclass
class AttrsOutputFormat(OutputFormat):
    slots: bool = attribute(default=True)
    cache_hash: bool = attribute(default=False)
    kw_only: bool = attribute(default=False)


class AttrsFilters(Filters):
    FACTORY_KEY = "factory"
    DEFAULT_KEY = "default"

    @classmethod
    def build_class_annotation(cls, format: OutputFormat) -> str:
        args = []

        if not format.repr:
            args.append("repr=False")
        if not format.eq:
            args.append("eq=False")
        if format.order:
            args.append("order=True")
        if format.unsafe_hash:
            args.append("unsafe_hash=True")
        if format.frozen:
            args.append("frozen=True")

        if isinstance(format, AttrsOutputFormat):
            if format.slots:
                args.append("slots=True")
            if format.kw_only:
                args.append("kw_only=True")
            if format.cache_hash:
                args.append("cache_hash=True")

        return f"@attr.s({', '.join(args)})" if args else "@attr.s"

    def field_definition(
        self,
        attr: Attr,
        ns_map: Dict,
        parent_namespace: Optional[str],
        parents: List[str],
    ) -> str:
        result = super().field_definition(attr, ns_map, parent_namespace, parents)

        return result.replace("field(", "attr.ib(")

    def field_default_value(self, attr: Attr, ns_map: Optional[Dict] = None) -> Any:
        result = super().field_default_value(attr, ns_map)
        if isinstance(self.format, AttrsOutputFormat):
            if self.format.kw_only and not attr.restrictions.is_optional:
                return False

        return result

    @classmethod
    def build_import_patterns(cls) -> Dict[str, Dict]:
        patterns = {"attr": {"__module__": [" attr.ib", "@attr.s"]}}

        patterns.update(super().build_import_patterns())
        return patterns
