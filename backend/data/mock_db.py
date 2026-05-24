"""
Mock data for TEXpress demo
In production, replace with a real database (PostgreSQL + SQLAlchemy)
"""
from models.schemas import StationStatus

# ---- Stations ----
STATIONS: list[StationStatus] = [
    StationStatus(name="南港", name_en="Nangang",  code="NNG", order=1),
    StationStatus(name="台北", name_en="Taipei",   code="TPE", order=2),
    StationStatus(name="板橋", name_en="Banqiao",  code="BNQ", order=3),
    StationStatus(name="桃園", name_en="Taoyuan",  code="TYN", order=4),
    StationStatus(name="新竹", name_en="Hsinchu",  code="HCU", order=5),
    StationStatus(name="苗栗", name_en="Miaoli",   code="MLI", order=6),
    StationStatus(name="台中", name_en="Taichung", code="TCH", order=7),
    StationStatus(name="彰化", name_en="Changhua", code="CHH", order=8),
    StationStatus(name="雲林", name_en="Yunlin",   code="YLN", order=9),
    StationStatus(name="嘉義", name_en="Chiayi",   code="CYI", order=10),
    StationStatus(name="台南", name_en="Tainan",   code="TNN", order=11),
    StationStatus(name="左營", name_en="Zuoying",  code="ZYG", order=12),
    StationStatus(name="高雄", name_en="Kaohsiung",code="KHH", order=13),
]

# ---- Price table (NT$) ----
# Key: (dep_order, arr_order) → adult price
PRICE_TABLE: dict[tuple[int,int], int] = {
    (13,12): 80,  (13,11): 270, (13,10): 410, (13,9): 500,
    (13,8):  570, (13,7):  790, (13,6):  850, (13,5):  940,
    (13,4): 1020, (13,3): 1080, (13,2): 1080, (13,1): 1090,
    (12,11): 200, (12,10): 340, (12,9):  430, (12,8):  500,
    (12,7):  710, (12,6):  770, (12,5):  860, (12,4):  940,
    (12,3): 1000, (12,2): 1000, (12,1): 1010,
    (11,10): 140, (11,9):  230, (11,8):  300, (11,7):  510,
    (11,6):  580, (11,5):  660, (11,4):  740, (11,3):  800,
    (11,2):  800, (11,1):  810,
    (10,9):   90, (10,8):  160, (10,7):  370, (10,6):  440,
    (10,5):  520, (10,4):  600, (10,3):  660, (10,2):  660, (10,1): 670,
    (9,8):    80, (9,7):   280, (9,6):   350, (9,5):   430,
    (9,4):   510, (9,3):   570, (9,2):   570, (9,1):   580,
    (8,7):   210, (8,6):   280, (8,5):   360, (8,4):   440,
    (8,3):   490, (8,2):   490, (8,1):   500,
    (7,6):    80, (7,5):   150, (7,4):   230, (7,3):   290,
    (7,2):   290, (7,1):   300,
    (6,5):    80, (6,4):   160, (6,3):   210, (6,2):   210, (6,1): 220,
    (5,4):    80, (5,3):   130, (5,2):   130, (5,1):   140,
    (4,3):    80, (4,2):    80, (4,1):    90,
    (3,2):    80, (3,1):    80,
    (2,1):    80,
}

def get_price(dep_order: int, arr_order: int) -> int:
    """Get price, supports reverse direction"""
    key = (max(dep_order, arr_order), min(dep_order, arr_order))
    return PRICE_TABLE.get(key, 500)

# ---- Train schedule template ----
TRAIN_SCHEDULE = [
    {"no": "0808", "dep": "08:00", "arr_offset": 43},
    {"no": "0812", "dep": "09:00", "arr_offset": 43},
    {"no": "0814", "dep": "10:00", "arr_offset": 49},
    {"no": "0820", "dep": "11:00", "arr_offset": 49},
    {"no": "0826", "dep": "12:00", "arr_offset": 43},
    {"no": "0832", "dep": "13:00", "arr_offset": 49},
    {"no": "0834", "dep": "14:43", "arr_offset": 49},
    {"no": "0838", "dep": "15:00", "arr_offset": 49},
    {"no": "0844", "dep": "16:00", "arr_offset": 43},
    {"no": "0850", "dep": "17:00", "arr_offset": 49},
    {"no": "0856", "dep": "18:00", "arr_offset": 49},
    {"no": "0862", "dep": "19:00", "arr_offset": 43},
    {"no": "0868", "dep": "20:00", "arr_offset": 49},
    {"no": "0872", "dep": "21:00", "arr_offset": 43},
]

# ---- In-memory booking store (replace with DB in production) ----
BOOKINGS: dict[str, dict] = {
    "BK20260309001": {
        "booking_id": "BK20260309001",
        "train_no": "0834",
        "departure": "高雄",
        "arrival": "台中",
        "departure_time": "14:43",
        "arrival_time": "15:32",
        "date": "2026-03-09",
        "car_type": "standard",
        "seat": "6車2B",
        "passenger_name": "王小明",
        "passenger_id": "A123456789",
        "total_price": 790,
        "status": "paid",
        "created_at": "2026-03-09T10:00:00",
    }
}

TICKETS: dict[str, dict] = {
    "TK001": {
        "ticket_id": "TK001",
        "booking_id": "BK20260309001",
        "train_no": "0834",
        "departure": "高雄",
        "arrival": "台中",
        "departure_time": "14:43",
        "arrival_time": "15:32",
        "date": "2026-03-09",
        "car_no": "6",
        "seat_no": "2B",
        "passenger_name": "王小明",
        "ticket_type": "全票",
        "booking_code": "THS928314",
        "status": "paid",
        "qr_data": "THSR|0834|KHH|TCH|20260309|14:43|6|2B|THS928314",
    }
}

FREE_SEAT_DATA = {
    "north": [
        {"from": "高雄", "to": "台南",  "std": "5分",  "bus": "立即"},
        {"from": "台南", "to": "嘉義",  "std": "10分", "bus": "5分"},
        {"from": "嘉義", "to": "雲林",  "std": "5分",  "bus": "立即"},
        {"from": "雲林", "to": "彰化",  "std": "20分", "bus": "10分"},
        {"from": "彰化", "to": "台中",  "std": "15分", "bus": "5分"},
        {"from": "台中", "to": "新竹",  "std": "10分", "bus": "立即"},
        {"from": "新竹", "to": "桃園",  "std": "5分",  "bus": "立即"},
        {"from": "桃園", "to": "板橋",  "std": "25分", "bus": "15分"},
        {"from": "板橋", "to": "台北",  "std": "30分", "bus": "20分"},
    ],
    "south": [
        {"from": "南港", "to": "台北",  "std": "20分", "bus": "15分"},
        {"from": "台北", "to": "板橋",  "std": "25分", "bus": "10分"},
        {"from": "板橋", "to": "桃園",  "std": "10分", "bus": "5分"},
        {"from": "桃園", "to": "新竹",  "std": "5分",  "bus": "立即"},
        {"from": "新竹", "to": "台中",  "std": "15分", "bus": "5分"},
        {"from": "台中", "to": "彰化",  "std": "5分",  "bus": "立即"},
        {"from": "彰化", "to": "嘉義",  "std": "10分", "bus": "立即"},
        {"from": "嘉義", "to": "台南",  "std": "5分",  "bus": "立即"},
        {"from": "台南", "to": "左營",  "std": "20分", "bus": "10分"},
    ],
}
