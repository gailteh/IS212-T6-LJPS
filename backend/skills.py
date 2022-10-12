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
    __tablename__ = 'skills'

    skills_name = db.Column(db.String, primary_key=True, nullable=False)
    skills_code = db.Column(db.Integer, primary_key=True, nullable=False)
    skills_desc = db.Column(db.String, nullable=False)

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
# display the skills respective to the role selected
def get_skills_code(role_code):
    
    skills = role_skill_relation.query.filter_by(role_code=role_code).all()   

    if (len(skills) > 0):
        return {
            "code": 200,
            "data": {
                "skills": [skill.json() for skill in skills]
                
            },
            "message": "These are the skills for this role."
        }
    elif (len(skills) == 0):
        return {
        "code": 204,
        "message": "There are no skills for this role."
        }
    if skills is None:
        return {
        "code": 404,
        "message": "Error occured while displaying skills for this role."
        }

if __name__ == '__main__':
    app.run(port=4999, debug=True)
