from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, DataRequired, EqualTo
from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user, current_user 
from matplotlib import pyplot as plt
from flask import Response
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    budget_amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    return render_template('login.html', form=form)


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            new_user = User(username=form.username.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    submit = SubmitField('Login')
    


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class ExpenseForm(FlaskForm):
    description = StringField('Description', validators=[InputRequired()])
    amount = FloatField('Amount', validators=[InputRequired()])
    category = SelectField('Category', choices=[('food', 'Food'), ('housing', 'Housing'), ('transportation', 'Transportation'), ('entertainment', 'Entertainment'), ('other', 'Other')], validators=[InputRequired()])
    submit = SubmitField('Add Expense')


class BudgetForm(FlaskForm):
    category = SelectField('Category', choices=[('food', 'Food'), ('housing', 'Housing'), ('transportation', 'Transportation'), ('entertainment', 'Entertainment'), ('other', 'Other')], validators=[InputRequired()])
    budget_amount = FloatField('Budget Amount', validators=[InputRequired()])
    submit = SubmitField('Set Budget')

@app.route('/')
@login_required
def index():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    total_expenses = sum(expense.amount for expense in expenses)
    categories = set(expense.category for expense in expenses)
    return render_template('index.html', expenses=expenses, total_expenses=total_expenses, categories=categories)

@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        description = form.description.data
        amount = form.amount.data
        category = form.category.data
        new_expense = Expense(description=description, amount=amount, category=category, user_id=current_user.id)
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully', 'success')
        return redirect(url_for('index'))
    return render_template('add_expense.html', form=form)

@app.route('/set_budget', methods=['GET', 'POST'])
@login_required
def set_budget():
    form = BudgetForm()

    if form.validate_on_submit():
        category = form.category.data
        budget_amount = form.budget_amount.data
        existing_budget = Budget.query.filter_by(category=category, user_id=current_user.id).first()
        if existing_budget:
            existing_budget.budget_amount = budget_amount
        else:
            new_budget = Budget(category=category, budget_amount=budget_amount, user_id=current_user.id)
            db.session.add(new_budget)
        db.session.commit()
        flash('Budget set successfully', 'success')
        return redirect(url_for('index'))
    return render_template('set_budget.html', form=form)

@app.route('/expense_summary')
@login_required
def expense_summary():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    category_totals = {}
    
    for expense in expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
    
    return render_template('expense_summary.html', category_totals=category_totals)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/chart')
@login_required
def chart():
    categories = []
    amounts = []

    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    for category in set(expense.category for expense in expenses):
        categories.append(category)
        category_total = sum(expense.amount for expense in expenses if expense.category == category)
        amounts.append(category_total)

    plt.figure(figsize=(8, 8))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution by Category')
    plt.axis('equal')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return Response(img, mimetype='image/png')

if __name__ == '__main__':
    with app.app_context():
        print("Creating database tables...")
        db.create_all()

    app.run(debug=True)

