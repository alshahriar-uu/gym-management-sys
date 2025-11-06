from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='member')  # admin, trainer, member
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Member(db.Model):
    """Member model for gym members"""
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.String(20), unique=True, nullable=False)  # M001, M002, etc.
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(20))  # Date of birth
    gender = db.Column(db.String(10))  # male, female, other
    address = db.Column(db.Text)
    membership_type = db.Column(db.String(50), nullable=False)  # basic, standard, premium
    amount = db.Column(db.Float, nullable=False)
    join_date = db.Column(db.String(20), nullable=False)
    expiry_date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')  # active, inactive, expired
    
    # Payment fields
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, failed
    payment_method = db.Column(db.String(50))  # cash, card, bkash, sslcommerz, etc.
    transaction_id = db.Column(db.String(100))
    payment_date = db.Column(db.String(20))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Member {self.member_id} - {self.first_name} {self.last_name}>'


class PendingRegistration(db.Model):
    """Pending registration model for new member applications"""
    __tablename__ = 'pending_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.String(20), unique=True, nullable=False)  # REG001, REG002, etc.
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    address = db.Column(db.Text)
    membership_type = db.Column(db.String(50), nullable=False)  # basic, standard, premium
    registration_date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, approved, rejected
    
    def __repr__(self):
        return f'<PendingRegistration {self.registration_id} - {self.first_name} {self.last_name}>'


class PasswordResetToken(db.Model):
    """Password reset token model"""
    __tablename__ = 'password_reset_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('reset_tokens', lazy=True))
    
    def __repr__(self):
        return f'<PasswordResetToken {self.token[:10]}...>'
