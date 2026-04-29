import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from app.schemas.auth import TokenPayload


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"authentication is not configured: {name} is required",
        )
    return value


def get_jwt_algorithm() -> str:
    return os.getenv("JWT_ALGORITHM", "HS256")


def get_access_token_expire_minutes() -> int:
    raw_value = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    try:
        return int(raw_value)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "authentication is not configured: "
                "ACCESS_TOKEN_EXPIRE_MINUTES must be an integer"
            ),
        ) from exc


def bearer_unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def verify_password(plain_password: str, password_hash: str) -> bool:
    try:
        return pwd_context.verify(plain_password, password_hash)
    except ValueError:
        return False


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(subject: str, role: str = "admin") -> str:
    secret_key = get_required_env("SECRET_KEY")
    algorithm = get_jwt_algorithm()
    expire_minutes = get_access_token_expire_minutes()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    payload = {"sub": subject, "role": role, "exp": expires_at}
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode_access_token(token: str) -> TokenPayload:
    secret_key = get_required_env("SECRET_KEY")
    algorithm = get_jwt_algorithm()

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
    except ExpiredSignatureError as exc:
        raise bearer_unauthorized("token has expired") from exc
    except JWTError as exc:
        raise bearer_unauthorized("invalid authentication token") from exc

    subject = payload.get("sub")
    if not isinstance(subject, str) or not subject:
        raise bearer_unauthorized("invalid authentication token")

    role = payload.get("role")
    if role is not None and not isinstance(role, str):
        raise bearer_unauthorized("invalid authentication token")

    return TokenPayload(sub=subject, role=role)


def authenticate_admin(username: str, password: str) -> bool:
    admin_username = get_required_env("ADMIN_USERNAME")
    admin_password_hash = get_required_env("ADMIN_PASSWORD_HASH")

    if username != admin_username:
        return False
    return verify_password(password, admin_password_hash)


async def require_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> TokenPayload:
    if credentials is None:
        raise bearer_unauthorized("missing bearer token")
    if credentials.scheme.lower() != "bearer":
        raise bearer_unauthorized("invalid authentication scheme")

    token_payload = decode_access_token(credentials.credentials)
    if token_payload.role != "admin":
        raise bearer_unauthorized("admin privileges are required")
    return token_payload
