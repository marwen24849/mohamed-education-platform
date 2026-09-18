from flask import Blueprint, request, session, redirect, url_for, render_template
from werkzeug.security import check_password_hash

from config import ADMIN_USERNAME, ADMIN_PASSWORD
from models import AdminUser

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = AdminUser.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['admin_logged_in'] = True
            session['admin_username'] = user.username
            return redirect(url_for('admin.dashboard'))

        return render_template('admin/login.html', error='Identifiants invalides.')

    return render_template('admin/login.html')


@auth_bp.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('auth.admin_login'))
