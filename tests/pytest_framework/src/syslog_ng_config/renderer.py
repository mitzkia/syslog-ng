#!/usr/bin/env python
#############################################################################
# Copyright (c) 2015-2018 Balabit
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# As an additional exemption you are allowed to compile & link against the
# OpenSSL libraries as published by the OpenSSL project. See the file
# COPYING for details.
#
#############################################################################

class ConfigRenderer(object):

    def __init__(self, syslog_ng_config):
        self.syslog_ng_config = syslog_ng_config
        self.syslog_ng_config_content = ""
        self.render()

    def render(self, re_create_config=None):
        if re_create_config:
            self.syslog_ng_config_content = ""
        if self.syslog_ng_config["version"]:
            self.render_version()
        if self.syslog_ng_config["include"]:
            self.render_include()
        if self.syslog_ng_config["global_options"]:
            self.render_global_options()
        if self.syslog_ng_config["sources"]:
            self.render_statements(root_statement="sources", statement_name="source")
        if self.syslog_ng_config["parsers"]:
            self.render_statements(root_statement="parsers", statement_name="parser")
        if self.syslog_ng_config["destinations"]:
            self.render_statements(root_statement="destinations", statement_name="destination")
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
            if option_name in mandatory_option_name:
                if "path" in option_name:
                    self.syslog_ng_config_content += "        {}\n".format(option_value)

    def render_driver_options(self, driver_options, mandatory_option_name):
        for option_name, option_value in driver_options.items():
            if (option_name not in mandatory_option_name) and (option_value != "default"):
                self.syslog_ng_config_content += "        {}({})\n".format(option_name, option_value)

    def render_statements(self, root_statement, statement_name):
        for statement_id, driver in self.syslog_ng_config[root_statement].items():
            # statement header
            self.syslog_ng_config_content += "\n{} {} {{\n".format(statement_name, statement_id)
            for dummy_driver_id, driver_properties in driver.items():
                driver_name = driver_properties["driver_name"]
                driver_options = driver_properties["driver_options"]
                # driver header
                self.syslog_ng_config_content += "    {} (\n".format(driver_name)

                # driver options
                self.render_first_place_driver_options(driver_options, driver_properties["mandatory_option_name"])
                self.render_driver_options(driver_options, driver_properties["mandatory_option_name"])

                # driver footer
                self.syslog_ng_config_content += "    );\n"

            # statement footer
            self.syslog_ng_config_content += "};\n"

    def render_logpath(self):
        for logpath in self.syslog_ng_config["logpaths"]:
            self.syslog_ng_config_content += "\nlog {\n"
            for src_driver in self.syslog_ng_config["logpaths"][logpath]["sources"]:
                self.syslog_ng_config_content += "    source({});\n".format(src_driver)
            for parser in self.syslog_ng_config["logpaths"][logpath]["parsers"]:
                self.syslog_ng_config_content += "    parser({});\n".format(parser)
            for dst_driver in self.syslog_ng_config["logpaths"][logpath]["destinations"]:
                self.syslog_ng_config_content += "    destination({});\n".format(dst_driver)
            for flags in self.syslog_ng_config["logpaths"][logpath]["flags"]:
                self.syslog_ng_config_content += "    flags({});\n".format(flags)
            self.syslog_ng_config_content += "};\n"
