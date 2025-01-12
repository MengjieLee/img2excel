"""验证工具模块"""
import re
from typing import Tuple, Optional

def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    验证邮箱格式
    
    Args:
        email: 待验证的邮箱地址
        
    Returns:
        Tuple[bool, Optional[str]]: (是否有效, 错误信息)
    """
    # 邮箱格式正则表达式
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not email:
        return False, "邮箱不能为空"
    
    if len(email) > 255:
        return False, "邮箱长度不能超过255个字符"
    
    if not re.match(pattern, email):
        return False, "邮箱格式不正确"
    
    return True, None

def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """
    验证密码强度
    
    Args:
        password: 待验证的密码
        
    Returns:
        Tuple[bool, Optional[str]]: (是否有效, 错误信息)
    """
    if not password:
        return False, "密码不能为空"
    
    if len(password) < 8:
        return False, "密码长度不能少于8个字符"
    
    if len(password) > 72:  # bcrypt 限制
        return False, "密码长度不能超过72个字符"
    
    # 检查是否包含数字
    if not any(char.isdigit() for char in password):
        return False, "密码必须包含至少一个数字"
    
    # 检查是否包含字母
    if not any(char.isalpha() for char in password):
        return False, "密码必须包含至少一个字母"
    
    # 检查是否包含特殊字符
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(char in special_chars for char in password):
        return False, "密码必须包含至少一个特殊字符"
    
    return True, None

def sanitize_email(email: str) -> str:
    """
    清理邮箱地址
    
    Args:
        email: 原始邮箱地址
        
    Returns:
        str: 清理后的邮箱地址
    """
    return email.lower().strip()
