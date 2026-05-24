from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import uvicorn
import os

from database import engine
from models import db_models
from routers import trains, booking, tickets


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 建立所有資料表（若已存在則略過）
    db_models.Base.metadata.create_all(bind=engine)
    print("🚄 TEXpress API 啟動中...")
    yield
    print("🛑 TEXpress API 關閉")


app = FastAPI(
    title="TEXpress 高鐵訂票 API",
    description="台灣高速鐵路訂票系統後端 API",
    version="2.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(trains.router,  prefix="/api/trains",  tags=["班次查詢"])
app.include_router(booking.router, prefix="/api/booking", tags=["訂票"])
app.include_router(tickets.router, prefix="/api/tickets", tags=["我的車票"])

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/css", StaticFiles(directory=os.path.join(frontend_path, "css")), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_index():
        return FileResponse(os.path.join(frontend_path, "pages", "booking.html"))

    @app.get("/{page}.html", include_in_schema=False)
    async def serve_page(page: str):
        path = os.path.join(frontend_path, "pages", f"{page}.html")
        if os.path.exists(path):
            return FileResponse(path)
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="頁面不存在")


@app.get("/api/health", tags=["系統"])
async def health_check():
    return {"status": "ok", "service": "TEXpress API", "version": "2.1.0"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
