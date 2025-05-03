from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_user(db: Session, user: UserCreate) -> User:
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user:
            return None

        db_user = User(
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=hash_password(user.password),
            role=user.role,
            phone_number=user.phone_number
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(f"Error while creating user: {e}")
        return None


def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user: UserUpdate) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if user.email:
            db_user.email = user.email
        if user.first_name:
            db_user.first_name = user.first_name
        if user.last_name:
            db_user.last_name = user.last_name
        if user.password:
            db_user.hashed_password = hash_password(user.password)  # Şifreyi hash'liyoruz
        if user.role:
            db_user.role = user.role
        if user.phone_number:
            db_user.phone_number = user.phone_number
        if user.is_active is not None:
            db_user.is_active = user.is_active

        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def delete_user(db: Session, user_id: int) -> bool:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
