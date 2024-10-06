#Task 1:Setting Up Flask with Flask-SQLAlchemy
#python -m venv venv
#venv\Scripts\activate
#pip install Flask Flask-SQLAlchemy Flask-Marshmallow
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:your_password@localhost/fitness_center_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define your models
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class WorkoutSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    session_date = db.Column(db.DateTime, nullable=False)
    workout_type = db.Column(db.String(100), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

#Task 2: Implementing CRUD Operations for Members Using ORM
@app.route('/members', methods=['POST'])
def add_member():
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    
    new_member = Member(name=name, email=email, phone=phone)
    db.session.add(new_member)
    db.session.commit()
    
    return {"message": "Member added successfully"}, 201

@app.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return jsonify([{
        "id": member.id, 
        "name": member.name, 
        "email": member.email, 
        "phone": member.phone
    } for member in members])

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    member = Member.query.get(id)
    if not member:
        return {"message": "Member not found"}, 404
    
    member.name = request.json.get('name', member.name)
    member.email = request.json.get('email', member.email)
    member.phone = request.json.get('phone', member.phone)
    db.session.commit()
    
    return {"message": "Member updated successfully"}, 200

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get(id)
    if not member:
        return {"message": "Member not found"}, 404
    
    db.session.delete(member)
    db.session.commit()
    
    return {"message": "Member deleted successfully"}, 200

#Task 3: Managing Workout Sessions with ORM
@app.route('/workouts', methods=['POST'])
def add_workout():
    member_id = request.json['member_id']
    session_date = request.json['session_date']
    workout_type = request.json['workout_type']
    
    new_workout = WorkoutSession(member_id=member_id, session_date=session_date, workout_type=workout_type)
    db.session.add(new_workout)
    db.session.commit()
    
    return {"message": "Workout session added successfully"}, 201

@app.route('/members/<int:member_id>/workouts', methods=['GET'])
def get_workouts_for_member(member_id):
    workouts = WorkoutSession.query.filter_by(member_id=member_id).all()
    return jsonify([{
        "id": workout.id,
        "session_date": workout.session_date,
        "workout_type": workout.workout_type
    } for workout in workouts])
