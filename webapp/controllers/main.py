from flask import Blueprint, redirect, url_for,render_template, flash
from flask_login import login_user, logout_user
from ..forms import LoginForm, RegisterForm
from ..models import User
from webapp import db


main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='../templates/main'
)


@main_blueprint.route('/')
def index():
    return redirect(url_for('blog.home'))


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=form.remember.data)
        flash("登录成功", category="success")
        return redirect(url_for('blog.home'))
    return render_template('login.html', form=form)


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(form.username.data)
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash("注册成功,请登录", category="success")
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)
