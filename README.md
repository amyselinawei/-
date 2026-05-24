# 🚄 TEXpress 高鐵訂票系統

模仿台灣高鐵官方 App 的完整訂票網站，含 FastAPI 後端 API。

---

## 📁 專案結構

```
texpress/
├── frontend/
│   ├── css/
│   │   └── style.css          # 共用樣式
│   └── pages/
│       ├── booking.html       # 訂票首頁（含車站選擇）
│       ├── train-list.html    # 班次查詢結果
│       ├── payment.html       # 付款確認
│       ├── my-ticket.html     # 我的車票 + QR Code
│       ├── free-seat.html     # 今日自由座等候時間
│       ├── credit-card.html   # 信用卡優惠
│       └── other.html         # 其他 / 設定
├── backend/
│   ├── main.py                # FastAPI 主程式
│   ├── models/
│   │   └── schemas.py         # Pydantic 資料模型
│   ├── data/
│   │   └── mock_db.py         # 模擬資料庫（可替換為真實 DB）
│   └── routers/
│       ├── trains.py          # 班次查詢 API
│       ├── booking.py         # 訂票 / 付款 / 退票 API
│       └── tickets.py         # 我的車票 API
└── requirements.txt
```

---

## 🚀 快速啟動

### 1. 安裝套件

```bash
pip install -r requirements.txt
```

### 2. 啟動後端 API

```bash
cd backend
uvicorn main:app --reload --port 8000
```

開啟後可訪問：
- **前端** → http://localhost:8000/
- **API 文件 (Swagger)** → http://localhost:8000/docs
- **ReDoc** → http://localhost:8000/redoc

### 3. 純前端模式（無需後端）

直接用瀏覽器打開 `frontend/pages/booking.html` 即可，所有頁面都可獨立運行。

---

## 🗺️ 頁面流程

```
booking.html  →  train-list.html  →  payment.html  →  my-ticket.html
    │
    ├── credit-card.html   （信用卡優惠）
    ├── free-seat.html     （今日自由座）
    └── other.html         （帳號 / 設定）
```

---

## 🔌 API 端點一覽

### 班次查詢
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET  | `/api/trains/stations` | 取得所有車站列表 |
| GET  | `/api/trains/search` | 查詢可用班次（帶 departure/arrival/date 參數）|
| GET  | `/api/trains/free-seat` | 自由座等候時間 |
| GET  | `/api/trains/status` | 全線運行狀況 |

### 訂票
| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/api/booking/create` | 建立訂單 |
| POST | `/api/booking/pay` | 執行付款 |
| GET  | `/api/booking/{id}` | 查詢訂單 |
| DELETE | `/api/booking/{id}` | 取消訂單（退票）|

### 車票
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET  | `/api/tickets/` | 取得車票列表 |
| GET  | `/api/tickets/{id}` | 取得單張車票 |
| GET  | `/api/tickets/{id}/qr` | 取得 QR Code 資料 |
| POST | `/api/tickets/{id}/use` | 驗票（進站）|

---

## 🛠️ 進階：連接真實資料庫

`backend/data/mock_db.py` 目前使用 dict 模擬資料庫。若要改用 PostgreSQL：

```bash
pip install sqlalchemy asyncpg alembic
```

然後將 `mock_db.py` 的 dict 操作替換為 SQLAlchemy 的 async session 操作即可。

---

## 📋 票價表

全線 13 站，票價依距離計算（NT$80 起），例如：
- 高雄 ↔ 台中：NT$ 790
- 高雄 ↔ 台北：NT$ 1,080
- 台北 ↔ 新竹：NT$ 130

---

## 技術棧

- **前端**：純 HTML / CSS / JavaScript（無框架，手機模擬 UI）
- **後端**：Python FastAPI + Pydantic v2
- **資料庫**：Mock（dict）→ 可換 PostgreSQL / SQLite
# -
