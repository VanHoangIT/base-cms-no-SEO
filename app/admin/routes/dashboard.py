"""
📊 Dashboard & Welcome Routes
- Dashboard: Cho Admin/Editor (view_dashboard permission)
- Welcome: Cho User thường (không cần permission)

🔒 Permissions:
- view_dashboard: Xem dashboard đầy đủ
"""

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from app.models import Product, Category, Blog, Contact
from app.decorators import permission_required
from app.admin import admin_bp

# ==================== DASHBOARD ====================
@admin_bp.route('/dashboard')
@permission_required('view_dashboard')
def dashboard():
    """
    Dashboard đầy đủ - CHỈ cho Admin & Editor
    User khác redirect sang Welcome
    """
    # Kiểm tra quyền - chỉ Admin/Editor vào được
    if not current_user.has_any_permission('manage_users', 'manage_products', 'manage_categories'):
        return redirect(url_for('admin.welcome'))

    # Dashboard cho Admin/Editor
    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_blogs = Blog.query.count()
    total_contacts = Contact.query.filter_by(is_read=False).count()
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                           total_products=total_products,
                           total_categories=total_categories,
                           total_blogs=total_blogs,
                           total_contacts=total_contacts,
                           recent_products=recent_products,
                           recent_contacts=recent_contacts)

# ==================== WELCOME USER ====================
@admin_bp.route('/welcome')
@login_required
def welcome():
    """Trang chào mừng cho User thường (không phải Admin/Editor)"""
    # Nếu là Admin/Editor, redirect về dashboard
    if current_user.has_any_permission('manage_users', 'manage_products', 'manage_categories'):
        return redirect(url_for('admin.dashboard'))

    # Lấy số liên hệ chưa đọc (nếu có quyền xem)
    total_contacts = 0
    if current_user.has_any_permission('view_contacts', 'manage_contacts'):
        total_contacts = Contact.query.filter_by(is_read=False).count()

    return render_template('admin/welcome.html', total_contacts=total_contacts)