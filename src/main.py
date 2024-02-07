from student import Roster
from flow import CourseFlow
from recommendations import get_all_recommendations
from courses import Course_List
from utils.csv_processor import read_csv, write_csv
from utils.yaml_processor import read_yaml
import time

#Change this to the current year
# In any given school year, the year is the year that the school year ends.
current_year = 2024

def main():
    start_time = time.time()
    structural_data = read_yaml('courseflow.yaml')
    course_data = structural_data['courses']
    flow_data = structural_data['flow']
    prereq_data = structural_data['prereqs']

    #Build the Course List
    course_list = Course_List.build_course_list(course_data)

    #Build the Course Flow
    course_flow = CourseFlow(flow_data, course_list)

    #Apply prerequisites to courses
    course_list.apply_prerequisites_to_courses(prereq_data)

    academic_data = read_csv('academic_data.csv')
    roster = Roster(current_year)
    roster.build_roster_from_data(academic_data, course_list)
    
    recommendations = {}
    recommendations = get_all_recommendations(roster, course_flow, current_year)
    
    #convert recommendations to friendly dictionaries
    csv_recs = [
        {
            'student': student.name, 
            'recommendations': [
                course.name for course in recommendations[student]
            ],
            'current_science_teacher': get_current_science_teacher(student) or '',
            'current_science_course': get_current_science_course(student).name if get_current_science_course(student) else ''
        } 
        for student in recommendations.keys()
    ]

    # Write recommendations to CSV
    write_csv('recommendations.csv', csv_recs, ['student', 'recommendations', 'current_science_teacher', 'current_science_course'])

    end_time = time.time()
    elapsed_time = round(end_time - start_time, 3)
    print(f'Recommendations completed in approximately {elapsed_time} seconds')

def get_current_science_teacher(student):
    current_science_course = get_current_science_course(student)
    if current_science_course is None:
        return None
    return student.get_teacher(current_science_course)

def get_current_science_course(student):
    current_courses = student.get_current_courses(current_year)
    science_courses = [course for course in current_courses if course.department == 'Science']
    if len(science_courses) == 0:
        return None
    return science_courses[0]

if __name__ == '__main__':
    main()
