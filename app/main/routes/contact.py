from flask import render_template, request, flash, redirect, url_for
from app.main import main_bp
from app import db
from app.models.contact import Contact
from app.forms.contact import ContactForm



@main_bp.route('/lien-he', methods=['GET', 'POST'])
def contact():
    """Trang liên hệ"""
    form = ContactForm()

    if form.validate_on_submit():
        # Tạo contact mới
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            subject=form.subject.data,
            message=form.message.data
        )

        db.session.add(contact)
        db.session.commit()

        flash('Cảm ơn bạn đã liên hệ! Chúng tôi sẽ phản hồi sớm nhất.', 'success')
        return redirect(url_for('main.contact'))

    return render_template('public/contact.html', form=form)

