'''
This module defines the course flow of the school. The course flow is
a directed graph of courses, where each course is a node and each 
prerequisite is an edge. The course flow is used to determine which 
courses a student can take based on their grade level and the courses they have taken.

The edges of the graph are represented by "arrows" which consist of a from_course, and a to_course.
Additionally each arrow
'''

from prerequisite import Prerequisite
from student import Student
from courses import Course

class CourseFlow:
    def __init__(self, data, course_list):
        self.arrows = {}
        for course in course_list:
            self.arrows[course] = []
        self.build_flow(data, course_list)
    
    def __add_arrow(self, arrow):
        if arrow.from_course not in self.arrows:
            self.arrows[arrow.from_course] = []
        self.arrows[arrow.from_course].append(arrow)
    
    def build_flow(self, flow_data, course_list):
        for entry in flow_data:
            grade_level = entry['grade_level']
            courses = entry['courses']
            for course in courses:
                from_course = course_list.get_course(course['course_name'])
                arrows = Arrow.build_arrows_from_data(course['arrows'], grade_level, from_course, course_list)
                for arrow in arrows:
                    self.__add_arrow(arrow)
    
    def get_arrows(self, course):
        return self.arrows[course]
    
    def get_arrows_by_grade_level(self, course, grade_level):
        return [arrow for arrow in self.arrows[course] if arrow.grade_level == grade_level]

class Arrow:
    def __init__(self, from_course, to_course, rank, grade_level):
        self.from_course = from_course
        self.to_course = to_course
        self.rank = rank
        self.grade_level = grade_level
    
    @classmethod
    def build_arrows_from_data(cls, arrows, grade_level, from_course, course_list):
        to_course = None
        rank = None
        result = []

        for arrow in arrows:
            to_course = course_list.get_course(arrow['course_name'])
            rank = arrow['rank']
            result.append(Arrow(from_course, to_course, rank, grade_level))

        return result
