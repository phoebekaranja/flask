import unittest
from app.models import Role

class RoleModelTest(unittest.TestCase):

    def setUp(self):
        self.new_role = Role('1','admin')

if __name__ =='__main__':
    unittest.main()
