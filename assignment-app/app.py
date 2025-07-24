from flask import Flask, render_template, redirect, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from mongoengine import connect
from models import User, Assignment, Submission

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'secret'

# MongoDB Atlas connection
connect(
    db='pythonFlask',
    host='mongodb+srv://atharvamore998:VadR9QyaeJ01J8cG@cluster0.leklp6p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
)

# Initialize extensions
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'  # redirect to login if not logged in

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.objects(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return redirect('/dashboard')
    return 'Login Failed'

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    role = request.form['role']
    password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    new_user = User(email=email, password=password, role=role)
    new_user.save()
    return redirect('/')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'teacher':
        return render_template('dashboard_teacher.html')
    else:
        return render_template('dashboard_student.html')

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.role != 'teacher':
        return "Unauthorized"
    if request.method == 'POST':
        title = request.form['title']
        assignment = Assignment(title=title, teacher=current_user)
        assignment.save()
        return redirect('/dashboard')
    return render_template('create_assignment.html')

@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    if current_user.role != 'student':
        return "Unauthorized"
    if request.method == 'POST':
        assignment_id = request.form['assignment_id']
        content = request.form['content']
        assignment = Assignment.objects(id=assignment_id).first()
        submission = Submission(student=current_user, assignment=assignment, content=content)
        submission.save()
        return redirect('/dashboard')
    assignments = Assignment.objects()
    return render_template('submit_assignment.html', assignments=assignments)

@app.route('/submissions')
@login_required
def submissions():
    if current_user.role != 'teacher':
        return "Unauthorized"
    assignments = Assignment.objects(teacher=current_user)
    return render_template('view_submissions.html', assignments=assignments)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
