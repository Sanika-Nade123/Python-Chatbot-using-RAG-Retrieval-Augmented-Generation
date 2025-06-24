from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import db, User, ChatHistory, Admin  # Added Admin import
from werkzeug.security import generate_password_hash, check_password_hash
import re
from chat_utils import get_rag_response
from datetime import datetime  # Add this import for last_login timestamp
from pdf_utils import create_user_report_pdf, create_chat_history_pdf
from flask import send_file
import os
import uuid  # Add this import at the top

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Ratan123456Verma@localhost/chatbot_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Function to create default admin accounts
def create_default_admins():
    try:
        # Create first admin
        admin1 = User.query.filter_by(user_id='admin1').first()
        if not admin1:
            admin1 = User(
                user_id='admin1',
                name='Admin One',
                email='admin1@pysensei.com',
                phone='9999999999',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin1)
            db.session.commit()  # Commit user first
            
            admin1_profile = Admin(
                user_id='admin1',
                department='IT',
                role='Super Admin',
                access_level=2
            )
            db.session.add(admin1_profile)
            db.session.commit()  # Commit admin profile

        # Create second admin
        admin2 = User.query.filter_by(user_id='admin2').first()
        if not admin2:
            admin2 = User(
                user_id='admin2',
                name='Admin Two',
                email='admin2@pysensei.com',
                phone='8888888888',
                password=generate_password_hash('admin456'),
                is_admin=True
            )
            db.session.add(admin2)
            db.session.commit()  # Commit user first
            
            admin2_profile = Admin(
                user_id='admin2',
                department='IT',
                role='Administrator',
                access_level=1
            )
            db.session.add(admin2_profile)
            db.session.commit()  # Commit admin profile

    except Exception as e:
        print(f"Error creating admin accounts: {str(e)}")
        db.session.rollback()

@app.route('/')
def home():
    return redirect(url_for('login'))

# In the login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        role = request.form['role']
        
        user = User.query.filter_by(user_id=user_id, is_admin=(role == 'admin')).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            session['user_name'] = user.name
            
            if user.is_admin:
                # Update admin last login
                admin = Admin.query.filter_by(user_id=user.user_id).first()
                if admin:
                    admin.last_login = datetime.utcnow()
                    db.session.commit()
            
            return redirect(url_for('chat') if not user.is_admin else url_for('admin'))
        flash('Invalid user ID or password')
    return render_template('login.html')

# Update the register route to remove admin registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        user_id = request.form['user_id']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        if User.query.filter_by(user_id=user_id).first():
            flash('User ID already exists')
            return render_template('register.html')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email format')
            return render_template('register.html')
        
        if not re.match(r"^\d{10}$", phone):
            flash('Invalid phone number')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        new_user = User(
            user_id=user_id,
            name=name, 
            email=email, 
            phone=phone, 
            password=hashed_password,
            is_admin=False  # Always create regular users
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin.html', users=users)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chat')
def chat():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    return render_template('chat.html')

@app.route('/chat_history')
def chat_history():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    history = ChatHistory.query.filter_by(user_id=session['user_id']).order_by(ChatHistory.timestamp.desc()).all()
    return render_template('chat_history.html', history=history)

@app.route('/api/chat', methods=['POST'])
def process_chat():
    if not session.get('user_id'):
        return {'error': 'Unauthorized'}, 401
    
    message = request.json.get('message')
    response = get_rag_response(message)
    
    chat_history = ChatHistory(
        user_id=session['user_id'],
        message=message,
        response=response
    )
    db.session.add(chat_history)
    db.session.commit()
    
    return {'response': response}

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/download_users_report')
def download_users_report():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    users = User.query.filter_by(is_admin=False).all()
    pdf = create_user_report_pdf(users)
    
    # Create unique temp file name
    temp_path = f'temp_users_report_{uuid.uuid4()}.pdf'
    pdf.output(temp_path)
    
    return send_file(
        temp_path,
        as_attachment=True,
        download_name=f'users_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
        max_age=0
    )

@app.route('/download_user_chat/<int:user_id>')
def download_user_chat(user_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    user = User.query.get(user_id)
    if not user:
        flash('User not found')
        return redirect(url_for('admin'))
    
    chat_history = ChatHistory.query.filter_by(user_id=user_id).order_by(ChatHistory.timestamp.desc()).all()
    pdf = create_chat_history_pdf(chat_history, user.name)
    
    temp_path = f'temp_chat_history_{uuid.uuid4()}.pdf'
    pdf.output(temp_path)
    
    return send_file(
        temp_path,
        as_attachment=True,
        download_name=f'chat_history_{user.user_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
        max_age=0
    )

@app.route('/download_my_chat')
def download_my_chat():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    chat_history = ChatHistory.query.filter_by(user_id=session['user_id']).order_by(ChatHistory.timestamp.desc()).all()
    pdf = create_chat_history_pdf(chat_history, session['user_name'])
    
    temp_path = f'temp_my_chat_{uuid.uuid4()}.pdf'
    pdf.output(temp_path)
    
    return send_file(
        temp_path,
        as_attachment=True,
        download_name=f'my_chat_history_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
        max_age=0
    )

# Add cleanup route
@app.after_request
def cleanup_temp_files(response):
    for file in os.listdir():
        if file.startswith('temp_') and file.endswith('.pdf'):
            try:
                os.remove(file)
            except:
                pass
    return response

if __name__ == '__main__':
    with app.app_context():
        # Only create tables if they don't exist
        db.create_all()
        create_default_admins()  # Create default admin accounts
    app.run(debug=True)