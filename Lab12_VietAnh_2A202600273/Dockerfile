# --- Stage 1: Builder ---
FROM python:3.11-slim AS builder

WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- Stage 2: Runtime ---
FROM python:3.11-slim AS runtime

# ✅ Tạo người dùng non-root và cài đặt curl cho healthcheck
RUN useradd -m agentuser && \
    apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY --from=builder /install /usr/local
COPY --chown=agentuser:agentuser . .

# Chạy với quyền user thường
USER agentuser

# Railway/Render/Docker dùng PORT này
ENV PORT=8000
EXPOSE 8000

# ✅ Lệnh HEALTHCHECK để Docker/Cloud tự theo dõi sức khỏe
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:$PORT/health || exit 1

# ✅ Chuyển sang shell form để $PORT được giải rộng (expand) chính xác
CMD python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT




