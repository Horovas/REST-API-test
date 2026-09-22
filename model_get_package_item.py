from pydantic import BaseModel, PositiveInt
from datetime import datetime


class Rack_Space_Item(BaseModel):
    rack_id: PositiveInt
    rack_space_id: PositiveInt
    sectionId: PositiveInt
    fragile: bool
    

class Get_Package_Item(BaseModel):
    package_item_id: PositiveInt
    barcode: str
    delivery_id: PositiveInt
    package_class_id: PositiveInt
    price: PositiveInt
    priceVat: int | None
    commission: int
    commissionVat: int | None
    rack_space_item: Rack_Space_Item
