# AUTHOR: Tyler Wilson
# Student ID: 100773241
# for: AIDI-2004 - AI in Enterprise Systems
# Assignment: Assignment 3 - Flask

from flask import Flask, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import os

# Init app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////instance/student.db'
# Init database
db = SQLAlchemy(app)
# Init Marshmallow
ma = Marshmallow(app)


# Student Model
class Student(db.Model):
    student_id = db.Column(db.String(9), primary_key=True, unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(100), nullable=False)
    amount_due = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, student_id, first_name, last_name, dob, amount_due):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.amount_due = amount_due

    with app.app_context():
        db.create_all()
        # print('stuff')


# Student Schema
class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True

    dob = fields.Date(required=True)


# Init Schema
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)


# Create a Student
@app.route('/test')
def test_server():
    test_string = "The server is running"
    appname = str(app.name)
    print(test_string + " " + appname)
    return "<p>The server is okay</p>"


# Create a Student
@app.route('/student', methods=['POST'])
def add_student():
    student_id = request.json['student_id']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    dob = request.json['dob']
    amount_due = request.json['amount_due']

    new_student = Student(student_id, first_name, last_name, dob, amount_due)

    db.session.add(new_student)
    db.session.commit()

    return student_schema.jsonify(new_student)


# Get All Students
@app.route('/student', methods=['GET'])
def get_students():
    all_students = Student.query.all()
    return students_schema.jsonify(all_students)


# Get Single Student
@app.route('/student/<id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if student:
        return student_schema.jsonify(student)
    else:
        return jsonify({"message": "Student not found"}), 404


# Update a Student
@app.route('/student/<id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if student:
        student.student_id = request.json['student_id']
        student.first_name = request.json['first_name']
        student.last_name = request.json['last_name']
        student.dob = request.json['dob']
        student.amount_due = request.json['amount_due']

        db.session.commit()

        return student_schema.jsonify(student)
    else:
        return jsonify({"message": "Student not found"}), 404


# Delete a Student
@app.route('/student/<id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()

        return student_schema.jsonify(student)
    else:
        return jsonify({"message": "Student not found"}), 404


# Run server
if __name__ == '__main__':
    app.run(debug=True)
    print(f'Current App: {current_app.name}')
    # Setup database

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.create_all()
