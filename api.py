from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL
import xml.etree.ElementTree as ET
import xmltodict
import functools

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] =  "root"
app.config["MYSQL_PASSWORD"] =  ""
app.config["MYSQL_DB"] =  "studentdb"
app.config["MYSQL_CURSORCLASS"] =  "DictCursor"

mysql = MySQL(app)

def login_reqiured(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == "admin" and auth.password== "admin":
            return f(*args, **kwargs)
        return make_response('Authentication failed!',401, {'WWW-Authenticate':'Basic realm="Login required!"'})
    return decorated_function
    


@app.route("/")
@login_reqiured
def studentdb():
    return "<p>Student database</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data



@app.route("/students", methods=["GET"])
@login_reqiured
def get_students():
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    address = request.args.get("address")
    
    format_param = request.args.get("format")
    
    qry = "select * from students where 1=1"
    if firstname:
        qry += f" AND FirstNAme LIKE '{firstname}%'" 
    if lastname:
        qry += f" AND LastName LIKE '{lastname}%'" 
    if address:
        qry += f" AND Address LIKE '{address}%'" 
    
    if format_param and format_param.lower() == 'xml':
        data = data_fetch(qry)
        xml_data = xmltodict.unparse({"students": {"student":data}})
        response = make_response(xml_data)
        response.headers["Content-Type"] = "application/xml"
        return response
    else:
        data = data_fetch(qry)
        return make_response(jsonify(data), 200)


@app.route("/students/<int:ID>", methods=["GET"])
@login_reqiured
def get_student_ID(ID):
    format_param = request.args.get("format")
    if format_param and format_param.lower() == 'xml':
        data = data_fetch("""select * from students where ID = {}""".format(ID))
        xml_data = xmltodict.unparse({"students": {"student":data}})
        response = make_response(xml_data)
        response.headers["Content-Type"] = "application/xml"
        return response
    else:
        data = data_fetch("""select * from students where ID = {}""".format(ID))
        return make_response(jsonify(data), 200)



@app.route("/students/<int:ID>/seat", methods=["GET"])
@login_reqiured
def get_seat_by_ID(ID):
    format_param = request.args.get("format")
    if format_param and format_param.lower() == 'xml':
        data = data_fetch("""
                        select students.FirstNAme, students.LastName, seat.seat_position, seat.seat_no
                        from students inner join seat 
                        on students.ID = seat.ID
                        where students.ID = {}
                        """.format(ID))
        xml_data = xmltodict.unparse({"students": {"student":data}})
        response = make_response(xml_data)
        response.headers["Content-Type"] = "application/xml"
        return response
    else:
        data = data_fetch("""
                        select students.FirstNAme, students.LastName, seat.seat_position, seat.seat_no
                        from students inner join seat 
                        on students.ID = seat.ID
                        where students.ID = {}
                        """.format(ID))
        return make_response(jsonify(data), 200)

@app.route("/students/<int:ID>/course", methods=["GET"])
def get_course_by_ID(ID):
    format_param = request.args.get("format")
    if format_param and format_param.lower() == 'xml':
        data = data_fetch("""
                        select students.FirstNAme, students.LastName, course.Course_name, course.Course_ID
                        from students inner join course 
                        on students.ID = course.ID
                        where students.ID = {}
                        """.format(ID))
        xml_data = xmltodict.unparse({"students": {"student":data}})
        response = make_response(xml_data)
        response.headers["Content-Type"] = "application/xml"
        return response
    else:
    
        data = data_fetch("""
                        select students.FirstNAme, students.LastName, course.Course_name, course.Course_ID
                        from students inner join course 
                        on students.ID = course.ID
                        where students.ID = {}
                        """.format(ID))
        return make_response(jsonify(data), 200)



@app.route("/students", methods=["POST"])
@login_reqiured
def add_student():
    cur = mysql.connection.cursor()
    info = request.get_json()
    FirstNAme = info["FirstNAme"]
    LastName = info["LastName"]
    Address = info["Address"]
    cur.execute(
        """Insert into students (FirstNAme, LastName, Address) value (%s, %s, %s)""",
        (FirstNAme, LastName, Address),
    )
    
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "student added successfully", "rows_affected":rows_affected}),201,)


@app.route("/students/<int:ID>", methods = ["PUT"])
@login_reqiured
def update_student(ID):
    cur = mysql.connection.cursor()
    info = request.get_json()
    FirstNAme = info["FirstNAme"]
    LastName = info["LastName"]
    Address = info["Address"]
    cur.execute(
        """update students set FirstNAme = %s, LastName = %s, Address = %s where ID = %s""",
        (FirstNAme, LastName, Address, ID),
    )
    
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "student updated successfully", "rows_affected":rows_affected}),200,)

@app.route("/students/<int:ID>", methods = ["DELETE"])
@login_reqiured
def delete_student(ID):
    cur = mysql.connection.cursor()
    cur.execute(""" delete from students where ID = %s """,(ID,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "student delete successfully", "rows_affected":rows_affected}),200,)


if __name__ == "__main__":
    app.run(debug=True)
    