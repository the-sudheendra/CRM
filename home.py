from flask import *
from flask_mysqldb import MySQL
from flask_mail import *
import random

import values

app = Flask(__name__)
# data base connection configuration.............................
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Kanna@123456"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_DB'] = "car_renter_management"
mysql = MySQL(app)
# -------------------------------------------------------------
# MAil send configuaration configuration .....................
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "190330141@klh.edu.in"
app.config['MAIL_PASSWORD'] = "63009772252701"

mail = Mail(app)


@app.route('/')
def index():
    email = request.cookies.get('email')
    name = request.cookies.get('name')
    print(name)
    if (name == None):
        email = ""
        name = ""
    print("name" + name)

    res = make_response(render_template('home.html', name=name, email=email))
    return res


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/book')
def book():
    return render_template('booknow.html')


@app.route('/contact')
def contact_us():
    res = make_response(render_template('contact-us.html'))

    return res


@app.route('/admin')
def admin():
    res = make_response(render_template('admin.html'))

    return res


@app.route('/edit_employees')
def edit_employees():
    res = make_response(render_template('edit_employees.html'))

    return res


@app.route('/profile_update')
def profile_update():
    res = make_response(render_template('profile_update.html'))

    return res


@app.route('/profile_submit', methods=['POST'])
def profile_submit():
    if (request.method == 'POST'):
        NAME = request.form['name']
        EMAIL = request.cookies.get('email')
        MOBILE = request.form['mobile']
        STATE = request.form['state']
        GENDER = request.form['gender']
        ADDRESS = request.form['address']
        DOB = request.form['dob']
    cur = mysql.connection.cursor()
    cur.execute("update coustemers set Name=%s,Mobile=%s,State=%s,Gender=%s,Date_Of_Birth=%s,address=%s where Email=%s",
                (NAME, MOBILE, STATE, GENDER, DOB, ADDRESS, EMAIL))
    mysql.connection.commit()
    res = make_response(render_template('home.html'))
    res.set_cookie("email", EMAIL)
    res.set_cookie("name", NAME)

    res.set_cookie("mobile", MOBILE)
    res.set_cookie("state", STATE)
    res.set_cookie("gender", GENDER)
    res.set_cookie("address", ADDRESS)
    res.set_cookie("dob", DOB)

    return res


@app.route('/is_admin', methods=['POST', 'GET'])
def is_admin():
    res = "Please enter right"
    if (request.method == 'POST'):

        form = request.form
        email = form['email']
        password = form['password']
        if (email == 'admin@cars.com' and password == 'cars'):
            cur = mysql.connection.cursor()
            cur.execute("select * from employees")
            employeess = cur.fetchall()
            cur.execute("select * from coustemers")
            coustemers = cur.fetchall()

            res = make_response(render_template('dashbord.html', employeess=employeess, coustemers=coustemers))

        else:
            res = "<h1 style='color:red'>Please enter right admin credentials</h1>"

    return res


@app.route('/cabs', methods=['POST', 'GET'])
def cabs():
    res = make_response(render_template('cabs.html'))
    if (request.method == 'POST'):
        form = request.form
        start = form['start']
        end = form['end']
        start_date = form['start_date']
        end_date = form['end_date']
        res.set_cookie('start', start)
        res.set_cookie('end', end)
        res.set_cookie('start_date', start_date)
        res.set_cookie('end_date', end_date)

    return res


@app.route('/contacting', methods=['GET', 'POST'])
def contacting():
    res = make_response(render_template('concern.html'))
    if (request.method == 'POST'):
        form = request.form
        name = form['name']
        email = form['email']
        msg = form['msg']

        cur = mysql.connection.cursor()
        cur.execute("insert into  concerns values(%s,%s,%s)", (name, email, msg))
        mysql.connection.commit()
        cur.close()

        msg = f"Mr. {name} we received your concern\n '{msg}' \n we will solve as soon as possible"
        message = Message("We Received your concern", sender='190330141@kh.edu.in', recipients=[email])
        message.body = str(msg)

        mail.send(message)
        return res


