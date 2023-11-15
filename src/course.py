from typing import Type
from typing import List
from typing import List, TypeVar
from student import Student
from typing import Dict
import json
from json import JSONEncoder



class Course:
    """
    A class representing a course in a school.

    Attributes:
    - name (str): The name of the course.
    - grade_levels (List[int]): A list of grade levels that can take the course.
    - prerequisites (List[Course]): A list of courses that must be taken before this course.

    Methods:
    - check_prerequisites(student: Student) -> bool: Checks if the student has taken all the prerequisites for the course.
    - check_grade_level(student: Student) -> bool: Checks if the student is in a grade level that can take the course.
    - check_course(student: Student) -> bool: Checks if the student can take the course based on prerequisites and grade level.
    - add_prerequisite(prerequisite: Course): Adds a course to the list of prerequisites for this course.
    """
    def __init__(self, name: str, grade_levels: List[int]):
        self.name = name
        self.grade_levels = grade_levels
        self.prerequisites = []

    def check_prerequisites(self, student: Student) -> bool:
        for prerequisite in self.prerequisites:
            if prerequisite.grade_level != student.grade_level:
                continue
            if not prerequisite.check_prerequisite(student):
                return False
        return True

    def check_grade_level(self, student: Student) -> bool:
        return student.grade_level in self.grade_levels
    
    def check_course(self, student: Student) -> bool:
        return self.check_prerequisites(student) and self.check_grade_level(student)
    
    def add_prerequisite(self, prerequisite):
        self.prerequisites.append(prerequisite)

    def __str__(self):
        return json.dumps(self.__dict__, indent=2, cls=PrerequisiteEncoder)
    
class Prerequisite:
    """
    Represents a prerequisite course required for another course.

    Attributes:
    - course (Type[Course]): the course that is a prerequisite
    - grade_levels (List[int]): the grade levels that the prerequisite is required for
    - min_grade (int): the minimum grade required to pass the prerequisite (default: 60)
    """
    def __init__(self, course: Type[Course], grade_levels: List[int], min_grade=60):
        self.course = course
        self.min_grade = min_grade
        self.grade_levels = grade_levels
    
    def check_prerequisite(self, student):
        if self.course not in student.courses:
            return False
        return student.courses[self.course] >= self.min_grade
    
    def __str__(self):
        return {"course": self.course.name, "min_grade": self.min_grade}
    
class PrerequisiteEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Alternatives):
            return {
                'courses': obj.courses,
                'grade_levels': obj.grade_levels,
                'min_grades': obj.min_grades
            }
        if isinstance(obj, Prerequisite):
            return {
                'course': obj.course.name,
                'grade_levels': obj.grade_levels,
                'min_grade': obj.min_grade
            }
        return super().default(obj)

class Alternatives(Prerequisite):
    def __init__(self, courses: list, grade_levels, min_grades: list):
        self.courses = courses
        self.min_grades = min_grades
        self.grade_levels = grade_levels
    
    def check_prerequisite(self, student):
        for i in range(len(self.courses)):
            if self.courses[i] in student.courses and student.courses[self.courses[i]] >= self.min_grades[i]:
                return True
        return False
    
    def __str__(self):
        return {"courses": self.courses, "min_grades": self.min_grades}
    
class CourseFlow:
    """
    A class representing the flow of courses from a given course, based on their rank and grade levels.

    Attributes:
    - from_course (Course): The course from which the flow is being determined.
    - rankflow (Dict[Course, int]): A dictionary mapping courses to their rank.
    - grade_levels (List[int]): A list of current (not future) grade levels to which the flow applies.
    """

    def __init__(self, from_course: Course,  rankflow: Dict[Course, int], grade_levels: List[int]):
        self.from_course = from_course
        self.rankflow = rankflow
        self.grade_levels = grade_levels
    
    def get_courses_by_rank(self, rank: int):
        return [course for course, course_rank in self.rankflow.items() if course_rank == rank]

