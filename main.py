from flask import Flask, render_template, request, redirect
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text
from datetime import date

app = Flask(__name__)
conn_str = "mysql://root:Tpob4711$@localhost/scammazon"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


@app.route('/')
def index():
    return redirect("/accounts/login", code=301)


@app.route('/accounts/login')
def get_accounts():
    return render_template('login_page.html')


@app.route('/accounts/login', methods=['POST'])
def post_get_accounts():
    auth = conn.execute(text(
        "SELECT CASE WHEN EXISTS (SELECT 1 FROM account WHERE username = :username AND (password = :password OR email = :password))THEN 'Yes'ELSE 'No' END"),
        request.form).one_or_none()
    maybe_user = request.form.get("username")
    print("Auth: ", auth[0])
    if auth[0] == 'Yes':
        type = conn.execute(text(f"SELECT type FROM account where username = '{maybe_user}'")).all()[0][0]
        if type == "vendor":
            cookie = redirect("/vendor_landing", code=301)
            cookie.set_cookie('logged_in', maybe_user)
            return cookie
        elif type == "customer":
            cookie = redirect("/landing", code=301)
            cookie.set_cookie('logged_in', maybe_user)
            return cookie
        else:
            cookie = redirect("/admin_landing", code=301)
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
        conn.execute(text(
            "INSERT INTO account (`first_name`, `last_name`, `email`, `username`, `password`, `type`) values (:first_name, :last_name, :email, :username, :password, :type)"),
            request.form)
        conn.commit()
        return redirect("/accounts/login", code=301)
    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('register_page.html', error=error, success=None)


@app.route('/landing')
def landing_page():
    return render_template('landing_page.html')


@app.route('/admin_landing')
def admin_landing_page():
    return render_template('admin_landing_page.html')


@app.route('/vendor_landing')
def vendor_landing_page():
    return render_template('vendor_landing_page.html')


@app.route('/accounts/information', methods=['GET'])
def get_information():
    user = str(request.cookies.get('logged_in'))
    user_info = conn.execute(text(
        f"SELECT account_id as id, concat(first_name, ' ', last_name) as name, email, username, password from account where username = '{user}'")).all()
    return render_template('Scammazon.html', user=user_info)


@app.route('/vendor', methods=['GET'])
def vendor_information():
    user = str(request.cookies.get('logged_in'))
    vendor_info = conn.execute(
        text(f"SELECT products.* FROM products JOIN account USING(account_id) WHERE account.username = '{user}'")).all()
    return render_template('vendor_products.html', user=vendor_info)


@app.route('/admin', methods=['GET'])
def admin_information():
    admin_info = conn.execute(text(
        "SELECT products.*, concat(first_name,' ',last_name) name FROM products join account using(account_id)")).all()
    return render_template('admin_products.html', user=admin_info)


@app.route('/product_edit/<id>', methods=['GET'])
def product_edit(id=0):
    id = int(id)
    product_info = conn.execute(text(
        f"SELECT product_id, title, description, image, active_warranty, color, size, quantity, price from products where product_id = '{id}';")).all()
    return render_template('admin_edit.html', product_info=product_info)


@app.route('/product_edit', methods=['POST'])
def post_product_edit():
    try:
        conn.execute(text(
            "UPDATE products SET {} = :info_change WHERE product_id = :product_id".format(request.form.get("type"))),
            request.form)
        conn.commit()
        return redirect("/vendor", code=301)
    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('admin_edit.html', error=error, success=None)


@app.route('/product_delete/<id>', methods=['GET'])
def product_delete(id=0):
    id = int(id)
    product_info = conn.execute(text(
        f"SELECT product_id, title, description, image, active_warranty, color, size, quantity, price from products where product_id = '{id}';")).all()
    return render_template('admin_delete.html', product_info=product_info)


@app.route('/product_delete', methods=['POST'])
def post_product_delete():
    try:
        conn.execute(text("DELETE FROM products WHERE (`product_id` = :product_id)"), request.form)
        conn.commit()
        return redirect("/vendor", code=301)
    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('admin_delete.html', error=error, success=None)


@app.route('/store', methods=['GET'])
def shopping():
    items = conn.execute(text("SELECT product_id, title, description, image, color, size, price FROM products")).all()
    return render_template('Product.html', items=items)


