#  PROJECTDNA NEXUS
> **Intelligent Academic Project Lifecycle, Knowledge Vault & Risk Management Platform**

PROJECTDNA NEXUS is an enterprise-grade Django web application designed for university project coordination, faculty evaluation, activity tracking, architectural decision logging (ADR), risk prediction, and institutional knowledge preservation.

---

##  Key Features

* ** User Roles & Dashboards**: Dedicated portals for Students, Faculty Advisors, Heads of Department (HOD), and System Administrators.
* ** Academic Projects Directory**: Project proposal submission, status workflows, and automated DNA hash initialization.
* **Intelligence & Knowledge Vault**: Institutional repository for architectural best practices, lessons learned, and risk prediction scoring.
* ** Collaboration Suite**: Team chat rooms, discussion forums, and interactive unread notifications.
* ** Analytics & Reports**: Departmental progress metrics, innovation scores, work log activity logs, and bug reporting.

---

##  Technology Stack

* **Backend Framework**: Python 3.10+ & Django 6.0+
* **Frontend**: HTML5, Vanilla CSS3, Bootstrap 5.3, FontAwesome 6, Chart.js, AOS Animations
* **Production WSGI & Static Server**: Gunicorn & WhiteNoise
* **Database**: SQLite (Development) / PostgreSQL compatible (Production)

---

##  Quick Start (Local Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/Dharshika-11/projectdna.git
cd projectdna
```

### 2. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations & Seed Demo Data
```bash
python manage.py migrate
python manage.py seed_data
```
> **Default Admin Credentials**:
> - **Username**: `admin`
> - **Password**: `admin123`

### 5. Start Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

##  Production Deployment (Render.com)

1. **Build Command**:
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   ```
2. **Start Command**:
   ```bash
   gunicorn nexus.wsgi:application
   ```

---

## 📄 License
This project is licensed under the MIT License.
