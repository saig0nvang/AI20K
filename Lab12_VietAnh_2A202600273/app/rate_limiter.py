from fastapi import HTTPException, Depends
from .auth import verify_api_key
from .config import settings
import redis

# Kết nối Redis
r = redis.from_url(settings.REDIS_URL, decode_responses=True)

def check_rate_limit(user_id: str = Depends(verify_api_key)):
    """
    Giới hạn số lượng request trên mỗi phút cho mỗi user.
    """
    key = f"rate_limit:{user_id}"
    current_count = r.get(key)
    
    if current_count and int(current_count) >= settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {settings.RATE_LIMIT_PER_MINUTE} requests per minute."
        )
    
    # Tăng biến đếm và set thời gian hết hạn là 60s nếu là request đầu tiên trong phút
    pipe = r.pipeline()
    pipe.incr(key)
    pipe.expire(key, 60, nx=True)
    pipe.execute()
    
    return True

