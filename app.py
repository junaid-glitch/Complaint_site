from flask import Flask, render_template, url_for, session, redirect,request
from datetime import datetime
import secrets
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy()
app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://jerry:jay4jerry2@localhost:3306/jerry"
app.config['SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


class Admin(db.Model):
    __tablename__='admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email= db.Column(db.String(50), nullable=False)
    password= db.Column(db.String(150), nullable=False)

class Teacher(db.Model):
    __tablename__='teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    qualification= db.Column(db.String(50), nullable=False)
    experience = db.Column(db.String(50), nullable=False)

class Students(db.Model):
    __tablename__='students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    fname = db.Column(db.String(50), nullable=False)
    gender= db.Column(db.String(50), nullable=False)
    pid= db.Column(db.Integer, nullable=False)
    sid= db.Column(db.Integer, nullable=False)
    phone= db.Column(db.String(50), nullable=False)
    email= db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Complaints(db.Model):
    __tablename__='complaints'
    id = db.Column(db.Integer, primary_key=True)
    subject= db.Column(db.String(50), nullable=False)
    stud_id= db.Column(db.Integer, nullable=False)
    against= db.Column(db.String(50), nullable=False)
    description= db.Column(db.String(500), nullable=False)
    date=db.Column(db.DATE, default=datetime.now())

class DptIssue(db.Model):
    __tablename__='dpt_issue'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)

class Sessions(db.Model):
    __tablename__='sessions'
    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.String(50), nullable=False)

class Programs(db.Model):
    __tablename__='programs'
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(50), nullable=False)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        char = request.form.get('char')
        if char=='admin':
            admin = Admin.query.filter_by(email=email, password=password).first()
            if admin:
                session['admin'] = admin.email
                session['id'] = admin.id
                return render_template('admin/index.html')
            else:
                return render_template("page-login.html")
        else:
            stud = Students.query.filter_by(email=email, password=password).first()
            if stud:
                session['stud'] = stud.email
                session['sid'] = stud.id
                return redirect(url_for('index'))
            else:
                error = 'Invalid Username or Password'
                return render_template("page-login.html", error=error)
    else:
        return render_template("page-login.html")

@app.route("/logoff", methods=['GET','POST'])
def logoff():
    session.clear()
    return redirect(url_for('login'))

@app.route("/", methods=['GET','POST'])
def index():
    if session.get('admin'):
        return render_template("admin/index.html")
    elif session.get('stud'):
        return render_template("index.html")
    else:
        return redirect(url_for('login'))


@app.route("/add_student", methods=['GET','POST'])
def add_student():
    if session.get('admin'):
        se=Sessions.query.all()
        prog=Programs.query.all()
        if request.method=='POST':
            name= request.form.get('name')
            fname= request.form.get('fname')
            gender= request.form.get('gender')
            program= request.form.get('program')
            ses= request.form.get('session')
            phone= request.form.get('phone')
            email= request.form.get('email')
            password= request.form.get('password')
            ns= Students(name=name, fname=fname, gender=gender, sid=ses,pid=program, phone=phone, email=email,password=password)
            db.session.add(ns)
            db.session.commit()
            return render_template("admin/add_student.html", se=se, prog=prog)
        else:
            return render_template("admin/add_student.html", se=se, prog=prog)
    else:
        return redirect(url_for('login'))

@app.route("/delete/student_id=<id>", methods=['GET','POST'])
def del_stud(id):
    if session.get('admin'):
        dele= db.session.query(Students).filter(Students.id==id).first()
        db.session.delete(dele)
        db.session.commit()
        return redirect(url_for('view_students'))
    else:
        return redirect(url_for('login'))

@app.route("/view_students", methods=['GET','POST'])
def view_students():
    if session.get('admin'):
        stud = db.session.query(Students, Sessions, Programs).filter(Students.sid == Sessions.id). \
            filter(Students.pid == Programs.id).all()
        return render_template("admin/view_students.html", stud=stud)
    else:
        return redirect(url_for('login'))


@app.route("/add_teacher", methods=['GET','POST'])
def add_teacher():
    if session.get('admin'):
        if request.method=='POST':
            tname= request.form.get('name')
            education= request.form.get('education')
            expe= request.form.get('exp')
            new= Teacher(name=tname, qualification=education, experience=expe)
            db.session.add(new)
            db.session.commit()
            return render_template("admin/add_teacher.html")
        else:
            return render_template("admin/add_teacher.html")
    else:
        return redirect(url_for('login'))

@app.route("/delete_teacher_id=<id>", methods=['GET','POST'])
def del_Teacher(id):
    if session.get('admin'):
        dele= db.session.query(Teacher).filter(Teacher.id==id).first()
        db.session.delete(dele)
        db.session.commit()
        return redirect(url_for('view_teachers'))
    else:
        return redirect(url_for('login'))


