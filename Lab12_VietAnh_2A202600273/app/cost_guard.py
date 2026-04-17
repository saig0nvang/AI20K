from fastapi import HTTPException, Depends
from .auth import verify_api_key
from .config import settings
import redis

# Kết nối Redis
r = redis.from_url(settings.REDIS_URL, decode_responses=True)

def check_budget(user_id: str = Depends(verify_api_key)):
    """
    Kiểm tra xem tổng chi phí trong tháng đã vượt quá ngân sách chưa.
    """
    # Key lưu trữ chi phí tích lũy theo tháng
    cost_key = f"total_cost:2024-04" # Giả định tháng hiện tại
    current_cost = r.get(cost_key)
    
    if current_cost and float(current_cost) >= settings.MONTHLY_BUDGET_USD:
        raise HTTPException(
            status_code=402, # Payment Required
            detail=f"Monthly budget of ${settings.MONTHLY_BUDGET_USD} exceeded. Contact admin."
        )
    
    # Giả lập tăng chi phí sau mỗi request (ví dụ: $0.01 mỗi query)
    r.incrbyfloat(cost_key, 0.01)
    
    return True

