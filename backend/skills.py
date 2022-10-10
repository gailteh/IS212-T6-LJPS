import flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey

app = flask(__name__)
# initiate database connection
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@localhost:8889/<xxx>"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

# initiate classes: Course, learning journey
class Courses(db.Model):
    __tablename__ = 'skills'

    skills_name = db.Column(db.String, primary_key=True, nullable=False)
    skills_code = db.Column(db.String, primary_key=True, nullable=False)
    skills_desc = db.Column(db.String, nullable=False)

    def __init__(self, skills_name, skills_code, skills_desc):
        self.skills_name = skills_name
        self.skills_code = skills_code
        self.skills_desc = skills_desc

    def json(self):
        return {"skills_name": self.skills_name,"skills_code": self.skills_code, "skills_desc":self.skills_desc}

class Skills(db.Model):
    __tablename__ = 'skills'

    skills_name = db.Column(db.String, primary_key=True, nullable=False)
    skills_code = db.Column(db.String, primary_key=True, nullable=False)
    skills_desc = db.Column(db.String, nullable=False)

    def __init__(self, skills_name, skills_code, skills_desc):
        self.skills_name = skills_name
        self.skills_code = skills_code
        self.skills_desc = skills_desc

    def json(self):
        return {"skills_name": self.skills_name,"skills_code": self.skills_code, "skills_desc":self.skills_desc}

@app.route('/<str:role_code>/skills', methods=['GET'])
# display the skills respective to the role selected
def display_skills():
    
    skills = Skills.query.filter_by(role_code).first()
    if (skills.length > 0):
        return {
            "code": 200,
            "data": {
                "skills_name": skills_name
                "skills_code": skills_code
                "skills_desc": skills_desc
            },
            "message": "These are the skills for this role."
        }
    elif (skills.length == 0):
        return {
        "code": 204,
        "message": "There are no skills for this role."
        }
    else:
        return {
        "code": 404,
        "message": "Error occured while displaying skills for this role."
        }

if __name__ == '__main__':
    app.run(port=4999, debug=True)