@app.route("/view_teachers", methods=['GET','POST'])
def view_teachers():
    if session.get('admin'):
        tchr = Teacher.query.all()
        return render_template("admin/view_teachers.html", tchr=tchr)
    else:
        return redirect(url_for('login'))


@app.route("/add_session", methods=['GET','POST'])
def add_session():
    if session.get('admin'):
        if request.method=='POST':
            ses= request.form.get('session')
            new= Sessions(session=ses)
            db.session.add(new)
            db.session.commit()
            return render_template("admin/add_session.html")
        else:
            return render_template("admin/add_session.html")
    else:
        return redirect(url_for('login'))

@app.route("/delete_sessions_id=<id>", methods=['GET','POST'])
def del_Sessions(id):
    if session.get('admin'):
        dele= db.session.query(Sessions).filter(Sessions.id==id).first()
        db.session.delete(dele)
        db.session.commit()
        return redirect(url_for('view_sessions'))
    else:
        return redirect(url_for('login'))

@app.route("/issue", methods=['GET','POST'])
def add_issue():
    if session.get('admin'):
        if request.method=='POST':
            dprob= request.form.get('dptprob')
            newissue= DptIssue(subject=dprob)
            db.session.add(newissue)
            db.session.commit()
            return render_template("admin/add_issue.html")
        else:
            return render_template("admin/add_issue.html")
    else:
        return redirect(url_for('login'))

@app.route("/view_issues", methods=['GET','POST'])
def view_issues():
    if session.get('admin'):
        dpt= DptIssue.query.all()
        return render_template("admin/view_issue.html", dpt=dpt)
    else:
        return redirect(url_for('login'))

@app.route("/view_sessions", methods=['GET','POST'])
def view_sessions():
    if session.get('admin'):
        sesion = Sessions.query.all()
        return render_template("admin/view_sessions.html", sesion=sesion)
    else:
        return redirect(url_for('login'))



@app.route("/add_programs", methods=['GET','POST'])
def add_program():
    if session.get('admin'):
        if request.method == 'POST':
            prog = request.form.get('program')
            new = Programs(program=prog)
            db.session.add(new)
            db.session.commit()
            return render_template("admin/add_program.html")
        else:
            return render_template("admin/add_program.html")
    else:
        return redirect(url_for('login'))

@app.route("/delete_program_id=<id>", methods=['GET','POST'])
def del_Programs(id):
    if session.get('admin'):
        dele= db.session.query(Programs).filter(Programs.id==id).first()
        db.session.delete(dele)
        db.session.commit()
        return redirect(url_for('view_programs'))
    else:
        return redirect(url_for('login'))

@app.route("/view_programs", methods=['GET','POST'])
def view_programs():
    if session.get('admin'):
        prog = Programs.query.all()
        return render_template("admin/view_programs.html", prog=prog)
    else:
        return redirect(url_for('login'))


@app.route("/complaints_history", methods=['GET','POST'])
def complaints_history():
    if session.get('admin'):
        comps= db.session.query(Complaints, Students, Sessions, Programs)\
            .filter(Complaints.stud_id==Students.id).filter(Students.sid==Sessions.id)\
            .filter(Students.pid==Programs.id).all()
        return render_template("admin/view_complaints.html", comps=comps)
    else:
        return redirect(url_for('login'))

@app.route("/read_complaint/<id>", methods=['GET','POST'])
def read_complain(id):
    if session.get('admin'):
        compl= db.session.query(Complaints, Students, Sessions, Programs)\
            .filter(Complaints.id==id)\
            .filter(Complaints.stud_id==Students.id).filter(Students.sid==Sessions.id)\
            .filter(Students.pid==Programs.id).first()
        return render_template("admin/tbls.html", compl=compl)
    else:
        return redirect(url_for('login'))


# Student Side

@app.route("/new_complain", methods=['GET','POST'])
def new_complain():
    if session.get('stud'):
        teachs=Teacher.query.all()
        dps= DptIssue.query.all()
        if request.method=='POST':
            subject= request.form.get('subject')
            against=request.form.get('against')
            description=request.form.get('description')
            new= Complaints(subject=subject, against=against, description=description, stud_id=session.get('sid'), date=datetime.now())
            db.session.add(new)
            db.session.commit()
            return render_template("add_complaint.html",teachs=teachs, dps=dps)
        else:
            return render_template("add_complaint.html", teachs=teachs, dps=dps)
    else:
        return redirect(url_for('login'))

@app.route("/my_complaints", methods=['GET','POST'])
def my_complaint():
    mycomp= db.session.query(Students,Complaints).filter(Complaints.stud_id==session.get('sid')).filter(Complaints.stud_id==Students.id).all()
    return render_template("complaints.html", mycomp=mycomp)

if __name__ == "__main__":
    app.run(debug=True, port=2002)
