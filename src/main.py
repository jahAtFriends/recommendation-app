from student import Roster
from flow import CourseFlow
from recommendations import get_all_recommendations
from courses import Course_List
from utils.csv_processor import read_csv, write_csv
from utils.yaml_processor import read_yaml

#Change this to the current year
# In any given school year, the year is the year that the school year ends.
current_year = 2024

def main():
    structural_data = read_yaml('courseflow.yaml')
    course_data = structural_data['courses']
    flow_data = structural_data['flow']
    prereq_data = structural_data['prereqs']

    #Build the Course List
    course_list = Course_List.build_course_list(course_data)

    #Build the Course Flow
    course_flow = CourseFlow()
    course_flow.build_flow(flow_data, course_list)

    #Apply prerequisites to courses
    course_list.apply_prerequisites_to_courses(prereq_data)

    academic_data = read_csv('academic_data.csv')
    roster = Roster()
    roster.build_roster_from_data(academic_data)
    
    recommendations = {}
    recommendations = get_all_recommendations(roster, course_flow, current_year)
    
    #convert recommendations to friendly dictionaries
    csv_recs = [{'student': student, 'recommendations': recommendations[student]} for student in recommendations.keys()]

    # Write recommendations to CSV
    write_csv('recommendations.csv', csv_recs, ['student', 'recommendations'])

if __name__ == '__main__':
    main()
