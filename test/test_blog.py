import unittest
from app.models import Blog

class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.new_blog = Blog(category = 'Personal_Blog')

if __name__ =='__main__':
    unittest.main()
