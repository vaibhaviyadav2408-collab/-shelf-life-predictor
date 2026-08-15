import os
from flask import Flask, render_template, request, redirect, url_for, flash

# Flask app initialization with proper paths
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "aishelflifesupersecretkey"

# In-Memory Product List
products_db = []

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
        product_name = request.form.get('product_name')
        category = request.form.get('category')
        mfg_date = request.form.get('mfg_date')
        expiry_date = request.form.get('expiry_date')

        products_db.append({
            'name': product_name,
            'category': category,
            'mfg_date': mfg_date,
            'expiry_date': expiry_date,
            'status': 'Fresh'
        })
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
        result = {
            "name": "Sample Food Item",
            "days": 4,
            "status": "Fresh",
            "suggestion": "Keep refrigerated below 4°C."
        }
    return render_template('ai_prediction.html', result=result)

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

@app.route('/profile')
def profile():
    user = {"name": "Vaibhavi Yadav", "email": "vaibhavi@gmail.com", "mobile": "9876543210"}
    return render_template('profile.html', user=user)

@app.route('/admin')
def admin():
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
