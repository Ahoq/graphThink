from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, SubmitField, BooleanField, TextAreaField,SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2,max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2,max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired(), Length(min=2)])
    tags = StringField('Tags', validators=[DataRequired()])
    text = TextAreaField('Insight', validators=[DataRequired()])
    reltn = StringField('Relation', validators=[DataRequired()])
    publish = SubmitField('Publish')


# class Inputs(FlaskForm):
#     myChoices = ['device','website','provider','plan_name','DD']

#     myField = SelectField(u'Field name', choices = myChoices, validators = [Required()])

class DropForm(FlaskForm):
    search = SubmitField('Search')

class RunForm(FlaskForm):
    search = SubmitField('Run')