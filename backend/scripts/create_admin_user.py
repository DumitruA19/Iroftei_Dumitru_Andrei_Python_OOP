# scripts/create_admin_user.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import SessionLocal
from models.orm import User
from utils.password import hash_password

db = SessionLocal()

existing = db.query(User).filter(User.username == "admin").first()
if existing:
    print("⚠️ User already exists.")
else:
    user = User(
        username="admin",
        hashed_password=hash_password("admin")
    )
    db.add(user)
    db.commit()
    print("✅ Admin user created: admin/admin")
