from sqlalchemy.orm import Session
from models import User

# Retrieve all users


def get_all_users(db: Session):
    return db.query(User).all()

# Find user by username


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Insert new user


def create_user(db: Session, username: str, email: str):
    try:
        new_user = User(username=username, email=email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
        return None

# Update user email


def update_user_email(db: Session, username: str, new_email: str):
    user = get_user_by_username(db, username)
    if user:
        user.email = new_email
        db.commit()
        db.refresh(user)
        return user
    return None
