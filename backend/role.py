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
@app.route("/role/<int:role_code>", methods=['GET', 'POST'])
#For every new role, a new record is created
def edit_role(role_code): 
    pass
    


if __name__ == '__main__':
    app.run(port=4999, debug=True)
