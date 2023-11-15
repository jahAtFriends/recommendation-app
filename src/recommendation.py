import yaml
from student import Student
from course import Course

class Recommendation:
    def __init__(self, student, course_flow):
        self.student = student
        self.course_flow = course_flow

    def generate_recommendation(self):
        recommendations = []
        for course_name, course_grade in self.student.courses.items():
            if course_name in self.course_flow:
                next_courses = self.course_flow[course_name]
                for next_course in next_courses:
                    course = Course(next_course, self.course_flow)
                    if course.check_prerequisites(self.student):
                        recommendations.append(next_course)
        return recommendations