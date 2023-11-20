'''
This module defines the course flow of the school. The course flow is
a directed graph of courses, where each course is a node and each 
prerequisite is an edge. The course flow is used to determine which 
courses a student can take based on their grade level and the courses they have taken.

The edges of the graph are represented by "arrows" which consist of a from_course, and a to_course.
Additionally each arrow
'''

from prerequisite import Prerequisite

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

