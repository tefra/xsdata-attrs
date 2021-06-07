from xsdata.codegen.writer import CodeWriter

from xsdata_attrs.generator import AttrsGenerator

CodeWriter.register_generator("attrs", AttrsGenerator)
