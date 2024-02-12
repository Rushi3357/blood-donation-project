from flask import Flask,render_template, request, session,url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key="teraGharChalaJayenga"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blood.db'
db = SQLAlchemy(app)  # added line break

# #------------------upload file
# class Book3(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(80), nullable=False)
#     author = db.Column(db.String(80), nullable=False)
#     cover_image = db.Column(db.LargeBinary, nullable=False)

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         title = request.form['title']
#         author = request.form['author']
#         cover_image = request.files['cover_image'].read()

#         book = Book3(title=title, author=author, cover_image=cover_image)
#         db.session.add(book)
#         db.session.commit()

#         return 'File uploaded and saved in the database!'

#     return render_template('templates/upload.html')

# ------------------default page

@app.route("/") 
def index():
    return render_template("index.html")

@app.route("/home")
def index1():
    return render_template("index.html")

#---------------------------------------ADMIN DETAILS--------------------------------------------

# --------admin login

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        admin_name = request.form.get('admin_name')
        admin_pass = request.form.get('admin_pass')

    # ---validation--

        # check if admin_name and password are correct
        if admin_name == 'admin' and admin_pass == 'admin':
            session['email']=admin_name
            # redirect to admin page
            return render_template('admin/admindashboard.html',email=admin_name)
        else:
            # show error message
            msg = 'Invalid Username/Password'
            return render_template('admin/adminlogin.html', msg=msg)
    
    return render_template('admin/adminlogin.html')

# ------------------admin logout

@app.route('/logout')
def logout():
    session.clear('admin_login',None)
    return redirect(url_for('adminlogin'))

# ------------------admin contact
@app.route("/contact")
def index4():
    return render_template("admin/contact.html")




#-----------------------donor table

class Blood4(db.Model):
    uname = db.Column(db.String(20), unique=False, nullable=False)
    uage = db.Column(db.Integer(), unique=False, nullable=False)
    blood_type = db.Column(db.String(20), unique=False, nullable=False)
    blood_qty = db.Column(db.Integer(), unique=False, nullable=False)
    disease = db.Column(db.String(25), unique=False, nullable=False)
    tele = db.Column(db.Integer(), primary_key=True)
    city = db.Column(db.String(30), unique=False, nullable=False)


# -------------------adding donor data in backend

@app.route("/bloodinfo", methods=['GET', 'POST'])
def bloodinfo():
    if request.method == 'POST':
        uname = request.form.get('uname')
        uage = request.form.get('uage')
        blood_type = request.form.get('blood_type')
        blood_qty = request.form.get('blood_qty')
        disease = request.form.get('disease')
        tele = request.form.get('tele')
        city = request.form.get('city')

        entry = Blood4(uname=uname, disease=disease, uage=uage, blood_type=blood_type,blood_qty=blood_qty, tele=tele, city=city)
        db.create_all()    
        db.session.add(entry)
        db.session.commit()

    return render_template('donar/blood.html')


# -------------------------displaying donor data on web page(Bdata.html)

@app.route("/blooddata")
def blooddata():

     # fetch all entries from the Blood table
    entries = Blood4.query.all()

    return render_template('donar/Bdata.html', entries=entries)

# --------------delete donor data

@app.route('/bloodinfo/delete/<int:tele>', methods=['POST'])
def delete_entry(tele):
    entry = Blood4.query.get(tele)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('blooddata'))

# ---------------------update donar data

@app.route('/bloodinfo/update/<int:tele>', methods=['GET', 'POST'])
def update_entry(tele):
    entry = Blood4.query.get(tele)
    if request.method == 'POST':
        entry.uname = request.form.get('uname')
        entry.uage = request.form.get('uage')
        entry.disease = request.form.get('disease')
        entry.blood_type = request.form.get('blood_type')
        entry.blood_qty = request.form.get('blood_qty')
        entry.tele = request.form.get('tele')
        entry.city = request.form.get('city')
        db.session.commit()
        return redirect(url_for('blooddata'))
    return render_template('donar/donarupdate.html', entry=entry)


# ----------------------user table


class userinfo(db.Model):
  
    uname = db.Column(db.String(20), unique=False, nullable=False)
    uage = db.Column(db.Integer(), unique=False, nullable=False)
    blood_type = db.Column(db.String(20), unique=False, nullable=False)
    blood_qty = db.Column(db.Integer(), unique=False, nullable=False)  
    disease = db.Column(db.String(25), unique=False, nullable=False)
    tele = db.Column(db.Integer(), primary_key=True)
    city = db.Column(db.String(30), unique=False, nullable=False)

# -------------------adding user data in backend

@app.route("/user", methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        # id = request.form.get('id')
        uname = request.form.get('uname')
        uage = request.form.get('uage')
        blood_type = request.form.get('blood_type')
        blood_qty = request.form.get('blood_qty')
        disease = request.form.get('disease')
        tele = request.form.get('tele')
        city = request.form.get('city')

        entry =userinfo(uname=uname, disease=disease, uage=uage, blood_type=blood_type,blood_qty=blood_qty, tele=tele, city=city)

        db.session.add(entry)
        db.session.commit()

    return render_template('user/userlogin.html')


# ------------------show user data 

@app.route("/userdata")
def userdata():
     # fetch all entries from the userinfo table
    entries = userinfo.query.all()

    return render_template('user/userdata.html', entries=entries)


# ----------------------delete user data

@app.route('/user/delete/<int:tele>', methods=['POST'])
def user_delete_entry(tele):
    entry = userinfo.query.get(tele)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('userdata'))

# ---------------update user data

@app.route('/user/update/<int:tele>', methods=['GET', 'POST'])
def user_update_entry(tele):
    entry = userinfo.query.get(tele)
    if request.method == 'POST':
        entry.uname = request.form.get('uname')
        entry.uage = request.form.get('uage')
        entry.disease = request.form.get('disease')
        entry.blood_type = request.form.get('blood_type')
        entry.tele = request.form.get('tele')
        entry.city = request.form.get('city')
        db.session.commit()
        return redirect(url_for('userdata'))
    return render_template('user/userupdate.html', entry=entry)

# -----------------------show specific data of donar to user

@app.route("/avldata")
def avldata():
     # fetch all entries from the Blood table
    entries = Blood4.query.all()

    return render_template('user/avlblood.html', entries=entries)


    

if __name__ == '__main__':
    app.run(debug=True,port=7000)
