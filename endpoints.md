--------------------------
Authentication Endpoints:
--------------------------

http://127.0.0.1:8080/api/user/register/teacher/
body = { "email": email, "password": password}

http://127.0.0.1:8080/api/user/register/student/
body = { "email": email, "password": password}

http://127.0.0.1:8080/api/user/login/
body = { "email": email, "password": password}

----------------------
Course Endpoints:
----------------------

GET: http://127.0.0.1:8080/api/online-course/courses/

POST: http://127.0.0.1:8080/api/online-course/courses/
      body = { 
            "teacher":int,
            "title": str,
            "description": str,
            "content": str,
        }}

GET: http://127.0.0.1:8080/api/online-course/courses/pk/

PUT:  http://127.0.0.1:8080/api/online-course/courses/pk/
     body = { 
            "teacher":int,
            "title": str,
            "description": str,
            "content": str,
        }}

DELETE:  http://127.0.0.1:8080/api/online-course/courses/pk/

---------------------------------
Course Registration Endpoints:
---------------------------------

GET: http://127.0.0.1:8080/api/online-course/course-registeration/

POST: http://127.0.0.1:8080/api/online-course/course-registeration/
      body = { 
            "student":int,
            "course": int,
        }}

POST: http://127.0.0.1:8080/api/online-course/course-registeration/pk/

PUT:  http://127.0.0.1:8080/api/online-course/course-registeration/pk/
      body = { 
            "student":int,
            "course": int,
        }}

DELETE: http://127.0.0.1:8080/api/online-course/course-registeration/pk/


----------------------------------------------------------------
search endpoint
----------------------------------------------------------------

GET http://127.0.0.1:8080/api/online-course/course/?search=
