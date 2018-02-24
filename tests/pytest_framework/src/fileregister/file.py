import os
from src.common.random import Random


class FileRegister(object):
    def __init__(self, logger_factory, working_dir):
        self.logger = logger_factory.create_logger("FileRegister")
        self.working_dir = working_dir

        self.registered_files = {}
        self.registered_dirs = {}
        self.registered_file_names = {}

        self.random = Random()

    def get_registered_file_path(self, prefix, extension="log", subdir=None):
        prefix_extension = "{prefix}_{extension}".format(prefix, extension)
        if self.__is_pattern_registered(pattern=prefix_extension, collection=self.registered_files):
            return self.registered_files[prefix]
        uniq_file_path = self.__generate_uniq_file_path(prefix=prefix, extension=extension, subdir=subdir)
        self.__register_uniq_file_path(prefix=prefix, uniq_file_path=uniq_file_path)
        self.logger.debug("Uniq driver_file path has been registered with prefix: prefix: [%s], path: [%s]", prefix, uniq_file_path)
        return uniq_file_path

    @staticmethod
    def __is_pattern_registered(pattern, collection):
        return pattern in collection.keys()

    def __generate_uniq_file_path(self, prefix, extension, subdir):
        base_dir = self.working_dir
        if subdir:
            base_dir = os.path.join(base_dir, subdir)
        return os.path.join(base_dir, "%s_%s.%s" % (prefix, self.random.get_unique_id(), extension))

    def __register_uniq_file_path(self, prefix, uniq_file_path):
        self.registered_files[prefix] = uniq_file_path
