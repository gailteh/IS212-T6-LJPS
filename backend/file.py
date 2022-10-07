#create flask app
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root' + \
                                        # '@localhost:3306/ <fill with the database filename>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

#Create Learning Journey class
class LearningJourney(db.model):
    __tablename__ = 'LearningJourney'
    LearningJourney_id = db.Column(db.Integer, primary_key = True)
    course_code = db.Column(db.Integer)
    role_code = db.Column(db.Integer)


#last line of the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

