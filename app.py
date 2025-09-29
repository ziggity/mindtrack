from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# Home router for home page rendering
@app.route("/home")
def home():
    return render_template("home.html")
    

# Check-in router for check-in page rendering
@app.route("/check-in", methods=["GET", "POST"])
def check_in():
    return render_template("check_in.html")


# Dashboard router for dashboard page rendering
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Journal router for journal page rendering
@app.route("/journal")
def journal():
    return render_template("journal.html")

# Resources router for resources page rendering
@app.route("/resources")
def resources():
    return render_template("resources.html")


if __name__ == "__main__":
    app.run(debug=True)
# Run the Flask application in debug mode           



