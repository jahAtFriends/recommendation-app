import csv
import yaml
from student import Student
from course import Course, Prerequisite, Alternatives, CourseFlow
from recommendation import Recommendation
from utils.csv_processor import read_csv, write_csv
from utils.yaml_processor import read_yaml

courses = []
flow = []

def main():
    flow_data = read_yaml('flow.yaml')
    build_courses(flow_data)
    build_flow(flow_data)
    prerequisite_data = read_yaml('prerequisites.yaml')

    for course in courses:
        set_prerequisites(course, prerequisite_data)
    
    for course in courses:
        print(str(course))


    
def build_courses(flow_data):
    global courses
    for element in flow_data["course_flow"]:
        course_name = element['course']
        grade_levels = element['grade_levels']
        course = Course(course_name, grade_levels)
        courses.append(course)

def build_flow(flow_data):
    """
    Builds a course flow based on the given flow data.

    Args:
        flow_data (dict): A dictionary containing the course flow data. Loaded from flow.yaml.

    Returns:
        None
    """
    global flow
    for element in flow_data["course_flow"]:
        course_name = element['course']
        course = get_course(course_name)
        if 'grade_level_recommendations' in element:
            gl_recs = element['grade_level_recommendations']
            for gl_rec in gl_recs:
                grade_levels = gl_rec['grade_levels']
                recs = gl_rec['recommendations']
                rank_flow = {}
                for rec in recs:
                    name = rec['name']
                    rank = rec['rank']
                    rank_flow[name] = rank
                course_flow = CourseFlow(course, grade_levels, rank_flow)
                flow.append(course_flow)
        else:
            recs = element['recommendations']
            grade_levels = element['grade_levels']
            rank_flow = {}
            for rec in recs:
                name = rec['name']
                rank = rec['rank']
                rank_flow[name] = rank
            course_flow = CourseFlow(course, grade_levels, rank_flow)
            flow.append(course_flow)

def get_course(course_name):
    """
    Get the course object with the given name. If the course does not exist, create a new course object and add it to the global courses list.

    Args:
        course_name (str): The name of the course to retrieve.

    Returns:
        Course: The course object with the given name.
    """
    global courses
    for course in courses:
        if course.name == course_name:
            return course
    course = Course(course_name, [])
    courses.append(course)
    return course


def set_prerequisites(course: Course, prerequisites: list):
    all_courses = prerequisites['courses']
    #select the course where course.name is the course name in all_courses
    prereq_course = None
    for c in all_courses:
        if c['name'] == course.name:
            prereq_course = c
            break
    if prereq_course is None:
        return
    if 'grade_level_prerequisites' in prereq_course:
        gl_reqs = prereq_course['grade_level_prerequisites']
        for gl_req in gl_reqs:
            grade_levels = gl_req['grade_levels']
            course.add_prerequisite(build_prerequistes(course, gl_req['prerequisites'], grade_levels))
    else:
        course.add_prerequisite(build_prerequistes(course, prereq_course['prerequisites'], prereq_course['grade_levels']))

def build_prerequistes(course: Course, prerequisite_data, grade_levels: list[int]) -> Prerequisite:
    for record in prerequisite_data:
        if 'one_of' in record:
            alts_data = record['one_of']
            alternatives = []
            min_grades = []
            for a in alts_data:
                alternatives.append(a['name'])
                min_grades.append(a['min_grade'])
            return Alternatives(alternatives, grade_levels, min_grades)
        else:
            prereq_name = record['name']
            prereq_course = get_course(prereq_name)
            return Prerequisite(prereq_course, grade_levels, record['min_grade'])
            
            
if __name__ == '__main__':
    main()