@app.route('/store', methods=['POST'])
def post_shopping():
    # person_id = conn.execute(
    #     text(f"SELECT account_id FROM account where username = '{str(request.cookies.get('logged_in'))}'")).all()[0][0]
    # item_id = request.form.get("product_id")
    # conn.execute(text(f"INSERT INTO cart (`product_id`, `account_id`)VALUES('{item_id}', '{person_id}')"), request.form)
    # conn.commit()
    person_id = conn.execute(text(f"select account_id from account where username = '{request.cookies.get('logged_in')}'")).all()
    cookie = request.cookies.get('logged_in')
    print(cookie)
    return redirect('/store', code=301)


@app.route('/create')
def add():
    return render_template('create.html')


@app.route('/create', methods=['POST'])
def post_add():
    person_id = conn.execute(
        text(f"SELECT account_id FROM account where username = '{str(request.cookies.get('logged_in'))}'")).all()[0][0]
    conn.execute(text(
        f"INSERT INTO products (`account_id`, `title`, `description`, `image`, `color`, `size`, `quantity`, `price`) VALUES ('{person_id}', :title, :description, :image, :color, :size, :quantity, :price)"),
        request.form)
    conn.commit()
    return redirect("/vendor", code=301)


@app.route('/create_admin', methods=['GET'])
def adminadd():
    vendors = conn.execute(
        text("SELECT account_id, concat(first_name,' ',last_name) as name from account where type = 'vendor'")).all()
    return render_template('admin_create.html', vendors=vendors)


@app.route('/create_admin', methods=['POST'])
def post_adminadd():
    conn.execute(text(
        f"INSERT INTO products (`account_id`, `title`, `description`, `image`, `color`, `size`, `quantity`, `price`) VALUES (:vendor, :title, :description, :image, :color, :size, :quantity, :price)"),
        request.form)
    conn.commit()
    return redirect("/admin", code=301)


@app.route('/cart', methods=['GET'])
def cart():
    person_id = conn.execute(
        text(f"SELECT account_id FROM account where username = '{str(request.cookies.get('logged_in'))}'")).all()[0][0]
    cart = conn.execute(text(
        f"SELECT cart.product_id, title, description, image, color, size, price from products join cart using(product_id) where products.product_id = cart.product_id AND cart.account_id = {person_id}"))
    total = conn.execute(text(
        f"SELECT SUM(price) as total from cart join products using(product_id) where cart.account_id = {person_id}"))
    return render_template('cart.html', cart=cart, total=total)


@app.route('/cart', methods=['POST'])
def post_cart():
    person_id = conn.execute(
        text(f"SELECT account_id FROM account where username = '{str(request.cookies.get('logged_in'))}'")).all()[0][0]
    total = float(conn.execute(text(
        f"SELECT SUM(price) as total from cart join products using(product_id) where cart.account_id = {person_id}")).all()[
                      0][0])
    order = conn.execute(text(f"SELECT product_id FROM cart where account_id = {person_id}")).all()
    order_list = []
    for i in range(len(order)):
        order_list.append(order[i][0])
    item_name = []
    for i in order_list:
        item_name.append(
            conn.execute(text(f"SELECT CONCAT(size,' ',title) from products where product_id = {i}")).all()[0][
                0].title())
    new_string = ', '.join(item_name)
    conn.execute(text(
        f"INSERT INTO orders (`account_id`, `order_date`, `items`, `text`, `total`) VALUES ('{person_id}', '{date.today()}', '{order_list}', '{new_string}', {total})"))
    conn.commit()
    return redirect("/order", code=301)


@app.route('/cart/delete/<id>', methods=['GET'])
def delete_cart(id=0):
    id = int(id)
    product_info = conn.execute(text(
        f"SELECT product_id, title, description, image, color, size, price from products where product_id = '{id}';")).all()
    return render_template('cart_delete.html', product_info=product_info)


