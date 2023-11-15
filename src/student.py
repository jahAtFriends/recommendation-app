from course import Course

class Student:
    def __init__(self, name, grade_level):
        self.name = name
        self.courses = {}
        self.grade_level = grade_level
        
    def add_course(self, course: Course, grade):
        self.courses[course] = grade
        
    def get_courses(self):
        return self.courses