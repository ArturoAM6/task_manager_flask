# routes.py

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from app import db, bcrypt
from app import app
from .models import User, Task
from .forms import LoginForm, RegisterForm, AddTaskForm, EditTaskForm

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        
    return render_template('login.html', form=form)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.username)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists!', 'error')
            return render_template('register.html', form=form), 400

        crypt_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=crypt_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration succesful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/tasks')
@login_required
def tasks():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        user_tasks = Task.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=per_page)
        return render_template('tasks.html', tasks=user_tasks)
    except Exception as e:
        flash('An error occurred while fetchin tasks.', 'error')
        return redirect(url_for('home'))

@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = AddTaskForm()
    if form.validate_on_submit():
        new_task = Task(
            title = form.title.data,
            description = form.description.data,
            priority = form.priority.data,
            user_id = current_user.id
        )

        db.session.add(new_task)
        db.session.commit()
        flash('Task added succesfully!', 'success')
        return redirect(url_for('tasks'))
    return render_template('add_task.html', form=form)

@app.route('/edit_task/<int:task_id>', methods=['GET','POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return redirect(url_for('tasks'))
    
    form = EditTaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        db.session.commit()
        flash('Task updated succesfully!', 'success')
        return redirect(url_for('tasks'))
    return render_template('edit_task.html', form=form)
    
@app.route('/complete_task/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        task.completed = True
        db.session.commit()
        flash('Task marked as completed!', 'success')
    return redirect(url_for('tasks'))

@app.route('/delete_task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted succesfully!', 'success')
    return redirect(url_for('tasks'))