@app.route('/cart/delete', methods=['POST'])
def post_delete_cart():
    person_id = conn.execute(
        text(f"SELECT account_id FROM account where username = '{str(request.cookies.get('logged_in'))}'")).all()[0][0]
    pro_id = request.form.get("product_id")
    cart_id = \
        conn.execute(text(f"SELECT cart_id from cart where product_id = {pro_id} AND account_id = {person_id}")).all()[
            0][0]
    conn.execute(text(f"DELETE FROM cart WHERE (cart_id = '{cart_id}')"), request.form)
    conn.commit()
    return redirect("/cart", code=301)


@app.route('/order', methods=['GET'])
def orders():
    person_id = conn.execute(
        text(f"SELECT account_id FROM account where username = '{str(request.cookies.get('logged_in'))}'")).all()[0][0]
    orders = conn.execute(text(
        f"SELECT order_status, order_date, total FROM orders where account_id = {person_id} ORDER BY order_id DESC LIMIT 1")).all()
    items = eval(conn.execute(text(f"SELECT items FROM orders ORDER by order_id DESC LIMIT 1")).all()[0][0])
    item_name = []
    num = 0
    for i in items:
        item_name.append([
            conn.execute(
                text(f"SELECT price, concat(size,' ',title) as item from products where product_id = '{i}'")).all()[
                num][0],
            conn.execute(
                text(f"SELECT price, concat(size,' ',title) as item from products where product_id = '{i}'")).all()[
                num][1]])
        num += 0
    print(item_name)
    return render_template('orders.html', orders=orders, items=item_name)


@app.route('/review', methods=['GET'])
def reviews():
    person_id = conn.execute(
        text(f"SELECT account_id FROM account where username = '{str(request.cookies.get('logged_in'))}'")).all()[0][0]
    orders = conn.execute(
        text(f"SELECT order_status, order_date, text, total FROM orders where account_id = {person_id}")).all()
    return render_template('review_check.html', orders=orders)


@app.route('/admin_review', methods=['GET'])
def admin_reviews():
    orders = conn.execute(text(f"SELECT order_id, order_status, order_date, text, total FROM orders")).all()
    return render_template('admin_review_check.html', orders=orders)


@app.route('/admin_review_edit', methods=['GET'])
@app.route('/admin_review_edit/<id>', methods=['GET'])
def admin_reviews_edit(id=0):
    number = int(id)
    order_edit = conn.execute(
        text(f"SELECT order_id, order_status, order_date, text, total FROM orders WHERE order_id = {number}")).all()
    return render_template('admin_review_edit.html', orders=order_edit)


@app.route('/admin_review_edit', methods=['POST'])
def post_admin_reviews_edit():
    conn.execute(text(f'UPDATE orders SET order_status = :status WHERE `order_id` = :order_id'), request.form)
    conn.commit()
    return redirect('/admin_review', code=301)


@app.route('/customer_review', methods=['GET'])
def customer_review():
    person_id = conn.execute(
        text(f"SELECT account_id FROM account where username = '{str(request.cookies.get('logged_in'))}'")).all()[0][0]
    can_review = conn.execute(text(
        f'SELECT order_id as id, text, total FROM orders WHERE order_status = "shipped" AND account_id = {person_id}'))
    reviews = conn.execute(text(
        f"SELECT review_id, rating, comment, reviews.date as date, text FROM reviews JOIN orders USING(order_id) WHERE orders.account_id = {person_id}"))
    complaints = conn.execute(text(
        f"select complaint.status as status, complaint.comment as comment, complaint_type, complaint.date as date, orders.text as text FROM complaint JOIN reviews USING(review_id) JOIN orders USING(order_id) where orders.account_id = {person_id};"))
    return render_template('customer_review_choose.html', deliveries=can_review, reviews=reviews, complaints=complaints)


@app.route('/leave_review/<id>', methods=['GET'])
def leave_review(id=0):
    id = int(id)
    return render_template('customer_review.html', id=id)


@app.route('/leave_review', methods=['POST'])
def post_leave_review():
    today = str(date.today())
    conn.execute(text(
        f"INSERT INTO reviews (`order_id`, `rating`, `comment`, `image`, `date`) VALUES (:order_id, :rating, :comment, :image, '{today}')"),
        request.form)
    conn.commit()
    return redirect('/customer_review', code=301)


@app.route('/complaint/<id>', methods=['GET'])
def complaint(id=0):
    review_id = id
    return render_template('complaint.html', id=review_id)


