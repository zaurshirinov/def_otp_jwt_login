
🚀 OTP Login API (Django DRF + JWT + Celery + Redis)

A secure authentication system using OTP (One-Time Password) via email, combined with JWT authentication, Redis caching, and Celery background tasks.
Includes a simple approval workflow system for user-created items.


✨ Features
	•	🔐 OTP-based login via email
	•	🎟 JWT authentication (access + refresh tokens)
	•	⚡ Redis caching for OTP storage
	•	🧵 Celery for async email sending
	•	🧾 Approval system (PENDING / APPROVED / REJECTED)
	•	🚦 Rate limiting (OTP requests)
	•	🔎 Filtering & pagination support
	•	📄 Swagger API documentation


🧱 Tech Stack
	•	Python
	•	Django
	•	Django REST Framework
	•	Simple JWT
	•	Redis
	•	Celery
	•	drf-yasg (Swagger)


⚙️ Installation
    git clone https://github.com/zaurshirinov/def_otp_jwt_login.git
    cd def_otp_jwt_login

    python -m venv venv
    source venv/bin/activate  # Mac/Linux

    pip install -r requirements.txt


🔐 Environment Setup

Create .env file:
    cp .env.example .env
    SECRET_KEY=your_secret_key
    DEBUG=True

    EMAIL_HOST_USER=your_email@gmail.com
    EMAIL_HOST_PASSWORD=your_password

    REDIS_URL=redis://127.0.0.1:6379/1
    REDIS_BROKER_URL=redis://127.0.0.1:6379/1


⚡ Running Services
Start Redis
    redis-server
Start Celery Worker
    celery -A core worker -l info


🚀 Run Project
    python manage.py migrate
    python manage.py runserver
    

📬 API Endpoints

Authentication
	•	POST /auth/send-otp/
	•	POST /auth/verify-otp/

Items
	•	POST /items/ → Create item (auth required)
	•	GET /items/approved/ → Public approved items
	•	GET /items/my/ → User’s items


🔒 Permissions
	•	Only authenticated users can create items
	•	Users can only view their own items
	•	Only admin can update item status

⸻

🧠 OTP Logic
	•	OTP stored in Redis
	•	Expires in 5 minutes
	•	Deleted after successful verification
	•	Rate limited to prevent spam

📄 API Documentation
Swagger UI available at:
    /swagger/


📦 Project Structure
core/        # settings, celery config
api/         # models, views, serializers
manage.py


🧑‍💻 Author

Zaur Şirinov
# 🚀 OTP Login API (Django DRF + JWT + Celery + Redis)

A secure authentication system using OTP (One-Time Password) via email, combined with JWT authentication, Redis caching, and Celery background tasks.  
Includes a simple approval workflow system for user-created items.

---

## ✨ Features

- 🔐 OTP-based login via email  
- 🎟 JWT authentication (access + refresh tokens)  
- ⚡ Redis caching for OTP storage  
- 🧵 Celery for async email sending  
- 🧾 Approval system (PENDING / APPROVED / REJECTED)  
- 🚦 Rate limiting (OTP requests)  
- 🔎 Filtering & pagination support  
- 📄 Swagger API documentation  

---

## 🧱 Tech Stack

- Python  
- Django  
- Django REST Framework  
- Simple JWT  
- Redis  
- Celery  
- drf-yasg (Swagger)  

---

## ⚙️ Installation

```bash
git clone https://github.com/zaursirinov/def_otp_jwt_login.git
cd def_otp_jwt_login

python -m venv venv
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

---

## 🔐 Environment Setup

Create `.env` file:

```bash
cp .env.example .env
```

Example `.env`:

```env
SECRET_KEY=your_secret_key
DEBUG=True

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_password

REDIS_URL=redis://127.0.0.1:6379/1
REDIS_BROKER_URL=redis://127.0.0.1:6379/1
```

---

## ⚡ Running Services

### Start Redis
```bash
redis-server
```

### Start Celery Worker
```bash
celery -A core worker -l info
```

---

## 🚀 Run Project

```bash
python manage.py migrate
python manage.py runserver
```

---

## 📬 API Endpoints

### Authentication
- POST `/auth/send-otp/`
- POST `/auth/verify-otp/`

### Items
- POST `/items/` → Create item (auth required)
- GET `/items/approved/` → Public approved items
- GET `/items/my/` → User’s items

---

## 🔒 Permissions

- Only authenticated users can create items  
- Users can only view their own items  
- Only admin can update item status  

---

## 🧠 OTP Logic

- OTP stored in Redis  
- Expires in 5 minutes  
- Deleted after successful verification  
- Rate limited to prevent spam  

---

## 📄 API Documentation

Swagger UI available at:
```
/swagger/
```

---

## 📦 Project Structure

```
core/        # settings, celery config
api/         # models, views, serializers
manage.py
```

---

## 🧑‍💻 Author

Zaur Şirinov