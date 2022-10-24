from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
# initiate database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@localhost:8889/is212_SPM?collate=utf8_general_ci"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
#                                           'pool_recycle': 280}

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@localhost:3306/is212_spm"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@localhost:8889/is212_SPM"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

# initiate classes: Course, learning journey
class Courses(db.Model):
    __tablename__ = 'courses'

    course_code = db.Column(db.String, primary_key=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_desc = db.Column(db.String, nullable=False)

    def __init__(self, course_code, course_name, course_desc):
        self.course_code = course_code
        self.course_name = course_name
        self.course_desc = course_desc

    def json(self):
        return jsonify({"course_code": self.course_code,"course_name":self.course_name, "course_desc": self.course_desc})

class Role(db.Model):
    __tablename__ = 'roles'

    role_code = db.Column(db.Integer, primary_key=True, nullable=False)
    role_name = db.Column(db.String, nullable=False)
    role_desc = db.Column(db.String, nullable=False)

    def __init__(self, role_code, role_name, role_desc):
        self.role_code = role_code
        self.role_name = role_name
        self.role_desc = role_desc


    def json(self):
        return {"role_code":self.role_code, "role_name":self.role_name, "role_desc":self.role_desc}

## not needed for now
# class Staff(db.Model):
#     __tablename__ = 'staff'

#     staff_id = db.Column(db.Integer, primary_key=True, nullable=False)
#     staff_name = db.Column(db.String, nullable=False)

#     def __init__(self, staff_id, staff_name):
#         self.staff_id = staff_id
#         self.staff_name = staff_name

#     def json(self):
#         return {"staff_id": self.staff_id, "staff_name": self.staff_name}


class Learning_Journey(db.Model):
    __tablename__ = 'learning_journey'

    lj_id = db.Column(db.Integer, primary_key=True, nullable=False)
    course_code = db.Column(db.String, db.ForeignKey('courses.course_code'), primary_key=True, nullable = False)
    role_code = db.Column(db.Integer,  db.ForeignKey('roles.role_code'), nullable = False)

    def __init__(self, lj_id, course_code, role_code):
        self.lj_id = lj_id
        self.course_code = course_code
        self.role_code = role_code


    def json(self):
        return {"lj_id":self.lj_id, "course_code":self.course_code, "role_code": self.role_code}



@app.route('/del_ljc/<int:lj_id>/<string:course_code>', methods=['DELETE'])
# deleting 1 course from learning journey
def del_course(lj_id, course_code):
    
    #  get learning journey rows using lj_id
    lj_course = Learning_Journey.query.filter_by(lj_id=lj_id, course_code=course_code).first()

    # delete
    try:
        db.session.delete(lj_course)
        db.session.commit()
    except:
        return jsonify({
            "code": 500,
            "data": {
                "lj_course": lj_course.json()
            },
            "message": "An error occurred while deleting the course from learning journey"
        })
    return jsonify({
        "code": 200,
        "data": lj_course.json(),
        "message": course_code + " on "+ str(lj_id) + " had been successfully deleted."
    })

if __name__ == '__main__':
    app.run(port=4888, debug=True)