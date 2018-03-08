from src.common.blocking import wait_until_false, wait_until_true
from src.syslog_ng_ctl.command_executor import CtlCommandExecutor


class SyslogNgCtl(CtlCommandExecutor):
    def __init__(self, logger_factory, instance_parameters):
        CtlCommandExecutor.__init__(self, logger_factory, instance_parameters)
        self.logger = logger_factory.create_logger("SyslogNgCtl")

        self.stats_cache = None
        self.query_cache = None

    def stats(self):
        return self.slng_ctl_executor(cmd_name="stats").get_all()

    def stats_reset(self):
        return self.slng_ctl_executor(cmd_name="stats_reset").get_all()

    def query_get(self, pattern="*"):
        return self.slng_ctl_executor(cmd_name="query_get", query_pattern=pattern).get_all()

    def query_get_sum(self, pattern="*"):
        return self.slng_ctl_executor(cmd_name="query_get_sum", query_pattern=pattern).get_all()

    def query_list(self, pattern="*"):
        return self.slng_ctl_executor(cmd_name="query_list", query_pattern=pattern).get_all()

    def query_reset(self, pattern="*"):
        return self.slng_ctl_executor(cmd_name="query_reset", query_pattern=pattern).get_all()

    def stop(self):
        return self.slng_ctl_executor(cmd_name="stop").get_all()

    def reload(self):
        return self.slng_ctl_executor(cmd_name="reload").get_all()

    def reopen(self):
        return self.slng_ctl_executor(cmd_name="reopen").get_all()

    def is_control_socket_alive(self):
        return self.slng_ctl_executor(cmd_name="stats").get_exit_code() == 0

    def wait_for_control_socket_start(self):
        return wait_until_true(self.is_control_socket_alive)

    def wait_for_control_socket_stop(self):
        return wait_until_false(self.is_control_socket_alive)

    def check_stats_and_query_counters(self, syslog_ng_config, destination_counter_values=None, source_counter_values=None):
        self.check_source_counters(syslog_ng_config, source_counter_values)
        self.check_destination_counters(syslog_ng_config, destination_counter_values)

    def check_source_counters(self, syslog_ng_config, source_counter_values):
        for driver_name, statement_id, mandatory_option_value in self.get_config_properties_for_stats(syslog_ng_config, "source_statements"):
            self.wait_and_assert_for_query_counters(component="src.{}".format(driver_name), config_id=statement_id, instance=mandatory_option_value, counter_values=source_counter_values)
            self.wait_and_assert_for_stats_counters(component="src.{}".format(driver_name), config_id=statement_id, instance=mandatory_option_value, counter_values=source_counter_values)

    def check_destination_counters(self, syslog_ng_config, destination_counter_values):
        for driver_name, statement_id, mandatory_option_value in self.get_config_properties_for_stats(syslog_ng_config, "destination_statements"):
            self.wait_and_assert_for_query_counters(component="dst.{}".format(driver_name), config_id=statement_id, instance=mandatory_option_value, counter_values=destination_counter_values)
            self.wait_and_assert_for_stats_counters(component="dst.{}".format(driver_name), config_id=statement_id, instance=mandatory_option_value, counter_values=destination_counter_values)

    @staticmethod
    def get_config_properties_for_stats(syslog_ng_config, root_statement):
        statement_properties = syslog_ng_config[root_statement]
        if statement_properties != {}:
            for statement_id, driver in statement_properties.items():
                for dummy_driver_id, driver_properties in driver.items():
                    driver_name = driver_properties['driver_name']
                    mandatory_option_value = driver_properties['mandatory_option_value']
                    yield driver_name, statement_id, mandatory_option_value

    def wait_and_assert_for_query_counters(self, component, config_id, instance, counter_values):
        for counter_type in self.get_counter_types_by_component(component):
            query_line = self.generate_query_line(component, config_id, instance, counter_type, counter_values[counter_type])

            if self.query_cache and (query_line in self.query_cache):
                result_of_query_in_query = True
            else:
                result_of_query_in_query = wait_until_true(self.is_line_in_statistics, query_line, self.query_get()[1], 'query', monitoring_time=1)
            self.logger.write_message_based_on_value(message="Found stat line: [{}] in query".format(query_line), value=result_of_query_in_query)
            if not result_of_query_in_query:
                self.logger.info(self.query_get()[1])
                self.logger.error("Current stats line: {}".format(self.query_get(pattern=query_line.split("=")[0])[1]))
                self.logger.error("Expected stats line: {}".format(query_line))
            assert result_of_query_in_query is True

    def wait_and_assert_for_stats_counters(self, component, config_id, instance, counter_values):
        for counter_type in self.get_counter_types_by_component(component):
            stats_line = self.generate_stats_line(component, config_id, instance, "a", counter_type, counter_values[counter_type])
            if self.stats_cache and (stats_line in self.stats_cache):
                result_of_stats_in_stats = True
            else:
                result_of_stats_in_stats = wait_until_true(self.is_line_in_statistics, stats_line, self.stats()[1], 'stats', monitoring_time=1)
            self.logger.write_message_based_on_value(message="Found stat line: [{}] in stats".format(stats_line), value=result_of_stats_in_stats)
            if not result_of_stats_in_stats:
                self.logger.info(self.stats()[1])
            assert result_of_stats_in_stats is True

    def save_statistics_output(self, statistics_output, query_type):
        if query_type == "query":
            self.query_cache = statistics_output
        elif query_type == "stats":
            self.stats_cache = statistics_output

    def is_line_in_statistics(self, expected_line, statistics_output, query_type):
        if expected_line in statistics_output:
            self.save_statistics_output(statistics_output, query_type)
            return True
        return False

    @staticmethod
    def generate_stats_line(component, config_id, instance, state_type, counter_type, message_counter):
        separator = ";"
        stats_line = "{}{}".format(component, separator)
        stats_line += "{}#0{}".format(config_id, separator)
        stats_line += "{}{}".format(instance, separator)
        stats_line += "{}{}".format(state_type, separator)
        stats_line += "{}{}{}".format(counter_type, separator, str(message_counter))
        return stats_line

    @staticmethod
    def generate_query_line(component, config_id, instance, counter_type, message_counter):
        separator = "."
        query_line = "{}{}".format(component, separator)
        query_line += "{}#0{}".format(config_id, separator)
        query_line += "{}{}".format(instance, separator)
        query_line += "{}={}".format(counter_type, str(message_counter))
        return query_line

    @staticmethod
    def get_counter_types_by_component(component):
        if component.startswith("src"):
            return ["processed"]
        elif component.startswith("dst"):
            return ["processed", "written", "dropped", "queued", "memory_usage"]
        return None
