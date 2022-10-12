from mimetypes import init
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey

app = Flask(__name__)
# initiate database connection
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@localhost:8889/learning-journey"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

# initiate classes: Course, learning journey
class Courses(db.Model):
    __tablename__ = 'courses'

    course_code = db.Column(db.String, primary_key=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String, nullable=False)

    def __init__(self, course_code, course_name, course_description):
        self.course_code = course_code
        self.course_name = course_name
        self.course_description = course_description

    def json(self):
        return {"course_code": self.course_code,"course_name":self.course_name, "course_description": self.course_description}

class Role(db.Model):
    __tablename__ = 'roles'

    role_code = db.Column(db.Integer, primary_key=True, nullable=False)
    role_name = db.Column(db.String, nullable=False)
    role_desc = db.Column(db.String, nullable=False)

    def __init__(self, role_code, role_name, role_desc):
        self.role_code = role_code
        self.role_name = role_name
        self.role_desc = role_desc


    def json(self):
        return {"role_code":self.role_code, "role_name":self.role_name, "role_desc":self.role_desc}

## not needed for now
# class Staff(db.Model):
#     __tablename__ = 'staff'

#     staff_id = db.Column(db.Integer, primary_key=True, nullable=False)
#     staff_name = db.Column(db.String, nullable=False)

#     def __init__(self, staff_id, staff_name):
#         self.staff_id = staff_id
#         self.staff_name = staff_name

#     def json(self):
#         return {"staff_id": self.staff_id, "staff_name": self.staff_name}


class Learning_Journey(db.Model):
    __tablename__ = 'learning-journey'

    LearningJourney_id = db.Column(db.Integer, primary_key=True, nullable=False)
    course_code = db.Column(db.String, ForeignKey('course.course_code'), nullable = False)
    role_code = db.Column(db.Integer, ForeignKey('role.role_code'), nullable = False)

    def __init__(self, LearningJourney_id, course_code, role_code):
        self.LearningJourney_id = LearningJourney_id
        self.course_code = course_code
        self.role_code = role_code


    def json(self):
        return {"LearningJourney_id":self.LearningJourney_id, "course_code":self.course_code, "role_code": self.role_code}


@app.route('/learning_journey/<int:LearningJourney_id>/<string:course_code>', methods=['DELETE'])
# deleting 1 course from learning journey
def del_course_from_learning_journey(LearningJourney_id, course_code):
    
    #  get learning journey row using LearningJourney_id and course_code
    lj_course = Learning_Journey.query.filter_by(LearningJourney_id=LearningJourney_id, course_code=course_code).first()

    # delete
    try:
        db.session.delete(lj_course)
        db.session.commit()
    except:
        return {
            "code": 500,
            "data": {
                "lj_course": lj_course
            },
            "message": "An error occurred while deleting the course from learning journey"
        }
    return {
        "code": 200,
        "message": str(lj_course) + " had been successfully deleted."
    }

if __name__ == '__main__':
    app.run(port=4999, debug=True)