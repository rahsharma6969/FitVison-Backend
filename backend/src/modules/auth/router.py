from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import create_access_token
from src.modules.auth.dependencies import get_current_user
from src.modules.auth.schemas import TokenResponse, UserResponse, UserSignupRequest
from src.modules.auth.service import authenticate_user, create_user

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: UserSignupRequest, db: Session = Depends(get_db)):
    user = create_user(db, payload)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    return user


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserResponse)
def read_me(current_user=Depends(get_current_user)):
    return current_user