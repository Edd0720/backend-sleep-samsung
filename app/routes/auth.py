from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserLogin, User
from app.services.auth_service import authenticate_user
from app.utils.jwt_handler import create_access_token, invalidate_token
from app.db.database import get_db
from app.middleware.auth_middleware import admin_only
from fastapi.security import OAuth2PasswordBearer

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
    
    # Convertir el usuario a un esquema Pydantic para retornarlo
    user_dict = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "gender": user.gender,
        "weight": user.weight,
        "id_user_type": user.id_user_type,
        "role": role
    }

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_dict
    }

# Para permitir el acceso solo si el usuario es admin
@router.get("/admin")
async def admin_route(user_data: dict = Depends(admin_only)):
    return {"message": "Bienvenido, admin"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # Invalidar el token
    invalidate_token(token)
    return {"message": "Sesión cerrada exitosamente"}
