from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models.db_models import Ticket
from models.schemas import TicketResponse

router = APIRouter()


def _ticket_to_response(t: Ticket) -> TicketResponse:
    return TicketResponse(
        ticket_id=t.ticket_id,
        booking_id=t.booking_id,
        train_no=t.train_no,
        departure=t.departure,
        arrival=t.arrival,
        departure_time=t.departure_time,
        arrival_time=t.arrival_time or "",
        date=t.date,
        car_no=t.car_no,
        seat_no=t.seat_no,
        passenger_name=t.passenger_name,
        ticket_type=t.ticket_type,
        booking_code=t.booking_code,
        status=t.status,
        qr_data=t.qr_data,
    )


@router.get("/", response_model=list[TicketResponse], summary="取得我的車票列表")
async def list_tickets(
    passenger_name: Optional[str] = Query(None, description="依乘客姓名篩選"),
    status: Optional[str] = Query(None, enum=["paid", "used", "refunded"], description="篩選狀態"),
    db: Session = Depends(get_db),
):
    query = db.query(Ticket)
    if passenger_name:
        query = query.filter(Ticket.passenger_name == passenger_name)
    if status:
        query = query.filter(Ticket.status == status)
    return [_ticket_to_response(t) for t in query.all()]


@router.get("/{ticket_id}", response_model=TicketResponse, summary="取得單張車票")
async def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="車票不存在")
    return _ticket_to_response(ticket)


@router.get("/{ticket_id}/qr", summary="取得 QR Code 資料")
async def get_qr(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="車票不存在")
    if ticket.status == "refunded":
        raise HTTPException(status_code=400, detail="已退票，QR Code 無效")
    return {
        "ticket_id": ticket_id,
        "qr_data": ticket.qr_data,
        "booking_code": ticket.booking_code,
        "valid": ticket.status == "paid",
    }


@router.post("/{ticket_id}/use", summary="驗票（進站使用）")
async def use_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="車票不存在")
    if ticket.status == "used":
        raise HTTPException(status_code=400, detail="此票已使用")
    if ticket.status == "refunded":
        raise HTTPException(status_code=400, detail="此票已退票")

    ticket.status = "used"
    db.commit()
    return {"success": True, "message": "驗票成功，祝您旅途愉快", "ticket_id": ticket_id}
