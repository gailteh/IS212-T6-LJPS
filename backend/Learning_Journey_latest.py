
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey
import json

'''
Assumed JSON:
{"lj_id": , "course_ID", "staff_id"}
'''

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root' + \
                                        '@localhost:3306/is212_spm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)



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



# initiate classes: Course, learning journey
class Course(db.Model):
    __tablename__ = 'Course'
    course_name = db.Column(db.String, nullable=False)

    course_code = db.Column(db.String, primary_key=True, nullable=False)
    course_desc = db.Column(db.String, nullable=False)
    course_status = db.Column(db.String, nullable=False)

    def __init__(self, course_name, course_code, course_desc, course_status):
        self.course_name = course_name
        self.course_code = course_code
        self.course_desc = course_desc
        self.course_status = course_status
    __mapper_args__ = {
        'polymorphic_identity': 'Course'
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
        return {"course_name": self.course_name,"course_code": self.course_code, "course_desc":self.course_desc,"course_status":self.course_status}

    # def json(self):
    #     return {"course_name": self.course_name, "course_code": self.course_code,"course_desc": self.course_desc, "course_status": self.course_status}


class Role(db.Model):
    __tablename__ = 'Role'

    role_name = db.Column(db.String, nullable=False)
    role_code = db.Column(db.Integer, primary_key=True, nullable=False)
    role_desc = db.Column(db.String, nullable=False)

    def __init__(self, role_name, role_code, role_desc):
        self.role_name = role_name       
        self.role_code = role_code
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
    # def json(self):
    #     return { "role_name":self.role_name, "role_code":self.role_code, "role_desc":self.role_desc}



@app.route('/learning_journey/<int:role_code>', methods=['GET'])
def display_role_course(role_code):

    courses_list = Learning_Journey.query.filter_by(role_code=role_code).all()

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
    lj_list = Learning_Journey.query.all()
    
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
        }), 500
    
    #create new record in the lj table
    new_course = Learning_Journey(lj_id = data['lj_id'], course_code = data['course_code'], role_code = data['role_code'])

    # commit to DB
    try:
        db.session.add(new_course)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({
            "message": "Unable to commit to database"
        }), 500

    return jsonify({
        "Status": "Success"
    }),201

# @app.route('/learning_journey/<string:staff_id>', methods=['GET'])
# # deleting 1 course from learning journey
# def get_all_learning_journey(staff_id):
    
#     #  get learning journey row using staff_id
#     lj = Learning_Journey.query.filter_by(staff_id=staff_id).all()

#     # get

#     if lj:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": [l.json() for l in lj]
                
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "An error occurred while getting the course from learning journey"
#         }
#     ), 404


# @app.route('/learning_journey/<in>', methods=['DELETE'])
# # deleting 1 course from learning journey
# def del_course_from_learning_journey(lj_id, course_code):
    
#     #  get learning journey row using lj_id and course_code
#     lj_course = Learning_Journey.query.filter_by(lj_id=lj_id, course_code=course_code).first()

#     # delete
#     try:
#         db.session.delete(lj_course)
#         db.session.commit()
#     except:
#         return {
#             "code": 500,
#             "data": {
#                 "lj_course": lj_course
#             },
#             "message": "An error occurred while deleting the course from learning journey"
#         }
#     return {
#         "code": 200,
#         "message": str(lj_course) + " had been successfully deleted."
#     }

if __name__ == '__main__':
    app.run(port=5000, debug=True)