from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Demo user credentials
USERS = {
    'admin': {'password': 'admin123', 'role': 'admin', 'name': 'Al Shahriar'},
    'trainer': {'password': 'trainer123', 'role': 'trainer', 'name': 'Trainer'},
    'member': {'password': 'member123', 'role': 'member', 'name': 'Member'}
}

# Temporary storage for pending registrations
PENDING_REGISTRATIONS = []

# Approved members (temporary storage)
APPROVED_MEMBERS = [
    {
        'id': 'M001',
        'first_name': 'Rakib',
        'last_name': 'Hassan',
        'email': 'rakib@email.com',
        'phone': '+880 1711-234567',
        'membership': 'Premium Plan',
        'amount': 7500,
        'join_date': '2025-10-15',
        'expiry_date': '2026-10-15',
        'status': 'active'
    },
    {
        'id': 'M002',
        'first_name': 'Nusrat',
        'last_name': 'Jahan',
        'email': 'nusrat@email.com',
        'phone': '+880 1712-345678',
        'membership': 'Standard Plan',
        'amount': 4500,
        'join_date': '2025-10-20',
        'expiry_date': '2025-11-20',
        'status': 'active'
    }
]

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
        
        # Validate credentials
        if username in USERS and USERS[username]['password'] == password:
            session['username'] = username
            session['role'] = role
            session['name'] = USERS[username]['name']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

# Route: Registration Page (GET and POST)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        registration_data = {
            'id': f'REG{len(PENDING_REGISTRATIONS) + 1:03d}',
            'first_name': request.form.get('firstName'),
            'last_name': request.form.get('lastName'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'dob': request.form.get('dob'),
            'gender': request.form.get('gender'),
            'address': request.form.get('address'),
            'membership': request.form.get('membership'),
            'registration_date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'pending'
        }
        
        # Check if email already exists
        email_exists = any(
            reg['email'] == registration_data['email'] 
            for reg in PENDING_REGISTRATIONS
        )
        
        if email_exists:
            flash('Email already registered! Please use a different email.', 'error')
            return render_template('register.html')
        
        # Add to pending registrations
        PENDING_REGISTRATIONS.append(registration_data)
        
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
    pending_count = len(PENDING_REGISTRATIONS)
    
    return render_template('dashboard.html', 
                         username=session.get('name'),
                         role=session.get('role'),
                         pending_count=pending_count,APPROVED_MEMBERS=APPROVED_MEMBERS)

# Route: Members Page
@app.route('/members')
def members():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('members.html', members=APPROVED_MEMBERS)

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
    
    return render_template('pending_registrations.html', 
                         registrations=PENDING_REGISTRATIONS)

# Route: Approve Registration
@app.route('/approve-registration/<reg_id>')
def approve_registration(reg_id):
    if 'username' not in session or session.get('role') != 'admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('dashboard'))
    
    # Find registration
    registration = next((r for r in PENDING_REGISTRATIONS if r['id'] == reg_id), None)
    
    if registration:
        # Create member ID
        member_id = f"M{len(APPROVED_MEMBERS) + 3:03d}"
        
        # Get membership amount
        membership_amounts = {
            'basic': 2500,
            'standard': 4500,
            'premium': 7500
        }
        amount = membership_amounts.get(registration['membership'], 2500)
        
        # Calculate expiry date
        from datetime import datetime, timedelta
        join_date = datetime.now()
        if registration['membership'] == 'basic':
            expiry_date = join_date + timedelta(days=30)
        elif registration['membership'] == 'standard':
            expiry_date = join_date + timedelta(days=30)
        else:  # premium
            expiry_date = join_date + timedelta(days=365)
        
        # Create approved member
        approved_member = {
            'id': member_id,
            'first_name': registration['first_name'],
            'last_name': registration['last_name'],
            'email': registration['email'],
            'phone': registration['phone'],
            'membership': f"{registration['membership'].title()} Plan",
            'amount': amount,
            'join_date': join_date.strftime('%Y-%m-%d'),
            'expiry_date': expiry_date.strftime('%Y-%m-%d'),
            'status': 'active'
        }
        
        # Add to approved members
        APPROVED_MEMBERS.append(approved_member)
        
        # Create user account
        username = registration['email'].split('@')[0]
        USERS[username] = {
            'password': 'member123',  # Default password
            'role': 'member',
            'name': f"{registration['first_name']} {registration['last_name']}"
        }
        
        # Remove from pending
        PENDING_REGISTRATIONS.remove(registration)
        
        flash(f'Registration approved! Member ID: {member_id}. Login credentials sent to {registration["email"]}', 'success')
    else:
        flash('Registration not found!', 'error')
    
    return redirect(url_for('pending_registrations'))

# Route: Reject Registration
@app.route('/reject-registration/<reg_id>')
def reject_registration(reg_id):
    if 'username' not in session or session.get('role') != 'admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('dashboard'))
    
    # Find and remove registration
    registration = next((r for r in PENDING_REGISTRATIONS if r['id'] == reg_id), None)
    
    if registration:
        PENDING_REGISTRATIONS.remove(registration)
        flash(f'Registration rejected for {registration["first_name"]} {registration["last_name"]}', 'warning')
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
    
    global APPROVED_MEMBERS
    
    # Find and remove member
    member = next((m for m in APPROVED_MEMBERS if m['id'] == member_id), None)
    
    if member:
        APPROVED_MEMBERS.remove(member)
        flash(f'Member {member["first_name"]} {member["last_name"]} deleted successfully!', 'success')
    else:
        flash('Member not found!', 'error')
    
    return redirect(url_for('dashboard'))

# Route: View Member Details (JSON for AJAX)
@app.route('/api/member/<member_id>')
def get_member(member_id):
    if 'username' not in session:
        return {'error': 'Unauthorized'}, 401
    
    member = next((m for m in APPROVED_MEMBERS if m['id'] == member_id), None)
    
    if member:
        return member
    else:
        return {'error': 'Member not found'}, 404

# Route: Edit Member (Future implementation)
@app.route('/edit-member/<member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    if 'username' not in session or session.get('role') != 'admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('dashboard'))
    
    member = next((m for m in APPROVED_MEMBERS if m['id'] == member_id), None)
    
    if not member:
        flash('Member not found!', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Update member data
        member['first_name'] = request.form.get('firstName')
        member['last_name'] = request.form.get('lastName')
        member['email'] = request.form.get('email')
        member['phone'] = request.form.get('phone')
        member['membership'] = request.form.get('membership')
        member['status'] = request.form.get('status')
        
        flash(f'Member {member["first_name"]} {member["last_name"]} updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_member.html', member=member)

# Context processor for current year
@app.context_processor
def inject_now():
    return {'now': datetime.now(), 'year': datetime.now().year}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)