from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
import os
from datetime import datetime, timezone

# Flask app setup
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

# SQLAlchemy and Flask-Migrate configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///register.database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

database = SQLAlchemy(app)
migrate = Migrate(app, database)

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(50), unique=True, nullable=False)
    email = database.Column(database.String(50), unique=True, nullable=False)
    password = database.Column(database.String(255), nullable=False)  # Use a hash for passwords
    profile_photo = database.Column(database.String(100), nullable=True)
    date_of_birth = database.Column(database.String(10), nullable=True)
    additional_details = database.Column(database.String(255), nullable=True)

class Order(database.Model):
    __tablename__ = 'orders'
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    product_id = database.Column(database.Integer, nullable=False)
    quantity = database.Column(database.Integer, nullable=False)
    total_price = database.Column(database.Float, nullable=False)
    order_date = database.Column(database.DateTime, default=datetime.utcnow)
    status = database.Column(database.String(50), nullable=False, default='Pending')
    payment_method = database.Column(database.String(50), nullable=False)
    payment_status = database.Column(database.String(50), nullable=False, default='Unpaid')

class About(database.Model):
    __tablename__ = 'aboutus'
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False)
    description = database.Column(database.Text, nullable=False)
    image_path = database.Column(database.String(200), nullable=True)

class Product(database.Model):
    __tablename__ = 'products'
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), nullable=False)
    price = database.Column(database.Float, nullable=False)
    image = database.Column(database.String(200), nullable=True)

class Sponsorship(database.Model):
    __tablename__ = 'sponsorships'
    id = database.Column(database.Integer, primary_key=True)
    sponsor_name = database.Column(database.String(100), nullable=False)
    product = database.Column(database.String(50), nullable=False)
    recipient = database.Column(database.String(100), nullable=False)
    message = database.Column(database.Text, nullable=True)
    date_submitted = database.Column(database.DateTime, default=datetime.utcnow)