@app.route('/complaint', methods=['POST'])
def post_complaint():
    conn.execute(text(
        f"INSERT INTO complaint (`review_id`, `complaint_type`, `date`) VALUES (:review_id, :complaintType, '{date.today()}')"))
    conn.commit()
    return redirect('/customer_review', code=301)


@app.route('/admin_complaints', methods=['GET'])
def admin_complaints():
    complaints = conn.execute(text(
        f"select complaint.complaint_id, complaint.status as status, complaint.comment as comment, complaint_type, complaint.date as date, orders.text as text FROM complaint JOIN reviews USING(review_id) JOIN orders USING(order_id);"))
    return render_template('admin_complaint_check.html', complaints=complaints)


@app.route('/admin_complaint_edit/<id>', methods=['GET'])
def admin_complaints_edit(id=0):
    complaint_id = id
    complaints = conn.execute(text(
        f"select complaint.status as status, complaint.comment as comment, complaint_type, complaint.date as date, orders.text as text FROM complaint JOIN reviews USING(review_id) JOIN orders USING(order_id) WHERE complaint_id = {complaint_id};"))
    return render_template('admin_complaint_edit.html', complaints=complaints)

@app.route('/customer_chats', methods=['GET'])
def chats():
    person_id = conn.execute(text(f"SELECT account_id FROM account where username = '{str(request.cookies.get('logged_in'))}'")).all()[0][0]
    open_chats = conn.execute(text(f"select chat_id, title from chat where {person_id} = participant1 or {person_id} = participant2 "))
    return render_template('chats.html', chats=open_chats)

@app.route('/customer_chats', methods=['POST'])
def post_chats():
    id = request.form.get("chats")
    print(id)
    return redirect(f'/chatting/{id}', code=301)

@app.route('/chat_create', methods=['GET'])
def chat_create():
    who_to = conn.execute(text(f"select account_id, concat(first_name, ' ', last_name) as name, type from account where type = 'admin' or type = 'vendor'"))
    return render_template('chat_create.html', whos=who_to)


@app.route('/chat_create', methods=['POST'])
def post_chat_create():
    person_id = conn.execute(text(f"SELECT account_id FROM account where username = '{str(request.cookies.get('logged_in'))}'")).all()[0][0]
    conn.execute(text(f"INSERT INTO chat (`participant1`, `participant2`, `title`) VALUES ('{person_id}', :p2, :title);"), request.form)
    conn.commit()
    # return render_template('chat_create.html')
    return redirect('/customer_chats', code=301)

@app.route('/chatting/<id>', methods=['GET'])
def chatting(id=0):
    id= int(id)
    previous_messages = conn.execute(text(f"SELECT concat(first_name,' ',last_name) as name, text from chat_messages join account using(account_id) where chat_id = {id}"))
    return render_template('chatting.html', messages=previous_messages, id=id)

@app.route('/chatting', methods=['POST'])
def post_chatting():
    id = request.form.get("chat_id")
    person_id = conn.execute(text(f"SELECT account_id FROM account where username = '{str(request.cookies.get('logged_in'))}'")).all()[0][0]
    conn.execute(text(f"INSERT INTO chat_messages (`account_id`, `chat_id`, `text`) VALUES ('{person_id}', :chat_id, :text)"), request.form)
    conn.commit()
    return redirect(f'/chatting/{id}', code=301)

@app.route('/a_v_chats', methods=['GET'])
def a_v_chats():
    person_id = conn.execute(text(f"SELECT account_id FROM account where username = '{str(request.cookies.get('logged_in'))}'")).all()[0][0]
    open_chats = conn.execute(text(f"select chat_id, title from chat where {person_id} = participant1 or {person_id} = participant2 "))
    return render_template('A_V_chats.html', chats=open_chats)

@app.route('/a_v_chats', methods=['POST'])
def post_a_v_chats():
    id = request.form.get("chats")
    print(id)
    return redirect(f'/chatting/{id}', code=301)

if __name__ == '__main__':
    app.run(debug=True)
# type = conn.execute(text(f"SELECT type FROM account where username = '{maybe_user}'")).all()[0][0]