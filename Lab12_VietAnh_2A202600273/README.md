# Ultimate AI Agent — Production Ready

Dự án AI Agent hoàn chỉnh được thiết kế theo chuẩn 12-Factor App, sẵn sàng triển khai lên Cloud (Railway/Render) với đầy đủ các tính năng bảo mật và mở rộng.

## 🚀 Tính năng nổi bật
- **Dockerization**: Multi-stage build tối ưu kích thước image.
- **Security**: Xác thực qua API Key, giới hạn lưu lượng (Rate Limiting).
- **Reliability**: Health checks, Readiness probes và Graceful shutdown.
- **Stateless**: Toàn bộ trạng thái phiên làm việc được lưu trữ tại Redis Cloud.
- **Scalability**: Sẵn sàng chạy sau Load Balancer (Nginx).

## 🛠️ Cài đặt & Chạy Local

### 1. Sử dụng Docker Compose (Khuyến nghị)
```bash
docker compose up --build
```
Hệ thống sẽ khởi chạy đồng thời Agent và Redis.

### 2. Chạy thủ công (Python)
```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

## 🌐 Triển khai Cloud (Railway)
1. Cài đặt Railway CLI.
2. `railway login`.
3. `railway up`.
4. Thiết lập các biến môi trường: `AGENT_API_KEY`, `REDIS_URL`.

## 📡 API Endpoints
- `GET /health`: Kiểm tra trạng thái container.
- `GET /ready`: Kiểm tra kết nối tới Redis.
- `POST /ask`: Truy vấn Agent (Yêu cầu Header `X-API-Key`).

## 🛡️ Bảo mật
Mọi request tới `/ask` cần đi kèm header:
`X-API-Key: <your_secret_key>`
