import unittest 
import flask_testing
import json
from role_skill_course import app, db, role, skill, course


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

##### For classes #####
# test Role
class TestRole(unittest.TestCase):
    def test_json(self):
        roleTest = role(role_code = 1, role_name = "admin", role_desc = "Admin is the best job in the world")
        self.assertEqual(roleTest.json(), {
            "role_code": 1, 
            "role_name": "admin", 
            "role_desc": "Admin is the best job in the world"
            # "role_skill_relation":"role-skill"
        })
        

# test Skill
class TestSkill(unittest.TestCase):
    def test_json(self):
        skillTest = skill(skill_code = 1, skill_name = "Interpersonal skills", skill_desc = "Communicate and interact")
        self.assertEqual(skillTest.json(), {
            "skill_code": 1, 
            "skill_name": "Interpersonal skills", 
            "skill_desc": "Communicate and interact"
            # "role_skill_relation":"role-skill"
        })

# test Course
class TestCourse(unittest.TestCase):
    def test_json(self):
        courseTest = course(course_code = 1, course_name = "Systems thinking", course_status = "active", course_desc = "Apply system thinking")
        self.assertEqual(courseTest.json(), {
            "course_code": 1, 
            "course_name":"Systems thinking", 
            "course_status": "active",
            "course_desc":"Apply system thinking"
            # "skill_course_relation":"role-skill"
        })

# For endpoints
class TestDisplayRole(TestApp):
    def test_display_role(self):
        r1 = role(role_code=1, role_name = "admin", role_desc = "Best job in the world")
        r2 = role(role_code=2, role_name = "HR", role_desc = "HR job")

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
                    "role_desc":"Best job in the world"
                },
                {
                    "role_code":2,
                    "role_name":"HR",
                    "role_desc":"HR job"
                }
                
                ]
                
            },
            "message": "These are the roles available."
        })
        self.assertRaises(Exception, r1 == None)
        self.assertRaises(Exception, r2 == None)


class TestDisplaySkill(TestApp):
    def test_display_skill(self):
        s1 = skill(skill_code = 1, skill_name = "Interpersonal skills", skill_desc = "Communicate and interact")
        s2 = skill(skill_code = 2, skill_name = "Communication skills", skill_desc = "Able to comunicate")

        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

        response = self.client.get("/skills")
        self.assertEqual(response.json,
        {
            "code": 200,
            "data": {
                "skills": [{
                    "skill_code": 1, 
                    "skill_name": "Interpersonal skills", 
                    "skill_desc": "Communicate and interact"
                },
                {
                    "skill_code": 2, 
                    "skill_name": "Communication skills", 
                    "skill_desc": "Able to comunicate"
                }
                ]
                
            },
            "message": "These are the skills available."
        })
        self.assertRaises(Exception, s1 == None)
        self.assertRaises(Exception, s1 == None)


if __name__ == "__main__":
    unittest.main()