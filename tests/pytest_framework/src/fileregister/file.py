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
        if self.__is_prefix_already_registered_in_collection(prefix=prefix, collection=self.registered_files):
            return self.registered_files[prefix]
        uniq_file_path = self.__generate_uniq_file_path(prefix=prefix, extension=extension, subdir=subdir)
        self.__register_uniq_file_path(prefix=prefix, uniq_file_path=uniq_file_path)
        self.logger.debug("Uniq driver_file path has been registered with prefix: prefix: [%s], path: [%s]", prefix, uniq_file_path)
        return uniq_file_path

    def get_registered_dir_path(self, prefix):
        if self.__is_prefix_already_registered_in_collection(prefix=prefix, collection=self.registered_dirs):
            return self.registered_dirs[prefix]
        uniq_dir_path = self.__generate_uniq_dir_path(prefix=prefix)
        self.__register_uniq_dir_path(prefix=prefix, uniq_dir_path=uniq_dir_path)
        self.logger.debug("Uniq dir path has been registered with prefix: prefix: [%s], dir: [%s]", prefix, uniq_dir_path)
        return uniq_dir_path

    def get_registered_file_name(self, prefix, extension="*"):
        if self.__is_prefix_already_registered_in_collection(prefix=prefix, collection=self.registered_file_names):
            return self.registered_file_names[prefix]
        uniq_file_name = self.__generate_uniq_file_name(prefix=prefix, extension=extension)
        self.__register_uniq_file_name(prefix=prefix, uniq_file_name=uniq_file_name)
        self.logger.debug("Uniq driver_file name has been registered with prefix: prefix: [%s], filename: [%s]", prefix, uniq_file_name)
        return uniq_file_name

    @staticmethod
    def __is_prefix_already_registered_in_collection(prefix, collection):
        return prefix in collection.keys()

    def __generate_uniq_file_path(self, prefix, extension, subdir):
        base_dir = self.working_dir
        if subdir:
            base_dir = os.path.join(base_dir, subdir)
        return os.path.join(base_dir, "%s_%s.%s" % (prefix, self.random.get_unique_id(), extension))

    def __generate_uniq_dir_path(self, prefix):
        return os.path.join(self.working_dir, "%s_%s" % (prefix, self.random.get_unique_id()))

    def __generate_uniq_file_name(self, prefix, extension="*"):
        return "%s_%s.%s" % (prefix, self.random.get_unique_id(), extension)

    def __register_uniq_file_path(self, prefix, uniq_file_path):
        self.registered_files[prefix] = uniq_file_path

    def __register_uniq_dir_path(self, prefix, uniq_dir_path):
        self.registered_dirs[prefix] = uniq_dir_path

    def __register_uniq_file_name(self, prefix, uniq_file_name):
        self.registered_file_names[prefix] = uniq_file_name
