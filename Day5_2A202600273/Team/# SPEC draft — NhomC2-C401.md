# SPEC draft — NhomC2-C401

## Track: Vinfast

## 1. Problem statement
Khách hàng mua xe VinFast không chỉ quan tâm đến giá bán lẻ mà còn hàng loạt ưu đãi đi kèm phức tạp như voucher Vinhomes, chính sách thu cũ đổi mới, gói thuê pin vs mua pin, ưu đãi trạm sạc, và các gói vay lãi suất từ ngân hàng liên kết. 

- **Pain point khách hàng:** Các ưu đãi thường phân tán ở nhiều kênh khác nhau, rule cộng dồn phức tạp, khiến khách hàng khó nắm bắt, mất phương hướng và khó ước tính được "giá lăn bánh" thực tế. Việc phải chờ đợi 15-30 phút trong những đợt cao điểm để Sale tư vấn chỉ cho một phép tính đơn giản làm tăng tỷ lệ rơi rớt (drop-off), gây nản lòng dẫn đến trì hoãn mua xe.
- **Pain point doanh nghiệp:** Đội ngũ Sales/CSKH bị quá tải bởi những câu hỏi tra cứu (FAQ) lặp đi lặp lại. Sales không có đủ thời gian để tập trung vào việc tư vấn chuyên sâu hay "chốt deal" với những khách hàng có tiềm năng thực sự. Đồng thời sai sót khi Sales tính nhẩm cũng gây khiếu nại, mất niềm tin.
- **Giải pháp AI:** Một AI Bot tư vấn trợ lý, tự động tra cứu, tổng hợp, so sánh và cá nhân hóa thiết kế gói ưu đãi, ước tính giá lăn bánh theo đúng profile khách hàng và khu vực hiện tại một cách tức thời, chính xác.

## 2. Canvas

| | Value | Trust | Feasibility |
|---|-------|-------|-------------|
| **Câu hỏi guide** | User nào? Pain gì? AI giải quyết gì mà cách hiện tại không giải được? | Khi AI sai thì user bị ảnh hưởng thế nào? User biết AI sai bằng cách nào? User sửa bằng cách nào? | Cost bao nhiêu/request? Latency bao lâu? Risk chính là gì? |
| **Trả lời** | **User:** Khách hàng quan tâm mua xe VinFast.<br>**Pain:** Ưu đãi phân tán, tính toán phức tạp, sale trả lời chậm.<br>**AI giải quyết:** Tự động tra cứu, tổng hợp quy tắc tích hợp ưu đãi và báo giá lăn bánh cá nhân hoá ngay lập tức (real-time). | **Hậu quả khi sai:** Báo sai giá hoặc khuyến mãi gây khiếu nại, ảnh hưởng uy tín thương hiệu.<br>**Nhận biết:** Khách hàng thấy bất hợp lý so với bảng giá niêm yết hoặc Sales kiểm tra lại.<br>**Cách sửa:** Luôn có tuỳ chọn "Kết nối Sales", kết quả AI sinh ra luôn dẫn nguồn (citation) rõ ràng để đối chiếu. | **Cost:** API gọi LLM ~$0.005 - 0.01/request.<br>**Latency:** < 3-5s.<br>**Risk chính:** Data khuyến mãi liên tục thay đổi, rules chồng chéo dễ dẫn tới ảo giác (hallucination) trong việc tính toán cộng trừ. |

### Automation hay augmentation?
☑ Augmentation — AI gợi ý (tư vấn), user và Sales quyết định cuối cùng.

**Justify:** AI xử lý luồng FAQ cơ bản và ước tính giá lăn bánh (tham khảo). Vì AI = Probabilistic, nên nếu uỷ quyền 100% tự chốt deal (Automation) khi AI tính sai khuyến mãi sẽ gây thiệt hại lớn về tài chính và pháp lý. Sales luôn cần can thiệp bước cuối để duyệt lại hồ sơ và khách hàng dùng thông tin AI cung cấp dưới nhãn dán "Thông tin mang tính tham khảo, kết nối tư vấn để chốt giá cuối".

### Learning signal
| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 1 | User correction đi vào đâu? | Các ca AI trả lời sai dẫn đến khách chỉnh sửa thông số, hoặc nhấp nút "Báo cáo lỗi / Ask Human", dữ liệu hội thoại sẽ lưu lại làm Hard-Negative Test Cases để update RAG và Prompt. |
| 2 | Product thu signal gì để biết tốt lên hay tệ đi? | Explicit: Thumbs up/down, feedback text. Implicit: Tỷ lệ khách bấm "Gặp Sales" (Lead Conversion Rate), Tỷ lệ drop-off giữa chừng. |
| 3 | Data thuộc loại nào? | ☑ User-specific · ☑ Domain-specific · ☐ Real-time · ☐ Human-judgment |

**Có marginal value không?** Tận dụng được insight từ lượng hội thoại khổng lồ: Biết được khách hàng đang quan tâm nhiều nhất kịch bản ưu đãi nào (VD: 80% hỏi về tuỳ chọn thuê pin), từ đó tối ưu lại bộ chính sách bán hàng.

## 3. User Stories 4 Paths

