from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from sqlalchemy.orm import joinedload
import os
from datetime import datetime

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///register.database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)



database = SQLAlchemy(app)
migrate = Migrate(app, database)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(50), unique=True, nullable=False)
    email = database.Column(database.String(50), unique=True, nullable=False)
    password = database.Column(database.String(255), nullable=False) 
    profile_photo = database.Column(database.String(100), nullable=True, default='profile.png')
    date_of_birth = database.Column(database.String(10), nullable=True)
    additional_details = database.Column(database.String(255), nullable=True)
    reviews = database.relationship('Review', back_populates='user')
    orders = database.relationship('Order', backref='user', lazy=True)

class Product(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), nullable=False)
    price = database.Column(database.Float, nullable=False)
    image = database.Column(database.String(100), nullable=False)
    rating = database.Column(database.Integer, default=0)
    category = database.Column(database.String(50), nullable=False) 
    reviews = database.relationship('Review', back_populates='product')
    cart_items = database.relationship('Cart_item', back_populates='product')

class Review(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    product_id = database.Column(database.Integer, database.ForeignKey('product.id'), nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    comment = database.Column(database.Text, nullable=False)
    rating = database.Column(database.Integer, nullable=False)
    created_at = database.Column(database.DateTime, default=datetime.utcnow)
    product = database.relationship('Product', back_populates='reviews')
    user = database.relationship('User', back_populates='reviews')

class Cart_item(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    product_id = database.Column(database.Integer, database.ForeignKey('product.id'), nullable=False)
    image = database.Column(database.String(100), nullable=False)
    quantity = database.Column(database.Integer, nullable=False, default=1)
    product = database.relationship('Product', back_populates='cart_items')

class Order(database.Model):
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
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False)
    description = database.Column(database.Text, nullable=False)
    image_path = database.Column(database.String(200), nullable=True)

class Sponsorship(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    sponsor_name = database.Column(database.String(100), nullable=False)
    product = database.Column(database.String(50), nullable=False)
    recipient = database.Column(database.String(100), nullable=False)
    message = database.Column(database.Text, nullable=True)
    date_submitted = database.Column(database.DateTime, default=datetime.utcnow)

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

# List of sample products
products = [
    {'id':1, 'name': 'Cotton Trending Shirt', 'price': 11.00, 'image': 'images/srt1.webp', 'rating': 4, 'category': 'Men'},
    {'id':2, 'name': 'Cotton Trending Shirt 2', 'price': 15.00, 'image': 'images/srt2.webp', 'rating': 4, 'category': 'Men'},
    {'id':3, 'name': 'Cotton Trending Shirt 9', 'price': 16.00, 'image': 'images/srt6.webp', 'rating': 4, 'category': 'Men'},
    {'id':4, 'name': 'Trending Girl Top6', 'price': 19.00, 'image': 'images/wn4.webp', 'rating': 4, 'category': 'Women'},
    {'id':5, 'name': 'Trending Girl Top 7', 'price': 20.00, 'image': 'images/wn5.webp', 'rating': 4, 'category': 'Women'},
    {'id':6, 'name': 'Trending Girl Top 8', 'price': 22.00, 'image': 'images/wn6.webp', 'rating': 4, 'category': 'Women'},
]

def seed_data():

 for product_data in products:
        existing_product = Product.query.filter_by(id=product_data['id']).first()
        if not existing_product:
            product = Product(**product_data)
            database.session.add(product)
        database.session.commit()

with app.app_context():
    database.create_all()
    populate_about_table()
    seed_data()

@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = []

# Routes
@app.route('/')
def index():
    mens_products = [
        {'id': 1, 'name': 'Cotton Trending Shirt ', 'price': '11.00', 'image': 'images/srt1.webp', 'rating': 4},
        {'id': 2, 'name': 'Cotton Trending Shirt 2', 'price': '15.00', 'image': 'images/srt2.webp', 'rating': 4},
        {'id': 3, 'name': 'Cotton Trending Shirt 3', 'price': '16.00', 'image': 'images/srt6.webp', 'rating': 4},
    ]
    womens_products = [
        {'id': 4, 'name': 'Trending Girl Top', 'price': '19.00', 'image': 'images/wn4.webp', 'rating': 4},
        {'id': 5, 'name': 'Trending Girl Top 2', 'price': '20.00', 'image': 'images/wn5.webp', 'rating': 4},
        {'id': 6, 'name': 'Trending Girl Top 3', 'price': '22.00', 'image': 'images/wn6.webp', 'rating': 4},
    ]
    return render_template('index.html', products=products, mens_products=mens_products, womens_products=womens_products)

@app.route('/shops')
def shops():
    men_products = [
        {'id': 7, 'name': 'Cotton Trending Shirt ', 'price': '11.00', 'image': 'images/srt1.webp', 'rating': 4},
        {'id': 8, 'name': 'Cotton Trending Shirt 2', 'price': '15.00', 'image': 'images/srt2.webp', 'rating': 4},
        {'id': 9, 'name': 'Cotton Trending Shirt 3', 'price': '16.00', 'image': 'images/srt6.webp', 'rating': 4},
    ]
    women_products = [
        {'id': 10, 'name': 'Trending Girl Top', 'price': '19.00', 'image': 'images/wn4.webp', 'rating': 4},
        {'id': 11, 'name': 'Trending Girl Top 2', 'price': '20.00', 'image': 'images/wn5.webp', 'rating': 4},
        {'id': 12, 'name': 'Trending Girl Top 3', 'price': '22.00', 'image': 'images/wn6.webp', 'rating': 4},
    ]
    return render_template('shops.html', men_products=men_products, women_products=women_products)

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

@app.route('/cart', methods=['GET'])
def cart():
    cart_items = Cart_item.query.options(joinedload(Cart_item.product)).all()
    for item in cart_items:
        if item.product:
            print(f"Cart Item ID: {item.id}, Product ID: {item.product_id}, Product Name: {item.product.name}, Quantity: {item.quantity}")
        else:
            print(f"Cart Item ID: {item.id}, Product ID: {item.product_id} - Product not found!")

    return render_template('cart.html', cart_items=cart_items)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
    try:
        product_id = int(product_id)
    except ValueError:
        return jsonify({'error': 'Invalid product ID'}), 400
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    cart_item = Cart_item.query.filter_by(product_id=product_id).first()
    
    if cart_item:
        return redirect(url_for('cart'))
    else:
        cart_item = Cart_item(product_id=product_id, quantity=1, image=product.image)
        database.session.add(cart_item)
    try:
        database.session.commit()
    except Exception as e:
        database.session.rollback()
        print(f"Error committing to the database: {e}")
        return jsonify({'error': 'An error occurred while adding to the cart'}), 500

    return redirect(url_for('cart'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')
    cart_item = Cart_item.query.filter_by(product_id=product_id).first()
    if cart_item:
        database.session.delete(cart_item)
        database.session.commit()
    return redirect(url_for('cart'))

@app.route('/wishlist')
def wishlist():
    wishlist = session.get('wishlist', [])
    return render_template('wishlist.html', wishlist=wishlist)

@app.route('/add_to_wishlist/<int:product_id>')
def add_to_wishlist(product_id):
    wishlist = session.get('wishlist', [])
    if not any(item['id'] == product_id for item in wishlist):
        product = next((p for p in product if p['id'] == product_id), None)
        if product:
            wishlist.append(product)
            session['wishlist'] = wishlist
            flash('Item added to wishlist!', 'success')
        else:
            flash('Product not found!', 'danger')
    else:
        flash('Item is already in the wishlist!', 'warning')

    return redirect(url_for('wishlist'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Get form data
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip')
        cardname = request.form.get('cardname')
        cardnumber = request.form.get('cardnumber')
        expdate = request.form.get('expdate')
        cvv = request.form.get('cvv')
        
        # Store relevant information in session
        session['fullname'] = fullname
        session['email'] = email
        session['address'] = address
        session['city'] = city
        session['state'] = state
        session['zip'] = zip_code
        
        # Optional: Store payment information in session (if needed)
        # session['cardname'] = cardname
        # session['cardnumber'] = cardnumber
        # session['expdate'] = expdate
        # session['cvv'] = cvv
        # return render_template('confirmation.html')
        # Perform your payment processing here
        # Set a flag or check whether the payment was successful

    # Handle GET request: Render the checkout page
    return render_template('checkout.html')

@app.route('/confirmation')
def confirmation():
    fullname = session.get('fullname')
    email = session.get('email')
    address = session.get('address')
    city = session.get('city')
    state = session.get('state')
    zip_code = session.get('zip')
    cardname = session.get('cardname')
    cardnumber = session.get('cardnumber')
    expdate = session.get('expdate')
    cvv = session.get('cvv')
    return render_template('confirmation.html',
                           fullname=fullname,
                           email=email,
                           address=address,
                           city=city,
                           state=state,
                           zip_code=zip_code,
                           cardname=cardname,
                           cardnumber=cardnumber,
                           expdate=expdate,
                           cvv=cvv)

@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).all()
    return render_template('product_detail.html', product=product, reviews=reviews)

@app.route('/submit_review/<int:product_id>', methods=['POST'])
@login_required
def submit_review(product_id):
    comment = request.form['comment']
    rating = int(request.form['rating'])
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
    flash('Subscribed to newsletter!', 'success')
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
