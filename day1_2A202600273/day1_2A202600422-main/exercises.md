# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** 
> Khi temperature tăng từ 0.0 lên 1.5, các phản hồi trở nên sáng tạo, đa dạng từ ngữ và ít dự đoán được hơn. Ở mức 0.0, câu trả lời thường rập khuôn, trực tiếp và thực tế, trong khi ở mức 1.5, phong cách diễn đạt đa dạng hơn nhưng có nguy cơ xuất hiện hallucination hoặc thông tin không mạch lạc.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Nên đặt ở mức thấp 0.0 - 0.2. Lý do là chatbot hỗ trợ khách hàng cần sự chính xác cao, nhất quán và đáng tin cậy khi cung cấp thông tin, tránh việc mô hình tự sáng tạo ra các chính sách, tính năng hay thông tin sai lệch gây nhầm lẫn và ảnh hưởng đến trải nghiệm khách hàng.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> GPT-4o đắt hơn GPT-4o-mini khoảng trên dưới 30 lần tùy thuộc vào tỷ trọng token input và output.

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> **Xứng đáng với GPT-4o:** Khi xử lý các tác vụ phức tạp đòi hỏi nhiều suy luận logic, lập trình chuyên sâu, phân tích toán học phức tạp, hoặc yêu cầu năng lực đa phương thức.
> **Tốt hơn với GPT-4o-mini:** Đối với các tác vụ đơn giản, lặp đi lặp lại với khối lượng dữ liệu khổng lồ nhưng không cần năng lực suy luận sâu, chẳng hạn như: phân loại cảm xúc văn bản, tóm tắt bài báo cơ bản, trích xuất thực thể, hoặc các chatbot hỏi đáp thông thường với nguồn kiến thức đã được cung cấp sẵn.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** 
> **Streaming** cực kỳ quan trọng trong các ứng dụng có giao diện đàm thoại theo thời gian thực vì nó giúp giảm đáng kể "thời gian chờ nhận text đầu tiên" , tạo ra trải nghiệm phản hồi liên tục. Ngược lại, 
**non-streaming** phù hợp hơn cho các xử lý tự động ngầm, tích hợp hệ thống, hay bóc tách dữ liệu có cấu trúc, nơi kết quả cuối cùng mới là thứ quan trọng thay vì xem text trả về từng chữ một.


## Danh Sách Kiểm Tra Nộp Bài
- [x] Tất cả tests pass: `pytest tests/ -v`
- [x] `call_openai` đã triển khai và kiểm thử
- [x] `call_openai_mini` đã triển khai và kiểm thử
- [x] `compare_models` đã triển khai và kiểm thử
- [x] `streaming_chatbot` đã triển khai và kiểm thử
- [x] `retry_with_backoff` đã triển khai và kiểm thử
- [x] `batch_compare` đã triển khai và kiểm thử
- [x] `format_comparison_table` đã triển khai và kiểm thử
- [x] `exercises.md` đã điền đầy đủ
- [x] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
