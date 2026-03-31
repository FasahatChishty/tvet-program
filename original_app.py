from flask import Flask, render_template, request, redirect, flash
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from backend.backend_logic import register_student_web

app = Flask(__name__)
app.secret_key = "supersecret"  # flash messages ke liye

# Removed MySQL connection, using backend CSV instead

# Registration route
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        roll = request.form['roll']
        email = request.form['email']
        password = request.form['password']
        mode = "FYP" if request.form.get('mode') == 'fyp' else "JOB"

        # Use backend function instead of SQLAlchemy
        student_id, message = register_student_web(name, roll, email, password, mode)
        if student_id:
            # Generate verification code (as in original)
            code = str(random.randint(100000, 999999))
            flash(f"Registration successful! Your Student ID: {student_id}, Verification code: {code}", "success")
            return redirect("/register")
        else:
            flash(message, "error")
            return redirect("/register")

    return render_template("original_register.html")

if __name__ == "__main__":
    # 🔹 Run Flask server
    app.run(debug=True)