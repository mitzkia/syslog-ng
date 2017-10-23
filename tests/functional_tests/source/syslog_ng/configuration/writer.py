class SyslogNgConfigWriter(object):
    def __init__(self, testdb_logger, syslog_ng_config, file_register, driver_data_provider, testdb_path_database):
        self.log_writer = testdb_logger.set_logger("SyslogNgConfigWriter")
        self.syslog_ng_config = syslog_ng_config
        self.file_register = file_register
        self.driver_data_provider = driver_data_provider
        self.testdb_path_database = testdb_path_database

        self.syslog_ng_config_content = ""
        self.first_place_driver_options = ["file_path", "ip"]
        self.disk_buffer_options = ['disk_buf_size', "mem_buf_length", "mem_buf_size", "reliable", "dir", "qout_size"]

    def write_raw_config(self, raw_config, file_writer, topology):
        syslog_ng_config_path = self.file_register.get_registered_file_path(prefix="config_%s" % topology, extension="conf")
        file_writer.write_content_to_regular_file(file_path=syslog_ng_config_path, content=raw_config)

    def write_config(self, file_writer, topology):
        if self.syslog_ng_config["version"]:
            self.render_version()
        if self.syslog_ng_config["include"]:
            self.render_include()
        if self.syslog_ng_config["module"]:
            self.render_module()
        if self.syslog_ng_config["global_options"]:
            self.render_global_options()
        if self.syslog_ng_config["source_statements"]:
            self.render_statements(statement_name="source")
        if self.syslog_ng_config["destination_statements"]:
            self.render_statements(statement_name="destination")
        if self.syslog_ng_config["logpaths"]:
            self.render_logpath()

        syslog_ng_config_path = self.file_register.get_registered_file_path(prefix="config_%s" % topology, extension="conf")
        file_writer.write_content_to_regular_file(file_path=syslog_ng_config_path, content=self.syslog_ng_config_content)

    def render_version(self):
        self.syslog_ng_config_content += "@version: %s\n" % self.syslog_ng_config["version"]

    def render_include(self):
        for include_path in self.syslog_ng_config["include"]:
            self.syslog_ng_config_content += "@include '%s'\n" % include_path

    def render_module(self):
        for syslog_ng_module in self.syslog_ng_config["module"]:
            self.syslog_ng_config_content += "@module %s\n" % syslog_ng_module

    def render_global_options(self):
        globals_options_header = "options {\n"
        globals_options_footer = "};\n"
        self.syslog_ng_config_content += globals_options_header
        for option_name, option_value in self.syslog_ng_config["global_options"].items():
            if option_value != "default":
                self.syslog_ng_config_content += "    %s(%s);\n" % (option_name, option_value)
        self.syslog_ng_config_content += globals_options_footer

    def render_first_place_driver_options(self, driver_options, statement_name):
        for option_name, option_value in driver_options.items():
            if option_name in self.first_place_driver_options:
                if (option_name == "ip") and (statement_name == "source"):
                    self.syslog_ng_config_content += "        %s(%s)\n" % (option_name, option_value)
                else:
                    self.syslog_ng_config_content += "        %s\n" % option_value

    def render_disk_buffer_options(self, driver_options):
        disk_buffer_options = set(driver_options.keys()).intersection(self.disk_buffer_options)
        if len(disk_buffer_options) != 0:
            self.syslog_ng_config_content += "        disk_buffer(\n"
            self.syslog_ng_config_content += "            dir(%s)\n" % (self.testdb_path_database.testcase_working_dir)
            for option_name in disk_buffer_options:
                self.syslog_ng_config_content += "            %s(%s)\n" % (option_name, driver_options[option_name])
            self.syslog_ng_config_content += "        )\n"

    def render_driver_options(self, driver_options):
        for option_name, option_value in driver_options.items():
            if (option_name not in self.first_place_driver_options) and (option_name not in self.disk_buffer_options) and (option_value != "default"):
                self.syslog_ng_config_content += "        %s(%s)\n" % (option_name, option_value)

    def render_statements(self, statement_name):
        for statement_id, driver in self.syslog_ng_config["%s_statements" % statement_name].items():
            # statement header
            self.syslog_ng_config_content += "\n%s %s {\n" % (statement_name, statement_id)
            for driver_id, driver_properties in driver.items():
                driver_name = driver_properties['driver_name']
                driver_options = driver_properties['driver_options']
                # driver header
                self.syslog_ng_config_content += "    %s (\n" % driver_name

                # driver options
                self.render_first_place_driver_options(driver_options, statement_name)
                if (statement_name == "destination") and (self.driver_data_provider.get_all_drivers_with_property(property_name="disk_buffer_support", property_value=True)):
                    self.render_disk_buffer_options(driver_options)
                self.render_driver_options(driver_options)

                # driver footer
                self.syslog_ng_config_content += "    );\n"

            # statement footer
            self.syslog_ng_config_content += "};\n"

    def render_logpath(self):
        for logpath in self.syslog_ng_config["logpaths"]:
            self.syslog_ng_config_content += "\nlog {\n"
            for src_driver in logpath["source_statements"]:
                self.syslog_ng_config_content += "    source(%s);\n" % src_driver
            for dst_driver in logpath["destination_statements"]:
                self.syslog_ng_config_content += "    destination(%s);\n" % dst_driver
            self.syslog_ng_config_content += "};\n"
