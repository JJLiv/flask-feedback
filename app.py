from flask import Flask, request, redirect, flash, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from form import RegisterUserForm, LoginUserForm, FeedbackForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register_form():
    """register user form [GET] and handle submit [POST]"""

    form = RegisterUserForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        email = form.email.data
        first = form.first_name.data
        last = form.last_name.data

        user = User.register(name, pwd,email,first,last)
       
        db.session.commit()
        session['username'] = user.username
        flash(f"{name} registered successfully!")
        return redirect('/secret')

    else:
        return render_template('register.html', form=form)
    

@app.route('/login', methods=['POST', 'GET'])
def login_form():
    """login form [GET], and handle submit [POST]"""
    form = LoginUserForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        
        user = User.authenticate(name, pwd)
        
        if user:
            session['username'] = user.username
            return redirect(f'/users/{session["username"]}')
        else:
            form.username.errors = ['Bad name/password']
    
    return render_template('login.html', form=form)





@app.route('/users/<username>')
def secret(username):
    if 'username' not in session:
        flash("You must be logged in to view!")
        return redirect('/login')
    else:
        user = User.query.get(username)
        
        return render_template('user.html', user=user)
    

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if 'username' not in session:
        flash("You must be logged in to delete")
        return redirect('/login')
    else:
        user = User.query.get(username)
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        return redirect('/login')
    
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback_form(username):
    if 'username' not in session:
        flash('Must be logged in to add feedback')
        return redirect('/login')
    else:
        form = FeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content=form.content.data
            feedback = Feedback(title=title,
                                content=content,
                                username=username)
            
            db.session.add(feedback)
            db.session.commit()
            flash(f'Feedback created by {username}')
            return redirect(f'/users/{feedback.username}')
        
        else: return render_template('feedback.html')

@app.route('/feedback/<int:feedback_id>/update', methods=['GET','POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)

    if 'username' not in session:
        flash('Must be logged in to leave feedback')
        return redirect('/login')
    else:
        form = FeedbackForm(obj=feedback)
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            db.session.commit()
            flash(f'{feedback.username} updated feedback successfully')
            return redirect(f'/users/{feedback.username}')
        else:
            return render_template('feedback.html', form=form, feedback=feedback)
        
@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    if 'username' not in session:
        flash('must be logged in to delete feedback')
        return('/login')
    else:
        feedback = Feedback.query.get(feedback_id)
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
        


            


        

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')




    

