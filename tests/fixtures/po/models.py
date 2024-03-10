from decimal import Decimal
from typing import List, Optional

import attr
from xsdata.models.datatype import XmlDate

__NAMESPACE__ = "foo"


@attr.s(slots=True, kw_only=True)
class Usaddress:
    class Meta:
        name = "USAddress"

    name: str = attr.ib(
        metadata={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    street: str = attr.ib(
        metadata={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    city: str = attr.ib(
        metadata={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    state: str = attr.ib(
        metadata={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    zip: Decimal = attr.ib(
        metadata={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    country: str = attr.ib(
        init=False,
        default="US",
        metadata={
            "type": "Attribute",
        },
    )


@attr.s(slots=True, kw_only=True)
class Comment:
    class Meta:
        name = "comment"
        namespace = "foo"

    value: str = attr.ib(
        default="",
        metadata={
            "required": True,
        },
    )


@attr.s(slots=True, kw_only=True)
class Items:
    item: List["Items.Item"] = attr.ib(
        factory=list,
        metadata={
            "type": "Element",
            "namespace": "foo",
        },
    )

    @attr.s(slots=True, kw_only=True)
    class Item:
        product_name: str = attr.ib(
            metadata={
                "name": "productName",
                "type": "Element",
                "namespace": "foo",
                "required": True,
            }
        )
        quantity: int = attr.ib(
            metadata={
                "type": "Element",
                "namespace": "foo",
                "required": True,
                "max_exclusive": 100,
            }
        )
        usprice: Decimal = attr.ib(
            metadata={
                "name": "USPrice",
                "type": "Element",
                "namespace": "foo",
                "required": True,
            }
        )
        comment: Optional[Comment] = attr.ib(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "foo",
            },
        )
        ship_date: Optional[XmlDate] = attr.ib(
            default=None,
            metadata={
                "name": "shipDate",
                "type": "Element",
                "namespace": "foo",
            },
        )
        part_num: str = attr.ib(
            metadata={
                "name": "partNum",
                "type": "Attribute",
                "required": True,
                "pattern": r"\d{3}-[A-Z]{2}",
            }
        )


@attr.s(slots=True, kw_only=True)
class PurchaseOrderType:
    ship_to: Usaddress = attr.ib(
        metadata={
            "name": "shipTo",
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    bill_to: Usaddress = attr.ib(
        metadata={
            "name": "billTo",
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    comment: Optional[Comment] = attr.ib(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "foo",
        },
    )
    items: Items = attr.ib(
        metadata={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    order_date: Optional[XmlDate] = attr.ib(
        default=None,
        metadata={
            "name": "orderDate",
            "type": "Attribute",
        },
    )


@attr.s(slots=True, kw_only=True)
class PurchaseOrder(PurchaseOrderType):
    class Meta:
        name = "purchaseOrder"
        namespace = "foo"
