import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

# standard templates folder settings
app = Flask(__name__)
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

# ==================== AI CHATBOT API ROUTE ====================
@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message", "").lower()
    
    if "milk" in user_msg or "doodh" in user_msg:
        response = "🥛 Fresh milk stays good for 3-5 days in the fridge. Boil it to extend shelf life!"
    elif "bread" in user_msg:
        response = "🍞 Bread lasts about 3-5 days at room temperature and up to 2 weeks in the fridge."
    elif "apple" in user_msg or "fruit" in user_msg:
        response = "🍎 Fruits like apples stay fresh for 1-2 weeks at room temp and a month in the fridge."
    elif "hi" in user_msg or "hello" in user_msg or "hey" in user_msg:
        response = "Hello! 👋 I am your AI Shelf Life Assistant. Ask me about storing food items!"
    else:
        response = f"🤖 Storage tip for '{user_msg}': Keep in a cool, dry environment away from direct sunlight."
        
    return jsonify({"reply": response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
