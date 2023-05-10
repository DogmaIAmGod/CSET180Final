# from flask import Flask, render_template, request
# from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

# app = Flask(__name__)
# conn_str = "mysql://root:Tpob4711$@localhost/scammazon"
# engine = create_engine(conn_str, echo=True)
# conn = engine.connect()


# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/accounts/login')
# def get_accounts():
#     # student_accounts = conn.execute(text("select * from student_accounts")).all()
#     # teacher_accounts = conn.execute(text("select * from teacher_accounts")).all()
#     # print(student_accounts)
#     # print(teacher_accounts)
#     return render_template('login_page.html')
#                         #    , student_accounts=student_accounts, teacher_accounts=teacher_accounts)


# @app.route('/accounts/register')
# def get_accounts_student():
#     # student_accounts = conn.execute(text("select * from student_accounts")).all()
#     # print(student_accounts)
#     return render_template('register_page.html')
#                         #    , student_accounts=student_accounts)


# @app.route('/products')
# def get_accounts_teacher():
#     # teacher_accounts = conn.execute(text("select * from teacher_accounts")).all()
#     # print(teacher_accounts)
#     return render_template('lorenzo_product_page.html')
#                         #    ,teacher_accounts=teacher_accounts)


# @app.route('/review')
# def get_boats():
#     # page = int(page)
#     # per_page = 10
#     # quiz_questions = conn.execute(text(f"SELECT quiz_questions.id, question1, question2, question3, concat(first_name, ' ', last_name) AS teacher_name FROM quiz_questions JOIN teacher_accounts ON teacher_id=teacher_accounts.id LIMIT {per_page} OFFSET {(page - 1) * per_page}")).all()
#     # print(quiz_questions)
#     return render_template('review.html')
#                         #    , boats=quiz_questions, page=page, per_page=per_page)


# @app.route('/vendor_products')
# def create_get_request_teacher():
#     return render_template('vendor_products.html')


# @app.route('/teacher_create', methods=['POST'])
# def create_teacher():
#     try:
#         conn.execute(
#             text("INSERT INTO teacher_accounts (`first_name`, `last_name`) values (:first_name, :last_name)"),
#             request.form
#         )
#         conn.commit()
#         return render_template('teacher_create.html', error=None, success="Data inserted successfully!")

#     except Exception as e:
#         error = e.orig.args[1]
#         print(error)
#         return render_template('teacher_create.html', error=error, success=None)


# @app.route('/student_create', methods=['GET'])
# def create_get_request_student():
#     return render_template('student_create.html')


# @app.route('/student_create', methods=['POST'])
# def create_student():
#     try:
#         conn.execute(
#             text("INSERT INTO student_accounts (`first_name`, `last_name`) values (:first_name, :last_name)"),
#             request.form
#         )
#         conn.commit()
#         return render_template('student_create.html', error=None, success="Data inserted successfully!")

#     except Exception as e:
#         error = e.orig.args[1]
#         print(error)
#         return render_template('student_create.html', error=error, success=None)


# @app.route('/test_create', methods=['GET'])
# def create_get_request_test():
#     teacher_accounts = conn.execute(text("select id, concat(first_name, ' ', last_name) as name from teacher_accounts")).all()
#     return render_template('test_create.html', teacher_accounts=teacher_accounts)


# @app.route('/test_create', methods=['POST'])
# def create_test():
#     try:
#         conn.execute(
#             text("INSERT INTO quiz_questions (`teacher_id`, `question1`, `question2`, `question3`) values (:teacher_id, :question1, :question2, :question3)"),
#             request.form
#         )
#         conn.commit()
#         return render_template('test_create.html', error=None, success="Data inserted successfully!")

#     except Exception as e:
#         error = e.orig.args[1]
#         print(error)
#         return render_template('test_create.html', error=error, success=None)


# @app.route('/test_delete', methods=['GET'])
# def delete_get_request_test():
#     quiz_questions = conn.execute(
#         text("select id from quiz_questions")).all()
#     return render_template('test_delete.html', quiz_questions=quiz_questions)


# @app.route('/test_delete', methods=['POST'])
# def delete_test():
#     try:
#         conn.execute(
#             text("DELETE FROM quiz_questions WHERE (`id` = :id)"),
#             request.form
#         )
#         conn.commit()
#         return render_template('test_delete.html', error=None, success="Data deleted successfully!")

