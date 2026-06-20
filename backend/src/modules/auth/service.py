from sqlalchemy.orm import Session

from src.core.security import hash_password, verify_password
from src.modules.auth.schemas import UserSignupRequest
from src.modules.users.models import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, payload: UserSignupRequest):
    existing_user = get_user_by_email(db, payload.email)
    if existing_user:
        return None

    user = User(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        password_hash=hash_password(payload.password),
        role="customer",
        status="active",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user