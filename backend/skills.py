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
role_skill_relation = db.Table('role_skill_relation',
    db.Column('role_code', db.Integer, db.ForeignKey('role.role_code')),
    db.Column('skill_code', db.Integer, db.ForeignKey('skill.skill_code'))
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

    def __init__(self, skills_name, skills_code, skills_desc):
        self.skill_code = skills_code
        self.skill_name = skills_name
        self.skill_desc = skills_desc

    def json(self):
        return {"skill_name": self.skill_name,"skill_code": self.skill_code, "skill_desc":self.skill_desc}

# class role_skill_relation(db.Model):
#     __tablename__ = 'role_skill_relation'

#     role_code = db.Column(db.Integer, primary_key=True, nullable=False, )
#     skill_code = db.Column(db.Integer, nullable=False, )

#     def __init__(self, role_code, skill_code):
#         self.role_code = role_code
#         self.skill_code = skill_code

#     def json(self):
#         return {"role_code": self.role_code,"skill_code": self.skill_code}



#display skills that respective to the role
@app.route('/<int:role_code>/skills', methods=['GET'])
def display_skills(role_code):
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

if __name__ == '__main__':
    app.run(port=4999, debug=True)