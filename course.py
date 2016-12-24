from urllib.request import urlopen, urlretrieve
from urllib.error import URLError
from bs4 import BeautifulSoup
from file import File
import os

class Course:

    def __init__(self, url, course_name):
        self.url = url
        self.course_name = course_name
        self.course_code = self.get_course_code()
        self.files = []

    # scraps the course's page and populates its material into files instance array
    def populate_material(self):
        html = urlopen("http://met.guc.edu.eg/Courses/Material.aspx?crsEdId=" + self.course_code)
        bsObj = BeautifulSoup(html);

        materialLists = bsObj.findAll("ul", {"class" : "materialList"})

        allLinks = []

        for list in materialLists:
            links = list.findAll("a")
            allLinks.extend(links)

        for link in allLinks:
            # create the absolute link
            download_link = self.normalize_link(link["href"])

            # get the local target path to download the file
            target_path = self.get_target_path(link.getText())
            self.files.append(File(target_path, download_link))


    # download all the courses material currently present in files instance array
    def download_all_material(self):
        for file in self.files:
            file.download()


    # creates an absolute path from a relative path
    def normalize_link(self, link):
        return "http://met.guc.edu.eg" + link[2:len(link)]

    def get_course_code(self):
        return self.url.split("=")[1]

    # returns the local target path to download the file
    def get_target_path(self, link):
        return "/home/mostafa/MET/" + self.course_name + "/" + link