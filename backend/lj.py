from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey, select

app = Flask(__name__)
# initiate database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@localhost:3306/is212_spm"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@localhost:8889/is212_spm"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

role_skill_relation = db.Table('role_skill_relation',
    db.Column('role_code', db.Integer, db.ForeignKey('role.role_code')),
    db.Column('skill_code', db.Integer, db.ForeignKey('skill.skill_code'))
)

skill_course_relation = db.Table('skill_course_relation',
    db.Column('skill_code', db.Integer, db.ForeignKey('skill.skill_code')),
    db.Column('course_code', db.Integer, db.ForeignKey('course.course_code'))
)

role_skill_course_relation = db.Table('role_skill_course_relation',
    db.Column('role_code', db.Integer, db.ForeignKey('role.role_code')),
    db.Column('skill_code', db.Integer, db.ForeignKey('skill.skill_code')),
    db.Column('course_code', db.Integer, db.ForeignKey('course.course_code'))
)

class Role(db.Model):
    __tablename__ = 'role'

    role_code = db.Column(db.Integer, primary_key=True, nullable=False)
    role_name = db.Column(db.String, nullable=False)
    role_desc = db.Column(db.String, nullable=False)

    def __init__(self, role_code, role_name, role_desc):
        self.role_code = role_code
        self.role_name = role_name
        self.role_desc = role_desc

    __mapper_args__ = {
        'polymorphic_identity': 'Role'
    }

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def json(self):
        return {"role_code":self.role_code, "role_name":self.role_name, "role_desc":self.role_desc}


class Skill(db.Model):
    __tablename__ = 'skill'

    skill_code = db.Column(db.Integer, primary_key=True, nullable=False)
    skill_name = db.Column(db.String, nullable=False)
    skill_desc = db.Column(db.String, nullable=False)

    def __init__(self, skill_name, skill_code, skill_desc):
        self.skill_code = skill_code
        self.skill_name = skill_name
        self.skill_desc = skill_desc

    __mapper_args__ = {
        'polymorphic_identity': 'skill'
    }
    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def json(self):
        return {"skill_name": self.skill_name,"skill_code": self.skill_code, "skill_desc":self.skill_desc}

class Course(db.Model):
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

    __mapper_args__ = {
        'polymorphic_identity': 'course'
    }
    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def json(self):
        return {"course_code":self.course_code, "course_name":self.course_name, "course_desc":self.course_desc, "course_status":self.course_status}

class LearningJourney(db.Model):
    __tablename__ = 'learning_journey'
    lj_id = db.Column(db.Integer, primary_key = True, nullable= False)
    course_code = db.Column(db.String, ForeignKey('course.course_code'), primary_key = True, nullable = False)
    role_code = db.Column(db.Integer, ForeignKey('role.role_code'), primary_key = True, nullable = False)
    

    def __init__(self, lj_id, role_code, course_code):
        self.lj_id = lj_id
        self.course_code = course_code
        self.role_code = role_code
        
    
    def json(self):
        return {"lj_id": self.lj_id, 
                "course_code": self.role_code,
                "role_code": self.role_code
                }
                
    __mapper_args__ = {
        'polymorphic_identity': 'learning_journey'
    }
    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

@app.route('/learning_journey/<int:role_code>', methods=['GET'])
def display_role_course(role_code):

    courses_list = LearningJourney.query.filter_by(role_code=role_code).all()

    courses = []

    for course in courses_list:

        course_dict = {}

        course_code = course.to_dict()['course_code']

        course_name_query = Course.query.filter_by(course_code=course_code).first()
        # print(role_name_query.to_dict()['role_name'])
        course_name = course_name_query.to_dict()['course_name']

        course__desc_query = Course.query.filter_by(course_code=course_code).first()
        # print(role_name_query.to_dict()['role_name'])
        course_desc = course__desc_query.to_dict()['course_desc']

        role_status_query = Course.query.filter_by(course_code=course_code).first()
        # print(role_name_query.to_dict()['role_name'])
        course_status = role_status_query.to_dict()['course_status']

        course_dict['course_code'] = course_code
        course_dict['course_name'] = course_name
        course_dict['course_desc'] = course_desc
        course_dict['course_status'] = course_status

        courses.append(course_dict)
        print(courses)

    if courses is None:
        return jsonify({
        "code": 404,
        "message": "Error occured while displaying skills for this role."
        })

    if (len(courses) > 0):
        return jsonify({
            "code": 200,
            "data": [cr for cr in courses],
            "message": "These are the courses for this role."
        })

    elif (len(courses) == 0):
        return {
        "code": 204,
        "message": "There are no courses for this role."
        }