class Review(database.Model):
    __tablename__ = 'reviews'
    id = database.Column(database.Integer, primary_key=True)
    product_id = database.Column(database.Integer, database.ForeignKey('products.id'), nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    comment = database.Column(database.Text, nullable=False)
    rating = database.Column(database.Integer, nullable=False)
    created_at = database.Column(database.DateTime, default=datetime.utcnow)
    
    product = database.relationship('Product', back_populates='reviews')
    user = database.relationship('User', back_populates='reviews')

# Add reverse relationships to User and Product models
User.reviews = database.relationship('Review', back_populates='user')
Product.reviews = database.relationship('Review', back_populates='product')


def populate_about_table():
    if not About.query.first():
        new_entry = About(
            title="Know Us",
            description="Lorem ipsum dolor sit amet, consectetur adipisicing elit.",
            image_path="images/lap.png"
        )
        database.session.add(new_entry)
        database.session.commit()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

with app.app_context():
    database.create_all()
    populate_about_table()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = []

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        men_products = [
            {'id': 1, 'name': 'Cotton Trending Shirt', 'price': '11.00', 'image': 'images/srt1.webp', 'rating': 4},
            {'id': 2, 'name': 'Cotton Trending Shirt 2', 'price': '15.00', 'image': 'images/srt2.webp', 'rating': 4},
            {'id': 3, 'name': 'Cotton Trending Shirt 3', 'price': '16.00', 'image': 'images/srt6.webp', 'rating': 4},
            # Add more men products as needed
        ]
        women_products = [
            {'id': 5, 'name': 'Trending Girl Top', 'price': '19.00', 'image': 'images/wn4.webp', 'rating': 4},
            {'id': 6, 'name': 'Trending Girl Top 2', 'price': '20.00', 'image': 'images/wn5.webp', 'rating': 4},
            {'id': 7, 'name': 'Trending Girl Top 3', 'price': '22.00', 'image': 'images/wn6.webp', 'rating': 4},
            # Add more women products as needed
        ]
        return render_template('index.html', men_products=men_products, women_products=women_products)
    return redirect(url_for('login'))


@app.route('/shops')
def shops():
    mens_products = [
        {'id': 1, 'name': 'Cotton Trending Shirt', 'price': '11.00', 'image': 'images/srt1.webp', 'rating': 4},
        {'id': 2, 'name': 'Cotton Trending Shirt 2', 'price': '15.00', 'image': 'images/srt2.webp', 'rating': 4},
        {'id': 3, 'name': 'Cotton Trending Shirt 3', 'price': '16.00', 'image': 'images/srt6.webp', 'rating': 4},
        # Add more men products as needed
    ]
    womens_products = [
        {'id': 5, 'name': 'Trending Girl Top', 'price': '19.00', 'image': 'images/wn4.webp', 'rating': 4},
        {'id': 6, 'name': 'Trending Girl Top 2', 'price': '20.00', 'image': 'images/wn5.webp', 'rating': 4},
        {'id': 7, 'name': 'Trending Girl Top 3', 'price': '22.00', 'image': 'images/wn6.webp', 'rating': 4},
        # Add more women products as needed
    ]
    return render_template('shops.html', mens_products=mens_products, womens_products=womens_products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        date_of_birth = request.form['date_of_birth']
        additional_details = request.form['additional_details']
        profile_photo = None
        if 'profile_photo' in request.files:
            file = request.files['profile_photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_photo = filename
        new_user = User(username=username, email=email, password=password,
                        date_of_birth=date_of_birth, additional_details=additional_details,
                        profile_photo=profile_photo)
        database.session.add(new_user)
        database.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    profile_photo = current_user.profile_photo or 'profile.png'
    return render_template('profile.html', user=current_user, profile_photo=profile_photo)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.username = request.form['username']
        current_user.email = request.form['email']
        current_user.date_of_birth = request.form['date_of_birth']
        current_user.additional_details = request.form['additional_details']
        if 'profile_photo' in request.files:
            file = request.files['profile_photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                current_user.profile_photo = filename
        database.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('edit_profile.html', user=current_user)

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item['quantity'] * item['price'] for item in cart)
    return render_template('cart.html', cart_items=cart, total=total)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get(product_id)  # Simplified query
    
    if product:
        cart = session.get('cart', [])
        product_in_cart = False
        
        for item in cart:
            if item['id'] == product_id:
                item['quantity'] += 1
                product_in_cart = True
                break
        
        if not product_in_cart:
            cart.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': 1,
                'image_path': product.image
            })
        
        session['cart'] = cart
        flash('Product added to cart!', 'success')
    else:
        flash('Product not found.', 'error')
    
    print(f"Cart after update: {session.get('cart')}")  # Debug statement
    return redirect(url_for('cart'))




@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [product for product in cart if product['id'] != product_id]
    session['cart'] = cart
    flash('Product removed from cart!', 'success')
    return redirect(url_for('cart'))

@app.route('/payment', methods=['POST'])
def payment():
    # Payment logic here
    if request.method == 'POST':
        flash('Payment successful! Thank you for your purchase.', 'success')
        session.pop('cart', None)  # Clear the cart after successful payment
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        flash('Payment successful! Thank you for your purchase.', 'success')
        session.pop('cart', None)  # Clear the cart after successful payment
        return redirect(url_for('index'))
    return render_template('checkout.html')

@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_detail(product_id):
    product = database.session.query(Product).filter_by(id=product_id).first()
    reviews = database.session.query(Review).filter_by(product_id=product_id).all()
    return render_template('product_detail.html', product=product, reviews=reviews)

@app.route('/submit_review/<int:product_id>', methods=['POST'])
def submit_review(product_id):
    comment = request.form['comment']
    rating = request.form['rating']
    user_id = current_user.id
    
    new_review = Review(
        product_id=product_id,
        user_id=user_id,
        comment=comment,
        rating=rating
    )
    database.session.add(new_review)
    database.session.commit()
    flash('Review submitted successfully!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/subscribe-newsletter', methods=['POST'])
def subscribe_newsletter():
    
    return redirect(url_for('blog'))  


@app.route('/about')
def about():
    about_data = {
        'title': 'About Us',
        'description': 'We are a company dedicated to providing quality products.',
        'partner_companies': ['Company A', 'Company B', 'Company C'],
        'sponsor_initiatives': ['Initiative 1', 'Initiative 2'],
        'image_path': 'images/lap.png'
    }
    return render_template('about.html', about_data=about_data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/orders', methods=['GET'])
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)


@app.route('/sponsor', methods=['GET', 'POST'])
def sponsor():
    if request.method == 'POST':
        sponsor_name = request.form['sponsor_name']
        product = request.form['product']
        recipient = request.form['recipient']
        message = request.form.get('message', '')

        new_sponsorship = Sponsorship(
            sponsor_name=sponsor_name,
            product=product,
            recipient=recipient,
            message=message
        )

        database.session.add(new_sponsorship)
        database.session.commit()

        return redirect(url_for('sponsor_confirmation'))

    return render_template('sponsor.html')

@app.route('/sponsor_confirmation')
def sponsor_confirmation():
    return "<h1>Thank you for your sponsorship!</h1><p>Your generosity makes a difference.</p>"
@app.route('/show')
def show():
    return render_template('product_details')
if __name__ == '__main__':
    app.run(debug=True)
