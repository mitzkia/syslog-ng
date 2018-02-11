import os
from src.common.blocking import wait_until_false, wait_until_true
from src.executor.executor_interface import ExecutorInterface


class SyslogNgCtl(object):
    def __init__(self, logger_factory, runtime_parameters, control_socket_path):
        self.logger = logger_factory.create_logger("SyslogNgCtl")
        self.working_dir = runtime_parameters['working_dir']
        self.install_dir = runtime_parameters['install_dir']

        self.executor = ExecutorInterface(logger_factory, self.working_dir)
        self.syslog_ng_control_tool_path = os.path.join(self.install_dir, "sbin/syslog-ng-ctl")
        self.syslog_ng_control_socket_path = control_socket_path

        self.first_matched_stats = None
        self.first_matched_query = None
        self.stats_command = "%s stats --control=%s" % (self.syslog_ng_control_tool_path, self.syslog_ng_control_socket_path)
        self.query_command = "%s query --control=%s" % (self.syslog_ng_control_tool_path, self.syslog_ng_control_socket_path)

    def stats(self, show_output=False):
        exit_code, stdout, stderr = self.executor.execute_command(self.stats_command)
        if show_output:
            self.logger.info(stdout)
        return exit_code, stdout, stderr

    def stats_reset(self):
        exit_code, stdout, stderr = self.executor.execute_command("%s --reset" % self.stats_command)
        return exit_code, stdout, stderr

    def query_get(self, pattern="*", show_output=False):
        return self.execute_query_command(command=" get '%s' " % pattern, show_output=show_output)

    def query_get_sum(self, pattern="*", show_output=False):
        return self.execute_query_command(command=" get --sum '%s' " % pattern, show_output=show_output)

    def query_list(self, pattern="*", show_output=False):
        return self.execute_query_command(command=" list '%s' " % pattern, show_output=show_output)

    def query_reset(self, pattern="*"):
        return self.execute_query_command(command=" get --reset '%s' " % pattern, show_output=False)

    def execute_query_command(self, command, show_output=False):
        exit_code, stdout, stderr = self.executor.execute_command(self.query_command + command)
        if show_output:
            self.logger.info(stdout)
        return exit_code, stdout, stderr

    def stop(self):
        stop_command = "%s stop --control=%s" % (self.syslog_ng_control_tool_path, self.syslog_ng_control_socket_path)
        exit_code, stdout, stderr = self.executor.execute_command(stop_command)
        return exit_code, stdout, stderr

    def reload(self):
        reload_command = "%s reload --control=%s" % (self.syslog_ng_control_tool_path, self.syslog_ng_control_socket_path)
        exit_code, stdout, stderr = self.executor.execute_command(reload_command)
        return exit_code, stdout, stderr

    def reopen(self):
        reopen_command = "%s reopen --control=%s" % (self.syslog_ng_control_tool_path, self.syslog_ng_control_socket_path)
        exit_code, stdout, stderr = self.executor.execute_command(reopen_command)
        return exit_code, stdout, stderr

    def is_control_socket_alive(self):
        return self.stats()[0] == 0

    def wait_for_control_socket_start(self):
        return wait_until_true(self.is_control_socket_alive)

    def wait_for_control_socket_stop(self):
        return wait_until_false(self.is_control_socket_alive)

    def check_stats_and_query_counters(self, syslog_ng_config, destination_counter_values=None, source_counter_values=None):
        self.check_source_counters(syslog_ng_config, source_counter_values)
        self.check_destination_counters(syslog_ng_config, destination_counter_values)

    def check_source_counters(self, syslog_ng_config, source_counter_values):
        for driver_name, statement_id, connection_mandatory_options in self.get_config_properties_for_stats(syslog_ng_config, "source_statements"):
            self.wait_and_assert_for_query_counters(component="src.%s" % driver_name, config_id=statement_id, instance=connection_mandatory_options, counter_values=source_counter_values)
            self.wait_and_assert_for_stats_counters(component="src.%s" % driver_name, config_id=statement_id, instance=connection_mandatory_options, counter_values=source_counter_values)

    def check_destination_counters(self, syslog_ng_config, destination_counter_values):
        for driver_name, statement_id, connection_mandatory_options in self.get_config_properties_for_stats(syslog_ng_config, "destination_statements"):
            self.wait_and_assert_for_query_counters(component="dst.%s" % driver_name, config_id=statement_id, instance=connection_mandatory_options, counter_values=destination_counter_values)
            self.wait_and_assert_for_stats_counters(component="dst.%s" % driver_name, config_id=statement_id, instance=connection_mandatory_options, counter_values=destination_counter_values)

    def get_config_properties_for_stats(self, syslog_ng_config, root_statement):
        statement_properties = syslog_ng_config[root_statement]
        if statement_properties != {}:
            for statement_id, driver in statement_properties.items():
                for _driver_id, driver_properties in driver.items():
                    driver_name = driver_properties['driver_name']
                    connection_mandatory_options = driver_properties['connection_mandatory_options']
                    yield driver_name, statement_id, connection_mandatory_options

    def wait_and_assert_for_query_counters(self, component, config_id, instance, counter_values):
        for counter_type in self.get_counter_types_by_component(component):
            query_line = self.generate_query_line(component, config_id, instance, counter_type, counter_values[counter_type])
            if self.first_matched_query and (query_line in self.first_matched_query):
                result_of_query_in_query = True
            else:
                result_of_query_in_query = wait_until_true(self.is_line_in_statistics, query_line, self.query_get()[1], 'query', monitoring_time=1)
            self.logger.info(self.query_get()[1])
            self.logger.write_message_based_on_value(message="Found stat line: [%s] in query" % query_line, value=result_of_query_in_query)
            assert result_of_query_in_query is True

    def wait_and_assert_for_stats_counters(self, component, config_id, instance, counter_values):
        for counter_type in self.get_counter_types_by_component(component):
            stats_line = self.generate_stats_line(component, config_id, instance, "a", counter_type, counter_values[counter_type])
            if self.first_matched_stats and (stats_line in self.first_matched_stats):
                result_of_stats_in_stats = True
            else:
                result_of_stats_in_stats = wait_until_true(self.is_line_in_statistics, stats_line, self.stats()[1], 'stats', monitoring_time=1)
            self.logger.info(self.stats()[1])
            self.logger.write_message_based_on_value(message="Found stat line: [%s] in stats" % stats_line, value=result_of_stats_in_stats)
            assert result_of_stats_in_stats is True

    def save_statistics_output(self, statistics_output, statistics_from):
        if statistics_from == "query":
            self.first_matched_query = statistics_output
        elif statistics_from == "stats":
            self.first_matched_stats = statistics_output

    def is_line_in_statistics(self, expected_line, statistics_output, statistics_from):
        if expected_line in statistics_output:
            self.save_statistics_output(statistics_output, statistics_from)
            return True
        return False

    def generate_stats_line(self, component, config_id, instance, state_type, counter_type, message_counter):
        separator = ";"
        stats_line = ""
        stats_line += component + separator
        stats_line += config_id + "#0" + separator
        stats_line += instance + separator
        stats_line += state_type + separator
        stats_line += counter_type + separator + str(message_counter)
        return stats_line

    def generate_query_line(self, component, config_id, instance, counter_type, message_counter):
        separator = "."
        query_line = ""
        query_line += component + separator
        query_line += config_id + "#0" + separator
        query_line += instance + separator
        query_line += counter_type + "=" + str(message_counter)
        return query_line

    def get_counter_types_by_component(self, component):
        if component.startswith("src"):
            return ["processed"]
        elif component.startswith("dst"):
            return ["processed", "written", "dropped", "queued", "memory_usage"]
