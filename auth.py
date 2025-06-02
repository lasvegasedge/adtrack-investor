from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from src.models.user import User, db
from flask_mail import Message
from src import mail
import uuid
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer

auth_bp = Blueprint('auth', __name__)

# Create serializer for generating tokens
def get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        company = request.form.get('company')
        position = request.form.get('position')
        
        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Create new user
        new_user = User(
            email=email,
            name=name,
            company=company,
            position=position,
            role='prospective',  # Default role for new users
            is_active=False,
            is_approved=False,
            email_confirmed=False
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate token for email verification
        s = get_serializer()
        token = s.dumps(email, salt='email-verification')
        
        # Send verification email
        msg = Message('Verify Your AdTrack Investor Account',
                     recipients=[email])
        verification_url = url_for('auth.verify_email', token=token, _external=True)
        msg.body = f'''Please click the link below to verify your email address:
{verification_url}

If you did not register for an AdTrack investor account, please ignore this email.
'''
        mail.send(msg)
        
        # Notify admin about new registration
        admin_msg = Message('New Investor Registration',
                          recipients=['admin@adtrack.online'])
        admin_msg.body = f'''A new investor has registered:
Name: {name}
Email: {email}
Company: {company}
Position: {position}

Please review and approve this registration in the admin panel.
'''
        mail.send(admin_msg)
        
        flash('Registration successful! Please check your email to verify your account.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/verify-email/<token>')
def verify_email(token):
    s = get_serializer()
    try:
        email = s.loads(token, salt='email-verification', max_age=3600)  # Token expires after 1 hour
    except:
        flash('The verification link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=email).first()
    if user:
        user.email_confirmed = True
        db.session.commit()
        flash('Email verified! Your account is now pending admin approval.', 'success')
    else:
        flash('User not found.', 'danger')
    
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if not user or not user.check_password(password):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Check if email is verified
        if not user.email_confirmed:
            flash('Please verify your email before logging in.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Check if user is approved by admin
        if not user.is_approved:
            flash('Your account is pending approval by an administrator.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Check if user is active
        if not user.is_active:
            flash('Your account has been deactivated. Please contact an administrator.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Update last login time
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Log in user
        login_user(user, remember=remember)
        
        # Check if user has accepted the agreement
        if not user.agreement_accepted:
            return redirect(url_for('auth.agreement'))
        
        # Redirect to requested page or default
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')
        
        return redirect(next_page)
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/agreement', methods=['GET', 'POST'])
@login_required
def agreement():
    if current_user.agreement_accepted:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        if request.form.get('accept'):
            current_user.accept_agreement()
            db.session.commit()
            flash('Thank you for accepting the agreement.', 'success')
            return redirect(url_for('main.index'))
    
    return render_template('auth/agreement.html')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            s = get_serializer()
            token = s.dumps(email, salt='password-reset')
            
            # Send password reset email
            msg = Message('Reset Your AdTrack Investor Account Password',
                         recipients=[email])
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            msg.body = f'''Please click the link below to reset your password:
{reset_url}

If you did not request a password reset, please ignore this email.
'''
            mail.send(msg)
        
        # Always show this message even if email doesn't exist (security best practice)
        flash('If your email is registered, you will receive password reset instructions.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    s = get_serializer()
    try:
        email = s.loads(token, salt='password-reset', max_age=3600)  # Token expires after 1 hour
    except:
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/reset_password.html', token=token)
        
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(password)
            db.session.commit()
            flash('Your password has been reset. You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', token=token)
