from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Create the Flask application
app = Flask(__name__)

# Configure the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connect SQLAlchemy to Flask
db = SQLAlchemy(app)


# Create the Student database model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    course = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "course": self.course
        }


# Home route
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Student Management API!",
        "status": "Application is running successfully"
    })


# Add a new student
@app.route("/students", methods=["POST"])
def create_student():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    name = data.get("name")
    email = data.get("email")
    course = data.get("course")

    if not all(isinstance(value, str) and value.strip()
               for value in (name, email, course)):
        return jsonify({
            "error": "Name, email, and course are required"
        }), 400

    name = name.strip()
    email = email.strip().lower()
    course = course.strip()

    if len(name) < 2 or len(name) > 100:
        return jsonify({"error": "Name must be 2-100 characters"}), 400

    if len(email) > 120 or "@" not in email or "." not in email.split("@")[-1]:
        return jsonify({"error": "Please provide a valid email"}), 400

    if len(course) < 2 or len(course) > 100:
        return jsonify({"error": "Course must be 2-100 characters"}), 400

    existing_student = Student.query.filter_by(email=email).first()

    if existing_student:
        return jsonify({"error": "Email already exists"}), 409

    student = Student(name=name, email=email, course=course)

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student created successfully",
        "student": student.to_dict()
    }), 201


# Get all students
@app.route("/students", methods=["GET"])
def get_students():
    students = Student.query.order_by(Student.id).all()

    return jsonify([
        student.to_dict() for student in students
    ]), 200


# Get one student by ID
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = db.session.get(Student, student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student.to_dict()), 200


# Update a student
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    student = db.session.get(Student, student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    name = data.get("name")
    email = data.get("email")
    course = data.get("course")

    if not all(isinstance(value, str) and value.strip()
               for value in (name, email, course)):
        return jsonify({
            "error": "Name, email, and course are required"
        }), 400

    name = name.strip()
    email = email.strip().lower()
    course = course.strip()

    if len(name) < 2 or len(name) > 100:
        return jsonify({"error": "Name must be 2-100 characters"}), 400

    if len(email) > 120 or "@" not in email or "." not in email.split("@")[-1]:
        return jsonify({"error": "Please provide a valid email"}), 400

    if len(course) < 2 or len(course) > 100:
        return jsonify({"error": "Course must be 2-100 characters"}), 400

    duplicate = Student.query.filter(
        Student.email == email,
        Student.id != student_id
    ).first()

    if duplicate:
        return jsonify({"error": "Email already exists"}), 409

    student.name = name
    student.email = email
    student.course = course

    db.session.commit()

    return jsonify({
        "message": "Student updated successfully",
        "student": student.to_dict()
    }), 200


# Delete a student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = db.session.get(Student, student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({
        "message": "Student deleted successfully"
    }), 200


# Create database tables
with app.app_context():
    db.create_all()


# Run the application
if __name__ == "__main__":
    app.run(debug=True)