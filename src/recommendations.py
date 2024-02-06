from flow import CourseFlow
from student import Roster, Student

def get_all_recommendations(roster, flow, year):
    recommendations = {}
    for student in roster:
        recommendations[student] = get_recommendations_for_student(student, flow, year)

def get_recommendations_for_student(student, flow, year):
    current_courses = student.get_current_courses(year)
    all_courses = student.get_courses()
    recommendations = []
    for course in current_courses:
        arrows = flow.get_arrows_by_grade_level(course, student.get_grade_level())
        for arrow in arrows:
            to_course = arrow.to_course
            rank = arrow.rank
            prereqs = arrow.prerequisites
            if not student.has_taken(to_course) and satisfies_prerequisites(student, to_course):
                    recommendations.append((to_course, rank))
    return reduce_recommendations(recommendations)

def reduce_recommendations(recommendations):
    lowest_rank = min(recommendations, key=lambda x: x[1])[1]
    reduced_recommendations = [course for course, rank in recommendations if rank == lowest_rank]
    return reduced_recommendations
    

def satisfies_prerequisites(student, course):
    """
    Checks if a student satisfies the prerequisites for a given course.

    Args:
        student: The student object.
        course: The course object.

    Returns:
        True if the student satisfies the prerequisites, False otherwise.
        If no prerequisites are defined, returns True.
    """
    prereq = course.prerequisites
    if prereq is None:
        return True
    return prereq.satisfied_by(student)