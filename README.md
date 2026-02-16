# Netlon Backend

Netlon Backend is a RESTful API backend built using **Flask (Python)**.  
This project provides core backend features for the Netlon application including user authentication, user management, quotations, inventory, and more.  
It is designed to work with a frontend client (React/Vue/Flutter) to deliver a complete full-stack solution.

---

## 🚀 Features

- User Authentication with JWT
- User Management (CRUD)
- Quotation Management
- Inventory Management
- Dashboard APIs
- Modular REST Architecture
- Database Migrations with Flask-Migrate

---

## 🛠️ Tech Stack

- Python 3.x  
- Flask  
- Flask-SQLAlchemy  
- Flask-Migrate  
- Flask-JWT-Extended  
- MySQL / SQLite  
- RESTful API Design

---

## 📁 Project Structure

```
netlonbackend/
│
├── app/
│   ├── auth/
│   ├── users/
│   ├── quotations/
│   ├── inventory/
│   └── __init__.py
│
├── migrations/
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```
git clone https://github.com/mahalakshmi0606/netlonbackend.git
cd netlonbackend
```

### 2. Create a Virtual Environment

```
python -m venv venv
```

Activate the virtual environment:

Windows:
```
venv\Scripts\activate
```

Mac/Linux:
```
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

## 🗄️ Database Configuration

Create a database and update the database URI in `config.py`:

Example for MySQL:

```
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@localhost/netlon_db"
```

Or SQLite:

```
SQLALCHEMY_DATABASE_URI = "sqlite:///netlon.db"
```

---

## 🔄 Database Migrations

```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## ▶️ Run the Application

```
python run.py
```

The backend server runs at:

```
http://127.0.0.1:5000
```

---

## 📡 API Endpoints (Examples)

### Authentication
- `POST /api/auth/login` – User login

### Users
- `GET /api/users` – Get all users
- `POST /api/users` – Create user
- `PUT /api/users/<id>` – Update user
- `DELETE /api/users/<id>` – Delete user

### Quotations
- `GET /api/quotations` – List all quotations
- `POST /api/quotations` – Create a quotation
- `GET /api/quotations/<id>` – Get specific quotation
- `PUT /api/quotations/<id>` – Update quotation
- `DELETE /api/quotations/<id>` – Delete quotation

### Inventory
- `GET /api/inventory` – List inventory items
- `POST /api/inventory` – Add inventory item
- `PUT /api/inventory/<id>` – Update inventory item
- `DELETE /api/inventory/<id>` – Delete inventory item

---

## 🔐 Environment Variables

```
FLASK_ENV=development
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
```

---

## 🤝 Contributing

1. Fork the repository  
2. Create a new branch  
3. Make your changes  
4. Commit & push  
5. Open a Pull Request

---

## 👩‍💻 Author

**Mahalakshmi M**  
Full Stack Developer
