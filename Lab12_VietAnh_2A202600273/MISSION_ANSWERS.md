# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. Hardcoded API Keys: Lộ thông tin nhạy cảm.
2. Hardcoded Ports: Thiếu linh hoạt khi triển khai Cloud.
3. No Health Checks: Không có cơ chế tự theo dõi sức khỏe.
4. No Graceful Shutdown: Ngắt kết nối đột ngột gây mất dữ liệu.
5. Print() statements: Khó quản lý log quy mô lớn.

### Exercise 1.3: Comparison table
| Feature | Develop | Production | Why Important? |
|---------|---------|------------|----------------|
| Config  | Hardcode| Env vars   | Bảo mật secrets và linh hoạt cấu hình. |
| Health  | N/A     | /health    | Tự động recovery khi app treo. |
| Logging | print() | JSON       | Dễ parse và phân tích log tập trung. |
| Shutdown| Sudden  | Graceful   | Hoàn tất request trước khi tắt app. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image: `python:3.11-slim` - Tối ưu kích thước.
2. Working directory: `/app`.
3. COPY requirements.txt trước: Tận dụng Layer Caching để build nhanh hơn.
4. CMD vs ENTRYPOINT: ENTRYPOINT cố định lệnh chạy, CMD là tham số mặc định.

### Exercise 2.3: Image size comparison
- Develop: ~160 MB
- Production: ~135 MB
- Difference: ~15% (nhờ Multi-stage và dọn dẹp cache).

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- URL: https://lab12final-production.up.railway.app
- Status: ✅ Online & Ready

## Part 4: API Security

### Exercise 4.1-4.3: Test results
- **Auth (No Key):** `401 Unauthorized` → `{"detail":"Not authenticated"}`
- **Auth (Valid Key):** `200 OK` → `{"user_id":"Pham-Viet-Anh","question":"Hello","answer":"..."}`
- **Rate Limit:** Trả về `429 Too Many Requests` sau 10 lần gọi trong 1 phút.

### Exercise 4.4: Cost guard implementation
Triển khai logic kiểm tra `total_cost` tại Redis trước khi gọi LLM. Nếu chi phí vượt quá `settings.MONTHLY_BUDGET_USD` ($10), hệ thống sẽ chặn và trả về lỗi `402 Payment Required`.

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
- **Health/Ready:** Agent đã vượt qua bài test Liveness và Readiness trên Cloud.
- **Stateless:** Dữ liệu history được lưu trữ bền vững tại Redis Cloud, đảm bảo dữ liệu không bị mất khi Agent khởi động lại.
- Stateless Design: Mọi trạng thái (history/rate limit) đều được đẩy ra Redis, cho phép scale ngang không giới hạn.
- Graceful Shutdown: Sử dụng `lifespan` của FastAPI để đóng các kết nối Redis an toàn.
