from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddForm, AddTovarForm
from app.models import User, Lead, Tovar
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.comp_name = form.comp_name.data
        current_user.comp_bill = form.comp_bill.data
        current_user.bank_name = form.bank_name.data
        current_user.cor_bill = form.cor_bill.data
        current_user.INN = form.INN.data
        current_user.KPP = form.KPP.data
        current_user.BIK = form.BIK.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.comp_name.data = current_user.comp_name
        form.comp_bill.data = current_user.comp_bill
        form.bank_name.data = current_user.bank_name
        form.cor_bill.data = current_user.cor_bill
        form.INN.data = current_user.INN
        form.KPP.data = current_user.KPP
        form.BIK.data = current_user.BIK
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/clients_manager', methods=['GET', 'POST'])
@login_required
def add_client():
    form = AddForm()
    form.tovar.choices = [(x.tovar_name, x.tovar_name) for x in current_user.tovars]
    if form.validate_on_submit():
        ld = Lead(fio = form.fio.data, tovar = request.form.get('tovar'), price = Tovar.query.filter_by(tovar_name=request.form.get('tovar'), user_id=current_user.id).first().tovar_price, contact = form.contact.data, address = form.address.data, delivery_price=form.delivery_price.data, cost_price = Tovar.query.filter_by(tovar_name=request.form.get('tovar'), user_id=current_user.id).first().tovar_cost_price, profit = Tovar.query.filter_by(tovar_name=request.form.get('tovar'), user_id=current_user.id).first().tovar_price - Tovar.query.filter_by(tovar_name=request.form.get('tovar'), user_id=current_user.id).first().tovar_cost_price - form.delivery_price.data*int(request.form.get('who_paid')), track = form.track.data, status = form.status.data, user_id = current_user.id)
        db.session.add(ld)
        db.session.commit()
        flash('Клиент успешно добавлен!')
        return redirect(url_for('add_client'))
    return render_template('clients_manager.html', title='Учёт кленитов', form=form)

@app.route("/client_edit/<int:lead_id>", methods=['GET', 'POST'])
@login_required
def update_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    if lead.author != current_user:
        abort(403)
    form = AddForm()
    form.tovar.choices = [(x.tovar_name, x.tovar_name) for x in current_user.tovars]
    form.tovar.default = lead.tovar
    if form.validate_on_submit():
        lead.fio = form.fio.data
        # lead.tovar = request.form.get('tovar')
        lead.price = form.price.data
        lead.contact = form.contact.data
        lead.address = form.address.data
        lead.delivery_price = form.delivery_price.data
        lead.cost_price = form.cost_price.data
        lead.profit = form.price.data-form.cost_price.data
        lead.track = form.track.data
        lead.status = form.status.data
        db.session.commit()
        flash('Клиент отредактирован!', 'success')
        return redirect(url_for('add_client'))
    elif request.method == 'GET':
        form.fio.data = lead.fio
        # form.tovar.default = lead.tovar
        form.price.data = lead.price
        form.contact.data = lead.contact
        form.address.data = lead.address
        form.delivery_price.data = lead.delivery_price
        form.cost_price.data = lead.cost_price
        form.track.data = lead.track
        form.status.data = lead.status
    return render_template('client_edit.html', title='Изменить данные клиента',
                           form=form)

@app.route("/clients_manager/<int:lead_id>/del", methods=['GET', 'POST'])
@login_required
def delete_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    if lead.author != current_user:
        abort(403)
    db.session.delete(lead)
    db.session.commit()
    flash('Клиент удалён!', 'success')
    return redirect(url_for('add_client'))

@app.route('/tovar_manager', methods=['GET', 'POST'])
@login_required
def add_tovar():
    form = AddTovarForm()
    if form.validate_on_submit():
        tv = Tovar(tovar_name = form.tovar_name.data, tovar_cost_price = form.tovar_cost_price.data, tovar_price = form.tovar_price.data, user_id = current_user.id)
        db.session.add(tv)
        db.session.commit()
        flash('Товар успешно добавлен!')
        return redirect(url_for('add_tovar'))
    return render_template('tovar_manager.html', title='Менеджер товаров', form=form)

@app.route("/tovar_manager/<int:tovar_id>/edit", methods=['GET', 'POST'])
@login_required
def update_tovar(tovar_id):
    tv = Tovar.query.get_or_404(tovar_id)
    if tv.author != current_user:
        abort(403)
    form = AddTovarForm()
    if form.validate_on_submit():
        tv.tovar_name = form.tovar_name.data
        tv.tovar_cost_price = form.tovar_cost_price.data
        tv.tovar_price = form.tovar_price.data
        db.session.commit()
        flash('Товар отредактирован!', 'success')
        return redirect(url_for('add_tovar'))
    elif request.method == 'GET':
        form.tovar_name.data = tv.tovar_name
        form.tovar_cost_price.data = tv.tovar_cost_price
        form.tovar_price.data = tv.tovar_price
    return render_template('tovar_manager.html', title='Изменить данные товара',
                           form=form)

@app.route("/tovar_manager/<int:tovar_id>/del", methods=['GET', 'POST'])
@login_required
def delete_tovar(tovar_id):
    tv = Tovar.query.get_or_404(tovar_id)
    if tv.author != current_user:
        abort(403)
    db.session.delete(tv)
    db.session.commit()
    flash('Товар удалён!', 'success')
    return redirect(url_for('add_tovar'))

@app.route('/check/<int:lead_id>', methods=['GET', 'POST'])
@login_required
def get_check(lead_id):
    ld = Lead.query.get_or_404(lead_id)
    if ld.author != current_user:
        abort(403)
    return render_template('check.html', title='Чек', ld=ld)