| Path | Câu hỏi thiết kế (UX) | Kịch bản áp dụng |
|------|-------------------|-------------------|
| **Happy (AI đúng)** | User thấy gì? Flow kết thúc ra sao? | Khách hỏi: "Tôi ở HN, mua VF 5 thuê pin, dùng voucher. Giá lăn bánh bao nhiêu?". AI list đầy đủ điều kiện, chiết khấu và ra bảng giá chính xác. Khách hài lòng, bấm "Gửi bảng giá qua Zalo" hoặc "Hẹn Sales lái thử". |
| **Low-confidence (AI không chắc)** | System báo bằng cách nào? User quyết thế nào? | Khách đưa ra tổ hợp phức tạp: "Tôi là cư dân Vin, mua trả góp 80% qua Techcombank, có 2 voucher...". AI chưa chắc chắn quy tắc cộng dồn. AI phản hồi: "Dạ cấu hình ưu đãi này có một số chính sách đặc biệt, em xin ước tính khoảng [X] triệu. Xin phép chuyển máy để Chuyên viên tư vấn chính xác nhất nhé!". |
| **Failure (AI sai)** | User biết sai bằng cách nào? Recover ra sao? | AI tính sai phí trước bạ ở tỉnh. Khách phát hiện do khác với số trước đó tìm hiểu. Khách bấm nút "Báo cáo sai - Yêu cầu con người". Sales tiếp quản ngay trên cùng cửa sổ chat (không bắt khách gõ lại từ đầu). |
| **Correction (User sửa)** | User sửa bằng cách nào? Data đó đi vào đâu? | Trên UI bảng giá, khách có thể tự check/uncheck các điều kiện (VD: bỏ tick Voucher). AI tính lại ngay lập tức. Hành vi thay đổi này được lưu xuống DB để phân tích preference của khách. |

## 4. Failure Mode Library

| Định nghĩa lỗi (Failure Mode) | Trigger | Hậu quả | Mitigation (UX/Tech) |
|-----------------------------------|---------|---------|-----------------------|
| Khuyến mãi chồng chéo (Logic Error) | Áp dụng nhiều lớp voucher và ưu đãi trả góp / thu cũ đổi mới. AI làm toán sai. | Báo giá cực thấp nhưng thực tế không mua được, khách khiếu nại lừa đảo. | **Tech:** Tách tác vụ. AI chỉ Extract entities → Hệ thống Rule-based Engine tính toán giá để ra bảng giá tĩnh cuối cùng.<br>**UX:** Disclaimer rõ: "Giá dự toán" |
| Dữ liệu Outdated (Knowledge Gap) | Chương trình "Mãnh liệt tinh thần VN" vừa hết hạn hôm qua, dữ liệu AI chưa update. | Báo giá dựa trên chính sách cũ. | RAG: Gắn expiry date (ngày hết hạn) cho từng chunk data. Nhắc khách hàng trên tooltip thời hạn áp dụng của giá này. |
| Ảo giác (Hallucination) | Khách hỏi cố tình: "Vinfast đang giảm 500tr cho mọi dòng xe đúng không?". AI tự tạo ra ưu đãi. | Bóp méo chính sách công ty. | Kéo mức Temperature = 0. Ép mandatory Prompt: "Tuyệt đối không tự suy diễn ưu đãi ngoài cơ sở dữ liệu đã cung cấp". |

## 5. ROI 3 kịch bản

| | Conservative (Dè dặt) | Realistic (Thực tế) | Optimistic (Lạc quan) |
|---|---|---|---|
| **Assumption** | Người dùng VN không thích bot, 80% vẫn gọi hotline gọi Sale ngay lập tức. | 40% khách tự research và chơi với AI Assistant trước khi quyết định gọi Sale. | Hệ thống chạy quá tốt. 70% khách hàng chốt sơ bộ ý định qua AI. |
| **Cost** | Triển khai: $1k-2k.<br>Vận hành API: ~$50/tháng.<br>Maintenance RAG: 1 người part-time. | Chi phí API/hệ thống tăng theo lượt query ~$200-300/tháng + Đội ngũ review (1 NV). | Scale lớn, API cost ~$1000/tháng. Đội ops RAG chuyên biệt. |
| **Benefit** | Lọc được các FAQ vô nghĩa, tiết kiệm ~5% thời gian cho CSKH. | Tiết kiệm 40% thời gian Sale phải support báo giá cơ bản. Giảm tỷ lệ drop off 15%. | Chốt sale tăng 25%. Trải nghiệm khách hàng cực tốt (WOW). Tiết kiệm chi phí mở rộng headcount CSKH khi có xe mới. |
| **Net** | Hoà vốn thời gian đầu (test thị trường). | Lợi nhuận dương từ tháng thứ 3 nhờ tăng hiệu suất Sale và Lead conversion. | Cực kì thành công, là key growth driver của digital sales. |

*(Kill criteria: Dừng dự án nếu sau 2 tháng, tỉ lệ report AI sai phép tính > 10% hoặc khách hoàn toàn bỏ qua bot)*

## 6. Eval metrics

- **Metric ưu tiên:** **Precision (Độ chính xác)**
  - Bối cảnh: Báo nhầm một ưu đãi không tồn tại (False Positive) nguy hiểm hơn nhiều việc vô tình không nhắc đến một ưu đãi nhỏ (False Negative). Do vậy, thà AI trả lời "Xin kết nối Sales" (giảm Recall) còn hơn đưa ra giá sai (giảm Precision).
- **Mục tiêu kỹ thuật:** Độ chính xác thông tin ưu đãi ≥ 95%. Zero Hallucination.
- **Metric kinh doanh:** Lead Conversion Rate (tỷ lệ chat xong để lại SĐT/Lead) tăng 15% so với flow thông thường. Reduce Average Handle Time của bộ phận Sales.

## 7. Phân công (Mini AI spec & Task)

- **An:** Tập trung viết Canvas chi tiết và liệt kê các Failure modes đầy đủ (edge cases).
- **Bình:** Vẽ Sketch UI Flow và chi tiết User stories 4 paths cho báo cáo.
- **Châu:** Ghi rõ số liệu Eval metrics, bộ Test cases và phân tích bảng ROI.
- **Dũng:** Prototype research (dùng công cụ AI UI builder như v0/Cursor), setup Prompt test case cơ bản (bảng giá VF 5).