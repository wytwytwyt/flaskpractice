from flask_wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL
from .models import User


'''表单'''


class LoginForm(Form):
    username = StringField('Username',
                           [DataRequired(), Length(max=20)]
                           )
    password = PasswordField('Password', [DataRequired()])

    remember = BooleanField('记住我')

    def validate(self):
        check_validate = super(LoginForm, self).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append(
                '用户名密码错误'
            )
            return False

        if not user.check_password(self.password.data):
            self.username.errors.append(
                '用户名密码错误'
            )
            return False
        return True
        

class RegisterForm(Form):
    username = StringField('Username', [DataRequired(), Length(max=20)])
    password = PasswordField('Password', [DataRequired(), Length(min=8)])
    check_password = PasswordField('Confirm Password', [DataRequired(), EqualTo('password')])
    
    def validate(self):
        check_validate = super(RegisterForm, self).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append(
                '用户名已存在'
            )
            return False
        return True


class PostForm(Form):
    title = StringField('Title', [DataRequired(), Length(max=100)])
    text = TextAreaField('Content', [DataRequired()])


class CommentForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(max=20)])
    text = TextAreaField(u'Comment', validators=[DataRequired()])
