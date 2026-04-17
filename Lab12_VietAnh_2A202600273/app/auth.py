from fastapi import Header, HTTPException
from .config import settings

def verify_api_key(x_api_key: str = Header(...)) -> str:
    """
    Kiểm tra API Key từ Header X-API-Key.
    Trả về user_id (giả định dùng chính key hoặc một định danh) nếu hợp lệ.
    """
    if x_api_key != settings.AGENT_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: Invalid API Key"
        )
    
    # Trong một hệ thống thật, bạn có thể map API Key này với một User ID cụ thể.
    # Ở đây chúng ta tạm dùng tag 'default_user' để demo.
    return "default_user"