"""
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(name, email, mobile, experience, city, photo):
    print("Inserting BLOB into python_employee table")
    
                connection = mysql.connector.connect(host='localhost',
                                                     database='car_renter_management',
                                                     user='root',
                                                     password='Kanna@123456')
                

    cursor = mysql.connection.cursor()
    sql_insert_blob_query =INSERT INTO employees
                                  ( name, email,mobile,experience,city, photo) VALUES (%s,%s,%s,%s,%s,%s)

    ephoto = convertToBinaryData(photo)

    # Convert data into tuple format
    cursor=mysql.connection.cursor()
    insert_blob_tuple = (name, email, mobile, experience, city, ephoto)
    result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
    mysql.connection.commit()

    print("Image and file inserted successfully as a BLOB into python_employee table", result)
"""


@app.route('/uploding', methods=['GET', 'POST'])
def uploading():
    if (request.method == 'POST'):
        form = request.form
        name = form['name']
        email = form['email']
        mobile = form['phno']
        exp = form['exp']
        city = form['city']
        carnumber = form['carnumber']

        print(name + email + mobile + exp + city)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employees VALUES (%s,%s,%s,%s,%s,%s)", (name, email, mobile, exp, city, carnumber))
        mysql.connection.commit()
        return "Success fully inserted Employed "
    return redirect("https://www.youtube.com/watch?v=6WruncSoCdI")


@app.route('/suggestion')
def suggestion():
    return render_template('suggestion.html')


@app.route('/suggest', methods=['GET', 'POST'])
def suggest():
    if (request.method == 'POST'):
        suggestion = request.form['suggestion']
        name = request.cookies.get('name')
        email = request.cookies.get('email')

    cur = mysql.connection.cursor()
    cur.execute("insert into  suggestion values(%s,%s,%s)", (name, email, suggestion))
    mysql.connection.commit()
    cur.close()

    return render_template('success_suggestion.html', name=name)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():

    if (request.method == 'POST'):
        cardname = request.form['cardname']
        cardnumber = request.form['cardnumber']
        expmonth = request.form['expmonth']
        expyear = request.form['expyear']
        cvv = request.form['cvv']
        name=request.cookies.get('name')
        email=request.cookies.get('email')
        start_date=request.cookies.get('start_date')
        end_date=request.cookies.get('end_date')
        start_place=request.cookies.get('start')
        end_place=request.cookies.get('end')
    cur = mysql.connection.cursor()
    cur.execute("insert into  payment values(%s,%s,%s,%s,%s)", (cardname, cardnumber, expmonth, expyear, cvv))
    mysql.connection.commit()
    cur.close()


    cursor = mysql.connection.cursor()

    cursor.execute("insert into joureny values(%s,%s,%s,%s,%s,%s)",(str(name),str(email),str(start_date),str(end_date),str(start_place),str(end_place)))
    mysql.connection.commit()
    cursor.close()

    return render_template('success_checkout.html')


@app.route('/register')
def register():
    return render_template('register.html')


a = []
user_details = []


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    try:
        if (request.method == 'POST'):
            print("52")

            form = request.form
            user_details.append(form['name'])

            user_details.append(form['email'])
            user_details.append(form['password'])
            user_details.append(form['mobile'])
            user_details.append(form['state'])
            user_details.append(form['gender'])
            user_details.append(form['dob'])
            user_details.append(form['address'])

            user_details.append(random.randint(10000, 100000))

            subject = "OTP Verification"

            msg = f"Mr. {user_details[0]} Please enter this  otp in car renter management \n your otp is: {user_details[8]}"
            message = Message(subject, sender='190330141@kh.edu.in', recipients=[user_details[1]])

            message.body = str(msg)

            mail.send(message)
            print("71")
            return render_template('verify.html', form=form)
        else:
            print("76")
            return render_template("not_successfully.html")
    except:
        return "<h3 style='color:red'> Mr. " + user_details[0] + " you have already register with email " + + \
            user_details[1] + "</h3> "


