"""认证相关的工具函数"""
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from passlib.context import CryptContext
from jose import jwt
from sqlalchemy.orm import Session
from . import models
from .validators import validate_email, validate_password, sanitize_email

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 配置
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24小时

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, email: str, password: str) -> Tuple[Optional[models.User], Optional[str]]:
    """
    验证用户
    
    Returns:
        Tuple[Optional[models.User], Optional[str]]: (用户对象, 错误信息)
    """
    # 验证邮箱格式
    email_valid, email_error = validate_email(email)
    if not email_valid:
        return None, email_error
    
    # 清理邮箱
    email = sanitize_email(email)
    
    # 获取用户
    user = get_user_by_email(db, email)
    if not user:
        return None, "用户不存在"
    
    # 验证密码
    if not verify_password(password, user.hashed_password):
        return None, "密码错误"
    
    return user, None

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """通过邮箱获取用户"""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, email: str, password: str) -> Tuple[Optional[models.User], Optional[str]]:
    """
    创建新用户
    
    Returns:
        Tuple[Optional[models.User], Optional[str]]: (用户对象, 错误信息)
    """
    # 验证邮箱格式
    email_valid, email_error = validate_email(email)
    if not email_valid:
        return None, email_error
    
    # 验证密码强度
    password_valid, password_error = validate_password(password)
    if not password_valid:
        return None, password_error
    
    # 清理邮箱
    email = sanitize_email(email)
    
    # 检查邮箱是否已存在
    if get_user_by_email(db, email):
        return None, "该邮箱已被注册"
    
    # 创建新用户
    try:
        hashed_password = get_password_hash(password)
        db_user = models.User(email=email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user, None
    except Exception as e:
        db.rollback()
        return None, f"创建用户失败：{str(e)}"
