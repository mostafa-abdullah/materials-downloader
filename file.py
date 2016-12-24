from urllib.request import urlretrieve
from urllib.error import URLError
import os

class File:
    def __init__(self, local_path, download_path, file_name):
        self.local_path = local_path
        self.download_path = download_path
        self.file_name = file_name

    def download(self):
        self.create_folder_if_not_exists()
        try:
            # download file
            urlretrieve(self.download_path, self.local_path)
            print("Downloaded: " + self.local_path)
            return True
        except URLError:
            print("Couldn't download: " + self.local_path)
            return False

    # creates new folder(s) in the local path
    def create_folder_if_not_exists(self):
        os.makedirs(os.path.dirname(self.local_path), exist_ok=True)