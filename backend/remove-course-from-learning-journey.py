
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey

'''
Assumed JSON:
{"ljID": , "course_ID", "StaffID"}
'''

app = flask(__name__)
# initiate database connection
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@localhost:8889/<xxx>"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

# initiate classes: Course, learning journey
class Courses(db.Model):
    __tablename__ = 'courses'

    CourseID = db.Column(db.String, primary_key=True, nullable=False)
    Description = db.Column(db.String, nullable=False)

    def __init__(self, CourseID, Description):
        self.CourseID = CourseID
        self.Description = Description

    def json(self):
        return {"courseID": self.CourseID,"description": self.Description}

class Role(db.Model):
    __tablename__ = 'roles'

    roleID = db.Column(db.Integer, primary_key=True, nullable=False)
    roleName = db.Column(db.String, nullable=False)

    def __init__(self, roleID, roleName):
        self.roleID = roleID
        self.roleName = roleName

    def json(self):
        return {"roleID":self.roleID, "roleName":self.roleName}

class Learning_Journey(db.Model):
    __tablename__ = 'learning-journey'

    ljID = db.Column(db.Integer, primary_key=True, nullable=False)
    StaffID = db.Column(db.String, ForeignKey("Staff.StaffID"))
    CourseID = db.Column(db.String, ForeignKey("Course.CourseID"))
    Role = db.Column(db.String, ForeignKey("Role.roleID"))

    def __init__(self, ljID, StaffID, CourseID):
        self.StaffID = StaffID
        self.ljID = ljID
        self.CourseID = CourseID


    def json(self):
        return {"staffID":self.StaffID, "ljID":self.ljID,"courseID":self.CourseID}


@app.route('/learning_journey/<in>', methods=['DELETE'])
# deleting 1 course from learning journey
def del_course_from_learning_journey(ljID, courseID):
    
    #  get learning journey row using ljID and courseID
    lj_course = Learning_Journey.query.filter_by(ljID=ljID, courseID=courseID).first()

    # delete
    try:
        db.session.delete(lj_course)
        db.session.commit()
    except:
        return {
            "code": 500,
            "data": {
                "lj_course": lj_course
            },
            "message": "An error occurred while deleting the course from learning journey"
        }
    return {
        "code": 200,
        "message": str(lj_course) + " had been successfully deleted."
    }

if __name__ == '__main__':
    app.run(port=4999, debug=True)