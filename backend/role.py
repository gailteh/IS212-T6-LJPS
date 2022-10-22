from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey
from flaskext.mysql import MySQL
import pymysql

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
    role_name = db.Column(db.String, nullable=False)
    role_desc = db.Column(db.String, nullable=False)
    
    def __init__(self, role_code, role_name, role_desc):
        self.role_code = role_code
        self.role_name = role_name
        self.role_desc = role_desc

    def json(self):
        return {"role_code":self.role_code, "role_name":self.role_name, "role_desc":self.role_desc}

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

########        level 1 control access      ########
@app.route("/update_role/<int:role_code>", methods=['PUT'])
def update_role(role_code):
    role_code = role.query.get(role_code)

    role_name = request.json['role_name']
    role_desc = request.json['role_name']

    role.role_name = role_name
    role.role_desc = role_desc

    db.session.commit()

    return {
        "code": 200,
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

    # delete
    try:
        db.session.delete(role_detail)
        db.session.commit()
    except:
        return {
            "code": 500,
            "data": {
                "lj_course": role_detail
            },
            "message": "An error occurred while deleting the course from learning journey"
        }
    return {
        "code": 200,
        "message": str(role_detail) + " had been successfully deleted."
    }

if __name__ == '__main__':
    app.run(port=4999, debug=True)
