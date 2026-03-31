import os
import random
import json
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from model_training import prepare_features, compute_tvet_index

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecret"
DATA_DIR = Path("data")
RESULTS_FILE = DATA_DIR / "fyp_results.csv"
QUESTIONS_FILE = DATA_DIR / "questions.json"
SETTINGS_FILE = DATA_DIR / "settings.json"
ADMIN_EMAILS = {"admin@tvet.com", "sherankhanasim@gmail.com"}

# ==============================
# EMAIL CONFIG (Flask-Mail)
# ==============================
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USER", "")
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASS", "")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("EMAIL_USER", "")
app.config["MAIL_DEBUG"] = True
app.config["MAIL_SUPPRESS_SEND"] = False
print("EMAIL USER:", app.config["MAIL_USERNAME"])
print("EMAIL PASS:", app.config["MAIL_PASSWORD"])

# ==============================
# DATABASE CONFIG (MySQL)
# ==============================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# ==============================
# USER MODEL
# ==============================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    roll = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    verification_code = db.Column(db.String(6))
    is_verified = db.Column(db.Boolean, default=False)

# ==============================
# HOME ROUTE (FIXED)
# ==============================
@app.route("/")
def home():
    return render_template("index.html")


def is_logged_in():
    return bool(session.get("user_id"))


def is_admin():
    return session.get("user_email") in ADMIN_EMAILS


def admin_required():
    if not is_logged_in() or not is_admin():
        return redirect(url_for("login"))
    return None


def load_questions(test_type=None):
    if not QUESTIONS_FILE.exists():
        return {}
    try:
        data = json.loads(QUESTIONS_FILE.read_text())
        if test_type in {"FYP", "JOB"}:
            return data.get(test_type, {})
        return data
    except Exception:
        return {}


def save_questions(questions):
    DATA_DIR.mkdir(exist_ok=True)
    QUESTIONS_FILE.write_text(json.dumps(questions, indent=2))


def load_settings():
    default_settings = {
        "FYP_enabled": True,
        "JOB_enabled": True,
        "time_per_question": 60,
    }
    if not SETTINGS_FILE.exists():
        DATA_DIR.mkdir(exist_ok=True)
        SETTINGS_FILE.write_text(json.dumps(default_settings, indent=4))
        return default_settings
    try:
        with open(SETTINGS_FILE) as f:
            settings = json.load(f)
        for key, value in default_settings.items():
            settings.setdefault(key, value)
        return settings
    except Exception:
        return default_settings


def generate_pdf(name, index, label, domains):
    file_path = "report.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)

    c.setFont("Helvetica", 12)

    y = 750

    c.drawString(50, y, "TVET Assessment Report")
    y -= 30

    c.drawString(50, y, f"Name: {name}")
    y -= 20

    c.drawString(50, y, f"Score: {round(index, 2)}")
    y -= 20

    c.drawString(50, y, f"Level: {label}")
    y -= 30

    c.drawString(50, y, "Domain Breakdown:")
    y -= 20

    for domain, score in domains.items():
        c.drawString(70, y, f"{domain}: {round(score, 1)}")
        y -= 20

    c.save()

    return file_path


def migrate_results_csv():
    if not RESULTS_FILE.exists():
        return

    try:
        df = pd.read_csv(RESULTS_FILE)

        if "email" not in df.columns:
            df["email"] = ""

        if "score" not in df.columns:
            if "tvet_index" in df.columns:
                df["score"] = df["tvet_index"]
            else:
                df["score"] = ""

        if "label" not in df.columns:
            df["label"] = ""

        if "timestamp" not in df.columns:
            df["timestamp"] = "N/A"

        df["timestamp"] = df["timestamp"].fillna("N/A")
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
        df["timestamp"] = df["timestamp"].fillna("N/A")

        df = df[["email", "score", "label", "timestamp"]]
        df.to_csv(RESULTS_FILE, index=False)
    except Exception:
        pass

