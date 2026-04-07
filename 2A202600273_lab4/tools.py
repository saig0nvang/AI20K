from langchain_core.tools import tool
from typing import Dict, List, Tuple

# ============================================================
# MOCK DATA — Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases.
# ============================================================

FLIGHTS_DB: Dict[Tuple[str, str], List[dict]] = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB: Dict[str, List[dict]] = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}


def format_price(price: int) -> str:
    """Format price with dots as thousand separators and 'đ' suffix."""
    return f"{price:,.0f}đ".replace(",", ".")


@tool
def search_flights(origin: str, destination: str) -> str:
    """Tìm kiếm các chuyến bay giữa hai thành phố.
    
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    # Normalize input strings
    origin_normalized = _normalize_city_name(origin)
    destination_normalized = _normalize_city_name(destination)
    
    if not origin_normalized or not destination_normalized:
        return f"Không nhận diện được thành phố '{origin}' hoặc '{destination}'. Các thành phố hỗ trợ: Hà Nội, Đà Nẵng, Phú Quốc, Hồ Chí Minh."
    
    # Try direct lookup
    key = (origin_normalized, destination_normalized)
    flights = FLIGHTS_DB.get(key)
    
    # If not found, try reverse lookup
    if flights is None:
        reverse_key = (destination_normalized, origin_normalized)
        flights = FLIGHTS_DB.get(reverse_key)
        if flights:
            return f"Không có chuyến bay trực tiếp từ {origin_normalized} đến {destination_normalized}. Tuy nhiên, có chuyến bay theo chiều ngược lại:\n\n" + _format_flights(flights)
    
    if flights is None:
        return f"Không tìm thấy chuyến bay từ {origin_normalized} đến {destination_normalized}."
    
    return _format_flights(flights)


def _normalize_city_name(city: str) -> str:
    """Normalize city name to match database keys."""
    city_lower = city.lower().strip()
    city_mapping = {
        "ha noi": "Hà Nội",
        "hà nội": "Hà Nội",
        "da nang": "Đà Nẵng",
        "đà nẵng": "Đà Nẵng",
        "phu quoc": "Phú Quốc",
        "phú quốc": "Phú Quốc",
        "ho chi minh": "Hồ Chí Minh",
        "hồ chí minh": "Hồ Chí Minh",
        "sai gon": "Hồ Chí Minh",
        "sài gòn": "Hồ Chí Minh",
    }
    return city_mapping.get(city_lower, city)


def _format_flights(flights: List[dict]) -> str:
    """Format a list of flights into a readable string."""
    result = "✈️ Danh sách chuyến bay:\n"
    result += "-" * 50 + "\n"
    for i, flight in enumerate(flights, 1):
        result += f"{i}. {flight['airline']}\n"
        result += f"   Giờ đi: {flight['departure']} → Giờ đến: {flight['arrival']}\n"
        result += f"   Hạng: {flight['class'].title()}\n"
        result += f"   Giá: {format_price(flight['price'])}\n"
        result += "-" * 50 + "\n"
    return result


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    city_normalized = _normalize_city_name(city)
    
    if not city_normalized:
        return f"Không nhận diện được thành phố '{city}'. Các thành phố hỗ trợ: Hà Nội, Đà Nẵng, Phú Quốc, Hồ Chí Minh."
    
    hotels = HOTELS_DB.get(city_normalized)
    
    if hotels is None:
        return f"Không tìm thấy khách sạn tại {city_normalized}."
    
    # Filter by max price
    filtered_hotels = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
    
    if not filtered_hotels:
        return f"Không tìm thấy khách sạn tại {city_normalized} với giá dưới {format_price(max_price_per_night)}/đêm. Hãy thử tăng ngân sách."
    
    # Sort by rating descending
    filtered_hotels.sort(key=lambda x: x["rating"], reverse=True)
    
    return _format_hotels(filtered_hotels, city_normalized)


def _format_hotels(hotels: List[dict], city: str) -> str:
    """Format a list of hotels into a readable string."""
    result = f"🏨 Danh sách khách sạn tại {city}:\n"
    result += "=" * 50 + "\n"
    for i, hotel in enumerate(hotels, 1):
        result += f"{i}. {hotel['name']} {'⭐' * hotel['stars']}\n"
        result += f"   Khu vực: {hotel['area']}\n"
        result += f"   Giá: {format_price(hotel['price_per_night'])}/đêm\n"
        result += f"   Đánh giá: {hotel['rating']}/5.0\n"
        result += "-" * 50 + "\n"
    return result


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    try:
        # Parse expenses
        expense_dict: Dict[str, int] = {}
        if expenses.strip():
            items = expenses.split(",")
            for item in items:
                item = item.strip()
                if ":" not in item:
                    return f"Lỗi format chi phí: '{item}' không có dấu ':'. Vui lòng dùng format 'tên_khoản:số_tiền'."
                parts = item.split(":", 1)
                if len(parts) != 2:
                    return f"Lỗi format chi phí: '{item}'. Vui lòng dùng format 'tên_khoản:số_tiền'."
                name, amount_str = parts[0].strip(), parts[1].strip()
                try:
                    amount = int(amount_str)
                except ValueError:
                    try:
                        amount = int(amount_str.replace(".", "").replace(",", ""))
                    except ValueError:
                        return f"Lỗi format số tiền: '{amount_str}' không phải là số hợp lệ."
                expense_dict[name] = amount
        
        # Calculate total expenses
        total_expenses = sum(expense_dict.values())
        remaining = total_budget - total_expenses
        
        # Format output
        result = "📊 Bảng chi phí:\n"
        result += "=" * 40 + "\n"
        for name, amount in expense_dict.items():
            result += f"  - {name.replace('_', ' ').title()}: {format_price(amount)}\n"
        result += "-" * 40 + "\n"
        result += f"  Tổng chi: {format_price(total_expenses)}\n"
        result += f"  Ngân sách: {format_price(total_budget)}\n"
        
        if remaining >= 0:
            result += f"  ✅ Còn lại: {format_price(remaining)}\n"
        else:
            result += f"  ❌ VƯỢT NGÂN SÁCH: Thiếu {format_price(abs(remaining))}!\n"
            result += f"  ⚠️ Cần điều chỉnh: giảm chi phí hoặc tăng ngân sách.\n"
        
        return result
        
    except Exception as e:
        return f"Lỗi khi tính toán ngân sách: {str(e)}. Vui lòng kiểm tra lại input."
