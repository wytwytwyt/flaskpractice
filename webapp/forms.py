from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


'''表单'''


class CommentForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(max=20)])
    text = TextAreaField(u'Comment', validators=[DataRequired()])