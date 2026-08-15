import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

# Template folder '.' केल्यामुळे रूट डिरेक्टरीतील सर्व HTML फाईल्स योग्य रीतीने लोड होतील
app = Flask(__name__, template_folder='templates')
app.secret_key = "aishelflifesupersecretkey"

# ==================== FIREBASE SETUP (SAFE FOR LOCALHOST & DEPLOYMENT) ====================
db = None
try:
    if os.path.exists('serviceAccountKey.json') and not firebase_admin._apps:
        cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase Connected Successfully!")
    else:
        print("⚠️ Warning: serviceAccountKey.json missing! Running with dynamic memory database.")
except Exception as e:
    print(f"⚠️ Firebase Connection Error: {e}")

# मॅन्युअल डेटा स्टोअर करण्यासाठी तात्पुरती (In-Memory) लिस्ट
products_db = [
    {
        'name': 'Fresh Organic Milk',
        'category': 'Dairy & Eggs',
        'quantity': '1 Liter',
        'purchase_date': '2026-08-10',
        'expiry_date': '2026-08-17',
        'status': 'Fresh'
    },
    {
        'name': 'Whole Wheat Bread',
        'category': 'Bakery',
        'quantity': '1 Packet',
        'purchase_date': '2026-08-12',
        'expiry_date': '2026-08-16',
        'status': 'Expiring Soon'
    }
]

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
    total = len(products_db)
    fresh = sum(1 for item in products_db if item.get('status') == 'Fresh')
    expiring = sum(1 for item in products_db if item.get('status') == 'Expiring Soon')
    expired = sum(1 for item in products_db if item.get('status') == 'Expired')
    
    return render_template('dashboard.html', total=total, fresh=fresh, expiring=expiring, expired=expired)

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # फॉर्ममधून आलेला डेटा गोळा करणे
        name = request.form.get('product_name')
        category = request.form.get('category')
        quantity = request.form.get('quantity')
        purchase_date = request.form.get('purchase_date')
        expiry_date = request.form.get('expiry_date')

        # प्रॉडक्ट लिस्टमध्ये ॲड करणे
        new_item = {
            'name': name,
            'category': category,
            'quantity': quantity,
            'purchase_date': purchase_date,
            'expiry_date': expiry_date,
            'status': 'Fresh'
        }
        products_db.append(new_item)

        flash("Product Added Successfully!", "success")
        return redirect(url_for('product_list'))
    
    return render_template('add_product.html')

@app.route('/product-list')
def product_list():
    return render_template('product_list.html', products=products_db)

@app.route('/ai-prediction', methods=['GET', 'POST'])
def ai_prediction():
    result = None
    if request.method == 'POST':
        item_name = request.form.get('item_name', 'Sample Food Item')
        temp = request.form.get('temperature', 4)
        pkg = request.form.get('packaging', 'Sealed Container')
        
        # साधे AI कॅल्क्युलेशन लॉजिक
        days = 5
        if int(temp) > 10:
            days = 2
        elif pkg == 'Refrigerated Vacuum Bag':
            days = 10

        result = {
            "name": item_name,
            "days": days,
            "status": "Fresh",
            "suggestion": f"Stored at {temp}°C in {pkg}. Recommended to use within {days} days."
        }
    return render_template('ai_prediction.html', result=result)

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = {
        "name": "Vaibhavi Yadav",
        "email": "vaibhavi@kbppolytechnic.ac.in",
        "college": "KBP Polytechnic, Satara",
        "project": "2026 Inplant Training Project"
    }
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    flash("Logged out successfully!", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
