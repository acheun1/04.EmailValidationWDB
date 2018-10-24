#Assignment: Email Validation w / DB
#2018 10 10
#Cheung Anthony

# You should pull appropriate information from the database to generate the table and the graph.  Once you retrieve all the information for 'all time', then allow the user to change the reporting date range by adjusting the two dates on the top right.  This assignment can be a bit difficult but teaches a lot of great lessons that could save you lots of time later when you're working on real complex projects.

from flask import Flask, render_template, redirect, request, session, flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key='as43df46asd3f4as4'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submitted', methods=['POST'])
def submitted():
    q0_str=str(request.form['q0'])
    mysql = connectToMySQL('emailvalidation_db')
    check_query = "SELECT email FROM email where email=%(email_chk)s;"
    record = {
            'email_chk':request.form['q0']
            }
    check=mysql.query_db(check_query, record)
    if check:
        cnt=1
    else:
        cnt=0
    print(check)
    print(cnt)
    if not q0_str.strip():
        flash("Please provide email to complete registration",'email')
    elif q0_str.strip() and not EMAIL_REGEX.match(request.form['q0']):
        flash("Please provide a valid email to complete registration",'email')
    elif cnt=='fail' and q0_str.strip() and not EMAIL_REGEX.match(request.form['q0']):
        flash("This email is already taken!",'email')
    if '_flashes' in session.keys():
        return redirect("/")

    else:
        mysql = connectToMySQL('emailvalidation_db')
        insert_query="INSERT INTO email (email, created_at, update_at) VALUES (%(new_email)s, NOW(), NOW());"
        record = {
                'new_email':request.form['q0'],
            }
        new_record_id=mysql.query_db(insert_query, record)
        mysql = connectToMySQL('emailvalidation_db')
        all_email=mysql.query_db("SELECT email FROM email")
        loopcnt=len(all_email)
        return render_template('submitted.html',email_front=all_email,loopcnt=loopcnt)

# @app.route('/update_records', methods=['POST'])
# def update():
#     mysql = connectToMySQL('cr')
#     insert_query="INSERT INTO user (name_first, name_last, occupation, created_at, updated_at) VALUES (%(name_first)s, %(name_last)s, %(occupation)s, NOW(), NOW());"
#     record = {
#                 'name_first':request.form['q1'],
#                 'name_last':request.form['q2'],
#                 'occupation':request.form['q3'],
#             }
#     new_record_id=mysql.query_db(insert_query, record)
#     return redirect('/')

if __name__=="__main__":
    app.run(debug=True)