@app.route("/learning_journey")
def role_course():
    lj_list = LearningJourney.query.all()
    
    role_list = []
    role_name_list = []

    for lj in lj_list:
        role_dict = {}

        role_code = lj.to_dict()['role_code']
        course_code = lj.to_dict()['course_code']

        role_name_query = Role.query.filter_by(role_code=role_code).first()
        # print(role_name_query.to_dict()['role_name'])
        role_name = role_name_query.to_dict()['role_name']

        course_name_query = Course.query.filter_by(course_code=course_code).first()
        # print(course_name_query.to_dict()['course_name'])
        course_name = course_name_query.to_dict()['course_name']

        if role_name not in role_name_list:
            role_dict['role_code'] = role_code
            role_dict['role_name'] = role_name
            role_dict['course_name'] = [course_name]
            # print(course_name)
            role_name_list.append(role_name)
            role_list.append(role_dict)

        else: 
            for index in (0,len(role_name_list)-1):
                if role_name == role_name_list[index]:
                    role_list[index]['course_name'].append(course_name)

    print(role_list)
       
    # Actionable: review the obj data type, create a for-loop to add courses for each role
    if len(role_list):
        return jsonify(
            {
                "code": 200,
                "data": [role for role in role_list]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no LJs."
        }
    ), 404

@app.route("/learning_journey", methods=['POST'])
#For every new course that is added to a learning journey, a new record is created
def add_new_course(): 
    data = request.get_json()

    if not all(key in data.keys() for 
                key in ('lj_id', 'course_code', 'role_code')):
        return  jsonify({
            'message': "Incorrect JSON object provided"
        }), 499

    # validate if a LJ already created previously
    if (LearningJourney.query.filter_by(role_code=data['role_code']).first()):
    

        #create new record in the lj table
        new_course = LearningJourney(lj_id = data['lj_id'], course_code = data['course_code'], role_code = data['role_code'])

        role_info = Role.query.filter_by(role_code=data['role_code']).first()
        role_name = role_info.to_dict()['role_name']

        course_info = Course.query.filter_by(course_code=data['course_code']).first()
        course_name = course_info.to_dict()['course_name']
        # commit to DB
        try:
            db.session.add(new_course)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({
                "message": "Unable to commit to database as this course is already added to Learning Journey for " + role_name
            }), 501

        return jsonify({
            "Status": "Success",
            "message": course_name + " is added to Learning Journey for " + role_name
        }),201

    else:
        #create new record in the lj table
        new_course = LearningJourney(lj_id = data['lj_id'], course_code = data['course_code'], role_code = data['role_code'])

        role_info = Role.query.filter_by(role_code=data['role_code']).first()
        role_name = role_info.to_dict()['role_name']
        print(role_name)
        course_info = Course.query.filter_by(course_code=data['course_code']).first()
        course_name = course_info.to_dict()['course_name']
        print(role_name)

        # commit to DB
        try:
            db.session.add(new_course)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({
                "message": "Unable to commit to database as this course is already added to Learning Journey for " + role_name
            }), 501

        return jsonify({
            "Status": "Success",
            "message": "Initiated Learning Journey for " + role_name + ", course " + course_name + " is added"
        }), 201

# @app.route("/role-skill-course-relation", methods=['GET'])
# def display_rs_relation():
#     # get all relation content
#     relations = db.session.execute(select(role_skill_course_relation)).all()

#     # get role,skill,course rs
#     relationship = []
#     for rs in relations:
#         rs = dict(rs)
#         role_c = rs['role_code']
#         skill_c = rs['skill_code']
#         course_c = rs['course_code']
#         role_info = db.session.execute(select(Role.role_code,Role.role_name).where(Role.role_code==role_c)).first()
#         skill_info = db.session.execute(select(Skill.skill_code,Skill.skill_name).where(Skill.skill_code==skill_c)).first()
#         course_info = db.session.execute(select(Course.course_code,Course.course_name).where(Course.course_code==course_c)).first()
#         rs_info = {}
#         rs_info.update(dict(role_info))
#         rs_info.update(dict(skill_info))
#         rs_info.update(dict(course_info))
#         relationship.append(rs_info)

#     if len(relations) > 0:
#         return {
#             "code":200,
#             "relations": relationship,
#             "message": "All relations displayed."
#         }
#     elif relations == None:
#         return{
#             "message":"Go check your code!"
#         }

@app.route("/role-skill-course-relation/<int:role_code>", methods=['GET'])
def display_course_from_role(role_code):
    relations = db.session.execute(select(role_skill_course_relation)).all()

    courses = []
    for rs in relations:
        rs = dict(rs)
        role_c = rs['role_code']
        skill_c = rs['skill_code']
        course_c = rs['course_code']

        if role_c == role_code:
            role_info = db.session.execute(select(Role.role_code,Role.role_name).where(Role.role_code==role_c)).first()
            skill_info = db.session.execute(select(Skill.skill_code,Skill.skill_name).where(Skill.skill_code==skill_c)).first()
            course_info = db.session.execute(select(Course.course_code,Course.course_name,Course.course_desc,Course.course_status).where(Course.course_code==course_c)).first()
            course_info_dict = dict(course_info)
            rs_info = {}
            if course_info_dict['course_status'] == "active":
                rs_info.update(dict(course_info))
                rs_info.update(dict(role_info))
                rs_info.update(dict(skill_info))
            if rs_info != {}:
                courses.append(rs_info)

    if len(courses) > 0:
        return {
            "code":200,
            "rel_courses": courses,
            "message": "Successfully displayed courses"
        }
    elif courses == None:
        return{
            "message":"Go check your code!"
        }


if __name__ == '__main__':
    app.run(port=4848, debug=True)