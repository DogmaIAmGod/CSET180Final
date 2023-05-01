from flask import Flask, render_template, request, redirect
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

app = Flask(__name__)
conn_str = "mysql://root:jtdStudent2023@localhost/scammazon"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/')
def index():
    return redirect("/accounts/login", code=301)

@app.route('/accounts/login', methods=['GET'])
def get_accounts():
    return render_template('login_page.html')

@app.route('/accounts/login', methods=['POST'])
def post_get_accounts():
    auth = conn.execute(text("SELECT if(password = :password, 'Yes', 'No') FROM account WHERE username = :username OR email = :username"), request.form).one_or_none()
    maybe_user = request.form.get("username")
    if auth[0] == 'Yes':
        type = conn.execute(text(f"SELECT type FROM account where username = '{maybe_user}'")).all()
        type = type[0][0]
        if type == "vendor":
            cookie = redirect("/vendor", code=301)
            cookie.set_cookie('logged_in', maybe_user)
            return cookie
        elif type == "customer":
            cookie = redirect("/accounts/information", code=301)
            cookie.set_cookie('logged_in', maybe_user)
            return cookie
        else:
            cookie = redirect("/admin", code=301)
            cookie.set_cookie('logged_in', maybe_user)
            return cookie
    else:
        return render_template('login_page.html', error=None, success="Invalid Login")

@app.route('/accounts/register', methods=['GET'])
def create_account():
    conn.execute(text("SELECT * FROM account")).all()
    return render_template('register_page.html')

@app.route('/accounts/register', methods=['POST'])
def post_create_account():
    try:
        conn.execute(text("INSERT INTO account (`first_name`, `last_name`, `email`, `username`, `password`, `type`) values (:first_name, :last_name, :email, :username, :password, :type)"),request.form)
        conn.commit()
        return redirect("/accounts/login", code=301)
    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('register_page.html', error=error, success=None)

@app.route('/accounts/information', methods=['GET'])
def get_information():
    user = request.cookies.get('logged_in')
    user=str(user)
    user_info = conn.execute(text(f"SELECT account_id as id, concat(first_name, ' ', last_name) as name, email, username, password from account where username = '{user}'")).all()
    return render_template('Scammazon.html', user=user_info)

@app.route('/vendor', methods=['GET'])
def vendor_information():
    user = request.cookies.get('logged_in')
    user = str(user)
    vendor_info = conn.execute(text(f"SELECT products.* FROM products JOIN account USING(account_id) WHERE account.username = '{user}'")).all()
    return render_template('vendor_products.html', user=vendor_info)

@app.route('/admin', methods=['GET'])
def admin_information():
    admin_info = conn.execute(text("SELECT products.* FROM products")).all()
    return render_template('admin_products.html', user=admin_info)

@app.route('/product_edit/<id>', methods=['GET'])
def product_edit(id=0):
    id=int(id)
    product_info = conn.execute(text(f"SELECT product_id, title, description, image, active_warranty, color, size, quantity, price from products where product_id = '{id}';")).all()
    return render_template('admin_edit.html', product_info=product_info)

@app.route('/product_edit', methods=['POST'])
def post_product_edit():
    try:
        conn.execute(text("UPDATE products SET {} = :info_change WHERE product_id = :product_id".format(request.form.get("type"))), request.form)
        conn.commit()
        return redirect("/vendor", code=301)
    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('admin_edit.html', error=error, success=None)

@app.route('/product_delete/<id>', methods=['GET'])
def product_delete(id=0):
    id=int(id)
    product_info = conn.execute(text(f"SELECT product_id, title, description, image, active_warranty, color, size, quantity, price from products where product_id = '{id}';")).all()
    return render_template('admin_delete.html', product_info=product_info)

@app.route('/product_delete', methods=['POST'])
def post_product_delete():
    try:
        conn.execute(text("DELETE FROM products WHERE (`product_id` = :product_id)"),request.form)
        conn.commit()
        return redirect("/vendor", code=301)
    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('admin_delete.html', error=error, success=None)

@app.route('/store', methods=['GET'])
def shopping():
    items = conn.execute(text("SELECT product_id, title, description, image, color, size, price FROM products")).all()
    return render_template('ProductPage.html', items=items)

@app.route('/store', methods=['POST'])
def post_shopping():
    user = request.cookies.get('logged_in')
    user = str(user)
    item_id = request.form.get("product_id")
    person = conn.execute(text(f"SELECT account_id FROM account where username = '{user}'")).all()
    person_id = person[0][0]
    items = conn.execute(text("SELECT product_id, title, description, image, color, size, price FROM products")).all()
    conn.execute(text(f"INSERT INTO cart (`product_id`, `account_id`)VALUES('{item_id}', '{person_id}')"), request.form)
    conn.commit()
    return render_template('ProductPage.html', items=items)

@app.route('/create', methods=['GET'])
def product_add():
    return render_template('admin_create.html')

if __name__ == '__main__':
    app.run(debug=True)