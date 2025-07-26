🛍️ ChazeFashion - Django E-Commerce Platform
ChazeFashion is a modern, full-featured e-commerce web application built with Django. It combines a sleek, responsive UI with powerful backend features like user authentication, cart/wishlist handling, and a customizable admin interface — all with dark mode support!
<br>

🚀 Live Demo:
🔗 https://productcatlog-2-nqre.onrender.com

✨ Features
👤 User Registration, Login & Profile Management

🛒 Product Catalog with Categories, Filtering & Search

⭐ Product Detail Pages with Customer Reviews

❤️ Add to Cart & Wishlist (Authenticated Users Only)

💡 Dark Mode Toggle for Better Accessibility

🎨 Beautiful, Responsive UI with Tailwind CSS, DaisyUI & Lottie Animations

🛠️ Admin Panel for Managing Products & Users

🗂️ Project Structure
Copy
Edit
ProductCatlog-master/
├── ChazeFashion/
│   ├── manage.py
│   ├── ChazeFashion/
│   │   ├── settings.py
│   │   ├── wsgi.py
│   │   └── ...
│   └── catalog/
│       ├── models.py
│       ├── views.py
│       ├── templates/
│       └── ...
├── requirements.txt
🛠️ Local Development Setup
Clone the repository

bash
Copy
Edit
git clone https://github.com/Adityaraj067/ProductCatlog.git
cd ProductCatlog-master/ChazeFashion
Create and activate a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate          # On Windows: venv\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Apply migrations

bash
Copy
Edit
python manage.py migrate
Create a superuser (optional)

bash
Copy
Edit
python manage.py createsuperuser
Run the development server

bash
Copy
Edit
python manage.py runserver
Access the application

🏠 Home: http://127.0.0.1:8000/

🔐 Admin: http://127.0.0.1:8000/admin/

🌐 Deployment on Render
Push your code to GitHub

Create a Web Service on Render:

Root Directory: ChazeFashion

Build Command:

bash
Copy
Edit
pip install -r requirements.txt && python manage.py collectstatic --noinput
Start Command:

bash
Copy
Edit
gunicorn ChazeFashion.wsgi:application
Environment Variables:

ini
Copy
Edit
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=your-database-url (PostgreSQL recommended)
Post-deploy: Run migrations from Render shell

bash
Copy
Edit
python manage.py migrate
(Optional) Create a superuser

bash
Copy
Edit
python manage.py createsuperuser
📁 Static & Media Files
Static files served from: /static/

Media uploads served from: /media/ (configure storage for production use)

🔐 Production Tips
Set DEBUG = False in settings.py

Use a secure and secret DJANGO_SECRET_KEY

Switch to PostgreSQL for production

Implement SSL/HTTPS, CSRF protection, and proper CORS settings

📸 Screenshots
Add screenshots here of homepage, product detail page, cart, dark mode, etc.

📜 License
This project is intended for educational/demo purposes. For real-world deployment, enhance the app’s security, payment integration, and hosting setup.

