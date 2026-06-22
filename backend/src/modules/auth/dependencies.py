from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import decode_access_token
from src.modules.auth.service import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception

    return user