from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, TextAreaField, SubmitField,
    DateTimeLocalField, IntegerField, SelectField,
)
from wtforms.validators import (
    DataRequired, Length, Email, EqualTo, NumberRange, ValidationError,
)
from app.models import CATEGORIES


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(3, 80)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')


class EventForm(FlaskForm):
    title = StringField('活动标题', validators=[DataRequired()])
    description = TextAreaField('活动描述')
    category = SelectField('活动分类', choices=[(c, c) for c in CATEGORIES], default='其他')
    location = StringField('活动地点')
    start_time = DateTimeLocalField('开始时间', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_time = DateTimeLocalField('结束时间', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    max_participants = IntegerField('最大参与人数', validators=[NumberRange(min=0)])
    checkin_code = StringField('签到码')
    submit = SubmitField('提交')

    def validate_end_time(self, field):
        if self.start_time.data and field.data and field.data <= self.start_time.data:
            raise ValidationError('结束时间必须晚于开始时间')


class CheckinForm(FlaskForm):
    code = StringField('签到码', validators=[DataRequired()])
    submit = SubmitField('签到')
