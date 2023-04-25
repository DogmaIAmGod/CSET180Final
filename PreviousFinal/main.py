from flask import Flask, render_template, request
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

app = Flask(__name__)
conn_str = "mysql://root:jtdStudent2023@localhost/schooltests"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/accounts')
def get_accounts():
    student_accounts = conn.execute(text("select * from student_accounts")).all()
    teacher_accounts = conn.execute(text("select * from teacher_accounts")).all()
    print(student_accounts)
    print(teacher_accounts)
    return render_template('accounts.html', student_accounts=student_accounts, teacher_accounts=teacher_accounts)


@app.route('/accounts/accounts_students')
def get_accounts_student():
    student_accounts = conn.execute(text("select * from student_accounts")).all()
    print(student_accounts)
    return render_template('accounts_students.html', student_accounts=student_accounts)


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