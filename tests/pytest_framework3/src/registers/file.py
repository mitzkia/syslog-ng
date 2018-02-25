import os
from src.common.random import Random


class FileRegister(object):
    def __init__(self, logger_factory, working_dir):
        self.logger = logger_factory.create_logger("FileRegister")
        self.working_dir = working_dir
        self.registered_files = {}
        self.random = Random()

    def get_registered_file_path(self, prefix, extension="log", subdir=None):
        prefix_extension = "{}_{}".format(prefix, extension)
        if self.is_key_registered_in_collection(key=prefix_extension, collection=self.registered_files):
            return self.registered_files[prefix_extension]
        unique_file_path = self.generate_unique_file_path(prefix=prefix, extension=extension, subdir=subdir)
        self.register_key_in_collection(key=prefix_extension, value=unique_file_path, collection=self.registered_files)
        return unique_file_path

    @staticmethod
    def is_key_registered_in_collection(key, collection):
        return key in collection.keys()

    def generate_unique_file_path(self, prefix, extension, subdir):
        base_dir = self.working_dir
        if subdir:
            base_dir = os.path.join(self.working_dir, subdir)
        return os.path.join(base_dir, "{}_{}.{}".format(prefix, self.random.get_unique_id(), extension))

    @staticmethod
    def register_key_in_collection(key, value, collection):
        collection[key] = value
