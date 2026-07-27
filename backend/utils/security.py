"""
PainToAd AI - Security & Authentication Utilities
=================================================
Implements JWT token generation/decoding, password hashing with bcrypt,
and security payload validation for FastAPI routes.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Union
import jwt
try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except ImportError:
    pwd_context = None

from backend.config.settings import settings
from backend.utils.logger import logger


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a raw password against an encrypted hash.
    """
    if pwd_context:
        return pwd_context.verify(plain_password, hashed_password)
    # Simple fallback check if passlib is missing
    import hashlib
    digest = hashlib.sha256((plain_password + settings.SECRET_KEY).encode("utf-8")).hexdigest()
    return digest == hashed_password


def get_password_hash(password: str) -> str:
    """
    Generates a secure password hash.
    """
    if pwd_context:
        return pwd_context.hash(password)
    import hashlib
    return hashlib.sha256((password + settings.SECRET_KEY).encode("utf-8")).hexdigest()


def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates an encoded JWT access token with expiration time and payload claims.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode: Dict[str, Any] = {
        "exp": expire,
        "sub": str(subject),
        "iat": datetime.now(timezone.utc),
        "iss": settings.APP_NAME
    }

    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error encoding JWT token: {str(e)}")
        raise e


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodes and validates a JWT token string.
    Returns the decoded token payload or None if invalid/expired.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("JWT Token has expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid JWT Token: {str(e)}")
        return None
