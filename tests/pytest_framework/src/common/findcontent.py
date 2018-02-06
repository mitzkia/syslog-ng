import re

def find_regexp_in_content(regexp, content, expected_counter=1):
    found = False
    counter = 0
    regexp_pattern = re.compile(regexp)
    for message in content.splitlines():
        if regexp_pattern.match(message) is not None:
            counter += 1
            found = True
    return found and (counter == expected_counter)
