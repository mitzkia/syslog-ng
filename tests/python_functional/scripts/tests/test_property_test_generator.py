from run_property_based_tests import PropertyTestGenerator


def get_user_filter_with_content(whitelist_drivers=[], whitelist_options=[], whitelist_blocks=[], blacklist_drivers=[], blacklist_options=[], blacklist_blocks=[]):
    return {
        "whitelist_drivers": whitelist_drivers,
        "whitelist_options": whitelist_options,
        "whitelist_blocks": whitelist_blocks,

        "blacklist_drivers": blacklist_drivers,
        "blacklist_options": blacklist_options,
        "blacklist_blocks": blacklist_blocks,
    }


def get_database_meta(db_values, db_type):
    return {
        "option_database": db_values,
        "db_type": db_type,
    }


def test_whitelist_driver_filtering_single_driver():
    user_filters = get_user_filter_with_content(whitelist_drivers=["file"])
    db_values = [
        {
            "option_name": "format1",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "file",
            ],
        },
        {
            "option_name": "positional",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "file",
            ],
        },
        {
            "option_name": "format2",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "fifo",
            ],
        },
        {
            "option_name": "format3",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "file",
                "fifo",
            ],
        },
        {
            "option_name": "format4",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [],
        },
    ]
    database_meta = get_database_meta(db_values, "source")
    ptg = PropertyTestGenerator(1, user_filters, database_meta)
    ptg.generate_pbts_for_database(write_testcase_content=False)
    assert ptg.testcase_names == ['test_source_format1_string', 'test_source_positional_string', 'test_source_format3_string']
    assert len(ptg.testcase_contents) == 3
    assert all("parent_drivers=['file']" in item for item in ptg.testcase_contents)


def test_whitelist_driver_filtering_multiple_drivers():
    user_filters = get_user_filter_with_content(whitelist_drivers=["file", "tcp", "udp"])
    db_values = [
        {
            "option_name": "format1",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "fifo",
                "file",
            ],
        },
        {
            "option_name": "format2",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "tcp",
                "file",
            ],
        },
        {
            "option_name": "format3",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "fifo",
                "tcp",
            ],
        },
        {
            "option_name": "positional",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "pipe",
                "tcp6",
            ],
        },
    ]
    database_meta = get_database_meta(db_values, "source")
    ptg = PropertyTestGenerator(1, user_filters, database_meta)
    ptg.generate_pbts_for_database(write_testcase_content=False)
    assert ptg.testcase_names == ['test_source_format1_string', 'test_source_format2_string', 'test_source_format3_string']
    assert len(ptg.testcase_contents) == 3
    assert ["parent_drivers=['file']" in item for item in ptg.testcase_contents] == [True, False, False]
    assert ["parent_drivers=['file', 'tcp']" in item for item in ptg.testcase_contents] == [False, True, False]
    assert ["parent_drivers=['tcp']" in item for item in ptg.testcase_contents] == [False, False, True]


def test_blacklist_driver_filtering_single_driver():
    user_filters = get_user_filter_with_content(blacklist_drivers=["file"])
    db_values = [
        {
            "option_name": "format1",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "file",
            ],
        },
        {
            "option_name": "positional",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "file",
            ],
        },
        {
            "option_name": "format2",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "fifo",
            ],
        },
        {
            "option_name": "format3",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "file",
                "fifo",
            ],
        },
        {
            "option_name": "format4",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [],
        },
    ]
    database_meta = get_database_meta(db_values, "destination")
    ptg = PropertyTestGenerator(1, user_filters, database_meta)
    ptg.generate_pbts_for_database(write_testcase_content=False)
    assert ptg.testcase_names == ['test_destination_format2_string', 'test_destination_format3_string']
    assert len(ptg.testcase_contents) == 2
    assert all("parent_drivers=['fifo']" in item for item in ptg.testcase_contents)


def test_blacklist_driver_filtering_multiple_drivers():
    user_filters = get_user_filter_with_content(blacklist_drivers=["file", "tcp", "udp"])
    db_values = [
        {
            "option_name": "format1",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "fifo",
                "file",
            ],
        },
        {
            "option_name": "format2",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "tcp",
                "file",
                "udp",
            ],
        },
        {
            "option_name": "format3",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "fifo",
                "tcp",
            ],
        },
        {
            "option_name": "positional",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "pipe",
                "tcp6",
            ],
        },
    ]
    database_meta = get_database_meta(db_values, "destination")
    ptg = PropertyTestGenerator(1, user_filters, database_meta)
    ptg.generate_pbts_for_database(write_testcase_content=False)
    assert ptg.testcase_names == ['test_destination_format1_string', 'test_destination_format3_string', 'test_destination_positional_string']
    assert len(ptg.testcase_contents) == 3
    assert ["parent_drivers=['fifo']" in item for item in ptg.testcase_contents] == [True, True, False]
    assert ["parent_drivers=['pipe', 'tcp6']" in item for item in ptg.testcase_contents] == [False, False, True]


def test_whitelist_option_filtering():
    user_filters = get_user_filter_with_content(whitelist_options=["format1", "positional"])
    db_values = [
        {
            "option_name": "format1",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "file",
            ],
        },
        {
            "option_name": "positional",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "file",
            ],
        },
        {
            "option_name": "format2",
            "option_types": ["<string>"],
            "block_names": [],
            "parent_drivers": [
                "fifo",
            ],
        },
    ]
    database_meta = get_database_meta(db_values, "source")
    ptg = PropertyTestGenerator(1, user_filters, database_meta)
    ptg.generate_pbts_for_database(write_testcase_content=False)
    assert ptg.testcase_names == ['test_source_format1_string', 'test_source_positional_string']
    assert len(ptg.testcase_contents) == 2
    print(ptg.testcase_contents)
    assert all("parent_drivers=['file']" in item for item in ptg.testcase_contents)
