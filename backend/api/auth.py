import os
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt
from database.mongodb import get_database, serialize_doc
from database.schemas import RegisterRequest, LoginRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-secret-key-change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid token", "detail": "Token could not be decoded"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    token = credentials.credentials
    payload = verify_token(token)

    db = get_database()
    user = await db.users.find_one({"_id": payload.get("user_id")})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "User not found", "detail": "Token references non-existent user"},
        )
    return serialize_doc(user)


@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest):
    db = get_database()

    existing_user = await db.users.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Email already registered", "detail": f"User with email {request.email} already exists"},
        )

    from bson import ObjectId
    user_id = str(ObjectId())
    user_doc = {
        "_id": user_id,
        "email": request.email,
        "hashed_password": hash_password(request.password),
        "business_name": request.business_name,
        "industry": request.industry,
        "created_at": datetime.utcnow(),
        "is_active": True,
    }

    await db.users.insert_one(user_doc)

    access_token = create_access_token({"user_id": user_id, "email": request.email})

    user_response = UserResponse(
        id=user_id,
        email=request.email,
        business_name=request.business_name,
        industry=request.industry,
        created_at=user_doc["created_at"],
        is_active=True,
    )

    return TokenResponse(access_token=access_token, user=user_response)


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    db = get_database()

    user = await db.users.find_one({"email": request.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid credentials", "detail": "No user found with this email"},
        )

    if not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid credentials", "detail": "Password does not match"},
        )

    user_id = str(user["_id"])
    access_token = create_access_token({"user_id": user_id, "email": user["email"]})

    user_response = UserResponse(
        id=user_id,
        email=user["email"],
        business_name=user.get("business_name", ""),
        industry=user.get("industry", ""),
        created_at=user["created_at"],
        is_active=user.get("is_active", True),
    )

    return TokenResponse(access_token=access_token, user=user_response)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        business_name=current_user.get("business_name", ""),
        industry=current_user.get("industry", ""),
        created_at=current_user["created_at"],
        is_active=current_user.get("is_active", True),
    )
