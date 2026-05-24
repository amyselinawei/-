from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid, random

from database import get_db
from models.db_models import Booking, Ticket
from models.schemas import BookingRequest, BookingResponse, PaymentRequest
from data.mock_db import STATIONS, get_price

router = APIRouter()


def _get_order(name: str) -> int:
    st = next((s for s in STATIONS if s.name == name), None)
    return st.order if st else 0


def _assign_seat() -> tuple[str, str]:
    car = random.randint(1, 12)
    row = random.randint(1, 18)
    side = random.choice(["A", "B", "C", "D", "E"])
    return str(car), f"{row}{side}"


def _booking_to_response(b: Booking) -> BookingResponse:
    return BookingResponse(
        booking_id=b.booking_id,
        train_no=b.train_no,
        departure=b.departure,
        arrival=b.arrival,
        departure_time=b.departure_time,
        arrival_time=b.arrival_time or "",
        date=b.date,
        car_type=b.car_type,
        seat=b.seat,
        passenger_name=b.passenger_name,
        total_price=b.total_price,
        status=b.status,
        created_at=b.created_at,
    )


@router.post("/create", response_model=BookingResponse, summary="建立訂票")
async def create_booking(req: BookingRequest, db: Session = Depends(get_db)):
    dep_order = _get_order(req.departure)
    arr_order = _get_order(req.arrival)
    if dep_order == 0 or arr_order == 0:
        raise HTTPException(status_code=400, detail="車站資料錯誤")

    unit_price  = get_price(dep_order, arr_order)
    child_price = int(unit_price * 0.5)
    total       = unit_price * req.adult_count + child_price * req.child_count

    car_no, seat_no = _assign_seat()
    booking_id = f"BK{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"

    booking = Booking(
        booking_id=booking_id,
        train_no=req.train_no,
        departure=req.departure,
        arrival=req.arrival,
        departure_time=req.departure_time,
        arrival_time="",
        date=req.date,
        car_type=req.car_type.value,
        seat=f"{car_no}車{seat_no}",
        passenger_name=req.passenger_name,
        passenger_id=req.passenger_id,
        total_price=total,
        status="pending_payment",
        created_at=datetime.now().isoformat(),
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return _booking_to_response(booking)


@router.post("/pay", response_model=dict, summary="執行付款")
async def pay_booking(req: PaymentRequest, db: Session = Depends(get_db)):
    booking = db.get(Booking, req.booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="訂單不存在")
    if booking.status == "paid":
        raise HTTPException(status_code=400, detail="此訂單已完成付款")
    if booking.status == "cancelled":
        raise HTTPException(status_code=400, detail="此訂單已取消")

    booking.status     = "paid"
    booking.pay_method = req.pay_method.value
    booking.paid_at    = datetime.now().isoformat()

    car_no, seat_no = booking.seat.split("車")
    booking_code = f"THS{uuid.uuid4().hex[:6].upper()}"
    ticket_id    = f"TK{uuid.uuid4().hex[:6].upper()}"

    ticket = Ticket(
        ticket_id=ticket_id,
        booking_id=req.booking_id,
        train_no=booking.train_no,
        departure=booking.departure,
        arrival=booking.arrival,
        departure_time=booking.departure_time,
        arrival_time=booking.arrival_time or "",
        date=booking.date,
        car_no=car_no,
        seat_no=seat_no,
        passenger_name=booking.passenger_name,
        ticket_type="全票",
        booking_code=booking_code,
        status="paid",
        qr_data=f"THSR|{booking.train_no}|{booking.departure}|{booking.arrival}|{booking.date}|{booking.departure_time}|{car_no}|{seat_no}|{booking_code}",
    )
    db.add(ticket)
    db.commit()

    return {
        "success": True,
        "message": "付款成功",
        "booking_id": req.booking_id,
        "ticket_id": ticket_id,
        "booking_code": booking_code,
        "total_charged": booking.total_price,
    }


@router.get("/{booking_id}", response_model=BookingResponse, summary="查詢訂單")
async def get_booking(booking_id: str, db: Session = Depends(get_db)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="訂單不存在")
    return _booking_to_response(booking)


@router.delete("/{booking_id}", summary="取消訂單（退票）")
async def cancel_booking(booking_id: str, db: Session = Depends(get_db)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="訂單不存在")
    if booking.status == "cancelled":
        raise HTTPException(status_code=400, detail="訂單已取消")

    refund = int(booking.total_price * 0.9) if booking.status == "paid" else booking.total_price
    booking.status       = "cancelled"
    booking.cancelled_at = datetime.now().isoformat()
    db.commit()

    return {
        "success": True,
        "message": "退票成功",
        "booking_id": booking_id,
        "refund_amount": refund,
    }
