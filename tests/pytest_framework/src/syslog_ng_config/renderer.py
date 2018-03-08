from src.syslog_ng_config.statements import Statements


class ConfigRenderer(Statements):
    def __init__(self, logger_factory, syslog_ng_config):
        Statements.__init__(self, logger_factory, syslog_ng_config)
        self.syslog_ng_config_content = ""
        self.render()

    def render(self, re_create_config=None):
        if re_create_config:
            self.syslog_ng_config_content = ""
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

    def render_version(self):
        self.syslog_ng_config_content += "@version: {}\n".format(self.syslog_ng_config["version"])

    def render_include(self):
        for include_path in self.syslog_ng_config["include"]:
            self.syslog_ng_config_content += "@include '{}'\n".format(include_path)

    def render_module(self):
        for syslog_ng_module in self.syslog_ng_config["module"]:
            self.syslog_ng_config_content += "@module {}\n".format(syslog_ng_module)

    def render_global_options(self):
        globals_options_header = "options {\n"
        globals_options_footer = "};\n"
        self.syslog_ng_config_content += globals_options_header
        for option_name, option_value in self.syslog_ng_config["global_options"].items():
            if option_value != "default":
                self.syslog_ng_config_content += "    {}({});\n".format(option_name, option_value)
        self.syslog_ng_config_content += globals_options_footer

    def render_first_place_driver_options(self, driver_options, mandatory_option_name):
        for option_name, option_value in driver_options.items():
            if option_name == mandatory_option_name:
                self.syslog_ng_config_content += "        {}\n".format(option_value)

    def render_driver_options(self, driver_options, mandatory_option_name):
        for option_name, option_value in driver_options.items():
            if (option_name != mandatory_option_name) and (option_value != "default"):
                self.syslog_ng_config_content += "        {}({})\n".format(option_name, option_value)

    def render_statements(self, statement_name):
        for statement_id, driver in self.syslog_ng_config["{}_statements".format(statement_name)].items():
            # statement header
            self.syslog_ng_config_content += "\n{} {} {{\n".format(statement_name, statement_id)
            for dummy_driver_id, driver_properties in driver.items():
                driver_name = driver_properties['driver_name']
                driver_options = driver_properties['driver_options']
                # driver header
                self.syslog_ng_config_content += "    {} (\n".format(driver_name)

                # driver options
                self.render_first_place_driver_options(driver_options, driver_properties['mandatory_option_name'])
                self.render_driver_options(driver_options, driver_properties['mandatory_option_name'])

                # driver footer
                self.syslog_ng_config_content += "    );\n"

            # statement footer
            self.syslog_ng_config_content += "};\n"

    def render_logpath(self):
        for logpath in self.syslog_ng_config["logpaths"]:
            self.syslog_ng_config_content += "\nlog {\n"
            for src_driver in self.syslog_ng_config["logpaths"][logpath]["source_statements"]:
                self.syslog_ng_config_content += "    source({});\n".format(src_driver)
            for dst_driver in self.syslog_ng_config["logpaths"][logpath]["destination_statements"]:
                self.syslog_ng_config_content += "    destination({});\n".format(dst_driver)
            for flags in self.syslog_ng_config["logpaths"][logpath]["flags"]:
                self.syslog_ng_config_content += "    flags({});\n".format(flags)
            self.syslog_ng_config_content += "};\n"