# ==============================
# REGISTER ROUTE
# ==============================
@app.route("/register", methods=["GET", "POST"])
def register():
    if is_logged_in():
        return redirect(url_for("test"))

    if request.method == "POST":
        name = request.form['name']
        roll = request.form['roll']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter(
            (User.email == email) | (User.roll == roll)
        ).first()

        if existing_user:
            flash("Email or Roll already exists!", "error")
            return redirect("/register")

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        code = str(random.randint(100000, 999999))

        new_user = User(
            name=name,
            roll=roll,
            email=email,
            password=hashed_password,
            verification_code=code
        )

        db.session.add(new_user)
        db.session.commit()

        try:
            msg = Message(
                subject="TVET Registration Verification Code",
                sender=app.config["MAIL_USERNAME"],
                recipients=[email],
                body=(
                    f"Hello {name},\n\n"
                    "Thank you for registering for the TVET Assessment System.\n\n"
                    "Your verification code is:\n"
                    f"{code}\n\n"
                    "Please enter this code to complete your registration and access the system.\n\n"
                    "Best regards,\n"
                    "TVET Program Team"
                ),
            )

            print("Sending email to:", email)
            mail.send(msg)
            print("Email sent successfully")

            flash("Registration successful! Verification code has been sent to your email.", "success")

        except Exception as e:
            import traceback
            traceback.print_exc()
            flash("Registration saved, but email could not be sent.", "error")

        return redirect("/login")

    return render_template("register.html")

