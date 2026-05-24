from sqlalchemy import Column, String, Integer
from database import Base


class Booking(Base):
    __tablename__ = "bookings"

    booking_id     = Column(String, primary_key=True, index=True)
    train_no       = Column(String, nullable=False)
    departure      = Column(String, nullable=False)
    arrival        = Column(String, nullable=False)
    departure_time = Column(String, nullable=False)
    arrival_time   = Column(String, default="")
    date           = Column(String, nullable=False)
    car_type       = Column(String, nullable=False)
    seat           = Column(String, nullable=False)
    passenger_name = Column(String, nullable=False)
    passenger_id   = Column(String, nullable=False)
    total_price    = Column(Integer, nullable=False)
    status         = Column(String, default="pending_payment")  # pending_payment | paid | cancelled
    pay_method     = Column(String, nullable=True)
    created_at     = Column(String, nullable=False)
    paid_at        = Column(String, nullable=True)
    cancelled_at   = Column(String, nullable=True)


class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id      = Column(String, primary_key=True, index=True)
    booking_id     = Column(String, nullable=False, index=True)
    train_no       = Column(String, nullable=False)
    departure      = Column(String, nullable=False)
    arrival        = Column(String, nullable=False)
    departure_time = Column(String, nullable=False)
    arrival_time   = Column(String, default="")
    date           = Column(String, nullable=False)
    car_no         = Column(String, nullable=False)
    seat_no        = Column(String, nullable=False)
    passenger_name = Column(String, nullable=False)
    ticket_type    = Column(String, nullable=False)
    booking_code   = Column(String, nullable=False)
    status         = Column(String, default="paid")  # paid | used | refunded
    qr_data        = Column(String, nullable=False)
