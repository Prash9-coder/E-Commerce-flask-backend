E-Commerce Site
Overview
This project is an e-commerce website built using Python Flask, SQLAlchemy, Flask-Migrate, HTML, CSS, and JavaScript. The site provides a platform for users to browse products, manage their cart, and complete purchases.
To visit my website you can click the following link https://ecommerceflask1.pythonanywhere.com/

Features
User Authentication: Register, log in, and manage user profiles.
Product Catalog: Browse and search products.
Shopping Cart: Add products to the cart and update quantities.
Checkout Process: Complete purchases and manage orders.
Admin Dashboard: Manage products, view orders, and update inventory (if implemented).
Technologies Used
Backend:

Flask: Web framework for Python.
SQLAlchemy: ORM for database management.
Flask-Migrate: Handles SQLAlchemy database migrations.
Frontend:

HTML/CSS: Markup and styling.
JavaScript: Client-side scripting.
Setup
Prerequisites
Python 3.8 or higher
pip (Python package installer)
Installation
Clone the Repository

bash
git clone https://github.com/prash9-coder/E-Commerce-flask-backend.git
cd your-repo
Create a Virtual Environment

bash
python -m venv prash
Activate the Virtual Environment

To activate environment
bash
prash\Scripts\activate

bash
pip install -r requirements.txt
Set Up the Database

bash
flask db upgrade
Run the Application

bash
flask run
The application will be available at http://127.0.0.1:5000.

Configuration
Environment Variables: Create a .env file in the root directory to configure environment-specific settings such as database URLs and secret keys. An example .env file might look like:

makefile
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///register.database
Usage
Home Page: View featured products and navigate to other sections of the site.
Product Pages: Browse individual product details and add items to the cart.
Cart: View and manage items in your cart.
Checkout: Complete the purchase process.
Testing
To run tests, ensure you have the necessary testing dependencies installed and use:

bash
pytest
