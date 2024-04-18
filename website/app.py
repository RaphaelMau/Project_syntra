from itertools import product
from unicodedata import category
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import current_user
from model.insert import insert_into
from model.getData import getData

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

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        if check_password(password):
            account_number = len(accounts) + 1
            accounts.append({'account_number': account_number, 'userid': userid, 'password': password, 'balance': 100.0})
            return redirect(url_for('index'))
        else:
            return "Invalid password! Password must contain at least 1 lowercase letter, 1 uppercase letter, 1 digit, 1 special character, and be between 6 and 12 characters long."
    return render_template('/create_account')

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
    
@app.route('/render')
def render_data():
    rendered_data= getData("project_db", request)
    return render_template('render_data.html', data = rendered_data)

@app.route('/insert', methods=['POST'])
def insert():
    iduser = request.form["iduser"]
    name = request.form['name']
    first_name = request.form['first_name']
    phone_number = request.form['phone number']
    email = request.form['email']
    data_to_insert = (iduser, name, first_name, phone_number)
    
    insert_into("project_db", "users", data_to_insert)
    
    return 'Data inserted successfully'

@app.route('/')
def index():
    products = ["product1", "product2", "product3"]
    if 'cart' not in session:
        session['cart'] = []
    return render_template('index.html', products=products, amount_products=len(session['cart']))


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product = request.form['product']
    if 'cart' not in session:
        session['cart'] = []
    list_products = session['cart']
    list_products.append(product)
    session['cart'] = list_products
    return redirect(url_for('index'))


@app.route('/view_cart')
def view_cart():
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)

@app.route('/edit_product', methods=['POST'])
def is_admin():
    return current_user.is_authenticated and current_user.is_admin

@app.route('/edit_product/<int:product_id>', methods=['GET'])
def edit_product(product_id):
    if not is_admin():
        return "Unauthorized", 403
    product = product.query.get_or_404(product_id)
    return render_template('edit_product.html', product=product)

@app.route('/update_product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    if not is_admin():
        return "Unauthorized", 403
    product = product.query.get_or_404(product_id)
    return redirect(url_for('product_details', product_id=product.id))

@app.route('/product/<int:product_id>', methods=['GET'])
def product_details(product_id):
    product = product.query.get_or_404(product_id)
    return render_template('product_details.html', product=product)



class Users:
    def __init__(self, name, first_name, phone_number, email,password, salt, admin):
        self.name = name
        self.first_name = first_name
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.salt = salt
        self.admin = admin

class Address(Users):
    def __init__(self,address_id, street, post_code, country):
        self.address_id = address_id
        self.street = street
        self.post_code = post_code
        self.country = country

class Order(Users):
    def __init__(self,id, userid, computer_id, artikel_id):
        self.id = id
        self.userid = userid
        self.computer_id = computer_id
        self.artikel_id = artikel_id

class Computer(Users):
    def __init__(self, price, amount):
        self.price = price
        self.amount = amount

class Articles(Users):
    def __init__(self, price, amount):
        self.price = price
        self.amount = amount



class Category_articles(Computer):
    def __init__(self, hard_drive, motherboard, RAM, CPU, graphic_card, monitor, case):
        self.hard_drive = hard_drive
        self.motherboard = motherboard
        self.RAM = RAM
        self.CPU = CPU
        self.graphic_card = graphic_card
        self.monitor = monitor
        self.case = case

class Case(Category_articles):
    def __init__(self, size, price, weight , glass):
        self.size = size
        self.price = price
        self.weight = weight
        self.glass = glass

class Motherboard(Category_articles):
    def __init__(self, name, USB_ports, Ram_slots, SSD_slots, HDMI_slots, price, garantie, size):
        self.name = name
        self.USB_ports = USB_ports
        self.RAM_slots = Ram_slots
        self.SSD_slots = SSD_slots
        self.HDMI_slots = HDMI_slots
        self.price = price
        self.garantie = garantie
        self.size = size

class Graphic_card(Category_articles):
    def __init__(self, name, price,brand , type, speed, garantie, size):
        self.name = name
        self.price = price
        self.brand = brand
        self.type = type
        self.speed = speed
        self.garantie = garantie
        self.size = size

class Ram_sticks(Category_articles):
    def __init__(self, name, price, brand, amount_sticks, type_DDR, garantie, size):
        self.name = name
        self.price = price
        self.brand = brand
        self.amount_sticks = amount_sticks
        self.type_DDR = type_DDR
        self.garantie = garantie
        self.size = size
class CPU(Category_articles):
    def __init__(self, name, price, brand, amount, clockspeed, chipset, amount_cores, garantie, size):
        self.name = name
        self.price = price
        self.brand = brand
        self.amount = amount
        self.clockspeed = clockspeed
        self. chipset = chipset
        self.amount_cores = amount_cores
        self.garantie = garantie
        self.size = size

class Hard_drive(Category_articles):
    def __init__(self, name, price, brand,  HDD_or_SSD, writing_pace, reading_pace, garantie, size):
        self.name = name
        self.price = price
        self.brand = brand
        self.HDD_orSSD = HDD_or_SSD
        self.writing_pace = writing_pace
        self.reading_pace = reading_pace
        self.garantie = garantie
        self.size = size

class Monitor(Category_articles):
    def __init__(self, name, price, brand, refresh_rate, resolution, response_time, weight, garantie, size):
        self.name = name
        self.price = price
        self.brand = brand
        self.refresh_rate = refresh_rate
        self.resolution = resolution
        self.response_time = response_time
        self.weight = weight
        self.garantie = garantie
        self.size = size

class Accessoires(Articles):
    def __init__(self, mouse_id, keyboard_id, mousepad_id, USB_id):
        self.mouse_id = mouse_id
        self.keyboard_id = keyboard_id
        self.mousepad_id = mousepad_id
        self.USB_id = USB_id


class keyboard(Accessoires):
    def __init__(self, brand, price, size, garantie):
        self.brand = brand
        self.price = price
        self.size = size
        self.garantie = garantie

class Mouse(Accessoires):
    def __init__(self, brand, price, side_buttons, garantie):
        self.brand = brand
        self.price = price
        self.side_buttons = side_buttons
        self.garantie = garantie

class Mousepad(Accessoires):
    def __init__(self, brand, price, size, garantie):
        self.brand = brand
        self.price = price
        self.size = size
        self.garantie = garantie

class USB_ports(Accessoires):
    def __init__(self, type, price, name):
        self.type = type    
        self.price = price
        self.name = name


if __name__ == '__main__':
    app.run(debug=True)