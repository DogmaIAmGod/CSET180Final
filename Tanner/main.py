from flask import Flask, render_template, request, redirect
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

app = Flask(__name__)
conn_str = "mysql://root:jtdStudent2023@localhost/scammazon"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/accounts/login', methods=['GET'])
def get_accounts():
    person_information = conn.execute(text("SELECT * FROM account"))
    return render_template('login_page.html', information=person_information)

#Work on with Daffy
@app.route('/accounts/login', methods=['POST'])
def post_get_accounts():
    auth = conn.execute(text("SELECT if(password = :password, 'Yes', 'No') FROM account WHERE username = :username OR email = :username"), request.form).one_or_none()
    maybe_user = request.form.get("username")
    if auth[0] == 'Yes':
        type = conn.execute(text(f"SELECT type FROM account where username = '{maybe_user}'")).all()
        type = str(type)
        print(type)
        if type == "[('vendor',)]":
            cookie = redirect("/vendor", code=301)
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
        return render_template('register_page.html', error=None, success="Account Created!")

    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('register_page.html', error=error, success=None)

@app.route('/accounts/information', methods=['GET'])
def get_information():
    user = request.cookies.get('logged_in')
    user=str(user)
    user_info = conn.execute(text(f"SELECT account_id as id, concat(first_name, ' ', last_name) as name, email, username, password from account where username = '{user}'")).all()
    print(user_info)
    return render_template('Scammazon.html', user=user_info)

@app.route('/vendor', methods=['GET'])
def vendor_information():
    user = request.cookies.get('logged_in')
    user = str(user)
    vendor_info = conn.execute(text(
        f"SELECT products.* FROM products JOIN account USING(account_id) WHERE account.username = '{user}'")).all()
    print(vendor_info)
    return render_template('vendor_products.html', user=vendor_info)


        # @app.route('/accounts/register')
# def get_accounts_student():
#     # student_accounts = conn.execute(text("select * from student_accounts")).all()
#     # print(student_accounts)
#     return render_template('register_page.html')
#                         #    , student_accounts=student_accounts)

# @app.route('/products', methods=['GET'])
# def products_page():
#     products = conn.execute(text("select * from products"))
#     return render_template('ProductPage.html', products=products)


@app.route('/accounts/accounts_teachers')
def get_accounts_teacher():
    teacher_accounts = conn.execute(text("select * from teacher_accounts")).all()
    print(teacher_accounts)
    return render_template('accounts_teachers.html', teacher_accounts=teacher_accounts)


@app.route('/quiz_questions/')
@app.route('/quiz_questions/<page>')
def get_boats(page=1):
    page = int(page)
    per_page = 10
    quiz_questions = conn.execute(text(f"SELECT quiz_questions.id, question1, question2, question3, concat(first_name, ' ', last_name) AS teacher_name FROM quiz_questions JOIN teacher_accounts ON teacher_id=teacher_accounts.id LIMIT {per_page} OFFSET {(page - 1) * per_page}")).all()
    print(quiz_questions)
    return render_template('boats.html', boats=quiz_questions, page=page, per_page=per_page)


@app.route('/teacher_create', methods=['GET'])
def create_get_request_teacher():
    return render_template('teacher_create.html')


@app.route('/teacher_create', methods=['POST'])
def create_teacher():
    try:
        conn.execute(
            text("INSERT INTO teacher_accounts (`first_name`, `last_name`) values (:first_name, :last_name)"),
            request.form
        )
        conn.commit()
        return render_template('teacher_create.html', error=None, success="Data inserted successfully!")

    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('teacher_create.html', error=error, success=None)


@app.route('/student_create', methods=['GET'])
def create_get_request_student():
    return render_template('student_create.html')


@app.route('/student_create', methods=['POST'])
def create_student():
    try:
        conn.execute(
            text("INSERT INTO student_accounts (`first_name`, `last_name`) values (:first_name, :last_name)"),
            request.form
        )
        conn.commit()
        return render_template('student_create.html', error=None, success="Data inserted successfully!")

    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('student_create.html', error=error, success=None)


@app.route('/test_create', methods=['GET'])
def create_get_request_test():
    teacher_accounts = conn.execute(text("select id, concat(first_name, ' ', last_name) as name from teacher_accounts")).all()
    return render_template('test_create.html', teacher_accounts=teacher_accounts)


@app.route('/test_create', methods=['POST'])
def create_test():
    try:
        conn.execute(
            text("INSERT INTO quiz_questions (`teacher_id`, `question1`, `question2`, `question3`) values (:teacher_id, :question1, :question2, :question3)"),
            request.form
        )
        conn.commit()
        return render_template('test_create.html', error=None, success="Data inserted successfully!")

    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('test_create.html', error=error, success=None)


@app.route('/test_delete', methods=['GET'])
def delete_get_request_test():
    quiz_questions = conn.execute(
        text("select id from quiz_questions")).all()
    return render_template('test_delete.html', quiz_questions=quiz_questions)


@app.route('/test_delete', methods=['POST'])
def delete_test():
    try:
        conn.execute(
            text("DELETE FROM quiz_questions WHERE (`id` = :id)"),
            request.form
        )
        conn.commit()
        return render_template('test_delete.html', error=None, success="Data deleted successfully!")

    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('test_delete.html', error=error, success=None)


@app.route('/test_edit', methods=['GET'])
def edit_get_request_test():
    quiz_questions = conn.execute(
    text("select id from quiz_questions")).all()
    return render_template('test_edit.html', quiz_questions=quiz_questions)


@app.route('/test_edit', methods=['POST'])
def edit_test():
    try:
        conn.execute(
            text("UPDATE quiz_questions SET {} = :edit_text WHERE id = :id".format(request.form.get("questions"))),
            request.form
        )
        conn.commit()
        return render_template('test_edit.html', error=None, success="Data updated successfully!")

    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('test_edit.html', error=error, success=None)


@app.route('/test_take/<id>', methods=['GET'])
def take_test_request(id = 0):
    id = int(id)
    student_accounts = conn.execute(
    text("select id, concat(first_name, ' ', last_name) as name from student_accounts")).all()
    quiz_questions = conn.execute(
        text(f"select * from quiz_questions WHERE id = {id}")).all()
    return render_template('test_take.html', quiz_questions=quiz_questions, student_accounts=student_accounts)

@app.route('/test_take', methods=['POST'])
def take_test():
    try:
        conn.execute(
            text("INSERT INTO quiz_answers (`questions_id`, `student_id`, `answer1`, `answer2`, `answer3`) values (:questions_id, :student_id, :answer1, :answer2, :answer3)"),
            request.form
        )
        conn.commit()
        return render_template('test_take.html', error=None, success="Data inserted successfully!")

    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('test_take.html', error=error, success=None)


if __name__ == '__main__':
    app.run(debug=True)