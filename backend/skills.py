from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey

app = Flask(__name__)
# initiate database connection
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@localhost:8889/db.sql"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

# initiate classes: Role, Skills
class Role(db.Model):
    __tablename__ = 'roles'

    role_code = db.Column(db.Integer, primary_key=True, nullable=False)
    roleName = db.Column(db.String, nullable=False)
    role_desc = db.Column(db.String, nullable=False)

    def __init__(self, role_code, roleName, role_desc):
        self.role_code = role_code
        self.roleName = roleName
        self.role_desc = role_desc

    def json(self):
        return {"role_code":self.role_code, "roleName":self.roleName, "role_desc":self.role_desc}


class Skills(db.Model):
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

class RoleSkillRelation(db.Model):
    __tablename__ = 'role_skill_relation'

    role_code = db.Column(db.Integer, primary_key=True, nullable=False)
    skills_code = db.Column(db.Integer, primary_key=True, nullable=False)

    def __init__(self, role_code, skills_code):
        self.role_code = role_code
        self.skills_code = skills_code

    def json(self):
        return {"role_code": self.role_code,"skills_code": self.skills_code}



@app.route('/<string:role_code>/skills', methods=['GET'])
# display the skills respective to the role selected
def display_skills(role_code):
    
    skills_name = Skills.query.filter_by(role_code=role_code).first()
    skills = []    

    if (len(skills_name) > 0):
        return {
            "code": 200,
            "data": {
                "skills_name": Skills[skills_name]
                
            },
            "message": "These are the skills for this role."
        }
    elif (len(skills_name) == 0):
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
