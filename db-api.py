import json
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True, nullable=False)
    grade_level = db.Column(db.String(10), nullable=False)
    fname = db.Column(db.String(10), nullable=False)
    lname = db.Column(db.String(10), nullable=False)
    major = db.Column(db.String(20), nullable=False)
    gpa = db.Column(db.Float)

    def __repr__ (self):
        return f"{self.fname} - {self.lname} - {self.grade_level} - {self.major}"

'''
class Enrolled(db.Model):
    #student_id = db.Column(db.Integer, primary_key=True)
    #class_id = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.String(10), nullable=False)
    year = db.Column(db.Integer)
    grade =  db.Column(db.Integer)

    def __repr__ (self):
        return f"{self.semester} - {self.year} - {self.grade}"
'''

class Class(db.Model):
    class_id = db.Column(db.Integer, primary_key=True)
    #teacher_id = db.Column(db.Integer, foriegn_key=True)
    class_name = db.Column(db.String(20), nullable=False)
    class_time = db.Column(db.String(20), nullable=False)

    def __repr__ (self):
        return f"{self.class_name} - {self.class_time}"

class Teacher(db.Model):
    teacher_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    college = db.Column(db.String(20))

    def __repr__ (self):
        return f"{self.fname} - {self.lname} - {self.email}"

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    occupation = db.Column(db.String(20), nullable=False)

    def __repr__ (self):
        return f"{self.fname} - {self.lname} - {self.email} - {self.phone_number} - {self.occupation}"

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __repr__ (self):
        return f"{self.username} - {self.status}"

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

'''
@app.route("/posts/<id>")
def get_post(id):
    post = Post.query.get_or_404(id)
    return {"title": post.title, "description": post.description}
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

'''
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
'''

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
@app.route('/posts/<id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    if post is None:
        return {"error": "not found"}
    db.session.delete(post)
    db.session.commit()
    return {"message": "Deleted"}
'''