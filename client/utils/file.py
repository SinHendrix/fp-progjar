import settings
import os

class File:
    @staticmethod
    def file_exists(file_name):
        if not os.path.exists(settings.FILE_SENDED_ROUTE + file_name):
            print("File tidak ditemukan")
            return False
        return True
