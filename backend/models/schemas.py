from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime


class CarType(str, Enum):
    standard = "standard"   # 標準車廂
    business = "business"   # 商務車廂


class TicketType(str, Enum):
    adult = "adult"         # 全票
    child = "child"         # 孩童票
    disabled = "disabled"   # 愛心票
    elder = "elder"         # 敬老票


class TripType(str, Enum):
    one_way = "one_way"     # 單程
    round_trip = "round"    # 去回


class PayMethod(str, Enum):
    credit_card = "credit_card"
    apple_pay = "apple_pay"
    line_pay = "line_pay"
    jko_pay = "jko_pay"


# ---- Request Schemas ----

class TrainSearchRequest(BaseModel):
    departure: str = Field(..., example="高雄", description="出發站")
    arrival: str = Field(..., example="台中", description="到達站")
    date: str = Field(..., example="2026-03-09", description="出發日期 YYYY-MM-DD")
    car_type: CarType = Field(CarType.standard, description="車廂種類")
    adult_count: int = Field(1, ge=1, le=10, description="全票人數")
    child_count: int = Field(0, ge=0, le=10, description="孩童票人數")


class BookingRequest(BaseModel):
    train_no: str = Field(..., example="0834", description="車次號碼")
    departure: str = Field(..., example="高雄")
    arrival: str = Field(..., example="台中")
    departure_time: str = Field(..., example="14:43")
    date: str = Field(..., example="2026-03-09")
    car_type: CarType = Field(CarType.standard)
    passenger_name: str = Field(..., example="王小明", description="乘客姓名")
    passenger_id: str = Field(..., example="A123456789", description="身分證號")
    adult_count: int = Field(1, ge=1)
    child_count: int = Field(0, ge=0)
    trip_type: TripType = Field(TripType.one_way)
    return_date: Optional[str] = Field(None, description="回程日期（去回票）")


class PaymentRequest(BaseModel):
    booking_id: str = Field(..., example="BK20260309001")
    pay_method: PayMethod = Field(PayMethod.credit_card)
    card_last4: Optional[str] = Field(None, example="1234")


# ---- Response Schemas ----

class SeatAvailability(BaseModel):
    standard: str   # "充足" | "少量" | "售罄"
    business: str


class TrainInfo(BaseModel):
    train_no: str
    departure: str
    arrival: str
    departure_time: str
    arrival_time: str
    duration_minutes: int
    price_adult: int
    price_child: int
    seats: SeatAvailability


class BookingResponse(BaseModel):
    booking_id: str
    train_no: str
    departure: str
    arrival: str
    departure_time: str
    arrival_time: str
    date: str
    car_type: str
    seat: str
    passenger_name: str
    total_price: int
    status: str   # "pending_payment" | "paid" | "cancelled"
    created_at: str


class TicketResponse(BaseModel):
    ticket_id: str
    booking_id: str
    train_no: str
    departure: str
    arrival: str
    departure_time: str
    arrival_time: str
    date: str
    car_no: str
    seat_no: str
    passenger_name: str
    ticket_type: str
    booking_code: str
    status: str   # "paid" | "used" | "refunded"
    qr_data: str


class FreeSeatWait(BaseModel):
    from_station: str
    to_station: str
    standard_wait: str
    business_wait: str


class StationStatus(BaseModel):
    name: str
    name_en: str
    code: str
    order: int
