import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

# Dynamic base directory and absolute path for templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = "aishelflifesupersecretkey"

# ==================== FIREBASE SETUP ====================
db = None
try:
    key_path = os.path.join(BASE_DIR, 'serviceAccountKey.json')
    if os.path.exists(key_path) and not firebase_admin._apps:
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase Connected Successfully!")
    else:
        print("⚠️ Warning: serviceAccountKey.json missing! Local demo mode running.")
except Exception as e:
    print(f"⚠️ Firebase Connection Error: {e}")

# ==================== ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        flash("Login Successful!", "success")
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        flash("Registration Successful!", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', total=24, fresh=16, expiring=5, expired=3)

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        flash("Product Added Successfully!", "success")
        return redirect(url_for('product_list'))
    return render_template('add_product.html')

@app.route('/product-list')
def product_list():
    return render_template('product_list.html', products=[])

@app.route('/ai-prediction', methods=['GET', 'POST'])
def ai_prediction():
    result = None
    if request.method == 'POST':
        result = {
            "name": "Sample Food Item",
            "days": 4,
            "status": "Fresh",
            "suggestion": "Keep refrigerated below 4°C."
        }
    return render_template('ai_prediction.html', result=result)

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

@app.route('/profile')
def profile():
    user = {"name": "User Name", "email": "user@gmail.com", "mobile": "9876543210"}
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
