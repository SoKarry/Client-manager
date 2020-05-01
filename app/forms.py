from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, FloatField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Lead

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('ВОЙТИ')

class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повтрите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('ЗАРЕГИСТРИРОВАТЬСЯ')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой логин.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой email-адрес.')

class EditProfileForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    about_me = TextAreaField('Для заметок: ', validators=[Length(min=0, max=140)])
    submit = SubmitField('Изменить!')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Пожалуйста, используйте другой логин.')

class AddForm(FlaskForm):
    fio = StringField('ФИО', validators=[DataRequired(), Length(min=1, max=140)])
    tovar = SelectField(u'Товар')
    price = FloatField('Цена')
    address = StringField('Адрес', validators=[DataRequired(), Length(min=0, max=140)])
    delivery_price = FloatField('Стоимость доставки', validators=[DataRequired()])
    cost_price = FloatField('Себестоимость')
    contact = StringField('Контакты', validators=[DataRequired(), Length(min=0, max=140)])
    track = StringField('Трек', validators=[Length(min=0, max=20)])
    status = StringField('Статус', validators=[Length(min=0, max=40)])
    who_paid = RadioField('Оплата доставки', choices=[('0','Покупатель'),('1','Мы')])
    submit = SubmitField('✔')

class AddTovarForm(FlaskForm):
    tovar_name = StringField('Товар', validators=[DataRequired(), Length(min=1, max=140)])
    tovar_cost_price = FloatField('Себестоимость', validators=[DataRequired()])
    tovar_price = FloatField('Цена', validators=[DataRequired()])
    submit = SubmitField('✔')