import os


class TestCaseParameters(dict):
    def __init__(self, testcase_context):
        testcase_name = testcase_context.node.name.replace("[", "_").replace("]", "_")
        testcase_file = testcase_context.node.fspath
        reports_base_path = testcase_context.getfixturevalue("reports")
        framework_root_dir = os.getcwd()

        self.testcase_parameters = {
            "dir_paths": {
                "working_dir": os.path.join(*[framework_root_dir, reports_base_path, testcase_name]),
                "relative_working_dir": os.path.join(*[reports_base_path, testcase_name]),
            },
            "file_paths": {
                "report_file": os.path.join(*[framework_root_dir, reports_base_path, testcase_name, "testcase_{}.log".format(testcase_name)]),
                "testcase_file": testcase_file,
            },
            "testcase_name": testcase_name,
            "loglevel": testcase_context.getfixturevalue("loglevel")
        }

        super().__init__(self.testcase_parameters)
