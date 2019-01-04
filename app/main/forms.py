from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import Required, Email, EqualTo
from ..models import User
from wtforms import ValidationError

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class BlogForm(FlaskForm):
    title = StringField('Blog title',validators=[Required()])
    content = TextAreaField('Your Blog.')
    category = SelectField('Category',choices=[('Institutional','Institutional'),('Personal_Blog','Personal_Blog')])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    comment_name = TextAreaField('Blog comment', validators=[Required()])
    submit = SubmitField('Submit')


class SubscriberForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    submit = SubmitField('subscribe')
