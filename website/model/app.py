from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your secret key.'

accounts = []

def check_password(password):
    if len(password) < 6 or len(password) > 12:
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in '#$@%' for char in password):
        return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_password(password):
            account_number = len(accounts) + 1
            accounts.append({'account_number': account_number, 'username': username, 'password': password, 'balance': 100.0})
            return redirect(url_for('index'))
        else:
            return "Invalid password! Password must contain at least 1 lowercase letter, 1 uppercase letter, 1 digit, 1 special character, and be between 6 and 12 characters long."
    return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for account in accounts:
            if account['username'] == username and account['password'] == password:
                session['account'] = account
                return redirect(url_for('dashboard'))
        return "Invalid username or password!"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'account' in session:
        account = session['account']
        print(account["balance"])
        return render_template('dashboard.html', account=account)
    return redirect(url_for('login'))

@app.route('/deposit', methods=['POST'])
def deposit():
    if 'account' in session:
        account = session.get('account')
        amount = float(request.form['amount'])
        account['balance'] += amount
        session['account'] = account
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'account' in session:
        account = session.get('account')
        amount = float(request.form['amount_withdraw'])
        if account['balance'] >= amount:
            account['balance'] -= amount
            session['account'] = account
            return redirect(url_for('dashboard'))
        else:
            return "Insufficient balance!"
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)