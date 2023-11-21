class Student:
    def __init__(self, name, class_year):
        self.name = name
        self.courses = {}
        self.recommendations = []
        
    def add_course(self, course, grade, year):
        """
        Add a course with its grade and year to the student's record.

        Args:
            course (str): The name of the course.
            grade (str): The grade obtained in the course.
            year (int): The year when the course was taken.

        Returns:
            None
        """
        self.courses[course] = (grade, year)
    
    def get_grade_level(self, year):
        """
        Calculates the grade level of the student based on the given year.

        Parameters:
        - year (int): The (usually current) year.

        Returns:
        - int: The grade level of the student.
        """
        return 12 - (self.class_year - year)

    def get_courses(self):
        return self.courses
    
    def get_current_courses(self, year):
        """
        Returns a list of current courses for the given year.

        Parameters:
        - year (int): The year for which to retrieve the current courses.

        Returns:
        - list: A list of current courses for the given year.
        """
        current_courses = []
        for course in self.courses:
            grade, course_year = self.courses[course]
            if course_year == year:
                current_courses.append(course)
        return current_courses
    
    def get_identifier(self):
        """
        Returns a unique-ish identifier for the student.

        Returns:
        - str: A unique identifier for the student.
        """
        return self.name + str(self.class_year)
    
    @classmethod
    def get_identifier(cls, first_name, last_name, class_year):
        """
        Returns a unique-ish identifier for the student.

        Returns:
        - str: A unique identifier for the student.
        """
        return first_name + " " + last_name + str(class_year)
    
    
class Roster:
    def __init__(self):
        self.students = {}

    def build_roster_from_data(self, data):
        """
        Builds a roster of students from a list of data and adds academic records.

        Args:
            data (list): A list of data from which to build the roster.

        Returns:
            None
        """
        for row in data:
            first_name, last_name, class_year, year, course, grade = row['first_name'], row['last_name'], row['class_year'], row['year'], row['course'], row['average']
            identifier = Student.get_identifier(first_name, last_name, class_year)
            student = None
            if identifier not in self.students:
                self.students[identifier] = Student(first_name + " " + last_name, class_year)
            student = self.students[identifier]
            student.add_course(course, grade, year)
    
    def __iter__(self):
        for student in self.students.values():
            yield student