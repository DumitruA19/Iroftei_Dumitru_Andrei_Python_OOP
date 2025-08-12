# scripts/create_admin_user.py
from database import SessionLocal
from models.orm import User
from utils.password import hash_password

db = SessionLocal()

# Prevent duplicates
existing = db.query(User).filter(User.username == "admin").first()
if not existing:
    user = User(
        username="admin",
        hashed_password=hash_password("admin")
    )
    db.add(user)
    db.commit()
    print("✅ Admin user created with username: admin and password: admin")
else:
    print("⚠️ User 'admin' already exists.")
