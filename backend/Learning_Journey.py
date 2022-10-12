
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey
import json

'''
Assumed JSON:
{"LearningJourney_id": , "course_ID", "staff_id"}
'''

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root' + \
                                        '@localhost:3306/is212_spm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

# initiate classes: Course, learning journey
class Course(db.Model):
    __tablename__ = 'Course'
    course_name = db.Column(db.String, nullable=False)

    course_code = db.Column(db.String, primary_key=True, nullable=False)
    course_desc = db.Column(db.String, nullable=False)
    course_status = db.Column(db.String, nullable=False)

    def __init__(self, course_name, course_code, course_desc, course_status):
        self.course_name = course_name
        self.course_code = course_code
        self.course_desc = course_desc
        self.course_status = course_status

    def json(self):
        return {"course_name": self.course_name, "course_code": self.course_code,"course_desc": self.course_desc, "course_status": self.course_status}

# class Skills(db.Model):
#     __tablename__ = 'Skill'

#     skills_name = db.Column(db.String, nullable=False)
#     skills_code = db.Column(db.Integer, primary_key=True, nullable=False)
#     skills_desc = db.Column(db.String, nullable=False)

#     def __init__(self, skills_name, skills_code, skills_desc):
#         self.skills_name = skills_name
#         self.skills_code = skills_code
#         self.skills_desc = skills_desc

#     def json(self):
#         return {"skills_name": self.skills_name,"skills_code": self.skills_code, "skills_desc":self.skills_desc}

class Role(db.Model):
    __tablename__ = 'Role'

    role_name = db.Column(db.String, nullable=False)
    role_code = db.Column(db.Integer, primary_key=True, nullable=False)
    role_desc = db.Column(db.String, nullable=False)
    def __init__(self, role_name, role_code, role_desc):
        self.role_name = role_name       
        self.role_code = role_code
        self.role_desc = role_desc

    def json(self):
        return { "role_name":self.role_name, "role_code":self.role_code, "role_desc":self.role_desc}

class Learning_Journey(db.Model):
    __tablename__ = 'LearningJourney'

    LearningJourney_id = db.Column(db.Integer, primary_key=True, nullable=False)
    # staff_id = db.Column(db.String, primary_key=True, nullable=False)
    course_code = db.Column(db.String, ForeignKey("Course.course_code"), primary_key=True, nullable=False)
    role_code = db.Column(db.String, ForeignKey("Role.role_code"), primary_key=True, nullable=False, )

    def __init__(self, LearningJourney_id, course_code, role_code):
        self.LearningJourney_id = LearningJourney_id
        # self.staff_id = staff_id
        self.course_code = course_code
        self.role_code = role_code

    def json(self):
        return {"LearningJourney_id":self.LearningJourney_id, "course_code":self.course_code, "role_code":self.role_code}


@app.route("/learning_journey")
def get_all():
    lj_list = Learning_Journey.query.all()
    if len(lj_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "orders": [LJ.json() for LJ in lj_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no LJs."
        }
    ), 404

# @app.route('/learning_journey/<string:staff_id>', methods=['GET'])
# # deleting 1 course from learning journey
# def get_all_learning_journey(staff_id):
    
#     #  get learning journey row using staff_id
#     lj = Learning_Journey.query.filter_by(staff_id=staff_id).all()

#     # get

#     if lj:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": [l.json() for l in lj]
                
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "An error occurred while getting the course from learning journey"
#         }
#     ), 404


# @app.route('/learning_journey/<in>', methods=['DELETE'])
# # deleting 1 course from learning journey
# def del_course_from_learning_journey(LearningJourney_id, course_code):
    
#     #  get learning journey row using LearningJourney_id and course_code
#     lj_course = Learning_Journey.query.filter_by(LearningJourney_id=LearningJourney_id, course_code=course_code).first()

#     # delete
#     try:
#         db.session.delete(lj_course)
#         db.session.commit()
#     except:
#         return {
#             "code": 500,
#             "data": {
#                 "lj_course": lj_course
#             },
#             "message": "An error occurred while deleting the course from learning journey"
#         }
#     return {
#         "code": 200,
#         "message": str(lj_course) + " had been successfully deleted."
#     }

if __name__ == '__main__':
    app.run(port=5000, debug=True)