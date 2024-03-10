from typing import Dict
from typing import List
from typing import Optional

from xsdata.codegen.models import Attr
from xsdata.formats.dataclass.filters import Filters
from xsdata.formats.dataclass.generator import DataclassGenerator
from xsdata.models.config import GeneratorConfig
from xsdata.models.config import OutputFormat


class AttrsGenerator(DataclassGenerator):
    """Python attrs classes code generator.

    Args:
        config: The generator config instance

    Attributes:
        env: The jinja2 environment instance
        filters: The template filters instance
    """

    @classmethod
    def init_filters(cls, config: GeneratorConfig) -> Filters:
        """Initialize the filters instance by the generator configuration."""
        return AttrsFilters(config)


class AttrsFilters(Filters):
    FACTORY_KEY = "factory"
    DEFAULT_KEY = "default"

    @classmethod
    def build_class_annotation(cls, format: OutputFormat) -> str:
        """Build the class annotations."""
        result = super().build_class_annotation(format)
        result = result.replace("unsafe_hash=", "hash=")
        result = result.replace("@dataclass", "@attr.s")
        return result

    def field_definition(
        self,
        attr: Attr,
        ns_map: Dict,
        parent_namespace: Optional[str],
        parents: List[str],
    ) -> str:
        """Return the field definition with any extra metadata."""
        result = super().field_definition(attr, ns_map, parent_namespace, parents)
        return result.replace("field(", "attr.ib(")

    @classmethod
    def build_import_patterns(cls) -> Dict[str, Dict]:
        """Build import search patterns."""
        patterns = {"attr": {"__module__": [" attr.ib", "@attr.s"]}}
        patterns.update(super().build_import_patterns())

        return patterns
