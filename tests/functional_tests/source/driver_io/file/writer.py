import os

class FileWriter(object):
    def __init__(self, testdb_logger, file_common):
        self.log_writer = testdb_logger.set_logger("FileWriter")
        self.file_common = file_common

    def write_content(self, file_path, content, driver_name):
        if driver_name == "file":
            self.write_content_to_regular_file(file_path=file_path, content=content)
        elif driver_name == "pipe":
            self.write_content_to_named_pipe(file_path=file_path, content=content)
        elif driver_name == "wildcard_file":
            file_path = file_path.replace("*", "log")
            self.file_common.create_dir(os.path.dirname(file_path))
            self.write_content_to_regular_file(file_path, content)
        else:
            self.log_writer.error("Unknown driver: %s" % driver_name)
            assert False

    def write_content_to_regular_file(self, file_path, content):
        if (content == "") or (content == []):
            assert False
        self.log_writer.info("SUBSTEP Content write\n>>>Content:%s \n>>>to: [%s]" % (content, file_path))
        with open(file_path, 'a+') as file_object:
            if isinstance(content, list):
                for line in content:
                    file_object.write(self.normalize_line_endings(line))
            else:
                file_object.write(self.normalize_line_endings(content))

    def write_content_to_named_pipe(self, file_path, content):
        if (content == "") or (content == []):
            assert False
        self.log_writer.info("SUBSTEP Content write\n>>>Content:%s \n>>>to: [%s]" % (content, file_path))
        with open(file_path, 'w') as file_object:
            if isinstance(content, list):
                for line in content:
                    file_object.write(self.normalize_line_endings(line))
            else:
                file_object.write(self.normalize_line_endings(content))
            file_object.flush()
        file_object.close()

    @staticmethod
    def normalize_line_endings(line):
        if not line.endswith("\n"):
            line += "\n"
        return line
