import unittest 
import warnings 
from api import app
from base64 import b64encode



class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        
        warnings.simplefilter("ignore", category=DeprecationWarning)
        
    def test_index_page(self):
        headers = {
            "Authorization": "Basic " + b64encode(b"admin:admin").decode()
        }
        
        response = self.app.get("/",headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Student database</p>")
        
    def test_get_students(self):
        headers = {
            "Authorization": "Basic " + b64encode(b"admin:admin").decode()
        }
        response = self.app.get("/students",headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Joseph" in response.data.decode())
    
    def test_get_student_by_ID(self):
        headers = {
            "Authorization": "Basic " + b64encode(b"admin:admin").decode()
        }
        response = self.app.get("/students/201980020",headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Joseph" in response.data.decode())
    
    def test_get_seat(self):
        headers = {
            "Authorization": "Basic " + b64encode(b"admin:admin").decode()
        }
        response = self.app.get("/students/201980020/seat",headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("front" in response.data.decode())
    
    def test_get_course(self):
        headers = {
            "Authorization": "Basic " + b64encode(b"admin:admin").decode()
        }
        response = self.app.get("/students/201980020/course", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("CNHS" in response.data.decode())
    
    def test_create_student(self):
        headers = {
            "Authorization": "Basic " + b64encode(b"admin:admin").decode()
        }
        data = {
            "FirstNAme": "Shon",
            "LastName": "Brandon",
            "Address" : "Bataraza"            
        }
        response = self.app.post("/students", json=data, headers=headers)
        self.assertEqual(response.status_code, 201)
        
    def test_update_student(self):
        headers = {
            "Authorization": "Basic " + b64encode(b"admin:admin").decode()
        }
        data = {
            "FirstNAme": "Ivan",
            "LastName": "Delosreyes",
            "Address" : "Brookes",
            "ID": 201980065           
        }
        response = self.app.post("/students", json=data,headers=headers)
        self.assertEqual(response.status_code, 201)
    
    def test_delete_student(self):
        headers = {
            "Authorization": "Basic " + b64encode(b"admin:admin").decode()
        }
        response = self.app.delete("/students/201980081",headers=headers)
        self.assertEqual(response.status_code, 200)
        
    
if __name__ == "__main__":
    unittest.main()