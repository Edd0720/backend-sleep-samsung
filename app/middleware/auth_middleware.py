from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt_handler import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def admin_only(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload.get("role") != "admin":  # Verificamos si el rol es "admin"
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder a este recurso",
        )
    return payload