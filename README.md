# 🛒 Flask E-Commerce Web Application

A **full-stack e-commerce web application** built using **Flask**, **SQLAlchemy**, and **SQLite**.  
This project focuses on **backend fundamentals**, **secure authentication**, **database relationships**, **filtering & searching**, and a **persistent favorite (like) system** rather than UI design.

---

## ✨ Overview

This application allows users to:

- Register & login securely  
- Browse products  
- Search & filter products  
- Like (favorite) products  
- Manage user profile  
- Sellers manage their own products  

🎯 **Goal:** Demonstrate Flask fundamentals, CRUD operations, session handling, database design, AJAX usage, and clean project structure.

---

## 🔥 Key Features

### 🔐 Authentication
- User Registration  
- Login & Logout  
- Session-based authentication  
- Buyer / Seller role handling  
- Profile page  

### 🛍️ Product Management
- View all products  
- Products displayed in **LIFO order** (latest added first)  

**Seller capabilities:**
- Add products  
- Update products  
- Delete products  
- View only their own products  

### 🔍 Search & Filter
- Live product search  
- Filter products by:
  - Category (Shirt, Pant, Shoes)
  - Gender (Men, Women, Kids)
  - Price range  

### ❤️ Favorites / Like System
- Like & unlike products using checkbox  
- Favorites stored in database  
- Favorite state persists after reload & logout  
- AJAX-based interaction (**no page reload**)  

### 👤 User Profiles
- View & manage profile  
- View favorite products  
- Role-based access control (buyer / seller)  

---

## 🧱 Project Structure

```text
e-commerce/
├── instance/
│   └── database.db
├── migrations/
├── static/
│   ├── uploads/
│   └── style.css
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── filter.html
│   ├── search.html
│   ├── favorite.html
│   ├── myproduct.html
│   └── profile.html
├── forms.py
├── main.py
├── requirement.txt
├── .env
└── README.md




## 🧱 Database Models

### User
- id
- username
- email
- password
- user_type (buyer / seller)

### Product
- id
- product_name
- product_price
- product_image
- product_details
- product_category
- product_gender
- product_stock
- seller_id (ForeignKey → User)

### UserProduct (Favorites)
- user_id
- product_id

---

## 🛠️ Tech Stack

| Layer      | Technology     |
|------------|----------------|
| Backend    | Flask          |
| ORM        | SQLAlchemy     |
| Database   | SQLite         |
| Templates  | Jinja2         |
| Forms      | Flask-WTF      |
| Migration  | Flask-Migrate  |
| Frontend   | HTML, CSS, JS  |
| AJAX       | Fetch API      |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/mayank-tagline/e-commerce.git
cd e-commerce


## 2️⃣ Create & Activate Virtual Environment

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 🪟 Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```


## 3️⃣ Install Dependencies

```bash
pip install -r requirement.txt
```


## 🔐 Environment Variables (.env)

## Create a .env file in the project root:

```bash
MAIL_ID=your_email@gmail.com
MAIL_PASSWORD=your_email_app_password
```

## ⚠️ .env is ignored by Git for security reasons.




## 🗄️ Database Migration
## First-time setup (if migrations/ does not exist)
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## If migrations already exist
```bash
flask db migrate
flask db upgrade
```



## ▶️ Running the Application
```bash
python main.py
```
## Open in browser:
## 👉 http://127.0.0.1:5000
