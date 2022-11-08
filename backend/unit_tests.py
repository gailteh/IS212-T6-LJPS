import unittest 
import flask_testing
import json
from role import app, db, role
#commented out the skills testing
#from skills import app,db, skill, role 

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

##testing Role##
# For classes
class TestRole(unittest.TestCase):
    def test_json(self):
        # Figure out a way to add in the relationship --> role_skill_relationship
        roleTest = role(role_code=1,role_name='admin',role_desc='Admin is the best job in the world',role_skill_relation='role-skill')
        self.assertEqual(roleTest.json(), {
            "role_code":1, 
            "role_name":'admin', 
            "role_desc":'Admin is the best job in the world',
            "role_skill_relation":'role-skill'
        })

# For endpoints
class TestDisplayRole(TestApp):
    def test_display_role(self):
        # Figure out a way to add in the relationship for r1,r2 --> role_skill_relationship
        r1 = role(role_code=1,role_name="admin",role_desc='Best job in the world',role_skill_relation="role-skill-1")
        r2 = role(role_code=2,role_name="HR",role_desc='HR job',role_skill_relation='role-skill-2')

        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()

        response = self.client.get("/role")
        self.assertEqual(response.json,
        {
            "code": 200,
            "data": {
                "roles": [{
                    "role_code":1,
                    "role_name":"admin",
                    "role_desc":"Best job in the world",
                    "role_skill_relation":"role-skill-1"
                },
                {
                    "role_code":2,
                    "role_name":"HR",
                    "role_desc":"HR job",
                    "role_skill_relation":"role-skill-2"
                }
                
                ]
                
            },
            "message": "These are the roles available."
        })

if __name__ == '__main__':
    unittest.main()