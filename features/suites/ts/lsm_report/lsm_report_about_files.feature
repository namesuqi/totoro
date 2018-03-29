# Created by liwenxuan at 2017/10/9
@ts @report @lsm_report @robustness
Feature: SDK report-srv receive the lsm_report request with field files

  @pnic @valid
  Scenario Outline: SDK can report lsm_report to report-srv successfully with valid stat
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of lsm_report with empty files
    And prepare a valid file_info of lsm_report
    And set field stat of file_info to <value> and type to str
    And add file_info to lsm_report
    When report-srv receive the lsm_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}
    Examples: valid stat
        | value        |
        | downloading  |
        | interrupt    |
        | done         |
        | waiting      |
        | deleted      |

  @pnic @invalid
  Scenario Outline: SDK cannot report lsm_report to report-srv with invalid file_id
    Given prepare valid request body of lsm_report with empty files
    And prepare a valid file_info of lsm_report
    And set field file_id of file_info to <value> and type to str
    And add file_info to lsm_report
    When report-srv receive the lsm_report request
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

  @pnic @invalid
  Scenario Outline: SDK cannot report lsm_report to report-srv with file_id (not str)
    Given prepare valid request body of lsm_report with empty files
    And prepare a valid file_info of lsm_report
    And set field file_id of file_info to <value> and type to <type>
    And add file_info to lsm_report
    When report-srv receive the lsm_report request
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

  @pnic @invalid
  Scenario Outline: SDK cannot report lsm_report to report-srv with ppc (not int)
    Given prepare valid request body of lsm_report with empty files
    And prepare a valid file_info of lsm_report
    And set field ppc of file_info to <value> and type to <type>
    And add file_info to lsm_report
    When report-srv receive the lsm_report request
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

  @pnic @invalid
  Scenario Outline: SDK cannot report lsm_report to report-srv with psize (not int)
    Given prepare valid request body of lsm_report with empty files
    And prepare a valid file_info of lsm_report
    And set field psize of file_info to <value> and type to <type>
    And add file_info to lsm_report
    When report-srv receive the lsm_report request
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

  @pnic @invalid
  Scenario Outline: SDK cannot report lsm_report to report-srv with cppc (not int)
    Given prepare valid request body of lsm_report with empty files
    And prepare a valid file_info of lsm_report
    And set field cppc of file_info to <value> and type to <type>
    And add file_info to lsm_report
    When report-srv receive the lsm_report request
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

  @pnic @invalid
  Scenario Outline: SDK cannot report lsm_report to report-srv with invalid stat
    Given prepare valid request body of lsm_report with empty files
    And prepare a valid file_info of lsm_report
    And set field stat of file_info to <value> and type to str
    And add file_info to lsm_report
    When report-srv receive the lsm_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: stat not in ("downloading", "interrupt", "done", "none")
        | value        |
        | Downloading  |
        | DOWNLOADING  |
        | download     |
        | *******      |

  @pnic @invalid
  Scenario Outline: SDK cannot report lsm_report to report-srv with stat (not str)
    Given prepare valid request body of lsm_report with empty files
    And prepare a valid file_info of lsm_report
    And set field stat of file_info to <value> and type to <type>
    And add file_info to lsm_report
    When report-srv receive the lsm_report request
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

  @pnic @invalid
  Scenario Outline: SDK cannot report lsm_report to report-srv when fields value ""
    Given prepare valid request body of lsm_report with empty files
    And prepare a valid file_info of lsm_report
    And set field <field> of file_info to "" and type to object
    And add file_info to lsm_report
    When report-srv receive the lsm_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: field type string
        | field    |
        | file_id  |
        | stat     |

  @pnic @valid
  Scenario Outline: SDK can report lsm_report to report-srv successfully with repeatable file_id
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of lsm_report with empty files
    And prepare a valid file_info of lsm_report
    And set field stat of file_info to <value_1> and type to str
    And add file_info to lsm_report
    And set field stat of file_info to <value_2> and type to str
    And add file_info to lsm_report
    When report-srv receive the lsm_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}
    Examples: valid stat
        | value_1      | value_2   |
        | downloading  | interrupt |



