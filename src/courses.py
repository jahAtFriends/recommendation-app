from prerequisite import Prerequisite

class Course:
    def __init__(self, name, grade_levels=[], department=None, prerequisites=None):
        self.prerequisites = prerequisites
        self.name = name
        self.grade_levels = grade_levels
        self.department = department
    
    def add_prerequisite(self, prerequisite):
        self.prerequisites.append(prerequisite)

class Course_List:
    def __init__(self):
        self.courses = []
    
    def add_course(self, course):
        self.courses.append(course)


    def get_course(self, name):
        """
        Retrieves a course object based on its name.

        Args:
            name (str): The name of the course to retrieve.

        Returns:
            Course: The course object with the specified name.

        Raises:
            ValueError: If the course with the specified name is not found in the course list.
        """
        for course in self.courses:
            if course.name == name:
                return course
        raise ValueError(f'Course {name} not found in course list.')
    
    
    @classmethod
    def build_course_list(cls, data):
        course_list = Course_List()
        for course in data:
            name = course['course_name']
            grade_levels = course['grade_levels']
            department = course['department']
            course_list.add_course(Course(name, grade_levels, department))
        return course_list
    
    def apply_prerequisites_to_courses(self, data):
        for course in data:
            name = course['course_name']
            prerequisites = Prerequisite.build_prereq(course['prerequisites'])
            self.get_course(name).prerequisites = prerequisites