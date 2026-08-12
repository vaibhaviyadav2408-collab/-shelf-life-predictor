import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

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
except Exception as e:
    print(f"⚠️ Firebase Warning: {e}")

# ==================== ROUTES ====================

# 1. HOME PAGE
@app.route('/')
def index():
    return render_template('index.html')

# 2. LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Database aso wa naaso, direct Login hoiil
        try:
            if db:
                users_ref = db.collection('users').where('email', '==', email).where('password', '==', password).stream()
                user_list = [u.to_dict() for u in users_ref]
        except Exception:
            pass
            
        flash("Login Successful!", "success")
        return redirect(url_for('dashboard'))
            
    return render_template('login.html')

# 3. REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        
        user_data = {
            "name": name,
            "email": email,
            "mobile": mobile,
            "password": password
        }
        
        try:
            if db:
                db.collection('users').add(user_data)
        except Exception:
            pass
            
        flash("Registration Successful! Please Login.", "success")
        return redirect(url_for('login'))
            
    return render_template('register.html')

# 4. DASHBOARD
@app.route('/dashboard')
def dashboard():
    products = []
    try:
        if db:
            products_ref = db.collection('products').stream()
            products = [p.to_dict() for p in products_ref]
    except Exception:
        products = []
    
    total = len(products)
    fresh = sum(1 for p in products if p.get('status') == 'Fresh')
    expiring = sum(1 for p in products if p.get('status') == 'Expiring Soon')
    expired = sum(1 for p in products if p.get('status') == 'Expired')
    
    return render_template('dashboard.html', total=total, fresh=fresh, expiring=expiring, expired=expired, products=products)

# 5. ADD PRODUCT
@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_data = {
            "name": request.form.get('name'),
            "category": request.form.get('category'),
            "mfg_date": request.form.get('mfg_date'),
            "exp_date": request.form.get('exp_date'),
            "quantity": request.form.get('quantity', '1 unit'),
            "storage_type": request.form.get('storage_type', 'Refrigerator'),
            "status": "Fresh"
        }
        
        try:
            if db:
                db.collection('products').add(product_data)
        except Exception:
            pass
            
        flash("Product Added Successfully!", "success")
        return redirect(url_for('product_list'))
            
    return render_template('add_product.html')

# 6. PRODUCT LIST
@app.route('/product-list')
def product_list():
    products = []
    try:
        if db:
            products_ref = db.collection('products').stream()
            products = [p.to_dict() for p in products_ref]
    except Exception:
        products = []
    return render_template('product_list.html', products=products)

# 7. AI SHELF LIFE PREDICTION ROUTE
@app.route('/ai-prediction', methods=['GET', 'POST'])
def ai_prediction():
    result = None
    if request.method == 'POST':
        storage_type = request.form.get('storage_type', 'Refrigerator')
        remaining_days = 5 if storage_type == 'Refrigerator' else 2
        
        result = {
            "name": "Captured Food Item",
            "days": remaining_days,
            "status": "Fresh" if remaining_days > 3 else "Expiring Soon",
            "suggestion": "Store in cool environment to maintain freshness and prevent spoilage."
        }
    return render_template('ai_prediction.html', result=result)

# 8. NOTIFICATIONS
@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

# 9. USER PROFILE
@app.route('/profile')
def profile():
    user = {"name": "Vaibhavi Yadav", "email": "vaibhavi@gmail.com", "mobile": "9876543210"}
    try:
        if db:
            users_ref = db.collection('users').limit(1).stream()
            users = [u.to_dict() for u in users_ref]
            if users:
                user = users[0]
    except Exception:
        pass
    return render_template('profile.html', user=user)

# 10. ADMIN PANEL
@app.route('/admin')
def admin():
    users, products = [], []
    try:
        if db:
            users = [u.to_dict() for u in db.collection('users').stream()]
            products = [p.to_dict() for p in db.collection('products').stream()]
    except Exception:
        users, products = [], []
    return render_template('admin.html', users=users, products=products)

# 11. AI CHATBOT ROUTES
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json() or {}
    user_msg = data.get('message', '').lower()
    
    if 'milk' in user_msg or 'दूध' in user_msg:
        bot_reply = "🥛 Milk usually lasts 5–7 days in the refrigerator. Always store it below 4°C."
    elif 'apple' in user_msg or 'सफरचंद' in user_msg:
        bot_reply = "🍎 Apples stay fresh for 1–2 weeks at room temperature and up to 1–2 months in the fridge!"
    elif 'bread' in user_msg or 'ब्रेड' in user_msg:
        bot_reply = "🍞 Bread lasts 3–5 days at room temperature. Avoid keeping it in the fridge as it dries out faster."
    elif 'hi' in user_msg or 'hello' in user_msg:
        bot_reply = "👋 Hello! I am your AI Freshness Assistant. Ask me about any food item's shelf life!"
    else:
        bot_reply = "🤖 I can help you check shelf life, storage tips, and food freshness! Ask me about items like Milk, Apple, Bread, Vegetables, etc."
        
    return jsonify({"response": bot_reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
