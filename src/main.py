from student import Student, Roster
from flow import CourseFlow
from student import Student
from utils.csv_processor import read_csv, write_csv
from utils.yaml_processor import read_yaml

courses = []
students = {}

#Change this to the current year
# In any given school year, the year is the year that the school year ends.
current_year = 2023

def main():
    flow_data = read_yaml('courseflow.yaml')
    course_flow = CourseFlow(data=flow_data['flow'])

    academic_data = read_csv('academic_data.csv')
    roster = Roster()
    roster.build_roster_from_data(academic_data)
    
    recommendations = {}
    for student in roster:
        recommendations[student] = course_flow.get_recommendations(student, current_year)
    
    #print recommendations
    for student in recommendations:
        print(student)
        print(recommendations[student])
        print()


if __name__ == '__main__':
    main()