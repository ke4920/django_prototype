import unittest

from assasdb import DatabaseManager

class DatabaseManagerTest(unittest.TestCase):
    
    def setUp(self):
        
        self.database_manager = DatabaseManager()
        
    def tearDown(self):
        
        self.database_manager = None

    def test_database_manager_basic(self):

        self.database_manager.upload()
        
if __name__ == '__main__':
    unittest.main()