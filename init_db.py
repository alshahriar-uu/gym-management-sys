#!/usr/bin/env python3
"""
Database initialization script
Creates the database and adds the admin account
"""

from app import app, db
from models import User
from flask_bcrypt import Bcrypt
from config import Config

bcrypt = Bcrypt()

def init_database():
    """Initialize the database and create admin account"""
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Check if admin already exists
        admin = User.query.filter_by(username=Config.ADMIN_USERNAME).first()
        
        if admin:
            print(f"✓ Admin account already exists: {Config.ADMIN_USERNAME}")
        else:
            # Create admin account
            print("Creating admin account...")
            hashed_password = bcrypt.generate_password_hash(Config.ADMIN_PASSWORD).decode('utf-8')
            
            admin_user = User(
                username=Config.ADMIN_USERNAME,
                email=Config.ADMIN_EMAIL,
                password_hash=hashed_password,
                role='admin',
                name='Admin User'
            )
            
            db.session.add(admin_user)
            db.session.commit()
            
            print(f"✓ Admin account created successfully!")
            print(f"  Username: {Config.ADMIN_USERNAME}")
            print(f"  Email: {Config.ADMIN_EMAIL}")
            # NOTE: Password displayed only during initial setup for admin access
            # This should only be run in a secure environment during installation
            print(f"  Password: {Config.ADMIN_PASSWORD}")
            print(f"  Role: admin")
            print(f"\n⚠️  IMPORTANT: Please change this password after first login!")
        
        print("\n✓ Database initialization complete!")

if __name__ == '__main__':
    init_database()
