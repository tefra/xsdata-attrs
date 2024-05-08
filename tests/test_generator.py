import os
from pathlib import Path

from click.testing import CliRunner
from xsdata.cli import cli
from xsdata.models.config import GeneratorConfig
from xsdata.utils.testing import FactoryTestCase

from xsdata_attrs.generator import AttrsGenerator


class AttrsGeneratorTests(FactoryTestCase):
    def setUp(self):
        super().setUp()
        config = GeneratorConfig()
        self.generator = AttrsGenerator(config)

    def test_generator(self):
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
