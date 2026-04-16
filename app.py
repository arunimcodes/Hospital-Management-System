from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Ensure the database path is correct
db_path = os.path.join(os.path.dirname(__file__), 'Healthcare.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 1. Map the model to your friend's exact table: "healthcare_appointments"
class HealthcareAppointment(db.Model):
    __tablename__ = 'healthcare_appointments'
    # Since SQLite raw didn't show a primary key, we'll treat patient_name as one for now 
    # OR you can add a primary key if you modify the DB later.
    patient_name = db.Column(db.String, primary_key=True) 
    age = db.Column(db.Integer)
    doctor_speciality = db.Column(db.String)
    appointment_date = db.Column(db.String)
    payment_method = db.Column(db.String)

@app.route('/')
def index():
    # Serves your i.html file
    return render_template('i.html')

@app.route('/book', methods=['POST'])
def book_appointment():
    try:
        data = request.json
        
        # Create a new record using the data sent from the HTML script
        new_appointment = HealthcareAppointment(
            patient_name=data['name'],
            age=int(data['age']),
            doctor_speciality=data['speciality'],
            appointment_date=data['date'],
            payment_method=data['payment']
        )
        
        db.session.add(new_appointment)
        db.session.commit()
        
        return jsonify({"status": "success", "message": "Data saved to Healthcare.db!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)