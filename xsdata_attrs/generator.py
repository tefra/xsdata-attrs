from typing import List

from xsdata.codegen.models import Class
from xsdata.codegen.resolver import DependenciesResolver
from xsdata.formats.dataclass.generator import DataclassGenerator


class AttrsGenerator(DataclassGenerator):
    """attrs generator."""

    def render_module(
        self, resolver: DependenciesResolver, classes: List[Class]
    ) -> str:
        result = super().render_module(resolver, classes)

        replacements = (
            ("from dataclasses import dataclass, field", "import attr"),
            ("from dataclasses import dataclass", "import attr"),
            ("@dataclass", "@attr.s"),
            (" = field(", " = attr.ib("),
            ("default_factory=", "factory="),
        )

        for search, replace in replacements:
            result = result.replace(search, replace)

        return result