#     except Exception as e:
#         error = e.orig.args[1]
#         print(error)
#         return render_template('test_delete.html', error=error, success=None)


# @app.route('/test_edit', methods=['GET'])
# def edit_get_request_test():
#     quiz_questions = conn.execute(
#     text("select id from quiz_questions")).all()
#     return render_template('test_edit.html', quiz_questions=quiz_questions)


# @app.route('/test_edit', methods=['POST'])
# def edit_test():
#     try:
#         conn.execute(
#             text("UPDATE quiz_questions SET {} = :edit_text WHERE id = :id".format(request.form.get("questions"))),
#             request.form
#         )
#         conn.commit()
#         return render_template('test_edit.html', error=None, success="Data updated successfully!")

#     except Exception as e:
#         error = e.orig.args[1]
#         print(error)
#         return render_template('test_edit.html', error=error, success=None)


# @app.route('/test_take/<id>', methods=['GET'])
# def take_test_request(id = 0):
#     id = int(id)
#     student_accounts = conn.execute(
#     text("select id, concat(first_name, ' ', last_name) as name from student_accounts")).all()
#     quiz_questions = conn.execute(
#         text(f"select * from quiz_questions WHERE id = {id}")).all()
#     return render_template('test_take.html', quiz_questions=quiz_questions, student_accounts=student_accounts)

# @app.route('/test_take', methods=['POST'])
# def take_test():
#     try:
#         conn.execute(
#             text("INSERT INTO quiz_answers (`questions_id`, `student_id`, `answer1`, `answer2`, `answer3`) values (:questions_id, :student_id, :answer1, :answer2, :answer3)"),
#             request.form
#         )
#         conn.commit()
#         return render_template('test_take.html', error=None, success="Data inserted successfully!")

#     except Exception as e:
#         error = e.orig.args[1]
#         print(error)
#         return render_template('test_take.html', error=error, success=None)


# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

app = Flask(__name__)
conn_str = "mysql://root:Tpob4711$@localhost/scammazon"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/')
def index():
    return redirect("/accounts/login", code=301)

@app.route('/home')
def home():
    return render_template('index.html')

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

@app.route('/create', methods=['POST'])
def post_add():
    user = request.cookies.get('logged_in')
    user = str(user)
    person = conn.execute(text(f"SELECT account_id FROM account where username = '{user}'")).all()
    person_id = person[0][0]
    conn.execute(text(f"INSERT INTO products (`account_id`, `title`, `description`, `image`, `color`, `size`, `quantity`, `price`) VALUES ('{person_id}', :title, :description, :image, :color, :size, :quantity, :price)"), request.form)
    conn.commit()
    return redirect("/vendor", code=301)

@app.route('/cart', methods=['GET'])
def cart():
    # person_id = conn.execute(text(f"SELECT account_id FROM account where username = '{str(request.cookies.get('logged_in'))}'")).all()[0][0]
    # cart = conn.execute(text(f"SELECT cart.product_id, title, description, image, color, size, price from products join cart using(product_id) where products.product_id = cart.product_id AND cart.account_id = {person_id}"))
    # total = conn.execute(text(f"SELECT SUM(price) as total from cart join products using(product_id) where cart.account_id = {person_id}"))
    # return render_template('cart.html', cart=cart, total=total)

# @app.route('/cart', methods=['POST'])
# def post_cart():
#     person_id = conn.execute(text(f"SELECT account_id FROM account where username = '{str(request.cookies.get('logged_in'))}'")).all()[0][0]
#     total = float(conn.execute(text(f"SELECT SUM(price) as total from cart join products using(product_id) where cart.account_id = {person_id}")).all()[0][0])
#     order = conn.execute(text(f"SELECT product_id FROM cart where account_id = {person_id}")).all()
#     order_list = []
#     for i in range(len(order)):
#         order_list.append(order[i][0])
#     item_name = []
#     for i in order_list:
#         item_name.append(conn.execute(text(f"SELECT CONCAT(size,' ',title) from products where product_id = {i}")).all()[0][0].title())
#     new_string = ', '.join(item_name)
#     conn.execute(text(f"INSERT INTO orders (`account_id`, `order_date`, `items`, `text`, `total`) VALUES ('{person_id}', '{date.today()}', '{order_list}', '{new_string}', {total})"))
#     conn.commit()
#     return redirect("/order", code=301)



    if __name__ == '__main__':
        app.run(debug=True)