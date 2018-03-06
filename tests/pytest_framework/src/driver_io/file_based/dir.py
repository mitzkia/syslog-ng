import os


class Dir(object):
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def is_dir_exist(self):
        return os.path.isdir(self.dir_path)

    def delete_dir(self):
        if self.is_dir_exist():
            os.rmdir(self.dir_path)
        raise Exception("Dir does not exist: {}".format(self.dir_path))

    def create_dir(self):
        if not self.is_dir_exist():
            os.makedirs(self.dir_path)
        raise Exception("Dir already exist: {}".format(self.dir_path))
