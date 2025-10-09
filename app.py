from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import os

# Create app and point to your folders
app = Flask(__name__, template_folder="templates", static_folder="static")

# Dev friendly config
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mindtrack.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0  # disable static cache in dev

# Init DB and Login
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))

# Create tables if missing
with app.app_context():
    db.create_all()

# ----------------- Authentication -----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not username or not password:
            flash("Username and password are required")
            return redirect(url_for("signup"))

        existing = User.query.filter_by(username=username).first()
        if existing:
            flash("Username already exists")
            return redirect(url_for("signup"))

        hashed = generate_password_hash(password, method="sha256")
        new_user = User(username=username, password=hashed)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created. Please log in.")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid credentials")
            return redirect(url_for("login"))

        login_user(user)
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("login"))

# ----------------- App Routes -----------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/check-in", methods=["GET", "POST"])
@login_required
def check_in():
    return render_template("check_in.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/journal")
@login_required
def journal():
    return render_template("journal.html")

@app.route("/resources")
@login_required
def resources():
    return render_template("resources.html")

@app.route("/safety")
@login_required
def safety():
    return render_template("safety.html")

@app.route("/login-redirect")
def login_redirect():
    return redirect(url_for("login"))

# Diagnostics route to verify paths Flask is using
@app.route("/__whereami")
def whereami():
    return jsonify({
        "cwd": os.getcwd(),
        "template_folder": os.path.abspath(app.template_folder),
        "static_folder": os.path.abspath(app.static_folder)
    })

# ----------------- Main -----------------

if __name__ == "__main__":
    # run with debug to auto reload templates and code
    app.run(debug=True)
