from course import Course
from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
from appJar import gui

class Main:
    def __init__(self):
        self.courses = []
        self.course_codes = []
        self.name_to_course = {}
        self.name_to_file = {}
        self.populate_courses()
        self.app = gui("MET Buddy")

    # scraps the courses listing and populates the instance courses array
    def populate_courses(self):
        try:
            html = urlopen("http://met.guc.edu.eg/Courses/Undergrad.aspx")
            bsObj = BeautifulSoup(html);
            allCourses = bsObj.findAll("a", {"class" : "coursesLst"})
            for course in allCourses:
                course_code = Main.get_course_code(course["href"])
                if course_code not in self.course_codes:
                    self.course_codes.append(course_code)
                    new_course = Course(course_code, course.getText())
                    self.name_to_course[course.getText()] = new_course
                    self.courses.append(new_course)
        except URLError:
            print("Couldn't retrieve courses..")

    # extract the course code from the url
    @staticmethod
    def get_course_code(url):
        return url.split("=")[1]

    # Run the program
    def run(self):
        app = self.app

        app.startScrollPane("Courses", 0, 0)

        # list all courses
        for course in self.courses:
            app.addButton(course.course_name, self.click_course)

        app.stopScrollPane()

        # start the GUI
        app.go()

    # The listener for the course button
    def click_course(self, button):
        app = self.app

        course = self.name_to_course[button]

        # scrap the course page and get the downloadable files
        course.populate_material()

        app.startScrollPane("Material", 0, 1)

        # list all files
        for file in course.files:
            self.name_to_file[file.file_name] = file
            app.addButton(file.file_name, self.click_file)

        app.stopScrollPane()

    # the listener for the file button
    def click_file(self, button):
        app = self.app

        file = self.name_to_file[button]

        # download file
        downloaded = file.download()

        if downloaded:
            app.infoBox("Success", "Downloaded successfully.")
        else:
            app.errorBox("Error", "Couldn't download file.")

# run the program
m = Main()
m.run()