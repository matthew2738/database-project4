import pandas as pd
import json
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uni_db_p4.db'
db = SQLAlchemy(app)

'''
, ForeignKey('students.student_id')
, ForeignKey('classes.class_id')

'''
class Enrolled(db.Model):

    __tablename__ = 'enrolled'

    enrolled_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    class_id = db.Column(db.Integer)
    semester = db.Column(db.String(10), nullable=False)
    year = db.Column(db.Integer)
    grade =  db.Column(db.String(1))

    def __repr__ (self):
        return f"{self.semester} - {self.year} - {self.grade}"

class Student(db.Model):
    
    __tablename__ = 'students'
    
    student_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True, nullable=False)
    grade_level = db.Column(db.String(10), nullable=False)
    fname = db.Column(db.String(10), nullable=False)
    lname = db.Column(db.String(10), nullable=False)
    major = db.Column(db.String(20), nullable=False)
    gpa = db.Column(db.Float)

    #classes_attending = relationship("Class", secondary=Enrolled, back_populates="students_attending")

    def __repr__ (self):
        return f"{self.fname} - {self.lname} - {self.grade_level} - {self.major}"

class Teacher(db.Model):

    __tablename__ = 'teachers'

    teacher_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    college = db.Column(db.String(20))
    #classes = db.relationship('Class', backref='teachers', lazy=True)

    def __repr__ (self):
        return f"{self.fname} - {self.lname} - {self.email}"

class Class(db.Model):

    __tablename__ = 'classes'
#, ForeignKey("teachers.teacher_id")
    class_id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer )
    class_name = db.Column(db.String(20), nullable=False)
    class_time = db.Column(db.String(20), nullable=False)
    
    #professor = relationship("Teacher", backref=backref("request", uselist=False))
    
    #students_attending = relationship("Student", secondary=Enrolled, back_populates="classes_attending")

    def __repr__ (self):
        return f"{self.class_name} - {self.class_time}"

class Admin(db.Model):

    __tablename__ = 'admin'

    admin_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    occupation = db.Column(db.String(20), nullable=False)

    def __repr__ (self):
        return f"{self.fname} - {self.lname} - {self.email} - {self.phone_number} - {self.occupation}"

class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(1), nullable=False)

    def __repr__ (self):
        return f"{self.username} - {self.status}"


def populate_students():
    df = pd.read_csv('file:StudentDatabase.txt', header=0, sep=',')
    #print(df.head())
    for index, row in df.iterrows():
        s = Student( 
            student_id = row['student_id'],
            email = row['email'],
            grade_level = row['grade_level'],
            fname =  row['first'],
            lname =  row['last'],
            major =  row['major'],
            gpa =  row['gpa']
        )
        print(s)
        db.session.add(s)
        db.session.commit()
    

def populate_teachers():
    df = pd.read_csv('file:TeacherDatabase.txt', header=0, sep=',')
    print(df.head())
    for index, row in df.iterrows():
        t = Teacher( 
            teacher_id = row['teacher_id'],
            email = row['email'],
            college = row['department'],
            fname =  row['first'],
            lname =  row['last'],
        )
        print(t)
        db.session.add(t)
        db.session.commit()

def populate_classes():
    df = pd.read_csv('file:ClassDatabase.txt', header=0, sep=',')
    #print(df.head())
    for index, row in df.iterrows():
        c = Class( 
            class_id = row['class_id'],
            teacher_id = row['teacher_id'],
            class_name = row['name'],
            class_time =  row['time'],
        )
        print(c)
        db.session.add(c)
        db.session.commit()

def populate_enrolled():
    df = pd.read_csv('file:EnrolledDatabase.txt', header=0, sep=',')
    print(df.head())
    for index, row in df.iterrows():
        e = Enrolled( 
            student_id = row['student_id'],
            class_id = row['class_id'],
            semester = row['Semester'],
            year =  row['year'],
            grade =  row['grade'],
        )
        print(e)
        db.session.add(e)
        db.session.commit()

def populate_admin():
    df = pd.read_csv('file:AdminDatabase.txt', header=0, sep=',')
    print(df.head())
    for index, row in df.iterrows():
        a = Admin( 
            admin_id = row['admin_id'],
            fname = row['first'],
            lname = row['last'],
            email =  row['email'],
            phone_number =  row['phone'],
            occupation = row['occupation']
        )
        print(a)
        db.session.add(a)
        db.session.commit()

def populate_users():
    df = pd.read_csv('file:UserDatabase.txt', header=0, sep=',')
    print(df.head())
    for index, row in df.iterrows():
        u = User( 
            user_id = row['uid'],
            username = row['username'],
            password = row['password'],
            status =  row['type'],
        )
        print(u)
        db.session.add(u)
        db.session.commit()

