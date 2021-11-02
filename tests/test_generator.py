import os
from pathlib import Path

from click.testing import CliRunner
from xsdata.cli import cli
from xsdata.models.config import GeneratorConfig
from xsdata.utils.testing import ClassFactory
from xsdata.utils.testing import FactoryTestCase

from xsdata_attrs.generator import AttrsGenerator


class AttrsGeneratorTests(FactoryTestCase):
    def setUp(self):
        super().setUp()
        config = GeneratorConfig()
        self.generator = AttrsGenerator(config)

    def test_render(self):
        classes = [
            ClassFactory.elements(2, package="foo"),
            ClassFactory.elements(3, package="foo"),
        ]

        classes[0].attrs[0].restrictions.max_occurs = 3

        iterator = self.generator.render(classes)

        actual = [(out.path, out.title, out.source) for out in iterator]

        expected = (
            "import attr\n"
            "from typing import List, Optional\n"
            "\n"
            '__NAMESPACE__ = "xsdata"\n'
            "\n"
            "\n"
            "@attr.s\n"
            "class ClassB:\n"
            "    class Meta:\n"
            '        name = "class_B"\n'
            "\n"
            "    attr_b: List[str] = attr.ib(\n"
            "        factory=list,\n"
            "        metadata={\n"
            '            "name": "attr_B",\n'
            '            "type": "Element",\n'
            '            "max_occurs": 3,\n'
            "        }\n"
            "    )\n"
            "    attr_c: Optional[str] = attr.ib(\n"
            "        default=None,\n"
            "        metadata={\n"
            '            "name": "attr_C",\n'
            '            "type": "Element",\n'
            "        }\n"
            "    )\n"
            "\n"
            "\n"
            "@attr.s\n"
            "class ClassC:\n"
            "    class Meta:\n"
            '        name = "class_C"\n'
            "\n"
            "    attr_d: Optional[str] = attr.ib(\n"
            "        default=None,\n"
            "        metadata={\n"
            '            "name": "attr_D",\n'
            '            "type": "Element",\n'
            "        }\n"
            "    )\n"
            "    attr_e: Optional[str] = attr.ib(\n"
            "        default=None,\n"
            "        metadata={\n"
            '            "name": "attr_E",\n'
            '            "type": "Element",\n'
            "        }\n"
            "    )\n"
            "    attr_f: Optional[str] = attr.ib(\n"
            "        default=None,\n"
            "        metadata={\n"
            '            "name": "attr_F",\n'
            '            "type": "Element",\n'
            "        }\n"
            "    )\n"
        )

        self.assertEqual(2, len(actual))
        self.assertEqual(3, len(actual[1]))

        self.assertEqual("foo.tests", actual[1][1])
        self.assertEqual(expected, actual[1][2])

    def test_with_unsafe_hash(self):
        config = GeneratorConfig()
        config.output.format.unsafe_hash = True
        self.generator = AttrsGenerator(config)

        iterator = self.generator.render(ClassFactory.list(1))
        actual = [(out.path, out.title, out.source) for out in iterator]
        self.assertTrue("@attr.s(hash=True)" in actual[1][2])

    def test_complete(self):
        runner = CliRunner()
        schema = Path(__file__).parent.joinpath("fixtures/schemas/po.xsd")
        os.chdir(Path(__file__).parent.parent)

        result = runner.invoke(
            cli,
            [
                str(schema),
                "--package",
                "tests.fixtures.po.models",
                "--structure-style=single-package",
                "--output",
                "attrs",
                "--config",
                "tests/fixtures/attrs.conf.xml",
            ],
        )

        self.assertIsNone(result.exception)
