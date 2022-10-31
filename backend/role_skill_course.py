from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey, select
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)
# initiate database connection
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@localhost:3306/is212_spm"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

# initiate classes: Role Skill Relation
role_skill_relation = db.Table('role_skill_relation',
    db.Column('role_code', db.Integer, db.ForeignKey('role.role_code')),
    db.Column('skill_code', db.Integer, db.ForeignKey('skill.skill_code'))
)
# initiate classes: Skill Course Relation
skill_course_relation = db.Table('skill_course_relation',
    
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


########################        Role backend      ########################
########        level 3 control access      ########
@app.route('/role', methods=['GET'])
def display_role():
    roles = role.query.all()
    if roles is None:
        return {
        "code": 404,
        "message": "Error occured while displaying roles."
        }

    if (len(roles) > 0):
        return {
            "code": 200,
            "data": {
                "roles": [r.json() for r in roles]
                
            },
            "message": "These are the roles available."
        }
    elif (len(roles) == 0):
        return {
        "code": 204,
        "message": "There are no roles available at the moment."
        }

########        level 1 control access (CRUD)      ########
@app.route("/edit_role/<int:role_code>", methods=['GET', 'POST'])
def edit_role(role_code):
    #display role existing details
    role_details = role.query.filter_by(role_code=role_code).first()

    if role_details:
        return{
            "code": 200,
            "roles": role_details.json(),
            "message": "Role successfully updated."
        }
    else :
        return {
            "message": "Unable to retreieve role."
        }


@app.route("/update_role/<int:role_code>", methods=['PUT'])
def update_role(role_code):
    #update role details
    role_detail = role.query.filter_by(role_code=role_code).first()
    data = request.get_json()

    edit_role_name = data.get('edit_role_name')
    edit_role_code = data.get('edit_role_code')
    edit_role_desc = data.get('edit_role_desc')

    try:
        role_detail.role_name = edit_role_name
        role_detail.role_code = edit_role_code
        role_detail.role_desc = edit_role_desc
        db.session.commit()
       
    except Exception as e:
        print(e)
        return jsonify({
            "message": "Unable to commit to database"
        }), 500
    return {
        "code": 200,
        "role": role_detail.json(),
        "message": "Role successfully updated."
    }


@app.route("/create_role", methods=['POST'])
# Add new role 
def create_role():
    data = request.get_json()

    if not all(key in data.keys() for 
                key in ('role_code', 'role_name', 'role_desc')):
        return  jsonify({
            'message': "Incorrect JSON object provided"
        }), 500
    
    #create new record in the lj table
    new_role = role(role_code = data['role_code'], role_name = data['role_name'], role_desc = data['role_desc'])

    # commit to DB
    try:
        db.session.add(new_role)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({
            "message": "Unable to commit to database"
        }), 500

    return jsonify({
        "Status": "Success"
    }),201


@app.route("/delete_role/<int:role_code>", methods=['DELETE'])
def delete_role(role_code):
    role_detail = role.query.filter_by(role_code=role_code).first()

    # delete role
    try:
        db.session.delete(role_detail)
        db.session.commit()
    except:
        return {
            "code": 500,
            "data": {
                "role_detail": role_detail
            },
            "message": "An error occurred while deleting this role"
        }
    return {
        "code": 200,
        "message": str(role_detail) + " had been successfully deleted."
    }

########################        Skill backend      ########################
########        level 3 control access      ########

#display skills that respective to the role 
@app.route('/<int:role_code>/skills', methods=['GET'])
def display_role_skills(role_code):
    # get skills content from skill
    skills = skill.query.filter(skill.position.any(role_code=role_code)).all()

    if skills is None:
        return {
        "code": 404,
        "message": "Error occured while displaying skills for this role."
        }

    if (len(skills) > 0):
        return {
            "code": 200,
            "data": {
                "skills": [sk.json() for sk in skills]
                
            },
            "message": "These are the skills for this role."
        }
    elif (len(skills) == 0):
        return {
        "code": 204,
        "message": "There are no skills for this role."
        }

########        level 1 control access (CRUD)      ########
@app.route("/edit_skill/<int:skill_code>", methods=['GET', 'POST'])
def edit_skill(skill_code):
    #display existing skill details
    skill_details = skill.query.filter_by(skill_code=skill_code).first()

    if skill_details:
        return{
            "code": 200,
            "roles": skill_details.json(),
            "message": "Skill successfully retrieved."
        }
    else :
        return {
            "message": "Unable to retreieve skill."
        }


@app.route("/update_skill/<int:skill_code>", methods=['PUT'])
def update_skill(skill_code):
    #update existing skill details
    skill_detail = skill.query.filter_by(skill_code=skill_code).first()
    data = request.get_json()

    edit_skill_name = data.get('edit_skill_name')
    edit_skill_code = data.get('edit_skill_code')
    edit_skill_desc = data.get('edit_skill_desc')

    try:
        skill_detail.skill_name = edit_skill_name
        skill_detail.skill_code = edit_skill_code
        skill_detail.skill_desc = edit_skill_desc
        db.session.commit()
       
    except Exception as e:
        print(e)
        return jsonify({
            "message": "Unable to commit to database"
        }), 500
    return {
        "code": 200,
        "role": skill_detail.json(),
        "message": "Skill successfully updated."
    }

#display all skills 
@app.route('/skills', methods=['GET'])
def display_skills():
    # get skills content from skill
    skills = skill.query.all()

    if skills is None:
        return {
        "code": 404,
        "message": "Error occured while displaying skills."
        }

    if skills:
        return {
            "code": 200,
            "data": {
                "skills": [sk.json() for sk in skills]
                
            },
            "message": "These are the skills available."
        }

@app.route("/create_skill", methods=['POST'])
# Add new role 
def create_skill():
    data = request.get_json()

    if not all(key in data.keys() for 
                key in ('skill_code', 'skill_name', 'skill_desc')):
        return  jsonify({
            'message': "Incorrect JSON object provided"
        }), 500
    
    #create new record in the lj table
    new_skill = skill(skill_code = data['skill_code'], skill_name = data['skill_name'], skill_desc = data['skill_desc'])

    # commit to DB
    try:
        db.session.add(new_skill)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({
            "message": "Unable to commit to database"
        }), 500

    return jsonify({
        "Status": "Success"
    }),201


@app.route("/delete_skill/<int:skill_code>", methods=['DELETE'])
def delete_skill(skill_code):
    skill_detail = skill.query.filter_by(skill_code=skill_code).first()

    # delete skill 
    try:
        db.session.delete(skill_detail)
        db.session.commit()
    except:
        return {
            "code": 500,
            "data": {
                "skill_detail": skill_detail
            },
            "message": "An error occurred while deleting this skill"
        }
    return {
        "code": 200,
        "message": str(skill_detail) + " had been successfully deleted."
    }
# display role-skill relation
@app.route("/role-skill-relation", methods=['GET'])
def display_rs_relation():
    # get all relation content
    relations = db.session.execute(select(role_skill_relation)).all()

    # get role and skill
    relationship = []
    for rs in relations:
        rs = dict(rs)
        role_c = rs['role_code']
        skill_c = rs['skill_code']
        role_info = db.session.execute(select(role.role_code,role.role_name).where(role.role_code==role_c)).first()
        skill_info = db.session.execute(select(skill.skill_code,skill.skill_name).where(skill.skill_code==skill_c)).first()
        rs_info = {}
        rs_info.update(dict(role_info))
        rs_info.update(dict(skill_info))
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

########################        Course backend      ########################
########        level 3 control access      ########
#display skills that respective to the role 
@app.route('/<int:skill_code>/course', methods=['GET'])
def display_skills_course(skill_code):
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

########        level 1 control access      ########
#display courses
@app.route('/course', methods=['GET'])
def display_course():
    courses = course.query.all()

    if courses is None:
        return {
        "code": 404,
        "message": "Error occured while displaying skills."
        }

    if courses:
        return {
            "code": 200,
            "data": {
                "skills": [c.json() for c in courses]
                
            },
            "message": "These are the skills available."
        }

if __name__ == '__main__':
    app.run(port=4999, debug=True)
