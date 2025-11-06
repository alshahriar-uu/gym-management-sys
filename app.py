from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import secrets
from config import Config
from models import db, User, Member, PendingRegistration, PasswordResetToken

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)
bcrypt = Bcrypt(app)

# Route: Landing Page
@app.route('/')
def index():
    return render_template('index.html')

# Route: Login Page (GET and POST)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Query user from database
        user = User.query.filter_by(username=username).first()
        
        # Validate credentials
        if user and bcrypt.check_password_hash(user.password_hash, password):
            # Check if role matches (optional validation)
            if user.role == role:
                session['username'] = user.username
                session['role'] = user.role
                session['name'] = user.name
                session['user_id'] = user.id
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid role selected!', 'error')
                return render_template('login.html', error='Invalid role')
        else:
            flash('Invalid username or password!', 'error')
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

# Route: Registration Page (GET and POST)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        phone = request.form.get('phone')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        address = request.form.get('address')
        membership = request.form.get('membership')
        
        # Check if email already exists in pending registrations or members
        existing_pending = PendingRegistration.query.filter_by(email=email).first()
        existing_member = Member.query.filter_by(email=email).first()
        
        if existing_pending or existing_member:
            flash('Email already registered! Please use a different email.', 'error')
            return render_template('register.html')
        
        # Generate registration ID
        count = PendingRegistration.query.count()
        registration_id = f'REG{count + 1:03d}'
        
        # Create new pending registration
        new_registration = PendingRegistration(
            registration_id=registration_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            dob=dob,
            gender=gender,
            address=address,
            membership_type=membership,
            registration_date=datetime.now().strftime('%Y-%m-%d'),
            status='pending'
        )
        
        db.session.add(new_registration)
        db.session.commit()
        
        # Send welcome email
        try:
            send_welcome_email(new_registration)
        except Exception as e:
            print(f"Error sending welcome email: {e}")
            # Continue even if email fails
        
        flash('Registration successful! Your application is pending admin approval. You will be notified via email once approved.', 'success')
        return redirect(url_for('register_success'))
    
    return render_template('register.html')

# Route: Registration Success Page
@app.route('/register-success')
def register_success():
    return render_template('register_success.html')

# Route: Dashboard (requires login)
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    # Count pending registrations
    pending_count = PendingRegistration.query.filter_by(status='pending').count()
    
    # Get approved members for dashboard display
    members = Member.query.all()
    
    return render_template('dashboard.html', 
                         username=session.get('name'),
                         role=session.get('role'),
                         pending_count=pending_count,
                         APPROVED_MEMBERS=members)

# Route: Members Page
@app.route('/members')
def members():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Query all members from database
    all_members = Member.query.all()
    
    return render_template('members.html', members=all_members)

# Route: Trainers Page
@app.route('/trainers')
def trainers():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('trainers.html')

# Route: Classes Page
@app.route('/classes')
def classes():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('classes.html')

# Route: Pending Registrations (Admin Only)
@app.route('/pending-registrations')
def pending_registrations():
    if 'username' not in session or session.get('role') != 'admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('dashboard'))
    
    # Query pending registrations from database
    registrations = PendingRegistration.query.filter_by(status='pending').all()
    
    return render_template('pending_registrations.html', 
                         registrations=registrations)

# Route: Approve Registration
@app.route('/approve-registration/<reg_id>')
def approve_registration(reg_id):
    if 'username' not in session or session.get('role') != 'admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('dashboard'))
    
    # Find registration in database
    registration = PendingRegistration.query.filter_by(registration_id=reg_id).first()
    
    if registration:
        # Generate member ID
        member_count = Member.query.count()
        member_id = f"M{member_count + 1:03d}"
        
        # Get membership amount
        membership_amounts = {
            'basic': 2500,
            'standard': 4500,
            'premium': 7500
        }
        amount = membership_amounts.get(registration.membership_type, 2500)
        
        # Calculate expiry date
        join_date = datetime.now()
        if registration.membership_type == 'basic':
            expiry_date = join_date + timedelta(days=30)
        elif registration.membership_type == 'standard':
            expiry_date = join_date + timedelta(days=30)
        else:  # premium
            expiry_date = join_date + timedelta(days=365)
        
        # Create approved member
        new_member = Member(
            member_id=member_id,
            first_name=registration.first_name,
            last_name=registration.last_name,
            email=registration.email,
            phone=registration.phone,
            dob=registration.dob,
            gender=registration.gender,
            address=registration.address,
            membership_type=f"{registration.membership_type.title()} Plan",
            amount=amount,
            join_date=join_date.strftime('%Y-%m-%d'),
            expiry_date=expiry_date.strftime('%Y-%m-%d'),
            status='active',
            payment_status='pending'
        )
        
        db.session.add(new_member)
        
        # Create user account with default password
        username = registration.email.split('@')[0]
        default_password = 'member123'
        hashed_password = bcrypt.generate_password_hash(default_password).decode('utf-8')
        
        new_user = User(
            username=username,
            email=registration.email,
            password_hash=hashed_password,
            role='member',
            name=f"{registration.first_name} {registration.last_name}"
        )
        
        db.session.add(new_user)
        
        # Update registration status
        registration.status = 'approved'
        
        # Commit all changes
        db.session.commit()
        
        # Send approval email
        try:
            send_approval_email(new_member, username, default_password)
        except Exception as e:
            print(f"Error sending approval email: {e}")
            # Continue even if email fails
        
        flash(f'Registration approved! Member ID: {member_id}. Login credentials sent to {registration.email}', 'success')
    else:
        flash('Registration not found!', 'error')
    
    return redirect(url_for('pending_registrations'))

