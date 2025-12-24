# 🧵 JAGDAMBA TEXTILES

JAGDAMBA TEXTILES is a full-stack Python-based textile e-commerce platform designed for Indian fabric businesses. The system supports multiple fabric categories, color-based pricing, secure authentication, and scalable payment integration.

## ✨ Features
- Admin & Customer Login (JWT Authentication)
- Fabric Categories: Georgette, Net, Velvet, Crepe, Djam, Rayon
- Multiple colors per fabric with individual pricing
- Indian currency (₹ INR)
- Order & Payment Management
- Clean & professional UI
- Scalable payment gateway support

## 🛠 Tech Stack
- Backend: Python, Flask
- Auth: JWT
- Database: MySQL
- ORM: SQLAlchemy
- Server: Gunicorn
- Frontend: HTML, CSS, Bootstrap

## 🚀 Run Locally
```bash
git clone https://github.com/mrsachingithub/Jagdamba-Textiles.git
cd JagdambaTextiles
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python create_db.py
python seed_data.py
python run.py
