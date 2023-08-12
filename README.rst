.. image:: https://raw.githubusercontent.com/tefra/xsdata-attrs/main/docs/_static/logo.svg
    :target: https://xsdata-attrs.readthedocs.io/

xsdata powered by attrs!
========================

.. image:: https://github.com/tefra/xsdata/workflows/tests/badge.svg
    :target: https://github.com/tefra/xsdata-attrs/actions

.. image:: https://readthedocs.org/projects/xsdata-attrs/badge
    :target: https://xsdata-attrs.readthedocs.io/

.. image:: https://codecov.io/gh/tefra/xsdata-attrs/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/tefra/xsdata-attrs

.. image:: https://img.shields.io/github/languages/top/tefra/xsdata-attrs.svg
    :target: https://xsdata-attrs.readthedocs.io/

.. image:: https://www.codefactor.io/repository/github/tefra/xsdata-attrs/badge
   :target: https://www.codefactor.io/repository/github/tefra/xsdata-attrs

.. image:: https://img.shields.io/pypi/pyversions/xsdata-attrs.svg
    :target: https://pypi.org/pypi/xsdata-attrs/

.. image:: https://img.shields.io/pypi/v/xsdata-attrs.svg
    :target: https://pypi.org/pypi/xsdata-attrs/

--------

xsData is a complete data binding library for python allowing developers to access and
use XML and JSON documents as simple objects rather than using DOM.

Now powered by attrs!


Install
=======

.. code:: console

    $ # Install with cli support
    $ pip install xsdata-attrs[cli]


Generate Models
===============

.. code:: console

    $ # Generate models
    $ xsdata http://rss.cnn.com/rss/edition.rss --output attrs
    Parsing document edition.rss
    Analyzer input: 9 main and 0 inner classes
    Analyzer output: 9 main and 0 inner classes
    Generating package: init
    Generating package: generated.rss

.. code-block:: python

    ...

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

    ...


XML Parsing
===========

.. code:: python

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


Changelog: 23.8 (2023-08-12)
----------------------------
- Removed python 3.6 and 3.7 support
- Added official support for 3.11 and 3.12
- Set xsdata minimum version v23.5

This project is still alive :)