# Route: Reject Registration
@app.route('/reject-registration/<reg_id>')
def reject_registration(reg_id):
    if 'username' not in session or session.get('role') != 'admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('dashboard'))
    
    # Find registration in database
    registration = PendingRegistration.query.filter_by(registration_id=reg_id).first()
    
    if registration:
        # Update status to rejected
        registration.status = 'rejected'
        db.session.commit()
        
        flash(f'Registration rejected for {registration.first_name} {registration.last_name}', 'warning')
    else:
        flash('Registration not found!', 'error')
    
    return redirect(url_for('pending_registrations'))

# Route: Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))
# Add this AFTER the existing routes, BEFORE if __name__ == '__main__':

# Route: Delete Member
@app.route('/delete-member/<member_id>')
def delete_member(member_id):
    if 'username' not in session or session.get('role') != 'admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('dashboard'))
    
    # Find member in database
    member = Member.query.filter_by(member_id=member_id).first()
    
    if member:
        db.session.delete(member)
        db.session.commit()
        flash(f'Member {member.first_name} {member.last_name} deleted successfully!', 'success')
    else:
        flash('Member not found!', 'error')
    
    return redirect(url_for('dashboard'))

# Route: View Member Details (JSON for AJAX)
@app.route('/api/member/<member_id>')
def get_member(member_id):
    if 'username' not in session:
        return {'error': 'Unauthorized'}, 401
    
    # Find member in database
    member = Member.query.filter_by(member_id=member_id).first()
    
    if member:
        return {
            'id': member.member_id,
            'first_name': member.first_name,
            'last_name': member.last_name,
            'email': member.email,
            'phone': member.phone,
            'membership': member.membership_type,
            'amount': member.amount,
            'join_date': member.join_date,
            'expiry_date': member.expiry_date,
            'status': member.status
        }
    else:
        return {'error': 'Member not found'}, 404

# Route: Edit Member (Future implementation)
@app.route('/edit-member/<member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    if 'username' not in session or session.get('role') != 'admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('dashboard'))
    
    # Find member in database
    member = Member.query.filter_by(member_id=member_id).first()
    
    if not member:
        flash('Member not found!', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Update member data
        member.first_name = request.form.get('firstName')
        member.last_name = request.form.get('lastName')
        member.email = request.form.get('email')
        member.phone = request.form.get('phone')
        member.membership_type = request.form.get('membership')
        member.status = request.form.get('status')
        member.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash(f'Member {member.first_name} {member.last_name} updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_member.html', member=member)

# Route: Forgot Password
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate reset token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(hours=1)
            
            # Create password reset token
            reset_token = PasswordResetToken(
                user_id=user.id,
                token=token,
                expires_at=expires_at,
                used=False
            )
            
            db.session.add(reset_token)
            db.session.commit()
            
            # Send password reset email
            try:
                send_password_reset_email(user, token)
                flash('Password reset link has been sent to your email!', 'success')
            except Exception as e:
                print(f"Error sending password reset email: {e}")
                flash('Error sending email. Please try again later.', 'error')
        else:
            # Don't reveal if email exists or not for security
            flash('If your email is registered, you will receive a password reset link.', 'success')
        
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html')

# Route: Reset Password
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Find token in database
    reset_token = PasswordResetToken.query.filter_by(token=token, used=False).first()
    
    if not reset_token:
        flash('Invalid or expired reset link!', 'error')
        return redirect(url_for('login'))
    
    # Check if token is expired
    if reset_token.expires_at < datetime.utcnow():
        flash('Reset link has expired!', 'error')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('reset_password.html', token=token)
        
        # Update user password
        user = User.query.get(reset_token.user_id)
        user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Mark token as used
        reset_token.used = True
        
        db.session.commit()
        
        flash('Password reset successful! You can now login with your new password.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)

# Email helper functions
def send_welcome_email(registration):
    """Send welcome email to new registration"""
    try:
        msg = Message(
            subject='Welcome to GymFit Bangladesh - Registration Received',
            recipients=[registration.email]
        )
        
        msg.html = render_template(
            'email/welcome.html',
            first_name=registration.first_name,
            last_name=registration.last_name,
            registration_id=registration.registration_id,
            membership_type=registration.membership_type.title(),
            registration_date=registration.registration_date,
            year=datetime.now().year
        )
        
        mail.send(msg)
    except Exception as e:
        print(f"Error sending welcome email: {e}")
        raise

def send_approval_email(member, username, password):
    """Send approval email with login credentials"""
    try:
        msg = Message(
            subject='Registration Approved - Welcome to GymFit Bangladesh!',
            recipients=[member.email]
        )
        
        login_url = url_for('login', _external=True)
        
        msg.html = render_template(
            'email/approval.html',
            first_name=member.first_name,
            last_name=member.last_name,
            member_id=member.member_id,
            membership_type=member.membership_type,
            join_date=member.join_date,
            expiry_date=member.expiry_date,
            amount=member.amount,
            username=username,
            password=password,
            login_url=login_url,
            year=datetime.now().year
        )
        
        mail.send(msg)
    except Exception as e:
        print(f"Error sending approval email: {e}")
        raise

def send_password_reset_email(user, token):
    """Send password reset email"""
    try:
        msg = Message(
            subject='Reset Your Password - GymFit Bangladesh',
            recipients=[user.email]
        )
        
        reset_url = url_for('reset_password', token=token, _external=True)
        
        msg.html = render_template(
            'email/reset_password.html',
            name=user.name,
            reset_url=reset_url,
            year=datetime.now().year
        )
        
        mail.send(msg)
    except Exception as e:
        print(f"Error sending password reset email: {e}")
        raise

# Context processor for current year
@app.context_processor
def inject_now():
    return {'now': datetime.now(), 'year': datetime.now().year}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)