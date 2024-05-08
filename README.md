[![image](https://github.com/tefra/xsdata-attrs/raw/main/docs/logo.svg)](https://xsdata-attrs.readthedocs.io/)

# xsdata powered by attrs!

[![image](https://github.com/tefra/xsdata-attrs/workflows/tests/badge.svg)](https://github.com/tefra/xsdata-attrs/actions)
[![image](https://readthedocs.org/projects/xsdata-attrs/badge)](https://xsdata-attrs.readthedocs.io/)
[![image](https://codecov.io/gh/tefra/xsdata-attrs/branch/main/graph/badge.svg)](https://codecov.io/gh/tefra/xsdata-attrs)
[![image](https://img.shields.io/github/languages/top/tefra/xsdata-attrs.svg)](https://xsdata-attrs.readthedocs.io/)
[![image](https://www.codefactor.io/repository/github/tefra/xsdata-attrs/badge)](https://www.codefactor.io/repository/github/tefra/xsdata-attrs)
[![image](https://img.shields.io/pypi/pyversions/xsdata-attrs.svg)](https://pypi.org/pypi/xsdata-attrs/)
[![image](https://img.shields.io/pypi/v/xsdata-attrs.svg)](https://pypi.org/pypi/xsdata-attrs/)

---

xsData is a complete data binding library for python allowing developers to access and
use XML and JSON documents as simple objects rather than using DOM.

Now powered by attrs!

```console
$ xsdata http://rss.cnn.com/rss/edition.rss --output attrs
Parsing document edition.rss
Analyzer input: 9 main and 0 inner classes
Analyzer output: 9 main and 0 inner classes
Generating package: init
Generating package: generated.rss
```

```python
@attr.s
class Rss:
    class Meta:
        name = "rss"

    version: Optional[float] = attr.ib(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    channel: Optional[Channel] = attr.ib(
        default=None,
        metadata={
            "type": "Element",
        }
    )
```

```console

>>> from xsdata_attrs.bindings import XmlParser
>>> from urllib.request import urlopen
>>> from generated.rss import Rss
>>>
>>> parser = XmlParser()
>>> with urlopen("http://rss.cnn.com/rss/edition.rss") as rq:
...     result = parser.parse(rq, Rss)
...
>>> result.channel.item[2].title
'Vatican indicts 10 people, including a Cardinal, over an international financial scandal'
>>> result.channel.item[2].pub_date
'Sat, 03 Jul 2021 16:37:14 GMT'
>>> result.channel.item[2].link
'https://www.cnn.com/2021/07/03/europe/vatican-financial-scandal-intl/index.html'

```

## Changelog: 24.5 (2024-05-08)

- Bump xsdata minimum version v24.5
