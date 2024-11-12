from bank import app, db
from bank.forms import RegisterForm, LoginForm, TransactionForm
from flask import render_template, redirect, url_for, flash
from bank.models import User, Account, Transaction
from flask_login import login_user, logout_user, login_required



@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.name.data).first()
        if attempted_user and attempted_user.check_password(form.password.data):
            login_user(attempted_user)
            flash(f"You are now logged in {form.name.data}", category='success')
            return redirect(url_for('transactions_page'))
        else:
            flash("This user doesn't exist, Try another Username of Password!")


    return render_template("login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_created = User(username= form.name.data, email=form.email.data, 
                            phone_number=form.phone.data, address=form.address.data,
                            hashing=form.password1.data)
        db.session.add(user_created)
        db.session.commit()
        login_user(user_created)
        flash(f'Your account have been successfully created, You are now Logged in {user_created.username}!!', category='success')
        return redirect (url_for('transactions_page'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}', category='danger')

    return render_template("register.html", form=form)


@app.route('/transactions')
@login_required
def transactions_page():
    form = TransactionForm()
    return render_template("transactions.html", form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You are now logged out!', category='info')
    return redirect(url_for("home_page"))