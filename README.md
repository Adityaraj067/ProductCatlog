# ChazeFashion - Django E-Commerce Platform

ChazeFashion is a modern, full-featured e-commerce web application built with Django. It features a beautiful UI, user authentication, product catalog, cart, wishlist, profile management, and dark mode support.

## Features
- User registration, login, and profile management
- Product catalog with categories, filtering, and search
- Product detail pages with reviews
- Add to cart and wishlist (with authentication)
- Responsive, modern UI with Tailwind CSS, DaisyUI, and Lottie animations
- Dark mode toggle
- Admin panel for product/user management

## Project Structure
```
ProductCatlog-master/
  ChazeFashion/
    manage.py
    ChazeFashion/
      settings.py
      wsgi.py
      ...
    catalog/
      models.py
      views.py
      templates/
      ...
  requirements.txt
```

## Local Development Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/Adityaraj067/ProductCatlog.git
   cd ProductCatlog-master/ChazeFashion
   ```
2. **Create a virtual environment and activate it:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```
5. **Create a superuser (optional):**
   ```sh
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```sh
   python manage.py runserver
   ```
7. **Visit:**
   - Home: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Deployment on Render
1. **Push your code to GitHub.**
2. **Create a new Web Service on [Render](https://render.com/):**
   - Set **Root Directory** to `ChazeFashion`
   - **Build Command:**
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - **Start Command:**
     ```
     gunicorn ChazeFashion.wsgi:application
     ```
   - **Environment Variables:**
     - `DJANGO_SECRET_KEY` (your secret key)
     - `DEBUG=False`
     - `ALLOWED_HOSTS=your-app.onrender.com`
     - `DATABASE_URL` (if using Postgres)
3. **After first deploy, run migrations in the Render shell:**
   ```sh
   python manage.py migrate
   ```
4. **(Optional) Create a superuser:**
   ```sh
   python manage.py createsuperuser
   ```

## Notes
- Static files are served from `/static/` after `collectstatic`.
- Media files are stored in `/media/` (configure storage for production).
- For production, set `DEBUG=False` and use a secure `DJANGO_SECRET_KEY`.
- For best results, use Postgres on Render (not SQLite).

## License
This project is for educational/demo purposes. For production use, review and update security, payments, and deployment settings. 