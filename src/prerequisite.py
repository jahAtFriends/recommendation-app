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

    
    def satisfied_by(self, student: Student):
        """
        Check if the student meets the prerequisite criteria.

        Args:
            student (Student): The student object to check the prerequisite for.

        Returns:
            bool: True if the student meets the prerequisite criteria, False otherwise.
        """
        # If this is a single-course pre-req, check the criteria directly.
        if self.this_course is not None:
            if self.this_course not in student.courses:
                return False
            temp = student.courses[self.this_course][0] >= self.min_grade
            return student.courses[self.this_course][0] >= self.min_grade
        # If this is a grade-level pre-req, check the grade level.
        elif len(self.grade_levels) > 0:
            return student.get_grade_level() in self.grade_levels
        else: # Recursively check the pre-reqs
            if len(self.simultaneous) > 0:
                for simul in self.simultaneous:
                    if not simul.satisfied_by(student):
                        return False
                return True
            else:
                for alt in self.alternatives:
                    if alt.satisfied_by(student):
                        return True
                return False
        
    @classmethod
    def build_prereq(cls, data, class_list):
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
                simuls.append(Prerequisite.build_prereq(a, class_list))
            return Prerequisite(simultaneous=simuls)
        if isinstance(data, list) and len(data) == 1:
            return Prerequisite.build_prereq(data[0], class_list)
        if 'one_of' in data.keys():
            alts_data = data['one_of']
            alts = []
            for a in alts_data:
                alts.append(Prerequisite.build_prereq(a, class_list))
            return Prerequisite(alternatives=alts)
        if 'all_of' in data.keys():
            all_data = data['all_of']
            simuls = []
            for a in all_data:
                simuls.append(Prerequisite.build_prereq(a, class_list))
            return Prerequisite(simultaneous=simuls)
        if 'grade_levels' in data.keys():
            return Prerequisite(grade_levels=data['grade_levels'])
        else:
            prereq_course = class_list.get_course(data['course_name'])
            return Prerequisite(this_course=prereq_course, min_grade=data['min_grade'])