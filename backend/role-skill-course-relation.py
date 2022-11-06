from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey, select

app = Flask(__name__)
# initiate database connection
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@localhost:3306/is212_spm"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

# initiate classes: Role, Skills, Course, RoleSkillRelation, courseSkillRelation, RoleSkillCourseRelation
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

class role(db.Model):
    __tablename__ = 'role'

    role_code = db.Column(db.Integer, primary_key=True, nullable=False)
    role_name = db.Column(db.String, nullable=False)
    role_desc = db.Column(db.String, nullable=False)
    role_skill = db.relationship('skill',secondary=role_skill_relation, backref=db.backref('position'))

    def __init__(self, role_code, role_name, role_desc):
        self.role_code = role_code
        self.role_name = role_name
        self.role_desc = role_desc

    def json(self):
        return {"role_code":self.role_code, "role_name":self.role_name, "role_desc":self.role_desc}


class skill(db.Model):
    __tablename__ = 'skill'

    skill_code = db.Column(db.Integer, primary_key=True, nullable=False)
    skill_name = db.Column(db.String, nullable=False)
    skill_desc = db.Column(db.String, nullable=False)

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

class Learning_Journey(db.Model):
    __tablename__ = 'Learning_Journey'

    lj_id = db.Column(db.Integer, primary_key=True, nullable=False)
    # staff_id = db.Column(db.String, primary_key=True, nullable=False)
    course_code = db.Column(db.String, ForeignKey("Course.course_code"), primary_key=True, nullable=False)
    role_code = db.Column(db.String, ForeignKey("Role.role_code"), primary_key=True, nullable=False, )

    def __init__(self, lj_id, course_code, role_code):
        self.lj_id = lj_id
        # self.staff_id = staff_id
        self.course_code = course_code
        self.role_code = role_code

    # def json(self):
    #     return {"lj_id":self.lj_id, "course_code":self.course_code, "role_code":self.role_code}
    
    __mapper_args__ = {
        'polymorphic_identity': 'LearningJourney'
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
        
# display role-skill-course relation
@app.route("/role-skill-course-relation", methods=['GET'])
def display_rs_relation():
    # get all relation content
    relations = db.session.execute(select(role_skill_course_relation)).all()

    # get role,skill,course rs
    relationship = []
    for rs in relations:
        rs = dict(rs)
        role_c = rs['role_code']
        skill_c = rs['skill_code']
        course_c = rs['course_code']
        role_info = db.session.execute(select(role.role_code,role.role_name).where(role.role_code==role_c)).first()
        skill_info = db.session.execute(select(skill.skill_code,skill.skill_name).where(skill.skill_code==skill_c)).first()
        course_info = db.session.execute(select(course.course_code,course.course_name).where(course.course_code==course_c)).first()
        rs_info = {}
        rs_info.update(dict(role_info))
        rs_info.update(dict(skill_info))
        rs_info.update(dict(course_info))
        relationship.append(rs_info)

    if len(relations) > 0:
        return {
            "code":200,
            "relations": relationship,
            "message": "All relations displayed."
        }
    elif relations == None:
        return{
            "message":"Go check your code!"
        }

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
            role_info = db.session.execute(select(role.role_code,role.role_name).where(role.role_code==role_c)).first()
            skill_info = db.session.execute(select(skill.skill_code,skill.skill_name).where(skill.skill_code==skill_c)).first()
            course_info = db.session.execute(select(course.course_code,course.course_name,course.course_desc,course.course_status).where(course.course_code==course_c)).first()
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
    app.run(port=4999, debug=True)