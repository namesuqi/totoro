# Created by liwenxuan at 2017/10/10
@ts @report @lsm_report @robustness
Feature: SDK report-srv receive the lsm_report request with fields except files
    # field files is empty
  
  @invalid @pnic
  Scenario: SDK cannot report lsm_report to report-srv without request parameter
    Given prepare valid request body of lsm_report with empty files
    And set param peer_id to "" and type to object
    When report-srv receive the lsm_report request
    Then response status_code should be 404
    And response error_code should be None
    And response data should be None

  @invalid @pnic
  Scenario Outline: SDK cannot report lsm_report to report-srv with incorrect peer_id
    Given prepare valid request body of lsm_report with empty files
    And set param peer_id to <value> and type to str
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

  @invalid @pnic
  Scenario Outline: SDK cannot report lsm_report to report-srv without required fields
    Given prepare valid request body of lsm_report with empty files
    And delete field <field> of lsm_report
    When report-srv receive the lsm_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: required fields of lsm_report
         | field      |
         | diskTotal  |
         | diskFree   |
         | lsmTotal   |
         | lsmFree    |
         | universe   |
         | files      |

  # to be update
  @invalid @pnic
  Scenario Outline: SDK cannot report lsm_report to report-srv when required fields value None
    Given prepare valid request body of lsm_report with empty files
    And set field <field> of lsm_report to None and type to NoneType
    When report-srv receive the lsm_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: required fields of lsm_report
         | field      |
         | diskTotal  |
         | diskFree   |
         | lsmTotal   |
         | lsmFree    |
         | universe   |
         | files      |

  @pnic @invalid
  Scenario Outline: SDK cannot report lsm_report to report-srv with disk_total (not long)
    Given prepare valid request body of lsm_report with empty files
    And set field diskTotal of lsm_report to <value> and type to <type>
    When report-srv receive the lsm_report request
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

  @pnic @invalid
  Scenario Outline: SDK cannot report lsm_report to report-srv with disk_free (not long)
    Given prepare valid request body of lsm_report with empty files
    And set field diskFree of lsm_report to <value> and type to <type>
    When report-srv receive the lsm_report request
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

  @pnic @invalid
  Scenario Outline: SDK cannot report lsm_report to report-srv with lsm_total (not long)
    Given prepare valid request body of lsm_report with empty files
    And set field lsmTotal of lsm_report to <value> and type to <type>
    When report-srv receive the lsm_report request
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

  @pnic @invalid
  Scenario Outline: SDK cannot report lsm_report to report-srv with lsm_free (not long)
    Given prepare valid request body of lsm_report with empty files
    And set field lsmFree of lsm_report to <value> and type to <type>
    When report-srv receive the lsm_report request
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

  @pnic @valid
  Scenario Outline: SDK can report lsm_report to report-srv successfully with valid universe
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of lsm_report with empty files
    And set field universe of lsm_report to <value> and type to bool
    When report-srv receive the lsm_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}
    Examples: type bool
         | value |
         | True  |
         | False |

  @pnic @invalid
  Scenario Outline: SDK cannot report lsm_report to report-srv with universe (not bool)
    Given prepare valid request body of lsm_report with empty files
    And set field universe of lsm_report to <value> and type to <type>
    When report-srv receive the lsm_report request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not bool type
         | value | type   |
         | ""    | object |
         | " "   | object |
         | 0     | str    |
         | 0     | int    |
         | 1     | int    |
         | 0.0   | float  |
         | 0.1   | float  |

  @pnic @invalid
  Scenario Outline: SDK cannot report lsm_report to report-srv with files (not array)
    Given prepare valid request body of lsm_report with empty files
    And set field files of lsm_report to <value> and type to <type>
    When report-srv receive the lsm_report request
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
