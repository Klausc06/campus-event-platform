from flask import current_app, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from urllib.parse import urlparse

from app.auth import auth_bp
from app.extensions import db
from app.models import User
from app.forms import LoginForm, RegisterForm


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('event.list_events'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('用户名已存在', 'danger')
            return render_template('auth/register.html', form=form)
        if User.query.filter_by(email=form.email.data).first():
            flash('邮箱已被注册', 'danger')
            return render_template('auth/register.html', form=form)
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('event.list_events'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            current_app.logger.warning('Failed login attempt for username=%s from %s', form.username.data, request.remote_addr)
            flash('用户名或密码错误', 'danger')
            return render_template('auth/login.html', form=form)
        login_user(user)
        current_app.logger.info('Successful login for username=%s from %s', user.username, request.remote_addr)
        next_page = request.args.get('next')
        if next_page:
            parsed = urlparse(next_page)
            if not next_page or not next_page.startswith('/') or next_page.startswith('//'):
                next_page = None
        return redirect(next_page or url_for('event.list_events'))
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    flash('已退出登录', 'info')
    return redirect(url_for('auth.login'))
