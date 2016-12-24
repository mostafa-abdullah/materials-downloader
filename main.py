from course import Course
from urllib.request import urlopen
from bs4 import BeautifulSoup

class Main:

    def __init__(self):
        self.courses = []
        self.courses_links = []
        self.populate_courses()

    # scraps the courses listing and populates the instance courses array
    def populate_courses(self):
        html = urlopen("http://met.guc.edu.eg/Courses/Undergrad.aspx")
        bsObj = BeautifulSoup(html);

        allCourses = bsObj.findAll("a", {"class" : "coursesLst"})
        for course in allCourses:
            course_link = "met.guc.edu.eg/Courses/" + course["href"]
            if course_link not in self.courses_links:
                self.courses_links.append(course_link)
                new_course = Course(course_link, course.getText())
                self.courses.append(new_course)



