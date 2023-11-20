import course as c

class Prerequisite:
    def __init__(self, this_course=None, grade_levels=[], min_grade=60, alternatives=None, simultaneous=None, data=None):
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
        if data is not None:
            self = Prerequisite.build_prereq(data)
            return
        self.simultaneous = simultaneous
        self.alternatives = alternatives
        self.this_course = this_course
        self.min_grade = 60
        self.grade_levels = []
    
    def check_prerequisite(self, student):
        """
        Check if the student meets the prerequisite criteria for this course.

        Args:
            student (Student): The student object to check the prerequisite for.

        Returns:
            bool: True if the student meets the prerequisite criteria, False otherwise.
        """
        # If this is a single-course pre-req, check the criteria directly.
        if self.simultaneous.length == 0 and self.alternatives.length == 0:
            if self.this_course not in student.courses:
                return False
            return student.courses[self.this_course] >= self.min_grade and student.grade_level in self.grade_levels
        else: # Recursively check the pre-reqs
            for course in self.simultaneous:
                if not course.check_course(student):
                    return False
            for alt in self.alternatives:
                if alt.check_prerequisite(student):
                    return True
            return False
        
    def build_prereq(data):
       
        """
        Recursively build a prerequisite object based on the provided data.

        Args:
            data (dict): The data representing the prerequisite.

        Returns:
            Prerequisite: The built prerequisite object.
        """

        
        if data.keys().length > 1:
            simuls = []
            for a in data:
                simuls.append(Prerequisite.build_prereq(a))
            return Prerequisite(simultaneous=simuls)
        elif 'one_of' in data.keys():
            alts_data = data['one_of']
            alts = []
            for a in alts_data:
                alts.append(Prerequisite.build_prereq(a))
            return Prerequisite(alternatives=alts)
        elif 'all_of' in data.keys():
            all_data = data['all_of']
            simuls = []
            for a in all_data:
                simuls.append(Prerequisite.build_prereq(a))
            return Prerequisite(simultaneous=simuls)
        else:
            prereq_course = data['course']
            return Prerequisite(prereq_course, data['grade_levels'], data['min_grade'])
            
