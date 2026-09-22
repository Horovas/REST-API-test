from pydantic import BaseModel, PositiveInt
from datetime import datetime
from typing import List


class PackageItem(BaseModel):
    packageItemId: PositiveInt
    barcode: str


class DestinationUserInfo(BaseModel):
    destination_user_id: PositiveInt
    intermediary_id: str


class Rack_Space_Item(BaseModel):
    rack_id: PositiveInt
    rack_space_id: PositiveInt
    package_class_id: PositiveInt
    price: PositiveInt
    priceVat: int | None
    commission: int
    commissionVat: int | None
    sectionId: PositiveInt
    fragile: bool
    package_item: PackageItem | None
    destination_user_info: DestinationUserInfo | None


class Get_Delivery(BaseModel):
    id: PositiveInt
    expireDateTime: datetime | None
    places: list[Rack_Space_Item]
    printed: bool
    printDateTime: datetime | None
    paid: bool
    paidDateTime: datetime | None

