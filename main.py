from flask import Flask, render_template, request
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text
app = Flask(__name__)  # routes 
conn_str = "mysql://root:Tpob4711$@localhost:3306/finalproject160"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/')
def index():     return render_template('index.html')


# @app.route('/teacher_reg', methods= ['GET'])
# def teacher_registration(): return render_template('teacher_registration.html')

# @app.route('/teacher_reg', methods= ['POST'])
# def post_teacher_reg():
#     try:

#         conn.execute(
#             text('INSERT INTO users (first_name, last_name, email, password) values (:first_name, :last_name, :email, :password)'),
#             request.form
#         )
#         conn.commit()
#         return render_template('teacher_registration.html', error=None, success= 'Data inserted successfully.')
#     except Exception as e:
#         error = e.orig.args[1]
#         print(error)
#         return render_template('teacher_registration.html', error=error, success= 'Data inserted successfully.')
        



# @app.route('/student_reg', methods= ['GET'])
# def student_registration(): return render_template('student_registration.html')

# @app.route('/student_reg', methods= ['POST'])
# def student_registration(): return render_template('student_registration.html')


# @app.route('/student_log')
# def student_login(): return render_template('student_login.html')


# @app.route('/teacher_log')
# def teacher_login(): return render_template('teacher_login.html')


# @app.route('/accounts')
# def accounts(): return render_template('accounts.html')


# @app.route('/tests', methods= ['GET'])
# def tests(): return render_template('tests.html')

# @app.route('/tests', methods= ['POST'])
# def post_tests():
#     try:

#         conn.execute(
#             text('INSERT INTO users (title, instructions, question1, question2, question3) values (:test_title, :intructions, :q1, :q2, q3)'),
#             request.form
#         )
#         conn.commit()
#         return render_template('tests.html', error=None, success= 'Data inserted successfully.')
#     except Exception as e:
#         error = e.orig.args[1]
#         print(error)
#         return render_template('tests.html', error=error, success= 'Data inserted successfully.')


if __name__ == '__main__':
    app.run(debug=True)