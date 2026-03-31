# 🚀 TVET Assessment System - Quick Start Guide

## ⚡ 5-Minute Setup

### 1. **Start the Application**
```bash
cd c:\Users\ABC\Desktop\fYP
python frontend\web_app.py
```

Server will run at: `http://localhost:5000`

### 2. **Register a New Student**
- Click "Register" on home page
- Fill in name, roll number, email, password
- Choose FYP or JOB mode
- Receive registration code

### 3. **Login**
- Click "Login" on home page
- Enter: Name, Email, Registration Code
- Click "Login"

### 4. **Take Assessment**
- You'll see two cards: FYP Assessment and JOB Assessment
- Click "Start FYP Assessment" or "Start JOB Assessment"
- Answer all questions
- Click "Submit Assessment"

### 5. **View Dashboard**
- After submission, you'll see your dashboard
- Your progress is shown with completion status
- Scores are displayed when assessments are completed

---

## 📊 New Features Overview

### ✅ Questionnaire Home
- Beautiful card-based interface
- Choose between FYP and JOB assessments
- Shows assessment descriptions and features

### ✅ Questionnaire Form
- Real-time progress tracking
- Countdown timer (45 minutes)
- Question counter
- Section categorization
- Form validation

### ✅ Student Dashboard
- Student information display
- Progress tracking for both paths
- Scores and completion dates
- Quick action buttons
- Overall summary with comparisons

---

## 🎯 Key URLs

| Feature | URL | Method |
|---------|-----|--------|
| Home | http://localhost:5000/ | GET |
| Register | http://localhost:5000/register | GET/POST |
| Login | http://localhost:5000/login | GET/POST |
| Questionnaire Home | http://localhost:5000/questionnaire_home | GET |
| FYP Questionnaire | http://localhost:5000/questionnaire/fyp | GET |
| JOB Questionnaire | http://localhost:5000/questionnaire/job | GET |
| Submit Questionnaire | http://localhost:5000/submit_questionnaire | POST |
| Dashboard | http://localhost:5000/dashboard | GET |
| API Progress | http://localhost:5000/api/student_progress | GET |
| Logout | http://localhost:5000/logout | GET |

---

## 📁 File Structure

```
fYP/
├── frontend/
│   ├── templates/
│   │   ├── questionnaire_home.html (NEW)
│   │   ├── questionnaire.html (NEW)
│   │   ├── dashboard.html (NEW)
│   │   ├── login.html
│   │   ├── register.html
│   │   └── ...
│   ├── web_app.py (UPDATED)
│   └── ...
├── backend/
│   ├── backend_logic.py (UPDATED)
│   ├── users_db.csv
│   └── ...
├── results/
│   └── questionnaire_progress.csv (NEW - Created on first submission)
└── IMPLEMENTATION_GUIDE.md (NEW)
```

---

## 🔧 Configuration

### Email Setup (Optional but Recommended)

Edit email configuration in `backend_logic.py` lines 15-16:

```python
EMAIL_USER = "your-email@gmail.com"
EMAIL_PASS = "your-16-char-app-password"
```

For Gmail:
1. Enable 2-Step Verification
2. Generate App Password at: https://myaccount.google.com/apppasswords
3. Use the 16-character password

---

## 📊 Test Data Format

Questions CSV should have columns:
```
question_id, question_text, section, option_a, option_b, option_c, option_d, option_e
```

Example:
```
Q001, What is your preferred work environment?, Technical, Outdoor, Office, Remote, Lab, Hybrid
```

---

## 🐛 Troubleshooting

### "Page not found" after login
- Make sure `/questionnaire_home` route is working
- Check Flask is running on correct port

### Questions not loading
- Verify CSV file exists: `frontend/full_question_bank_with_responses.csv`
- Check column names match the code

### Results not saving
- Check `results/` folder exists
- Verify write permissions

### Email not sending
- Configure EMAIL_USER and EMAIL_PASS
- Check SMTP settings
- Verify email address is correct

---

## 🎨 Customization

### Change Timer Duration
In `questionnaire.html`, line ~115:
```javascript
let timeLimit = 45 * 60; // Change 45 to desired minutes
```

### Change Assessment Names
Edit template text:
- `questionnaire_home.html` - Card titles
- `dashboard.html` - Progress labels

### Modify Progress Categories
Add/remove domains in `backend_logic.py`:
```python
DOMAINS = ["GOLEK","RIASEC","LearningStyle","Verbal","Strength","Technical","WorkValues"]
```

---

## 📱 Browser Support

✅ Chrome 90+
✅ Firefox 88+
✅ Safari 14+
✅ Edge 90+
✅ Mobile browsers

---

## 🔐 Session Duration

Default session timeout: Browser session
- Session cleared on logout
- Session persists during active use

---

## 📊 Progress Database

Auto-created file: `results/questionnaire_progress.csv`

Tracks:
- Student ID
- FYP completion status
- JOB completion status
- Completion dates
- Scores for each path

---

## ✨ Best Practices

1. **Before Going Live**
   - [ ] Test registration flow
   - [ ] Test both FYP and JOB questionnaires
   - [ ] Verify email configuration
   - [ ] Test on mobile devices
   - [ ] Check dashboard displays correctly

2. **During Use**
   - [ ] Backup CSV files regularly
   - [ ] Monitor Flask logs for errors
   - [ ] Verify emails are being sent

3. **After Use**
   - [ ] Archive results regularly
   - [ ] Review student progress
   - [ ] Send summary emails to students

---

## 🆘 Support

### Common Issues:

**"Invalid credentials" on login:**
- Verify email and registration code match registration
- Check users_db.csv has correct entries

**Timer shows "--:--":**
- Refresh page if JavaScript hasn't loaded
- Check browser console for errors

**Progress not updating:**
- Refresh dashboard page
- Check questionnaire_progress.csv is writable

---

## 🎉 You're All Set!

The TVET Assessment System is ready to use with:
- ✅ Dual questionnaire system
- ✅ User dashboard
- ✅ Progress tracking
- ✅ Email notifications
- ✅ Mobile responsive design

Start the application and enjoy! 🚀

---

## 📞 Need Help?

Check the following in order:
1. IMPLEMENTATION_GUIDE.md - Detailed documentation
2. Browser console (F12) - For frontend errors
3. Flask server logs - For backend errors
4. CSV files - For data issues
5. Email configuration - For notification issues

Happy testing! ✨
