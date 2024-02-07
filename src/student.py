from deprecated import deprecated

class Student:
    def __init__(self, name, class_year, current_grade):
        self.name = name
        self.courses = {}
        self.recommendations = []
        self.class_year = class_year
        self.current_grade = current_grade
        
    def add_course(self, course, grade, year, instructor):
        """
        Add a course with its grade and year to the student's record.

        Args:
            course (str): The name of the course.
            grade (str): The grade obtained in the course.
            year (int): The year when the course was taken.

        Returns:
            None
        """
        self.courses[course] = (grade, year, instructor)
    
    def get_grade_level(self):
        """
        Calculates the grade level of the student based on the given year.

        Parameters:
        - year (int): The (usually current) year.

        Returns:
        - int: The grade level of the student.
        """
        return self.current_grade

    def get_courses(self):
        return self.courses
    
    def get_courses_by_year(self, year):
        """
        Returns a list of courses taken by the student in the given year.

        Parameters:
        - year (int): The year for which to retrieve the courses.

        Returns:
        - list: A list of courses taken by the student in the given year.
        """
        courses = []
        for course in self.courses:
            grade, course_year, instructor = self.courses[course]
            if course_year == year:
                courses.append(course)
        return courses
    
    
    @deprecated(version='0.2.1-alpha', reason="Use get_courses_by_year(year) instead.")
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
            grade, course_year, instructor = self.courses[course]
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

    def __str__(self):
        return self.name + " " + str(self.class_year)
    
    @classmethod
    def get_identifier(cls, name, class_year):
        """
        Returns a unique-ish identifier for the student.

        Returns:
        - str: A unique identifier for the student.
        """
        return name + str(class_year)
    
    def has_taken(self, course):
        return course in self.courses
    
    def get_teacher(self, course):
        if course not in self.courses:
            return None
        return self.courses[course][2]
    
    
class Roster:
    def __init__(self, year):
        self.students = {}
        self.year = year

    def build_roster_from_data(self, data, course_list):
        """
        Builds a roster of students from a list of data and adds academic records.

        Args:
            data (list): A list of data from which to build the roster.

        Returns:
            None
        """
        for row in data:
            name = row['name']
            class_year = int(row['class_year'])
            year = int(row['year'])
            course = row['course']
            grade = float(row['average'])
            instructor = row['instructor']

            identifier = Student.get_identifier(name, class_year)
            student = None
            if identifier not in self.students:
                student_current_grade = 12 - (class_year - self.year)
                self.students[identifier] = Student(name, class_year, student_current_grade)
            student = self.students[identifier]
            course = course_list.get_course(course)
            student.add_course(course, grade, year, instructor)
    
    def __iter__(self):
        for student in self.students.values():
            yield student