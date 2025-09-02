# from flask import Flask, render_template, request, redirect, url_for, session, flash
#
# app = Flask(__name__)
# app.secret_key = "your_secret_key_here"  # Change this in production
#
# # Dummy user database (you can connect with MySQL or MongoDB later)
# users = {
#     "admin@gmail.com": "merapassward",
#     "suraj@gmail.com": "12345"
# }
#
#
# @app.route("/", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["email"]
#         password = request.form["password"]
#         print(username)
#         print(password)
#         if users[username] == password:
#             flash("Login successful!", "success")
#             return redirect(url_for("home"))
#         else:
#             flash("Invalid username or password!", "danger")
#     else:
#         print("Nahi chala")
#     return render_template("login_page.html")
#
#
# @app.route("/home")
# def home():
#     return render_template("home_page.html")
#
#
# @app.route("/logout")
# def logout():
#     session.pop("username", None)
#     flash("Logged out successfully!", "info")
#     return redirect(url_for("login"))
#
#
# if __name__ == "__main__":
#     app.run(debug=True)




from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key"  # change in production

# In-memory user storage (replace with DB later)
users = {"suraj@gmail.com": "12345"}


@app.route("/")
def home():
    return render_template("login_page.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    print("In login")
    print(users[email])
    print("->", password)

    if users[email] == password:
        print("Yes----")
        flash("✅ Login successful!", "success")
        return render_template("home_page.html")
    else:
        print("NO----")
        flash("❌ Invalid email or password!", "danger")
        return render_template("login_page.html")


if __name__ == "__main__":
    app.run(debug=True)
