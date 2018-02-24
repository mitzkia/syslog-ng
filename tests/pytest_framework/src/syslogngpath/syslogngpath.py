import os

from src.common.random import Random


class SyslogNgPath(object):
    def __init__(self, runtime_parameters):
        self.runtime_parameters = runtime_parameters
        self.libjvm_dir = self.runtime_parameters['libjvm_dir']
        self.working_dir = self.runtime_parameters['working_dir']
        self.working_dir_relative = self.runtime_parameters['working_dir_relative']
        self.install_dir = self.runtime_parameters['install_dir']
        self.syslog_ng_runtime_files = {}

    def set_syslog_ng_runtime_files(self, instance_name):
        if instance_name:
            instance_name = instance_name
        else:
            random = Random(use_static_seed=False)
            instance_name = random.get_unique_id()

        self.syslog_ng_runtime_files.update({
            instance_name: {
                "stdout_path": os.path.join(self.working_dir, "slng_stdout_{}.log".format(instance_name)),
                "stderr_path": os.path.join(self.working_dir, "slng_stderr_{}.log".format(instance_name)),
                "stdout_fd": open(os.path.join(self.working_dir, "slng_stdout_{}.log".format(instance_name)), 'w'),
                "stderr_fd": open(os.path.join(self.working_dir, "slng_stderr_{}.log".format(instance_name)), 'w'),
                "config_path": os.path.join(self.working_dir, "slng_config_{}.conf".format(instance_name)),
                "persist_path": os.path.join(self.working_dir, "slng_persist_{}.persist".format(instance_name)),
                "pid_path": os.path.join(self.working_dir, "slng_pid_{}.pid".format(instance_name)),
                "control_socket_path": os.path.join(self.working_dir_relative, "slng_control_socket_{}.ctl".format(instance_name)),
            }
        })

    def get_syslog_ng_runtime_files(self, instance_name):
        return self.syslog_ng_runtime_files[instance_name]
