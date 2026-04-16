# 🚀 Internship Portal

<div align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green" alt="Django" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Vanilla_CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
</div>

<br>

A premium, fully-featured Internship Management Tracking Portal built with Django. Designed with a stunning **Glassmorphism UI** and **Dark Mode**, this application connects students with top companies while providing an incredibly smooth administrative experience.

## ✨ Key Features

- **💼 Role-Based Dashboards**: Independent portals tailored uniquely for Students (to track their applied jobs) and Admins (to shortlist/reject candidates).
- **🎨 Premium UI/UX**: Custom-built CSS library employing modern design systems including dynamic hovering, frosted glass UI components, and fluid animations.
- **✉️ Automated Email Notifications**: Fully integrated Google SMTP functionality. Generates instant confirmation emails and status updates (Shortlisted/Rejected).
- **📄 Resume Parsing**: Upload and securely store PDF resumes directly through the portal during the application phase.
- **🛡️ Secure Auth System**: Django-backed authentication and route protection.

---

## 🛠️ Run Locally (Development)

Follow these steps to run the portal on your local machine.

### 1. Clone & Setup
```bash
git clone https://github.com/surya-srinidhi/Internship-Portal.git
cd internship_portal

# Create and execute virtual environment
python -m venv venv
source venv/bin/activate

# Install requirements
pip install django
```

### 2. Configure Emails
Open `portal/settings.py` and strictly replace the email keys with a valid **Google App Password**:
```python
EMAIL_HOST_USER = 'your_real_gmail@gmail.com' 
EMAIL_HOST_PASSWORD = 'your_16_character_app_password' 
```

### 3. Migrate & Launch
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## 🚀 Deployment Guide (Production via Render.com)

1. **Install Production Packages**: Run `pip install gunicorn whitenoise psycopg2-binary` locally, then save them by running `pip freeze > requirements.txt`.
2. **Hide Keys**: In `portal/settings.py`, replace your hardcoded `SECRET_KEY`, `EMAIL_HOST_USER`, and `EMAIL_HOST_PASSWORD` with `os.environ.get('SECRET_KEY')` so hackers don't scrape your keys! (Change `DEBUG = False`).
3. **Deploy**: Push your code to GitHub, go to [Render.com](https://render.com), and create a new **Web Service**.
4. **Link it**: Connect your GitHub. Put `pip install -r requirements.txt && python manage.py migrate` as the Build Command, and `gunicorn portal.wsgi:application` as the Start Command.
5. **Add Environment Variables**: Add your secret keys directly into Render's dashboard. Click **Deploy**!
