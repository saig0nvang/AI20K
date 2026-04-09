# Individual reflection — Việt Anh

## 1. Role
Product Owner + Developer. Phụ trách lên ý tưởng đề tài, phân tích định hình giải pháp (Canvas & SPEC) và xây dựng nền tảng kỹ thuật ban đầu cho AI Agent.

## 2. Đóng góp cụ thể
- **Lên ý tưởng đề tài & Phân tích:** Đưa ra đề tài xây dựng AI Agent cho VinFast, viết định nghĩa vấn đề (problem) liên quan đến sự phân mảnh thông tin khuyến mãi và những bất cập trong quy trình sales hiện tại.
- **Xây dựng Canvas & Giải pháp:** Hoàn thiện Solution Canvas, đề xuất giải pháp ứng dụng AI Agent kết hợp RAG (Retrieval-Augmented Generation) để tự động hóa tư vấn và cá nhân hóa mức giá cho khách hàng.
- **Phát triển kỹ thuật:** Khởi tạo cấu trúc project, viết khung sườn code (skeleton code) cho các file cốt lõi bao gồm `tools.py` (chức năng tìm kiếm và tính toán), `agent.py` (vòng lặp LangGraph), và soạn thảo `system prompt` định hướng luồng tư vấn.

## 3. SPEC mạnh/yếu
- **Mạnh nhất:** Xác định từ sớm kiến trúc giải pháp thực t — dùng local/Deep RAG để tra lời từ các tài liệu chính sách (`Sale.md`- được tổng hợp từ 17 file pdf trong Hợp đồng và chính sách cho xe ô tô 2026 của Vinfast. Link:https://vinfastauto.com/vn_vi/hop-dong-va-chinh-sach/chinh-sach/cho-xe-oto/2026) thay vì để AI tự bịa thông tin (hallucinate). Giải pháp giải quyết "đúng chỗ ngứa" của cả người dùng và doanh nghiệp.
- **Yếu nhất:** Có nhiều chương trình khuyến mãi, theo xe, theo đối tượng, theo sự kiện trong năm,... Một số trường hợp gây khó khăn trong việc tính giá sau khuyến mãi do các chương trình chồng chéo. Việc định nghĩa tool ban đầu còn hơi chung chung, cần phải refine lại nhiều lần để agent hiểu.

## 4. Đóng góp khác
- Tạo test case và fix các lỗi xuất hiện
- Tham gia thiết kế system prompt

## 5. Điều học được
- Xây dựng Agent không chỉ đơn thuần là gọi API, mà phần khó nhất là điều hướng tư duy của mô hình. Việc thiết kế `system prompt` và tool description là quyết định sống còn đến độ chính xác (precision).
- Nhận ra rằng với các truy vấn liên quan đến giá cả và tiền bạc, việc ép AI tuân thủ strict constraint (tuyệt đối dựa vào file) quan trọng hơn việc cho AI tự do sáng tạo.

## 6. Nếu làm lại
- Sẽ dành nhiều thời gian hơn để tối ưu các rule trong System prompt
- Chia nhỏ các agents theo dạng Multi-Agent (một agent chuyên tra cứu chính sách, một agent chuyên tính toán giá lăn bánh) thay vì gom hết vào một agent xử lý.

## 7. AI giúp gì / AI sai gì
- **Giúp:** AI (đặc biệt là các công cụ chat) đã hỗ trợ thiết kế nhanh chóng bộ khung xương (Canvas) và sinh mã nguồn nhanh cho cấu trúc đồ thị của LangGraph, tiết kiệm được rất nhiều thời gian boilerplate.
- **Sai/mislead:** Khi triển khai các tool tính toán, đôi lúc AI gợi ý các hàm xử lý logic quá phức tạp. Khi triển khai system prompt, AI đưa ra các quy luật không chặt chẽ, đôi khi đưa ra thông tin thừa nhưng vẫn không đúng trọng tâm, cần có sự kiểm soát của con người.
