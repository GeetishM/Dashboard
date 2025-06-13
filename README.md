# Material Management Dashboard

A robust web-based **Material Management Dashboard** built with **Django** and powered by **MySQL**, designed to manage and analyze over **300,000+ records**. It offers clean and intuitive charts, graphs, and insights through real-time data visualization using `Chart.js`, `Bootstrap`, and core frontend tools.

This dashboard provides efficient material tracking, stock trends, category distribution, and usage insights through powerful backend logic and frontend visualization.

---

## Features

- Built on Django (Python Web Framework)
- Backend connected with a large-scale **MySQL database** (>3 lakh records)
- Clean, responsive UI using **HTML, CSS, JavaScript, Bootstrap**
- Data analysis and dynamic charts/graphs using `Chart.js`
- Secure environment configuration using `.env`
- RESTful architecture and modular codebase

---

## Tech Stack

- **Backend:** Django (Python)
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Visualization:** Chart.js
- **Environment Management:** python-dotenv (`.env` for secrets and config)

---

## Data Insights & Analysis

The system performs backend-level data aggregation, trend analysis, and presents them via:

- Bar charts for stock usage trends
- Pie charts for material distribution
- Line graphs for temporal usage patterns
- Dashboard widgets for real-time metrics

---

## Setup & Installation Guide

### Prerequisites

Make sure you have the following installed:

- Python 3.8+
- MySQL Server
- pip
- Git

### Step-by-Step Installation

1. **Clone the Repository**

```
git clone https://github.com/your-username/material-management-dashboard.git
cd material-management-dashboard
```

2. **Create Virtual Environment & Activate**
```
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

3. **Install Requirements**
``` pip install -r requirements.txt ```

4. **Configure .env File**
```
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=your_database_name
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

5. **Apply Migrations & Run Server**
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## Credits & Collaborators
This project is made possible by the efforts of:
- [Geetish Mahato](https://github.com/GeetishM)
- [Anamika Dey](https://github.com/anamikadey099)
- [Pragya Kumar](https://github.com/Pragya-Kumar) 
\n Thanks to all contributors who helped shape this dashboard.
