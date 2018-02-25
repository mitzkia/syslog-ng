import re


def find_regexp_in_content(regexp, content, expected_counter=1):
    regexp_pattern = re.compile(regexp)
    return expected_counter == len(list(filter(regexp_pattern.match, content.splitlines())))
