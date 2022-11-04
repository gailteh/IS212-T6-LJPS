from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey
# from flaskext.mysql import MySQL
# import pymysql

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
    role_skill_relation = db.Column(db.String, nullable=False)
    
    def __init__(self, role_code, role_name, role_desc, role_skill_relation):
        self.role_code = role_code
        self.role_name = role_name
        self.role_desc = role_desc
        self.role_skill_relation = role_skill_relation

    def json(self):
        return {"role_code":self.role_code, "role_name":self.role_name, "role_desc":self.role_desc, "role_skill_relation":self.role_skill_relation}

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
@app.route("/edit_role/<int:role_code>", methods=['GET', 'POST'])
def edit_role(role_code):
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

    # delete
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

@app.route("/assign_role", methods=['GET'])
def assign_role():
    # role_detail = role.query.all()
    # for role in role_detail:
        
    pass

if __name__ == '__main__':
    app.run(port=4999, debug=True)
