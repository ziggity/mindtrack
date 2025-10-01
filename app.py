from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, request, render_template
from models import db, User

app = Flask(__name__)

# Config
app.config['SECRET_KEY'] = 'supersecretkey'   # replace with env variable later
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mindtrack.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB + Login manager
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()


# ----------------- Authentication -----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists!")
            return redirect(url_for("signup"))

        new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash("Account created! Please login.")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid credentials")
            return redirect(url_for("login"))

        login_user(user)
        return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ----------------- Our Routes -----------------

@app.route("/")
def index():
    return render_template("index.html")

# Home router for home page rendering
@app.route("/home")
def home():
    return render_template("home.html")
    

# Check-in router for check-in page rendering
@app.route("/check-in", methods=["GET", "POST"])
@login_required
def check_in():
    return render_template("check_in.html")


# Dashboard router for dashboard page rendering
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# Journal router for journal page rendering
@app.route("/journal")
@login_required
def journal():
    return render_template("journal.html")

# Resources router for resources page rendering
@app.route("/resources")
@login_required
def resources():
    return render_template("resources.html")


# ----------------- Main -----------------
if __name__ == "__main__":
    app.run(debug=True)
# Run the Flask application in debug mode           



