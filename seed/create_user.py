"""
Create initial user for development
"""

import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.database import AsyncSessionLocal, User
from src.auth import get_password_hash
from sqlalchemy import select


async def create_admin_user():
    """Create admin user for development"""
    async with AsyncSessionLocal() as db:
        # Check if admin user already exists
        result = await db.execute(select(User).where(User.username == "admin"))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True
        )
        
        db.add(admin_user)
        await db.commit()
        await db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("Email: admin@example.com")


if __name__ == "__main__":
    asyncio.run(create_admin_user())