def main():

   # populate_students()
   # populate_teachers()
   # populate_classes()
   # populate_enrolled()
   # populate_admin()
   populate_users()

if __name__ == "__main__":
    main()



@app.route("/")
def home():
    return "Hello, This is the API for the Database Class"

@app.route('/students')
def get_students():
    students = Student.query.all()
    
    output = []
    for stud in students:
        stud_data = {
            'student_id': stud.student_id,
            'fname': stud.fname, 
            'lname': stud.lname,
            'grade_level': stud.grade_level,
            'major': stud.major,
            'email': stud.email
            }
        output.append(stud_data)
    return {"students" : output}

@app.route('/classes')
def get_classes():
    clss = Class.query.all()
    
    output = []
    for c in clss:
        class_data = {
            'class_id': c.class_id,
            'class_name': c.class_name, 
            'class_time': c.class_time
            }
        output.append(class_data)
    return {"classes" : output}

@app.route('/teachers')
def get_teachers():
    teachers = Teacher.query.all()
    
    output = []
    for teacher in teachers:
        teacher_data = {
            'teacher_id': teacher.teacher_id,
            'fname': teacher.fname, 
            'lname': teacher.lname,
            'college': teacher.college,
            'email': teacher.email
            }
        output.append(teacher_data)
    return {"teachers" : output}

@app.route('/enrolled')
def get_enrolled():
    enrolled = Enrolled.query.all()
    
    output = []
    for e in enrolled:
        e_data = {
            'semester': e.semester,
            'year': e.year, 
            'grade': e.grade
            }
        output.append(e_data)
    return {"enrolled" : output}

@app.route('/admins')
def get_admins():
    admins = Admin.query.all()
    
    output = []
    for admin in admins:
        admin_data = {
            'admin_id': admin.admin_id,
            'fname': admin.fname, 
            'lname': admin.lname,
            'occupation': admin.occupation,
            'email': admin.email,
            'phone_number': admin.phone_number
            }
        output.append(admin_data)
    return {"admins" : output}

@app.route('/api/getUser/login')
def get_user():
    username = request.args.get('username')
    pw = request.args.get('password')
    print(username)
    print(pw)
    user = User.query.filter_by(username='LeeGL40@usf.edu').all()
    print(user)
    
    #if user.password != pw:
    #    return {"error" : "Incorrect Password"}
    
    if user is None:
        return {"error": "Incorrect Username"}
    output = []
    for u in user:
        user_data = {
            'user_id' : u.user_id,
            'username' : u.username,
            'password' : u.password,
            'status' : u.status
        }
        output.append(user_data)
    return {"User": output}
'''
@app.route('/students', methods=['POST'])
def add_student():
    student = Student( student_id=request.json['student_id'],
                fname=request.json['fname'],
                lname=request.json['lname'],
                email=request.json['email'],
                grade_level=request.json['grade_level'],
                major=request.json['major'],
                gpa=request.json['gpa'] )
    db.session.add(student)
    db.session.commit()
    return {'id': student.student_id}

@app.route('/classes', methods=['POST'])
def add_class():
    c = Class(class_id=request.json['class_id'],
                class_name=request.json['class_name'],
                class_time=request.json['class_time'] )
    db.session.add(c)
    db.session.commit()
    return {'id': c.class_id}

@app.route('/teachers', methods=['POST'])
def add_teacher():
    teacher = Teacher(teacher_id=request.json['teacher_id'],
                fname=request.json['fname'],
                lname=request.json['lname'],
                college=request.json['college'],
                email=request.json['email'] )
    db.session.add(teacher)
    db.session.commit()
    return {'id': teacher.teacher_id}


@app.route('/enrolled', methods=['POST'])
def add_enrolled():
    post = Post(title=request.json['title'],
                image=request.json['image'],
                zip=request.json['zip'],
                city=request.json['city'],
                category=request.json['category'],
                postdate=request.json['postdate'],
                startdate=request.json['startdate'],
                enddate=request.json['enddate'],
                description=request.json['description'])
    db.session.add(post)
    db.session.commit()
    return {'id': post.id}


@app.route('/admins', methods=['POST'])
def add_admin():
    admin = Admin(admin_id=request.json['admin_id'],
                email=request.json['email'],
                fname=request.json['fname'],
                lname=request.json['lname'],
                phone_number=request.json['phone_number'],
                occupation=request.json['occupation'] )
    db.session.add(admin)
    db.session.commit()
    return {'id': admin.admin_id}

'''
