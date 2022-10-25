from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey

app = Flask(__name__)
# initiate database connection
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@localhost:3306/is212_spm"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)


# initiate classes: Role, Skills, RoleSkillRelation
skill_course_relation = db.Table('skill_course_relation',
    
    db.Column('skill_code', db.Integer, db.ForeignKey('skill.skill_code')),
    db.Column('course_code', db.Integer, db.ForeignKey('course.course_code'))
)


class skill(db.Model):
    __tablename__ = 'skill'

    skill_code = db.Column(db.Integer, primary_key=True, nullable=False)
    skill_name = db.Column(db.String, nullable=False)
    skill_desc = db.Column(db.String, nullable=False)
    skill_course = db.relationship('course',secondary=skill_course_relation, backref=db.backref('position'))


    def __init__(self, skill_name, skill_code, skill_desc):
        self.skill_code = skill_code
        self.skill_name = skill_name
        self.skill_desc = skill_desc

    def json(self):
        return {"skill_name": self.skill_name,"skill_code": self.skill_code, "skill_desc":self.skill_desc}


class course(db.Model):
    __tablename__ = 'course'

    course_code = db.Column(db.Integer, primary_key=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_desc = db.Column(db.String, nullable=False)
    course_status = db.Column(db.String, nullable=False)

    def __init__(self, course_code, course_name, course_desc, course_status):
        self.course_code = course_code
        self.course_name = course_name
        self.course_desc = course_desc
        self.course_status = course_status

    def json(self):
        return {"course_code":self.course_code, "course_name":self.course_name, "course_desc":self.course_desc, "course_status":self.course_status}



# class skill_course_relation(db.Model):
#     __tablename__ = 'skill_course_relation'

#     course_code = db.Column(db.Integer, primary_key=True, nullable=False, )
#     skill_code = db.Column(db.Integer, nullable=False, )

#     def __init__(self, course_code, skill_code):
#         self.course_code = course_code
#         self.skill_code = skill_code

#     def json(self):
#         return {"course_code": self.course_code,"skill_code": self.skill_code}


########        level 3 control access      ########
#display skills that respective to the role 
@app.route('/<int:skill_code>/course', methods=['GET'])
def display_role_skills(skill_code):
    # get skills content from skill
    courses = course.query.filter(course.position.any(skill_code=skill_code)).all()

    if courses is None:
        return {
        "code": 404,
        "message": "Error occured while displaying courses for this skill."
        }

    if (len(courses) > 0):
        return {
            "code": 200,
            "data": {
                "courses": [crs.json() for crs in courses]
                
            },
            "message": "These are the courses for this skill."
        }
    elif (len(courses) == 0):
        return {
        "code": 204,
        "message": "There are no courses for this skill."
        }

# ########        level 1 control access      ########
# @app.route("/edit_skill/<int:skill_code>", methods=['GET', 'POST'])
# def edit_skill(skill_code):
#     skill_details = skill.query.filter_by(skill_code=skill_code).first()

#     if skill_details:
#         return{
#             "code": 200,
#             "roles": skill_details.json(),
#             "message": "Skill successfully retrieved."
#         }
#     else :
#         return {
#             "message": "Unable to retreieve skill."
#         }


# @app.route("/update_skill/<int:skill_code>", methods=['PUT'])
# def update_skill(skill_code):
#     skill_detail = skill.query.filter_by(skill_code=skill_code).first()
#     data = request.get_json()

#     edit_skill_name = data.get('edit_skill_name')
#     edit_skill_code = data.get('edit_skill_code')
#     edit_skill_desc = data.get('edit_skill_desc')

#     try:
#         skill_detail.skill_name = edit_skill_name
#         skill_detail.skill_code = edit_skill_code
#         skill_detail.skill_desc = edit_skill_desc
#         db.session.commit()
       
#     except Exception as e:
#         print(e)
#         return jsonify({
#             "message": "Unable to commit to database"
#         }), 500
#     return {
#         "code": 200,
#         "role": skill_detail.json(),
#         "message": "Skill successfully updated."
#     }



# #display all skills 
# @app.route('/skills', methods=['GET'])
# def display_skills():
#     # get skills content from skill
#     skills = skill.query.all()

#     if skills is None:
#         return {
#         "code": 404,
#         "message": "Error occured while displaying skills."
#         }

#     if skills:
#         return {
#             "code": 200,
#             "data": {
#                 "skills": [sk.json() for sk in skills]
                
#             },
#             "message": "These are the skills available."
#         }

# @app.route("/create_skill", methods=['POST'])
# # Add new role 
# def create_skill():
#     data = request.get_json()

#     if not all(key in data.keys() for 
#                 key in ('skill_code', 'skill_name', 'skill_desc')):
#         return  jsonify({
#             'message': "Incorrect JSON object provided"
#         }), 500
    
#     #create new record in the lj table
#     new_skill = skill(skill_code = data['skill_code'], skill_name = data['skill_name'], skill_desc = data['skill_desc'])

#     # commit to DB
#     try:
#         db.session.add(new_skill)
#         db.session.commit()
#     except Exception as e:
#         print(e)
#         return jsonify({
#             "message": "Unable to commit to database"
#         }), 500

#     return jsonify({
#         "Status": "Success"
#     }),201


# @app.route("/delete_skill/<int:skill_code>", methods=['DELETE'])
# #Delete role
# def delete_skill(skill_code):
#     skill_detail = skill.query.filter_by(skill_code=skill_code).first()

#     # delete
#     try:
#         db.session.delete(skill_detail)
#         db.session.commit()
#     except:
#         return {
#             "code": 500,
#             "data": {
#                 "skill_detail": skill_detail
#             },
#             "message": "An error occurred while deleting this skill"
#         }
#     return {
#         "code": 200,
#         "message": str(skill_detail) + " had been successfully deleted."
#     }


if __name__ == '__main__':
    app.run(port=4999, debug=True)