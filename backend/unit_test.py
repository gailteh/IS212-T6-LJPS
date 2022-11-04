import unittest
from role_skill_course import role, skill, course

class TestRole(unittest.TestCase):
    #create objects that all functions uses
    def setUp(self):
        self.r = role("CEO", 1, 'manage the whole company')
        self.rl = role("UI designer", 2, 'design the web application')
        self.r2 = role("Business manager", 3, 'get profits')

    #teardown is at the end, make sure the code is clean and remove the things 
    def tearDown(self):
        self.r = None
        self.rl = None
        self.r2 = None

    # each unit test is run independently 
    def test_display_role(self):
        role_code = self.r.balance
        #assertEqual tells pass or fail and break loop and the rest will not run
        self.assertEqual(self.r.role_code, 1)
        self.assertEqual(self.r.role_name, "CEO")
        self.s.deposit(500)
        self.assertEqual(self.s.balance, 1500)

    def test_createRole(self):
        
        self.s.withdraw(1000)
        self.assertEqual(self.s.balance, 500)

        #test if the amount goes beyond the balance amount, throw an error
        self.assertRaises(Exception, self.s.withdraw, 600)

    def test_EqualAccounts(self): # could be for boundary test cases
        

        #assert checking the object itself
        #assert checking the fields at a time
        self.assertTrue(self.s.balance > 0)
        # check with s is = to s
        self.assertIs(self.s, self.s)
        self.assertIsNot(self.s, self.sl)

if __name__ == "__main__":
    unittest.main()