
C:\Users\speed\Desktop\lab4>python agent.py
Xin chào! Tôi có thể giúp gì cho bạn hôm nay?


# Test case 1
Bạn: Bạn: Xin chào! tôi đang muốn đi du lịch nhưng không biết đi đâu

Thinking...
Trả lời trực tiếp

TravelBuddy: Thưa bạn, bạn thích đi du lịch trong nước hay nước ngoài? Bạn có ngân sách và thời gian dự kiến cho chuyến đi không? Mình sẽ giúp bạn tư vấn điểm đến phù hợp nhé! Bạn có thắc mắc gì không?

# Test case 2
Bạn: Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

Thinking...
Đang gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
Trả lời trực tiếp

TravelBuddy: Thưa bạn, dưới đây là một số chuyến bay từ Hà Nội đi Đà Nẵng bạn có thể tham khảo:

-Vietnam Airlines (hạng phổ thông): bay lúc 06:00 đến 07:20, giá vé khoảng 1.450.000đ
-Vietnam Airlines (hạng thương gia): bay lúc 14:00 đến 15:20, giá vé khoảng 2.800.000đ
-VietJet Air (hạng phổ thông): bay lúc 08:30 đến 09:50, giá vé khoảng 890.000đ
-Bamboo Airways (hạng phổ thông): bay lúc 11:00 đến 12:20, giá vé khoảng 1.200.000đ

# Test case 3
Bạn: Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

Thinking...
Đang gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
Đang gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 2500000})
Đang gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1100000,khách_sạn:1600000'})
Trả lời trực tiếp

TravelBuddy: Thưa bạn,

Chuyến bay: VietJet Air, bay lúc 16:00 - 18:15, giá vé 1.100.000đ
Khách sạn: Lahana Resort, 3 sao, khu vực Dương Đông, giá phòng 800.000đ/đêm (2 đêm tổng 1.600.000đ)

Bảng chi phí:
- Vé máy bay: 1.100.000đ
- Khách sạn: 1.600.000đ
---
Tổng chi: 2.700.000đ
Ngân sách: 5.000.000đ
Còn lại: 2.300.000đ

Gợi ý thêm: Bạn có thể thưởng thức hải sản tươi ngon tại chợ đêm Dinh Cậu hoặc tham quan Vinpearl Safari Phú Quốc. Thời tiết Phú Quốc thường nắng ấm, bạn nên chuẩn bị kem chống nắng và đồ bơi nhé.

Bạn có thắc mắc gì không?

# Test case 4
Bạn: Tôi muốn đặt khách sạn

Thinking...
Trả lời trực tiếp
TravelBuddy: Thưa bạn, bạn muốn đặt khách sạn ở đâu và ngân sách của bạn là bao nhiêu? Bạn có thể cho tôi biết thêm chi tiết để tôi tư vấn phù hợp nhé. Bạn có thắc mắc gì không?

# Test case 5
Bạn: Giải giúp tôi bài tập lập trình Python về Linkedlist 

Thinking...
Trả lời trực tiếp

TravelBuddy: Thưa bạn, mình chuyên tư vấn về du lịch và các dịch vụ liên quan của TravelBuddy thôi nhé. Nếu bạn cần hỗ trợ về du lịch, mình rất sẵn lòng giúp đỡ bạn! Bạn có muốn hỏi về chuyến đi nào không?