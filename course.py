from urllib.request import urlopen, urlretrieve
from urllib.error import URLError
from bs4 import BeautifulSoup
import os

class Course:

    def __init__(self, url, course_name):
        self.url = url
        self.course_name = course_name
        self.course_code = self.get_course_code()

    def download_material(self):
        html = urlopen("http://met.guc.edu.eg/Courses/Material.aspx?crsEdId=" + self.course_code)
        bsObj = BeautifulSoup(html);

        materialLists = bsObj.findAll("ul", {"class" : "materialList"})

        allLinks = []

        for list in materialLists:
            links = list.findAll("a")
            allLinks.extend(links)

        for link in allLinks:
            # create the absolute link
            normalized_link = self.normalize_link(link["href"])

            # get the local target path to download the file
            target_path = self.get_target_path(link.getText())

            # make sure that the target folder exists
            self.create_folder_if_not_exists(target_path)

            try:
                # download file
                urlretrieve(normalized_link, target_path)
                print("Downloaded: " + target_path)
            except URLError:
                print("Couldn't download: " + target_path)



    # creates an absolute path from a relative path
    def normalize_link(self, link):
        return "http://met.guc.edu.eg" + link[2:len(link)]

    def get_course_code(self):
        return self.url.split("=")[1]

    # returns the local target path to download the file
    def get_target_path(self, link):
        return "/home/mostafa/MET/" + self.course_name + "/" + link

    # creates new folder(s) in the local path
    def create_folder_if_not_exists(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)