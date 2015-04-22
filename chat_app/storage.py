from django.core.files.storage import FileSystemStorage
# function to overwrite the existing file when changing user image
class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name):
        if self.exists(name):
            self.delete(name)
        return name
