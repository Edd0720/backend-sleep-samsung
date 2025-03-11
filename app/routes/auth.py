from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserLogin
from app.services.auth_service import authenticate_user
from app.utils.jwt_handler import create_access_token
from app.db.database import get_db

router = APIRouter()

@router.post("/login")
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    
    # Obtener el tipo de usuario desde la relación con UserType
    role = user.user_type.name  # Accedemos al nombre del tipo de usuario
    
    # Crear el token JWT
    token_data = {"sub": user.email, "role": role}
    access_token = create_access_token(token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}