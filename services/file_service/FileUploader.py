from abc import abstractmethod


class FileUploader:
    def __init__(self, file):
        self.file = file

    @abstractmethod
    def upload(self):
        pass


class LocalFileUploader(FileUploader):
    def upload(self):
        print(f"Uploading {self.file} to local file system")
