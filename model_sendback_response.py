from pydantic import BaseModel, PositiveInt, TypeAdapter # for root list
from datetime import datetime
from typing import List


class RefundTerms(BaseModel):
    refundTypeForDelivery: str
    reasonForRefund: str
    daysBeforeFinalDelivery: int
    minReturnPercent: int
    refundCommissionPercent: int


class Refund_Terms(BaseModel):
    packageItemId: PositiveInt
    refundTerms: List[RefundTerms]

Sendback_Adapter = TypeAdapter(list[Refund_Terms])
