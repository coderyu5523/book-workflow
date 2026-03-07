"""ex08 — FastAPI 애플리케이션 진입점 모듈."""

import os

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .chat_api import router as chat_router

# ---------------------------------------------------------------------------
# 1. FastAPI 앱 생성
# ---------------------------------------------------------------------------

app = FastAPI(
    title="ConnectHR ex08 - RAG 튜닝",
    description="RAG 튜닝 + 평가 프레임워크 + 실험 데모",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# 2. 정적 파일 및 라우터 등록
# ---------------------------------------------------------------------------

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_STATIC_DIR = os.path.join(_BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")  # ①
app.include_router(chat_router)  # ②


# ---------------------------------------------------------------------------
# 3. 루트 리다이렉트 및 헬스체크
# ---------------------------------------------------------------------------

@app.get("/", include_in_schema=False)
async def root():
    """루트 경로를 채팅 페이지로 리다이렉트한다."""
    return RedirectResponse(url="/chat")


@app.get("/health")
async def health():
    """서버 상태를 반환한다."""
    return {"status": "ok", "version": "ex08", "title": "RAG 튜닝"}
