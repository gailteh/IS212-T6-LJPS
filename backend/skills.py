from flask import Flask
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
class role(db.Model):
    __tablename__ = 'role'

    role_code = db.Column(db.Integer, primary_key=True, nullable=False)
    roleName = db.Column(db.String, nullable=False)
    role_desc = db.Column(db.String, nullable=False)

    def __init__(self, role_code, roleName, role_desc):
        self.role_code = role_code
        self.roleName = roleName
        self.role_desc = role_desc

    def json(self):
        return {"role_code":self.role_code, "roleName":self.roleName, "role_desc":self.role_desc}


class skill(db.Model):
    __tablename__ = 'skill'

    skill_name = db.Column(db.String, primary_key=True, nullable=False)
    skill_code = db.Column(db.Integer, primary_key=True, nullable=False)
    skill_desc = db.Column(db.String, nullable=False)

    def __init__(self, skills_name, skills_code, skills_desc):
        self.skills_name = skills_name
        self.skills_code = skills_code
        self.skills_desc = skills_desc

    def json(self):
        return {"skills_name": self.skills_name,"skills_code": self.skills_code, "skills_desc":self.skills_desc}

class role_skill_relation(db.Model):
    __tablename__ = 'role_skill_relation'

    role_code = db.Column(db.Integer, primary_key=True, nullable=False)
    skill_code = db.Column(db.Integer, primary_key=True, nullable=False)

    def __init__(self, role_code, skill_code):
        self.role_code = role_code
        self.skill_code = skill_code

    def json(self):
        return {"role_code": self.role_code,"skill_code": self.skill_code}



@app.route('/<string:role_code>/skill', methods=['GET'])
# retreieve the skills code respective to the role selected
def get_skills_code(role_code):
    
    skill_codes = role_skill_relation.query.filter_by(role_code=role_code).all()

    # initialise empty list 
    # skill_codes_list = []

    #append all skills code to list
    #for skill_code in skill_codes_list:
    #    skill_codes_list.append(skill_code)
    
    
    #skills = skill.query.filter_by(skill_code=skill_code).all()
    
    if (len(skill_codes) > 0):
        return {
            "code": 200,
            "data": {
                "skills": [skill.json() for skill in skill_codes]
                
            },
            "message": "These are the skills for this role."
        }
    elif (len(skill_codes) == 0):
        return {
        "code": 204,
        "message": "There are no skills for this role."
        }
    if skill_codes is None:
        return {
        "code": 404,
        "message": "Error occured while displaying skills for this role."
        }

@app.route('/<string:role_code>/<string:skill_code>/skill', methods=['GET'])
# display the skills respective to the role selected from the skills code
def display_skills(role_code, skill_code):
    
    skill_code = get_skills_code(role_code=role_code)
    all_skill = skill.query.filter_by(skill_code=skill_code).all()   
    
    skill_codes_list = []

    if (len(all_skill) > 0):
        return {
            "code": 200,
            "data": {
                "skills": [skill.json() for skill in all_skill]
                
            },
            "message": "These are the skills for this role."
        }
    elif (len(all_skill) == 0):
        return {
        "code": 204,
        "message": "There are no skills for this role."
        }
    if all_skill is None:
        return {
        "code": 404,
        "message": "Error occured while displaying skills for this role."
        }


if __name__ == '__main__':
    app.run(port=4999, debug=True)
