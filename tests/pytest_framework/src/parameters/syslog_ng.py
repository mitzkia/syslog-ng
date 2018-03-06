import os
from src.common.random import Random


class SyslogNgParameters(object):
    def __init__(self, testcase_context, tc_parameters):
        self.testcase_context = testcase_context
        self.tc_parameters = tc_parameters
        self.syslog_ng_parameters = {}

    def set_instance_parameters(self, instance_name):
        instance_name = self.set_instance_name(instance_name)
        working_dir = self.tc_parameters.testcase_parameters['dir_paths']['working_dir']
        relative_working_dir = self.tc_parameters.testcase_parameters['dir_paths']['relative_working_dir']
        install_dir = self.testcase_context.getfixturevalue("installdir")

        self.syslog_ng_parameters.update({
            instance_name: {
                "dir_paths": {
                    "working_dir": working_dir,
                    "install_dir": install_dir,
                    "libjvm_dir": "/usr/lib/jvm/default-java/jre/lib/amd64/server/"
                },
                "file_paths": {
                    "config_path": os.path.join(*[working_dir, 'syslog_ng_{}.conf'.format(instance_name)]),
                    "persist_path": os.path.join(*[working_dir, 'syslog_ng_{}.persist'.format(instance_name)]),
                    "pid_path": os.path.join(*[working_dir, 'syslog_ng_{}.pid'.format(instance_name)]),
                    "control_socket_path": os.path.join(*[relative_working_dir, 'syslog_ng_{}.ctl'.format(instance_name)]),
                },
                "binary_file_paths": {
                    "syslog_ng_binary": os.path.join(*[install_dir, "sbin/syslog-ng"]),
                    "syslog_ng_ctl": os.path.join(*[install_dir, "sbin/syslog-ng-ctl"]),
                },
            }
        })
        return self.syslog_ng_parameters[instance_name]

    @staticmethod
    def set_instance_name(instance_name):
        if instance_name:
            instance_name = instance_name
        else:
            random = Random(use_static_seed=False)
            instance_name = random.get_unique_id()
        return instance_name
