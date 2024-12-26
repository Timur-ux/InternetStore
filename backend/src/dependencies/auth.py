from fastapi import Depends, HTTPException
from async_fastapi_jwt_auth import AuthJWT
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(Authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme)) -> int:
    try:
        await Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return int(user_id)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
