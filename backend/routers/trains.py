from fastapi import APIRouter, Query, HTTPException
from typing import Optional
import random
from datetime import datetime, timedelta

from models.schemas import TrainInfo, SeatAvailability, FreeSeatWait, StationStatus
from data.mock_db import STATIONS, TRAIN_SCHEDULE, FREE_SEAT_DATA, get_price

router = APIRouter()


def _get_station(name: str) -> Optional[StationStatus]:
    return next((s for s in STATIONS if s.name == name), None)


def _calc_arrival(dep_time: str, offset_min: int) -> str:
    h, m = map(int, dep_time.split(":"))
    total = h * 60 + m + offset_min
    return f"{total // 60:02d}:{total % 60:02d}"


def _seat_status() -> str:
    r = random.random()
    if r < 0.55: return "充足"
    elif r < 0.8: return "少量"
    else: return "售罄"


@router.get("/stations", response_model=list[StationStatus], summary="取得所有車站列表")
async def list_stations():
    """回傳由北至南所有高鐵車站資料"""
    return STATIONS


@router.get("/search", response_model=list[TrainInfo], summary="查詢可用班次")
async def search_trains(
    departure: str = Query(..., example="高雄", description="出發站"),
    arrival:   str = Query(..., example="台中", description="到達站"),
    date:      str = Query(..., example="2026-03-09", description="日期 YYYY-MM-DD"),
    adult:     int = Query(1, ge=1, le=10),
    child:     int = Query(0, ge=0, le=10),
):
    dep_st = _get_station(departure)
    arr_st = _get_station(arrival)

    if not dep_st:
        raise HTTPException(status_code=400, detail=f"出發站 '{departure}' 不存在")
    if not arr_st:
        raise HTTPException(status_code=400, detail=f"到達站 '{arrival}' 不存在")
    if dep_st.order == arr_st.order:
        raise HTTPException(status_code=400, detail="出發站與到達站不可相同")

    price = get_price(dep_st.order, arr_st.order)

    random.seed(date + departure + arrival)
    trains = []
    for t in TRAIN_SCHEDULE:
        arr_time = _calc_arrival(t["dep"], t["arr_offset"])
        trains.append(TrainInfo(
            train_no=t["no"],
            departure=departure,
            arrival=arrival,
            departure_time=t["dep"],
            arrival_time=arr_time,
            duration_minutes=t["arr_offset"],
            price_adult=price,
            price_child=int(price * 0.5),
            seats=SeatAvailability(
                standard=_seat_status(),
                business=_seat_status(),
            )
        ))
    return trains


@router.get("/free-seat", response_model=dict, summary="查詢自由座等候時間")
async def get_free_seat_wait(direction: str = Query("north", enum=["north", "south"])):
    """回傳各站自由座候車時間（north=北上，south=南下）"""
    data = FREE_SEAT_DATA.get(direction, [])
    return {
        "direction": direction,
        "updated_at": datetime.now().strftime("%H:%M"),
        "stations": [
            FreeSeatWait(
                from_station=d["from"],
                to_station=d["to"],
                standard_wait=d["std"],
                business_wait=d["bus"],
            ) for d in data
        ]
    }


@router.get("/status", summary="查詢全線運行狀況")
async def get_line_status():
    return {
        "status": "normal",
        "message": "全線正常營運",
        "updated_at": datetime.now().isoformat(),
        "incidents": [],
    }