@app.route("/otp", methods=['GET', 'POST'])
def otp():
    print("in otp")
    try:
        if (request.method == 'POST'):
            print("in post")
            votp = request.form['votp']
            name = user_details[0]
            email = user_details[1]
            password = user_details[2]
            mobile = user_details[3]
            state = user_details[4]
            gender = user_details[5]
            dob = user_details[6]
            address = user_details[7]

            otp = user_details[8]

            cur = mysql.connection.cursor()
            print(type(otp))
            print(type(votp))
            print(str(otp) + " " + votp)
            print(user_details[0])
            print(user_details[1])
            print(user_details[2])
            print(user_details[3])
            print(user_details[4])
            print(user_details[5])
            print(user_details[6])
            print(user_details[7])
            print(user_details[8])

            if otp == int(votp):
                cur.execute("insert into  coustemers values(%s,%s,%s,%s,%s,%s,%s,%s)",
                            (name, email, password, mobile, state, gender, dob, address))
                mysql.connection.commit()
                cur.close()
                res = """
                <h3 style="color:green">Registration done Successfully..............</h3>
                <a href="login">Login here</a>
                """
                return res


            else:
                return "<h3 style='color:red'>Please enter Right Otp..</h3>"
    except:
        return "<h3 style='color:red'> Mr. " + user_details[0] + " you have already register with email " + \
               user_details[1] + "</h3>"


@app.route('/log', methods=['GET', 'POST'])
def log():
    if (request.method == 'POST'):
        form = request.form
        print(type(form))
        email = form['email']
        password = form['password']
        cur = mysql.connection.cursor()

        sql_Query = "select * from coustemers where email =%s"
        id = (email,)
        print(type(id))
        cursor = mysql.connection.cursor()
        cursor.execute(sql_Query, id)
        print(password)
        record = cursor.fetchall()
        print(record)

        try:
            name = record[0][0]
            email = record[0][1]
            password1 = record[0][2]
            mobile = record[0][3]
            state = record[0][4]
            gender = record[0][5]
            dob = record[0][6]
            address = record[0][7]
            print(record[0][1])
            print(record[0][7])

            if (password == password1):
                res = make_response(render_template("home.html", name=name, email=email))
                res.set_cookie("email", email)
                res.set_cookie("name", name)

                res.set_cookie("mobile", mobile)
                res.set_cookie("state", state)
                res.set_cookie("gender", gender)
                res.set_cookie("address", address)
                res.set_cookie("dob", dob)

                return res
            else:
                return render_template("not_success.html")
        except:
            return "<h3  style='color:red'>There is no record with " + email + " Please Sign up..<br><a href='register'> Sign up</a>"


@app.route('/logout')
def logout():
    res = make_response(render_template("login.html"))

    res.set_cookie("name", "")

    res.set_cookie("email", "")

    res.set_cookie("mobile", "")
    res.set_cookie("state", "")
    res.set_cookie("gender", "")
    res.set_cookie("address", "")
    res.set_cookie("dob", "")
    res.set_cookie('start', "")
    res.set_cookie('end', "")
    res.set_cookie('start_date', "")
    res.set_cookie('end_date', "")
    return res


@app.route('/profile')
def profile():
    email = request.cookies.get('email')
    cur = mysql.connection.cursor()
    cur.execute("select * from joureny where email =%s", (email,))
    mysql.connection.commit()
    journey="None"
    journey = cur.fetchall()
    res = make_response(render_template("profile.html", journey=journey))
    return res


@app.route('/forgot')
def forgot():
    return render_template("forgot.html")


email_list = []


@app.route('/marichipoina', methods=['POST', 'GET'])
def marichipoina():
    # res=make_response()
    if (request.method == 'POST'):
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("select email from coustemers")
        emails = (cur.fetchall())

        if ((email,) in emails):
            email_list.append(email)
            return render_template('marichipoina.html')
        else:
            return "Unable to find email .. <a href='forgot'>please enter right email</a>"


@app.route('/newpass', methods=['POST', 'GET'])
def new_pass():
    if (request.method == 'POST'):

        new_pass = request.form['newpassword']
        c_pass = request.form['cpassword']
        if (new_pass == c_pass):
            cur = mysql.connection.cursor()
            print("email_list", email_list[0])
            print("new pass:", new_pass)
            cur.execute("update coustemers set Password = %s where email=%s", (new_pass, email_list[0]))
            mysql.connection.commit()
            return "Your Password is Success fully updated...<a href='login'>Login here..</a>"
        else:
            return "Please enter write Passsowrd ... <a href='forgot'>Please Enter again...</a>"


@app.route('/logout')
def log_out():
    res = make_response(render_template('login.html'))
    res.set_cookie("email", "")
    res.set_cookie("name", "")
    return res


if (__name__ == '__main__'):
    app.run(debug=True)
