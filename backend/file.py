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

#Initiate Learning Journey class
class LearningJourney(db.model):
    __tablename__ = 'LearningJourney'
    LearningJourney_id = db.Column(db.Integer, primary_key = True)
    role_code = db.Column(db.Integer)
    course_code = db.Column(db.Integer)

    def __init__(self, LearningJourney_id, role_code, course_code):
        self.LearningJourney_id = LearningJourney_id
        self.role_code = role_code
        self.course_code = course_code
    
    def json(self):
        return {"LearningJourney_id": self.LearningJourney_id, 
                "role_code": self.role_code,
                "courde_code": self.role_code}





@app.route("/learningjourney", methods=['POST'])
#essentially, for every new course that is added to a learning journey, a new record is created
def add_new_course(): 
    data = request.get_json()
    if not all(key in data.keys() for 
                key in ('LearningJourney_id', 'role_code', 'course_code')):
        return  jsonify({
            'message': "Incorrect JSON object provided"
        }), 500
    
    #create new record in the lj table
    new_course = LearningJourney(LearningJourney = data['LearningJourney_id'], role_code = data['role_code'], course_code = data['course_code'])

    # commit to DB
    try:
        db.session.add(new_course)
        db.session.commit()
        return jsonify(new_course.to_dict()), 201
    except Exception:
        return jsonify({
            'message': "Unable to commit to database"
        }), 500





#last line of the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

