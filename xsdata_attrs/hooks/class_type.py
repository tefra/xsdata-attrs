from xsdata.formats.dataclass.compat import class_types

from xsdata_attrs.compat import Attrs

class_types.register("attrs", Attrs())
