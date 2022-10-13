#create flask app
from email import message
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/is212_spm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

#Initiate Course Class
class Course(db.Model):
    __tablename__ = 'course'

    course_code = db.Column(db.String,primary_key = True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_desc = db.Column(db.String, nullable=False)
    course_status = db.Column(db.String, nullable=False)

    def __init__(self, course_code, course_name, course_desc, course_status):
        self.course_code = course_code
        self.course_name = course_name
        self.course_desc = course_desc
        self.course_status = course_status
    
    def json(self):
        return {"course_code": self.course_code,
                'course_name': self.course_name,
                'course_desc': self.course_desc,
                'course_status': self.course_status}

#Initiate Role Class
class Role(db.Model):
    __tablename__ = 'role'

    role_code = db.Column(db.Integer, primary_key=True, nullable=False)
    role_name = db.Column(db.String, nullable=False)
    role_desc = db.Column(db.String, nullable=False)

    def __init__(self, role_code, role_name, role_desc):
        self.role_code = role_code
        self.role_name = role_name
        self.role_desc = role_desc


    def json(self):
        return {"role_code":self.role_code, 
                "role_name":self.role_name, 
                "role_desc":self.role_desc}


#Initiate Learning Journey class
class LearningJourney(db.Model):
    __tablename__ = 'learningjourney'
    LearningJourney_id = db.Column(db.Integer, primary_key = True, nullable= False)
    course_code = db.Column(db.String, ForeignKey('course.course_code'), primary_key = True, nullable = False)
    role_code = db.Column(db.Integer, ForeignKey('role.role_code'), primary_key = True, nullable = False)
    

    def __init__(self, LearningJourney_id, role_code, course_code):
        self.LearningJourney_id = LearningJourney_id
        self.course_code = course_code
        self.role_code = role_code
        
    
    def json(self):
        return {"LearningJourney_id": self.LearningJourney_id, 
                "course_code": self.role_code,
                "role_code": self.role_code
                }


@app.route("/learning_journey", methods=['POST'])
#For every new course that is added to a learning journey, a new record is created
def add_new_course(): 
    data = request.get_json()

    if not all(key in data.keys() for 
                key in ('LearningJourney_id', 'course_code', 'role_code')):
        return  jsonify({
            'message': "Incorrect JSON object provided"
        }), 500
    
    #create new record in the lj table
    new_course = LearningJourney(LearningJourney_id = data['LearningJourney_id'], course_code = data['course_code'], role_code = data['role_code'])

    # commit to DB
    try:
        db.session.add(new_course)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({
            "message": "Unable to commit to database"
        }), 500

    return jsonify({
        "Status": "Success"
    }),201






if __name__ == '__main__':
    app.run(port=5000, debug=True)

