import unittest 
import warnings 
from api import app


class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        
        warnings.simplefilter("ignore", category=DeprecationWarning)
        
    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Student database</p>")
        
    def test_get_students(self):
        response = self.app.get("/students")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Joseph" in response.data.decode())
    
    def test_get_student_by_ID(self):
        response = self.app.get("/students/201980020")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Joseph" in response.data.decode())
    
    def test_get_seat(self):
        response = self.app.get("/students/201980020/seat")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("front" in response.data.decode())
    
    def test_get_course(self):
        response = self.app.get("/students/201980020/course")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("CNHS" in response.data.decode())
    
    def test_create_student(self):
        data = {
            "FirstNAme": "Shon",
            "LastName": "Brandon",
            "Address" : "Bataraza"            
        }
        response = self.app.post("/students", json=data)
        self.assertEqual(response.status_code, 201)
        
    def test_update_student(self):
        data = {
            "FirstNAme": "Ivan",
            "LastName": "Delosreyes",
            "Address" : "Brookes",
            "ID": 201980065           
        }
        response = self.app.post("/students", json=data)
        self.assertEqual(response.status_code, 201)
    
    def test_delete_student(self):
        response = self.app.delete("/students/201980081")
        self.assertEqual(response.status_code, 200)
        
    
if __name__ == "__main__":
    unittest.main()