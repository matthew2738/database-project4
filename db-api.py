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

    def getFullName(self):
        return f"{self.fname} {self.lname}"

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
    def getFullName(self):
        return f"{self.fname} {self.lname}"

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

'''
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
   # populate_users()

if __name__ == "__main__":
    main()
'''

# Home Page
@app.route("/")
def home():
    return "Hello, This is the API for the Database Class"

# Queries to retrieve all data of a table
@app.route('/api/students')
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

@app.route('/api/enrolled')
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


@app.route('/api/admins')
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

@app.route('/api/classes')
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

@app.route('/api/teachers')
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

# Student -> get Classes for sem/year that you are enrolled in
@app.route('/api/students/classes', methods=['GET'])
def get_StudSemYrClasses():
    sid = request.args.get('student_id')
    sem = request.args.get('semester')
    yr = request.args.get('year')

    stud_classes = Enrolled.query.filter_by(student_id=sid, semester=sem, year=yr).all()
    if stud_classes is None:
        return {"error": "No Current Information"}
    output = []
    for sc in stud_classes:
        cid = sc.class_id
        class_info = Class.query.filter_by(class_id=cid).first()
        data = {
            'Class Name' : class_info.class_name,
            'Grade' : sc.grade,
            'Semester' : sc.semester,
            'Year' : sc.year
        }
        output.append(data)
    return {"Student Classes": output}

# Student -> Queries all classes he has taken w/ GPA
@app.route('/api/students/allClasses', methods=['GET'])
def get_StudAllClasses():
    sid = request.args.get('student_id')

    enrolled_query = Enrolled.query.filter_by(student_id=sid).all()
    stud_query = Student.query.filter_by(student_id=sid).first()
    
    if stud_query is None:
        return {"error": "Invalid Student ID"}
    
    output = []
    
    output.append({ 'GPA' : stud_query.gpa })
    for e_data in enrolled_query:
        cid = e_data.class_id
        class_data = Class.query.filter_by(class_id=cid).first()
        data = {
            'Class Name' : class_data.class_name,
            'Grade' : e_data.grade,
            'Semester' : e_data.semester,
            'Year' : e_data.year
        }
        output.append(data)
    return {"All Classes": output}

# Student -> Query for a teacher by name and return their info
@app.route('/api/students/find/teacher')
def get_TeacherByName():
    fname = request.args.get("fname")
    lname = request.args.get("lname")

    teacher_query = Teacher.query.filter_by(fname=fname, lname=lname).all()
    if teacher_query is None:
        return {"error" : "Teacher Not Found"}
    output = []
    for t_data in teacher_query:
        data = {
            'Teacher Name' : t_data.getFullName(),
            'Teacher Email' : t_data.email,
            'Teacher College' : t_data.college
        }
        output.append(data)
    return {"Teacher" : output}

# Teacher -> Searches a class he is teaching and gets student info
@app.route('/api/teachers/class/info/<tid>/<cid>', methods=['GET'])
def get_StudentsFromClass(tid, cid):
    enrolled_query = Enrolled.query.filter_by(class_id=cid, teacher_id=tid).all()

    if enrolled_query is None:
        return {"error": "Class Not Found"}
    
    output = []
    for e_data in enrolled_query:
        sid = e_data.student_id
        stud_data = Student.query.filter_by(student_id=sid).first()
        
        data = {
            'Student Name' : stud_data.getFullName(),
            'Student ID' : stud_data.student_id,
            'Grade' : e_data.grade,
        }
        output.append(data)
    return {"Students": output}

# Teacher -> Search for a student and return their info
@app.route('/api/teachers/student/<sid>', methods=['GET'])
def get_StudentInfo(sid):
    stud_data = Student.query.filter_by(student_id=sid).first()

    if stud_data is None:
        return {"error" : "Student Not Found"}
    output = []
    data = {
        'Student Name' : stud_data.getFullName(),
        'Student Email' : stud_data.email,
        'Student ID' : stud_data.student_id,
        'Student Major' : stud_data.major
    }
    output.append(data)
    return {"Student" : output}

# Admin -> Search for student in a class and remove them
@app.route('/api/admins/remove/<sid>/<cid>', methods=['DELETE'])
def delete_StudentFromClass(sid, cid):

    enrolled_info = Enrolled.query.filter_by(student_id=sid, class_id=cid).first()

    if enrolled_info is None:
        return {"error" : "Student Not Found"}
    db.session.delete(enrolled_info)
    db.session.commit()
    return { "message" :  "Student Removed" }

# Admin -> Add an existing student to a class
@app.route('/api/admins/add/student/<sid>/<cid>', methods=['POST'])
def add_StudentToClass(sid, cid):
    stud_data = Student.query.get(sid)
    if stud_data is None:
        return {"error" : "Student Not Found"}
    class_data = Class.query.get(cid)
    if class_data is None:
        return {"error" : "Class Not Found"}
    new_stud = Enrolled(
        student_id=stud_data.student_id,
        class_id=class_data.class_id,
        semester="Fall",
        year=2021,
        grade="A"
    )
    db.session.add(new_stud)
    db.session.commit()
    return { "message" : "Student Successfully Added" }

# Admin -> Change an teachers for a class with an existing teacher
@app.route('/api/admins/add/teacher/<tid>/<cid>')
def add_TeacherToClass(tid, cid):
    class_data = Class.query.get(cid)
    if class_data is None:
        return {"error" : "Class Not Found"}
    teacher_data = Teacher.query.get(tid)
    if teacher_data is None:
        return {"error" : "Teacher Not Found"}
    
    db.session.delete(class_data)
    db.session.commit()

    new_class = Class(
        class_id=class_data.class_id,
        teacher_id = teacher_data.teacher_id,
        class_name = class_data.class_name,
        class_time = class_data.class_time
    )
    db.session.add(new_class)
    db.session.commit()
    return {"message" : "Teacher Successfully Added"}

# Admin -> Search for a class and returns info with teacher info
@app.route('/api/admins/search/class/<cid>', methods=['GET'])
def get_ClassTeacherInfo(cid):
    
    class_data = Class.query.get(cid)
    if class_data is None:
        return {"error" : "Class Not Found"}
    
    teacher_data = Teacher.query.get(class_data.teacher_id)
    if teacher_data is None:
        return {"error" : "Teacher Not Found"}

    output = []
    data = {
        'Class Name' : class_data.class_name,
        'Class ID' : class_data.class_id,
        'Teacher Name' : teacher_data.getFullName(),
        'Teacher Email': teacher_data.email,
        'Teacher ID' : teacher_data.teacher_id
    }
    output.append(data)
    return {"Class Info" : output}

# Get a login information
@app.route('/api/getUser/login/<un>/<pw>')
def get_user(un, pw):
    user = User.query.filter_by(username=un, password=pw).first()
    
    if user is None:
        return {"error": "Invalid Login"}
    
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