# ==============================
# LOGIN ROUTE (ADDED)
# ==============================
@app.route("/login", methods=["GET", "POST"])
def login():
    if is_logged_in():
        return redirect("/dashboard")

    if request.method == "POST":
        email = request.form['email']
        code = request.form['code']

        user = User.query.filter_by(email=email).first()

        if not user or user.verification_code != code:
            flash("Invalid information!", "error")
            return redirect("/login")

        session["user_id"] = user.id
        session["user_email"] = user.email
        session["user_name"] = user.name
        flash("Login successful!", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


# ==============================
# SELECT TEST ROUTE
# ==============================
@app.route("/select-test", methods=["GET", "POST"])
def select_test():
    if not is_logged_in():
        return redirect(url_for("login"))

    if request.method == "POST":
        test_type = request.form.get("test_type", "FYP")
        session["test_type"] = "JOB" if test_type == "JOB" else "FYP"
        return redirect(url_for("test"))

    return render_template("select_test.html")

# ==============================
# TEST ROUTE
# ==============================
@app.route("/test", methods=["GET", "POST"])
def test():
    if not is_logged_in():
        return redirect(url_for("login"))

    settings = load_settings()
    test_type = session.get("test_type", "FYP")

    if test_type == "FYP" and not settings.get("FYP_enabled", True):
        return render_template("disabled.html", message="FYP test is currently disabled. Contact Fatima@gmail.com")

    if test_type == "JOB" and not settings.get("JOB_enabled", True):
        return render_template("disabled.html", message="Job test is currently disabled. Contact Fatima@gmail.com")

    if request.method == "POST":
        try:
            questions = load_questions(test_type)
            sections = ["GOLEK", "RIASEC", "LearningStyle", "Verbal", "Strength", "Technical", "WorkValues"]

            response_rows = []
            feature_rows = []

            for section in sections:
                answers = []
                domain_questions = questions.get(section, [])
                for i, _question_text in enumerate(domain_questions, start=1):
                    question_name = f"{section}_{i}"
                    value = request.form.get(question_name)
                    if value is None or value.strip() == "":
                        flash("Please answer all questions before submitting.", "error")
                        return redirect(url_for("test"))
                    try:
                        answer = int(value)
                    except ValueError:
                        flash("Invalid test input. Please choose a valid option.", "error")
                        return redirect(url_for("test"))
                    if answer < 1 or answer > 5:
                        flash("Invalid test input. Please choose a valid option.", "error")
                        return redirect(url_for("test"))
                    answers.append(answer)
                    response_rows.append({
                        "email": session.get("user_email", ""),
                        "section": section,
                        "question": question_name,
                        "answer": answer,
                        "timestamp": pd.Timestamp.now().isoformat(),
                    })

                score = (sum(answers) / (5 * 4)) * 100
                feature_rows.append({"section": section, "normalized": score})

            df = pd.DataFrame(feature_rows)
            domain_scores = {
                "GOLEK": df[df["section"] == "GOLEK"]["normalized"].values[0],
                "RIASEC": df[df["section"] == "RIASEC"]["normalized"].values[0],
                "LearningStyle": df[df["section"] == "LearningStyle"]["normalized"].values[0],
                "Verbal": df[df["section"] == "Verbal"]["normalized"].values[0],
                "Strength": df[df["section"] == "Strength"]["normalized"].values[0],
                "Technical": df[df["section"] == "Technical"]["normalized"].values[0],
                "WorkValues": df[df["section"] == "WorkValues"]["normalized"].values[0],
            }
            features = prepare_features(df)
            index, label = compute_tvet_index(features)

            session["tvet_result"] = {
                "index": index,
                "label": label,
                "domains": domain_scores
            }

            DATA_DIR.mkdir(exist_ok=True)
            responses_file = DATA_DIR / "fyp_responses.csv"
            responses_df = pd.DataFrame(response_rows)
            responses_df.to_csv(
                responses_file,
                mode="a",
                index=False,
                header=not responses_file.exists()
            )
            pd.DataFrame([{
                "email": session.get("user_email", ""),
                "score": round(index, 2),
                "label": label,
                "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            }]).to_csv(RESULTS_FILE, mode="a", index=False, header=not RESULTS_FILE.exists())

            try:
                recipient = session.get("user_email")
                if recipient:
                    pdf_path = generate_pdf(
                        session.get("user_name", ""),
                        index,
                        label,
                        domain_scores
                    )
                    msg = Message(
                        subject="Your TVET Assessment Report",
                        sender=app.config["MAIL_USERNAME"],
                        recipients=[recipient],
                        body=(
                            f"Hello {session.get('user_name', '')},\n\n"
                            "Your TVET assessment has been completed successfully.\n\n"
                            f"Score: {index}\n"
                            f"Level: {label}\n\n"
                            f"Interpretation: {('high alignment with the assessment profile.' if label == 'Strong' else 'a balanced match with room for further growth.' if label == 'Moderate' else 'further exploration and guidance may be helpful.')}\n\n"
                            "Thank you for completing the assessment.\n\n"
                            "Best regards,\n"
                            "TVET Program Team"
                        ),
                    )
                    with app.open_resource(pdf_path) as fp:
                        msg.attach(
                            "TVET_Report.pdf",
                            "application/pdf",
                            fp.read()
                        )
                    mail.send(msg)
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
            except Exception as e:
                import traceback
                traceback.print_exc()

            return redirect(url_for("result"))
        except Exception as e:
            import traceback
            traceback.print_exc()
            flash("Something went wrong while processing the test. Please try again.", "error")
            return redirect(url_for("test"))

    questions = load_questions(test_type)
    time_per_question = settings.get("time_per_question", 60)
    return render_template("test.html", questions=questions, test_type=test_type, time_per_question=time_per_question)

# ==============================
# RESULT ROUTE
# ==============================
@app.route("/result")
def result():
    if not is_logged_in():
        return redirect(url_for("login"))

    result_data = session.get("tvet_result")
    if not result_data:
        return redirect(url_for("test"))

    raw_label = result_data.get("label", "")
    display_label = raw_label.replace(" Preference", "") if raw_label else raw_label
    domains = result_data.get("domains", {})
    domain_messages = {
        "GOLEK": "Strong analytical and problem-solving ability",
        "RIASEC": "Clear career interest alignment",
        "LearningStyle": "Effective practical learning ability",
        "Verbal": "Strong communication and expression skills",
        "Strength": "Good physical endurance and discipline",
        "Technical": "High technical aptitude",
        "WorkValues": "Strong work ethics and values"
    }
    strengths = []
    weaknesses = []

    for domain, score in domains.items():
        if score >= 70:
            strengths.append(domain_messages.get(domain, domain))
        elif score < 50:
            weaknesses.append(domain_messages.get(domain, domain))

    return render_template(
        "result.html",
        tvet_index=result_data.get("index"),
        label=display_label,
        domains=domains,
        strengths=strengths,
        weaknesses=weaknesses
    )


@app.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    email = session.get("user_email")

    history = []
    if RESULTS_FILE.exists():
        df = pd.read_csv(RESULTS_FILE)

        if "email" in df.columns:
            df = df[df["email"] == email]
        else:
            df = df.iloc[0:0]

        if "score" in df.columns:
            df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0)
        else:
            df["score"] = 0

        if "timestamp" not in df.columns:
            df["timestamp"] = ""

        df["timestamp"] = df["timestamp"].fillna("N/A")
        df = df.sort_values(by="timestamp", ascending=False)
        history = df.to_dict("records")

    latest = history[0] if history else None
    domains = session.get("tvet_result", {}).get("domains", {})

    return render_template(
        "dashboard.html",
        history=history,
        latest=latest,
        domains=domains
    )


# ==============================
# ADMIN ROUTES
# ==============================
@app.route("/admin")
def admin_dashboard():
    denied = admin_required()
    if denied:
        return denied
    return render_template("admin.html")


@app.route("/admin/users")
def admin_users():
    denied = admin_required()
    if denied:
        return denied
    users = User.query.order_by(User.id.asc()).all()
    return render_template("users.html", users=users)


@app.route("/admin/results")
def admin_results():
    denied = admin_required()
    if denied:
        return denied
    results = []
    if RESULTS_FILE.exists():
        df = pd.read_csv(RESULTS_FILE)
        expected_cols = ["email", "score", "label", "timestamp"]
        df = df.reindex(columns=expected_cols)
        df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0)
        df["email"] = df["email"].fillna("N/A")
        df["label"] = df["label"].fillna("N/A")
        df["timestamp"] = df["timestamp"].fillna("N/A")
        results = df.to_dict(orient="records")
    return render_template("results.html", results=results)


@app.route("/admin/questions", methods=["GET", "POST"])
def admin_questions():
    denied = admin_required()
    if denied:
        return denied

    sections = ["GOLEK", "RIASEC", "LearningStyle", "Verbal", "Strength", "Technical", "WorkValues"]
    all_questions = load_questions()
    active_type = session.get("test_type", "FYP")
    questions = all_questions.get(active_type, {})

    if request.method == "POST":
        action = request.form.get("action")
        domain = request.form.get("domain")

        if domain not in sections:
            flash("Invalid domain.", "error")
            return redirect(url_for("admin_questions"))

        all_questions.setdefault("FYP", {})
        all_questions.setdefault("JOB", {})
        all_questions[active_type].setdefault(domain, [])

        if action == "add":
            new_question = request.form.get("question", "").strip()
            if not new_question:
                flash("Question cannot be empty.", "error")
                return redirect(url_for("admin_questions"))
            all_questions[active_type][domain].append(new_question)
            save_questions(all_questions)
            flash("Question added.", "success")
        elif action == "delete":
            index = int(request.form.get("index", "-1"))
            if 0 <= index < len(all_questions[active_type][domain]):
                all_questions[active_type][domain].pop(index)
                save_questions(all_questions)
                flash("Question deleted.", "success")
            else:
                flash("Question not found.", "error")

        return redirect(url_for("admin_questions"))

    return render_template("questions.html", questions=questions, sections=sections)


@app.route("/admin/settings", methods=["GET", "POST"])
def admin_settings():
    denied = admin_required()
    if denied:
        return denied

    settings = load_settings()
    if request.method == "POST":
        updated_settings = {
            "FYP_enabled": request.form.get("FYP_enabled") == "on",
            "JOB_enabled": request.form.get("JOB_enabled") == "on",
            "time_per_question": int(request.form.get("time_per_question", 60) or 60),
        }
        DATA_DIR.mkdir(exist_ok=True)
        with open(SETTINGS_FILE, "w") as f:
            json.dump(updated_settings, f, indent=4)
        flash("Settings updated successfully.", "success")
        return redirect(url_for("admin_settings"))

    return render_template("settings.html", settings=settings)


# ==============================
# LOGOUT ROUTE
# ==============================
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect("/login")


@app.route("/test-email")
def test_email():
    try:
        msg = Message(
            subject="Test Email",
            recipients=[app.config["MAIL_USERNAME"]],
            body="This is a test email from Flask."
        )
        mail.send(msg)
        return "Email sent!"
    except Exception as e:
        import traceback
        traceback.print_exc()
        return "Error sending email"

# ==============================
# CREATE TABLES (IMPORTANT)
# ==============================
with app.app_context():
    db.create_all()
    migrate_results_csv()

# ==============================
# RUN APP
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
