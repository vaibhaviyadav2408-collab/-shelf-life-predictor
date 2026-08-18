import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

# ==================== FLASK APP SETUP ====================
# Absolute path वापरून templates फोल्डर नक्की कुठे आहे ते शोधणे
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = "aishelflifesupersecretkey"

# ==================== FIREBASE SETUP ====================
db = None
try:
    if os.path.exists('serviceAccountKey.json') and not firebase_admin._apps:
        cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase Connected Successfully!")
    else:
        print("⚠️ Warning: serviceAccountKey.json missing! Running in local demo mode.")
except Exception as e:
    print(f"⚠️ Firebase Connection Error: {e}")

# ==================== ALL ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if db:
            try:
                users_ref = db.collection('users').where('email', '==', email).limit(1).stream()
                user_data = [u.to_dict() for u in users_ref]
                if user_data:
                    flash("Login Successful!", "success")
                    return redirect(url_for('dashboard'))
                else:
                    flash("User not found. Please register.", "danger")
                    return redirect(url_for('login'))
            except Exception as e:
                flash(f"Login error: {str(e)}", "danger")
        
        flash("Login Successful!", "success")
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        password = request.form.get('password')

        if db:
            try:
                db.collection('users').add({
                    'name': name,
                    'email': email,
                    'mobile': mobile,
                    'password': password
                })
                flash("Registration Successful! Please log in.", "success")
                return redirect(url_for('login'))
            except Exception as e:
                flash(f"Error saving user: {str(e)}", "danger")

        flash("Registration Successful!", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    total_count = 24
    fresh_count = 16
    expiring_count = 5
    expired_count = 3

    if db:
        try:
            products_ref = db.collection('products').stream()
            products = [p.to_dict() for p in products_ref]
            total_count = len(products)
            fresh_count = sum(1 for p in products if p.get('status', '').lower() == 'fresh')
            expiring_count = sum(1 for p in products if p.get('status', '').lower() == 'expiring')
            expired_count = sum(1 for p in products if p.get('status', '').lower() == 'expired')
        except Exception as e:
            print(f"Firestore query error: {e}")

    return render_template(
        'dashboard.html',
        total=total_count,
        fresh=fresh_count,
        expiring=expiring_count,
        expired=expired_count
    )

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        category = request.form.get('category')
        expiry_date = request.form.get('expiry_date')
        quantity = request.form.get('quantity')

        if db:
            try:
                db.collection('products').add({
                    'name': product_name,
                    'category': category,
                    'exp_date': expiry_date,
                    'quantity': quantity,
                    'status': 'Fresh'
                })
            except Exception as e:
                print(f"Error adding product: {e}")

        flash("Product Added Successfully!", "success")
        return redirect(url_for('product_list'))
    return render_template('add_product.html')

@app.route('/product-list')
def product_list():
    products = []
    if db:
        try:
            products_ref = db.collection('products').stream()
            products = [p.to_dict() for p in products_ref]
        except Exception as e:
            print(f"Error fetching products: {e}")
            
    return render_template('product_list.html', products=products)

@app.route('/ai-prediction', methods=['GET', 'POST'])
def ai_prediction():
    result = None
    if request.method == 'POST':
        item_name = request.form.get('item_name', 'Sample Food Item')
        storage = request.form.get('storage_condition', 'Refrigerated')
        
        result = {
            "name": item_name,
            "days": 5,
            "status": "Fresh",
            "suggestion": f"Stored via {storage}. Keep temperature below 4°C for maximum freshness."
        }
    return render_template('ai_prediction.html', result=result)

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

@app.route('/profile')
def profile():
    user = {"name": "Vaibhavi Yadav", "email": "vaibhavi@gmail.com", "mobile": "9876543210"}
    return render_template('profile.html', user=user)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
