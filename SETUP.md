# GymFit Bangladesh - Setup Guide

Complete setup instructions for installing and running the GymFit Bangladesh gym management system on Fedora 42.

## Prerequisites

Before you begin, ensure you have the following:
- Fedora 42 (or compatible Linux distribution)
- Python 3.8 or higher
- Internet connection
- Gmail account (for email functionality)

## Installation Steps

### 1. Install Python and Required System Packages

Open a terminal and run:

```bash
# Update system packages
sudo dnf update -y

# Install Python 3 and pip
sudo dnf install python3 python3-pip -y

# Install Git
sudo dnf install git -y
```

### 2. Clone the Repository

```bash
# Navigate to your preferred directory
cd ~

# Clone the repository
git clone https://github.com/alshahriar-uu/gym-management-sys.git

# Navigate to the project directory
cd gym-management-sys
```

### 3. Set Up Python Virtual Environment (Recommended)

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# You should see (venv) at the beginning of your terminal prompt
```

### 4. Install Python Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-SQLAlchemy (database ORM)
- Flask-Migrate (database migrations)
- Flask-Mail (email functionality)
- Flask-Bcrypt (password hashing)
- python-dotenv (environment variables)
- email-validator (email validation)

### 5. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your settings
nano .env  # or use your preferred text editor
```

Update the following values in `.env`:

```bash
# Generate a secret key (run this command in Python terminal):
# python3 -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-generated-secret-key-here

# Email configuration (Gmail)
MAIL_USERNAME=your-gmail-address@gmail.com
MAIL_PASSWORD=your-gmail-app-password

# Admin configuration (optional - defaults are already set)
ADMIN_EMAIL=rakibalshahriar@gmail.com
ADMIN_USERNAME=rakib
ADMIN_PASSWORD=admin123
```

**Important: Getting Gmail App Password**

1. Go to your Google Account settings: https://myaccount.google.com/
2. Click "Security" in the left menu
3. Enable "2-Step Verification" if not already enabled
4. After enabling 2-Step Verification, search for "App Passwords"
5. Create a new app password for "Mail"
6. Copy the 16-character password and paste it in MAIL_PASSWORD

### 6. Initialize the Database

```bash
# Create the instance directory (if not exists)
mkdir -p instance

# Run the database initialization script
python3 init_db.py
```

You should see output like:
```
Creating database tables...
✓ Database tables created successfully!
Creating admin account...
✓ Admin account created successfully!
  Username: rakib
  Email: rakibalshahriar@gmail.com
  Password: admin123
  Role: admin

✓ Database initialization complete!
```

### 7. Run the Application

```bash
# Start the Flask development server
python3 app.py
```

You should see output like:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://0.0.0.0:5000
```

### 8. Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## Default Login Credentials

After initialization, you can login with:

- **Admin Account:**
  - Username: `rakib`
  - Password: `admin123`
  - Role: Administrator

## Application Features

### For Users (Members)
1. **Register** - Fill out the registration form on the homepage
2. **Receive Welcome Email** - Get confirmation email after registration
3. **Wait for Approval** - Admin must approve your registration
4. **Receive Login Credentials** - Get email with username and password after approval
5. **Login** - Access your member dashboard
6. **Password Reset** - Use "Forgot Password" if needed

### For Administrators
1. **Login** - Use admin credentials
2. **View Dashboard** - See overview of members and pending registrations
3. **Approve/Reject Registrations** - Process new member applications
4. **Manage Members** - View, edit, and delete member records
5. **View Member Details** - Access complete member information

## Directory Structure

```
gym-management-sys/
├── app.py                 # Main application file
├── config.py             # Configuration settings
├── models.py             # Database models
├── init_db.py           # Database initialization script
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (create from .env.example)
├── .env.example         # Example environment file
├── .gitignore          # Git ignore rules
├── instance/           # Database storage directory
│   └── gymfit.db       # SQLite database file (created after init)
├── templates/          # HTML templates
│   ├── *.html         # Main templates
│   └── email/         # Email templates
│       ├── welcome.html
│       ├── approval.html
│       ├── reset_password.html
│       └── expiry_reminder.html
└── static/            # Static files (CSS, JS, images)
    ├── css/
    └── js/
```

## Database Schema

The application uses SQLite with the following tables:

1. **users** - User authentication (admin, trainer, member)
2. **members** - Gym member details and membership information
3. **pending_registrations** - New registration applications
4. **password_reset_tokens** - Password reset functionality

## Troubleshooting

### Issue: "unable to open database file"
**Solution:** Ensure the `instance` directory exists:
```bash
mkdir -p instance
```

### Issue: "ModuleNotFoundError"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Email not sending
**Solution:** 
- Check your Gmail App Password is correct
- Ensure you have 2-Step Verification enabled
- Check MAIL_USERNAME and MAIL_PASSWORD in .env file
- Check your internet connection

### Issue: "Address already in use"
**Solution:** Stop any other Flask applications or change the port:
```bash
# Kill the process using port 5000
sudo lsof -ti:5000 | xargs kill -9

# Or run on a different port
flask run --port 5001
```

### Issue: Permission denied
**Solution:** Ensure you have write permissions to the directory:
```bash
chmod -R 755 gym-management-sys
```

## Production Deployment

**Important:** The current setup is for development only. For production deployment:

1. Use a production-grade WSGI server (Gunicorn, uWSGI)
2. Use a more robust database (PostgreSQL, MySQL)
3. Set up proper SSL/TLS certificates
4. Configure a reverse proxy (Nginx, Apache)
5. Set DEBUG=False in configuration
6. Use strong SECRET_KEY
7. Implement proper backup strategies

## Security Considerations

1. **Never commit .env file** - It contains sensitive information
2. **Use strong passwords** - Change default admin password immediately
3. **Keep dependencies updated** - Regularly update packages for security patches
4. **Enable HTTPS** - Always use HTTPS in production
5. **Regular backups** - Backup your database regularly

## Getting Help

If you encounter any issues:

1. Check this setup guide thoroughly
2. Review the error messages carefully
3. Check the application logs
4. Ensure all prerequisites are met
5. Verify environment variables are set correctly

## Next Steps

After successful setup:

1. Change the default admin password
2. Test the registration flow
3. Configure email settings
4. Customize templates as needed
5. Add additional members
6. Explore all features

## License

This project is for educational and commercial use. Please refer to the LICENSE file for more information.

## Support

For support and questions, contact: rakibalshahriar@gmail.com
