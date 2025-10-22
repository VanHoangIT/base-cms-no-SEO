"""
📧 Contacts Management Routes
Quản lý tin nhắn liên hệ từ khách hàng

FEATURES:
- List với filter read/unread
- View detail (tự động đánh dấu đã đọc)
- Delete message
- Không có Add/Edit (chỉ nhận từ form frontend)

FIELDS:
- name: Họ tên khách hàng *
- email: Email *
- phone: Số điện thoại
- subject: Tiêu đề
- message: Nội dung *
- is_read: Đã đọc/chưa đọc (auto set khi view)
- created_at: Thời gian gửi (VN timezone)

🔒 Permissions:
- view_contacts: Xem danh sách
- manage_contacts: Xóa message

WORKFLOW:
1. Khách gửi form → Contact record created
2. Admin vào /admin/contacts → Thấy danh sách
3. Click "Xem chi tiết" → is_read = True
4. Có thể xóa message sau khi xử lý

📊 DASHBOARD INTEGRATION:
- Hiển thị số message chưa đọc trên dashboard
- Badge "New" cho message mới
"""

from flask import render_template, request, flash, redirect, url_for
from app import db
from app.models.contact import Contact
from app.decorators import permission_required
from app.admin import admin_bp


# ==================== LIST ====================
@admin_bp.route('/contacts')
@permission_required('view_contacts')
def contacts():
    """
    📋 Danh sách liên hệ
    - Phân trang 20 items/page
    - Sắp xếp theo created_at (mới nhất trên đầu)
    - Hiển thị badge "Mới" cho unread
    - Filter: All / Unread / Read
    """
    page = request.args.get('page', 1, type=int)
    contacts = Contact.query.order_by(Contact.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/contacts.html', contacts=contacts)



# ==================== VIEW DETAIL ====================
@admin_bp.route('/contacts/view/<int:id>')
@permission_required('view_contacts')
def view_contact(id):
    """
    👁️ Xem chi tiết liên hệ

    AUTO PROCESSING:
    - Tự động set is_read = True khi view lần đầu
    - Hiển thị đầy đủ thông tin khách hàng
    - Button: Reply (mailto:), Delete

    DISPLAY:
    - Thời gian: VN timezone (created_at_vn)
    - Format: dd/mm/yyyy lúc HH:MM
    """
    contact = Contact.query.get_or_404(id)

    if not contact.is_read:
        contact.is_read = True
        db.session.commit()

    return render_template('admin/contact_detail.html', contact=contact)


# ==================== DELETE ====================
@admin_bp.route('/contacts/delete/<int:id>')
@permission_required('manage_contacts')
def delete_contact(id):
    """
    🗑️ Xóa liên hệ

    - Xóa sau khi đã xử lý xong
    - Không thể khôi phục
    """
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()

    flash('Đã xóa liên hệ thành công!', 'success')
    return redirect(url_for('admin.contacts'))
