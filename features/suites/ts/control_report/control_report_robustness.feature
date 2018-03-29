# Created by liwenxuan at 2017/10/11
@ts @report @control_report @robustness
Feature: report-srv received a control_report request with unexpected data
  # As report-srv,
  # when I receive an invalid control_report request,
  # I will not return 200 OK and do nothing

  # request body
  @invalid
  Scenario Outline: control_report without required fields
    Given prepare valid request body of control_report with empty seeds and empty channels
    And delete field <field> of control_report
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: required fields
        | field    |
        | peer_id  |
        | duration |
        | seeds    |
        | channels |

  @invalid
  Scenario Outline: the value of required fields is None
    Given prepare valid request body of control_report with empty seeds and empty channels
    And modify the value of field "<field>" of control_report to "None" and type to "NoneType"
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: required fields
        | field    |
        | peer_id  |
        | duration |
        | seeds    |
        | channels |

  @invalid
  Scenario: the value of "peer_id" is ""
    Given prepare valid request body of control_report with empty seeds and empty channels
    And modify the value of field "peer_id" of control_report to """" and type to "object"
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None

  @invalid
  Scenario Outline: the value of "peer_id" is incorrect
    Given prepare valid request body of control_report with empty seeds and empty channels
    And modify the value of field "peer_id" of control_report to "<value>" and type to "str"
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not hexadecimal 32 bytes
         | value                                       |
         | a                                           |
         | 00000000123451234512345                     |
         | 1234567890123456789012345678931             |
         | 1234567890123456789012345678932G            |
         | 123456789012345678901234567890133           |
         | 000000001234512345123451234AADBCFDABCDDADDD |
         | ********************************            |

  @invalid
  Scenario Outline: "peer_id" is not a string
    Given prepare valid request body of control_report with empty seeds and empty channels
    And modify the value of field "peer_id" of control_report to "<value>" and type to "<type>"
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |

  @invalid
  Scenario Outline: "duration" is not an int
    Given prepare valid request body of control_report with empty seeds and empty channels
    And modify the value of field "duration" of control_report to "<value>" and type to "<type>"
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not int type
        | value | type   |
        | ""    | object |
        | " "   | object |
        | 0     | str    |
        | 0.0   | float  |
        | 0.1   | float  |

  @invalid
  Scenario Outline: "seeds" is not an array
    Given prepare valid request body of control_report with empty seeds and empty channels
    And modify the value of field "seeds" of control_report to "<value>" and type to "<type>"
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not array type
        | value  | type    |
        | ""     | object  |
        | " "    | object  |
        | 0      | int     |
        | 0.0    | float   |
        | {}     | dict    |

  @invalid
  Scenario Outline: "channels" is not an array
    Given prepare valid request body of control_report with empty seeds and empty channels
    And modify the value of field "channels" of control_report to "<value>" and type to "<type>"
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not array type
        | value  | type    |
        | ""     | object  |
        | " "    | object  |
        | 0      | int     |
        | 0.0    | float   |
        | {}     | dict    |

  # field: seeds
  @invalid
  Scenario: the value of "file_id" in seeds is ""
    Given prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid seed_info of control_report
    And modify the value of field "file_id" of seed_info to """" and type to "object"
    And add seed_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None

  @invalid
  Scenario Outline: the value of "file_id" in seeds is incorrect
    Given prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid seed_info of control_report
    And modify the value of field "file_id" of seed_info to "<value>" and type to "str"
    And add seed_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not hexadecimal 32 bytes
        | value                                       |
        | a                                           |
        | 00000000123451234512345                     |
        | 1234567890123456789012345678931             |
        | 1234567890123456789012345678932G            |
        | 123456789012345678901234567890133           |
        | 000000001234512345123451234AADBCFDABCDDADDD |
        | ********************************            |

  @invalid
  Scenario Outline: "file_id" in seeds is not a string
    Given prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid seed_info of control_report
    And modify the value of field "file_id" of seed_info to "<value>" and type to "<type>"
    And add seed_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |

  @invalid
  Scenario Outline: "cppc" in seeds is not an int
    Given prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid seed_info of control_report
    And modify the value of field "cppc" of seed_info to "<value>" and type to "<type>"
    And add seed_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not int type
        | value | type   |
        | ""    | object |
        | " "   | object |
        | 0     | str    |
        | 0.0   | float  |
        | 0.1   | float  |

  @invalid
  Scenario Outline: "download" in seeds is not a long
    Given prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid seed_info of control_report
    And modify the value of field "download" of seed_info to "<value>" and type to "<type>"
    And add seed_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not long type
        | value | type   |
        | ""    | object |
        | " "   | object |
        | 0     | str    |
        | 0.0   | float  |
        | 0.1   | float  |

  @invalid
  Scenario Outline: "provide" in seeds is not a long
    Given prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid seed_info of control_report
    And modify the value of field "provide" of seed_info to "<value>" and type to "<type>"
    And add seed_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not long type
        | value | type   |
        | ""    | object |
        | " "   | object |
        | 0     | str    |
        | 0.0   | float  |
        | 0.1   | float  |

  # field: channels  # type&err_type value unlimited
  @invalid
  Scenario: the value of "file_id" in seeds is ""
    Given prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid channel_info of control_report
    And modify the value of field "file_id" of channel_info to """" and type to "object"
    And add channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None

  @invalid
  Scenario Outline: the value of "file_id" in channels is incorrect
    Given prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid channel_info of control_report
    And modify the value of field "file_id" of channel_info to "<value>" and type to "str"
    And add channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not hexadecimal 32 bytes
        | value                                       |
        | a                                           |
        | 00000000123451234512345                     |
        | 1234567890123456789012345678931             |
        | 1234567890123456789012345678932G            |
        | 123456789012345678901234567890133           |
        | 000000001234512345123451234AADBCFDABCDDADDD |
        | ********************************            |

  @invalid
  Scenario Outline: "file_id" in channels is not a string
    Given prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid channel_info of control_report
    And modify the value of field "file_id" of channel_info to "<value>" and type to "<type>"
    And add channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |

  @invalid
  Scenario Outline: "type" in channels is not a string
    Given prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid channel_info of control_report
    And modify the value of field "type" of channel_info to "<value>" and type to "<type>"
    And add channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |

  @invalid
  Scenario Outline: "cdn" in channels is not a long
    Given prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid channel_info of control_report
    And modify the value of field "cdn" of channel_info to "<value>" and type to "<type>"
    And add channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not long type
        | value | type   |
        | ""    | object |
        | " "   | object |
        | 0     | str    |
        | 0.0   | float  |
        | 0.1   | float  |

  @invalid
  Scenario Outline: "p2p" in channels is not a long
    Given prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid channel_info of control_report
    And modify the value of field "p2p" of channel_info to "<value>" and type to "<type>"
    And add channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not long type
        | value | type   |
        | ""    | object |
        | " "   | object |
        | 0     | str    |
        | 0.0   | float  |
        | 0.1   | float  |

  @invalid
  Scenario Outline: the value of "op" in channels is incorrect
    Given prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid channel_info of control_report
    And modify the value of field "op" of channel_info to "<value>" and type to "<type>"
    And add channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: invalid op
        | value    | type   |
        | ""       | object |
        | ADD      | str    |
        | DEL      | str    |
        | PLAYING  | str    |
        | *        | str    |

  @invalid
  Scenario Outline: "op" in channels is not a string
    Given prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid channel_info of control_report
    And modify the value of field "op" of channel_info to "<value>" and type to "<type>"
    And add channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |

  @invalid
  Scenario Outline: "err_type" in channels is not a string
    Given prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid channel_info of control_report
    And modify the value of field "err_type" of channel_info to "<value>" and type to "<type>"
    And add channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |

