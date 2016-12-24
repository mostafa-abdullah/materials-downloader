from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import os

class Course:
    def __init__(self, url, course_name):
        self.url = url
        self.course_name = course_name
        self.assign_attrs()

    def download_material(self):
        html = urlopen("http://met.guc.edu.eg/Courses/Material.aspx?crsEdId=" + self.course_code)
        bsObj = BeautifulSoup(html);

        materialLists = bsObj.findAll("ul", {"class" : "materialList"})

        allLinks = []

        for list in materialLists:
            links = list.findAll("a")
            allLinks.extend(links)

        for link in allLinks:
            normalized_link = self.normalize_link(link["href"])
            target_path = self.get_target_path(link.getText())
            self.create_folder_if_not_exists(target_path)
            print("START: " + target_path)
            urlretrieve(normalized_link, target_path)
            print("END: " + target_path)


    def normalize_link(self, link):
        return "http://met.guc.edu.eg" + link[2:len(link)]

    def assign_attrs(self):
        self.course_code = self.get_course_code(self.url)

    def get_course_code(self, url):
        return url.split("=")[1]

    def get_target_path(self, link):
        return "/home/mostafa/MET/" + self.course_name + "/" + link

    def create_folder_if_not_exists(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

