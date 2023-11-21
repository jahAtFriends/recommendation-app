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

class CourseFlow:
    def __init__(self, data=None):
        self.nodes = {}
        if data is not None:
            self.build_flow(data)
    
    def __add_arrow(self, from_course, to_course, rank, grade_levels, prerequisites):
        to_course = {
            'course': to_course,
            'rank': rank,
            'grade_levels': grade_levels,
            'prerequisites': prerequisites
        }
        if from_course not in self.nodes:
            self.nodes[from_course] = []
        self.nodes[from_course].append(to_course)
    
    def build_flow(self, flow_data):
        """
        Builds the flow of courses based on the provided flow_data.

        Args:
            flow_data (list): A list of dictionaries representing the flow data.

        Returns:
            None
        """
        for record in flow_data:
            from_course = record['course']
            arrows = record['arrows']
            for arrow in arrows:
                to_course = arrow['to_course']
                rank = arrow['rank']
                grade_levels = arrow['grade_levels']
                prerequisite_data = arrow['prerequisites']
                prerequisites = Prerequisite(data=prerequisite_data)
                self.__add_arrow(from_course, to_course, rank, grade_levels, prerequisites)

    def get_recommendations(self, student: Student, year):
        """
        Get the recommendations for the given student.

        Args:
            student (Student): The student to get recommendations for.
            year (int): The year to get recommendations for.

        Returns:
            list: A list of courses that the student should take next.
        """
        recommendations = []
        for course in student.get_current_courses(year):
            for arrow in self.nodes[course]:
                to_course = arrow['to_course']
                rank = arrow['rank']
                grade_levels = arrow['grade_levels']
                prerequisites = arrow['prerequisites']
                if student.grade_level in grade_levels and prerequisites.check_prerequisite(student):
                    recommendations.append({
                        'course': to_course,
                        'rank': rank
                    })
        return recommendations