from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from src.models.user import User, db
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin required decorator
def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.role == 'admin':
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/')
@admin_required
def index():
    # Get user statistics
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    pending_users = User.query.filter_by(is_approved=False, email_confirmed=True).count()
    
    # Get recent activity
    from src.models.user import PageView
    recent_activity = PageView.query.order_by(PageView.timestamp.desc()).limit(10).all()
    
    return render_template(
        'admin/index.html',
        total_users=total_users,
        active_users=active_users,
        pending_users=pending_users,
        recent_activity=recent_activity
    )

@admin_bp.route('/users')
@admin_required
def users():
    all_users = User.query.all()
    return render_template('admin/users.html', users=all_users)

@admin_bp.route('/users/<int:user_id>/approve', methods=['POST'])
@admin_required
def approve_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    user.is_active = True
    db.session.commit()
    
    flash(f'User {user.email} has been approved.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/reject', methods=['POST'])
@admin_required
def reject_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_approved = False
    user.is_active = False
    db.session.commit()
    
    flash(f'User {user.email} has been rejected.', 'warning')
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/change-role', methods=['POST'])
@admin_required
def change_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    
    if new_role in ['admin', 'tier1', 'tier2', 'prospective']:
        user.role = new_role
        db.session.commit()
        flash(f'Role for {user.email} changed to {new_role}.', 'success')
    else:
        flash('Invalid role specified.', 'danger')
    
    return redirect(url_for('admin.users'))

@admin_bp.route('/analytics')
@admin_required
def analytics():
    # Get user activity statistics
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    pending_users = User.query.filter_by(is_approved=False, email_confirmed=True).count()
    
    # Get page view statistics
    from src.models.user import PageView
    
    # Most viewed pages
    page_views = db.session.query(
        PageView.page_url, 
        db.func.count(PageView.id).label('view_count')
    ).group_by(PageView.page_url).order_by(db.text('view_count DESC')).limit(10).all()
    
    # Recent activity
    recent_activity = PageView.query.order_by(PageView.timestamp.desc()).limit(20).all()
    
    return render_template(
        'admin/analytics.html',
        total_users=total_users,
        active_users=active_users,
        pending_users=pending_users,
        page_views=page_views,
        recent_activity=recent_activity
    )
