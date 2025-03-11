from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.user import User
import bcrypt

async def authenticate_user(db: AsyncSession, user_data):
    try:
        # Consultar al usuario en la base de datos y cargar la relación 'user_type'
        result = await db.execute(
            select(User)
            .filter(User.email == user_data.email)
            .options(selectinload(User.user_type))  # Cargar la relación 'user_type'
        )
        user = result.scalars().first()

        # Verificar si el usuario existe
        if not user:
            return None

        # Comparar la contraseña encriptada
        if not bcrypt.checkpw(user_data.password.encode('utf-8'), user.password.encode('utf-8')):
            return None

        return user

    except Exception as e:
        # Manejo de errores (puedes personalizar el registro del error)
        print(f"Error autenticando al usuario: {e}")
        return None
