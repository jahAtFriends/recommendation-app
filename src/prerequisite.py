from student import Student

class Prerequisite:
    """
    Represents a prerequisite for a course.

    Attributes:
        this_course (str): The course for which the prerequisite is defined.
        grade_levels (list): A list of grade levels that satisfy the prerequisite.
        min_grade (int): The minimum grade required to satisfy the prerequisite.
        alternatives (list): A list of alternative courses that can satisfy the prerequisite.
        simultaneous (list): A list of courses that can be taken simultaneously with the prerequisite.

    Methods:
        __init__(self, this_course=None, grade_levels=[], min_grade=60, alternatives=None, simultaneous=None, data=None):
            Initializes a Prerequisite object.
        
        check_prerequisite(self, student):
            Check if the student meets the prerequisite criteria for this course.
        
        build_prereq(data):
            Recursively build a prerequisite object based on the provided data.
    """

    def __init__(self, this_course=None, grade_levels=[], min_grade=60, alternatives=[], simultaneous=[]):
        """
        Initializes a Prerequisite object. In the argruments below, only one of this_course, alternatives,
        or simultaneous should be provided. Alternatively, if data is provided, the Prerequisite object
        will be built from the data, ignoring the other arguments.

        Args:
            this_course (str): The course for which the prerequisite is defined.
            grade_levels (list): A list of grade levels that satisfy the prerequisite.
            min_grade (int): The minimum grade required to satisfy the prerequisite.
            alternatives (list): A list of alternative courses that can satisfy the prerequisite.
            simultaneous (list): A list of courses that can be taken simultaneously with the prerequisite.
            data (dict): A dictionary containing data to build the Prerequisite object.

        Returns:
            None
        """
        self.simultaneous = simultaneous
        self.alternatives = alternatives
        self.this_course = this_course
        self.min_grade = min_grade
        self.grade_levels = grade_levels
    
    def check_prerequisite(self, student: Student, year):
        """
        Check if the student meets the prerequisite criteria for this course.

        Args:
            student (Student): The student object to check the prerequisite for.

        Returns:
            bool: True if the student meets the prerequisite criteria, False otherwise.
        """
        # If this is a single-course pre-req, check the criteria directly.
        if len(self.simultaneous) == 0 and len(self.alternatives) == 0:
            if self.this_course not in student.courses:
                return False
            return student.courses[self.this_course][0] >= self.min_grade and student.get_grade_level(year) in self.grade_levels
        else: # Recursively check the pre-reqs
            if len(self.simultaneous) > 0:
                for course in self.simultaneous:
                    if not course.check_prerequisite(student, year):
                        return False
                return True
            else:
                for alt in self.alternatives:
                    if alt.check_prerequisite(student, year):
                        return True
                return False
        
    @classmethod
    def build_prereq(cls, data, grade_levels):
        """
        Recursively build a prerequisite object based on the provided data.

        Args:
            data (dict): The data representing the prerequisite.

        Returns:
            Prerequisite: The built prerequisite object.
        """
        if len(data) == 0:
            return None
        if isinstance(data, list) and len(data) > 1:
            simuls = []
            for a in data:
                simuls.append(Prerequisite.build_prereq(a, grade_levels))
            return Prerequisite(simultaneous=simuls, grade_levels=grade_levels)
        if isinstance(data, list) and len(data) == 1:
            return Prerequisite.build_prereq(data[0], grade_levels=grade_levels)
        if 'one_of' in data.keys():
            alts_data = data['one_of']
            alts = []
            for a in alts_data:
                alts.append(Prerequisite.build_prereq(a, grade_levels=grade_levels))
            return Prerequisite(alternatives=alts)
        if 'all_of' in data.keys():
            all_data = data['all_of']
            simuls = []
            for a in all_data:
                simuls.append(Prerequisite.build_prereq(a, grade_levels=grade_levels))
            return Prerequisite(simultaneous=simuls)
        else:
            prereq_course = data['course']
            return Prerequisite(this_course=prereq_course, grade_levels = grade_levels, min_grade=data['min_grade'])
            
