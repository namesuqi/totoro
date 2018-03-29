# Created by liwenxuan at 2017/10/23
Feature: courier send download_tasks request to push-hub with invalid fields

  @push_hub @download_tasks @pspfc @invalid
  Scenario Outline: push-hub should not add any task when required fields value None
    Given prepare valid request body of download_tasks
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And set field <field> of task_info to None and type to NoneType
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should not add any task to PSPFC_PUSH_ID
    Examples: required fields
        | field      |
        | file_id    |
        | file_url   |
        | file_size  |
        | ppc        |
        | cppc       |
        | piece_size |
        | priority   |
        | push_id    |
        | push_ip    |

  @push_hub @download_tasks @pspfc @invalid
  Scenario Outline: push-hub should not add any task when missing required fields
    Given prepare valid request body of download_tasks
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And delete field <field> of task_info
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should not add any task to PSPFC_PUSH_ID
    Examples: required fields
        | field      |
        | file_id    |
        | file_url   |
        | file_size  |
        | ppc        |
        | cppc       |
        | piece_size |
        | priority   |
        | push_id    |
        | push_ip    |

  @push_hub @download_tasks @pspfc @invalid
  Scenario Outline: push-hub should not add any task to PSPFC with invalid file_id
    Given prepare valid request body of download_tasks
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And set field file_id of task_info to <value> and type to str
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should not add any task to PSPFC_PUSH_ID
    Examples: not hexadecimal 32 bytes
        | value                                       |
        | a                                           |
        | 00000000123451234512345                     |
        | 1234567890123456789012345678931             |
        | 1234567890123456789012345678932G            |
        | 123456789012345678901234567890133           |
        | 000000001234512345123451234AADBCFDABCDDADDD |
        | ********************************            |

  @push_hub @download_tasks @pspfc @invalid
  Scenario Outline: push-hub should not add any task to PSPFC with invalid file_id (not string)
    Given prepare valid request body of download_tasks
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And set field file_id of task_info to <value> and type to <type>
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should not add any task to PSPFC_PUSH_ID
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |

  @push_hub @download_tasks @pspfc @invalid
  Scenario Outline: push-hub should not add any task to PSPFC with invalid file_url (not string)
    Given prepare valid request body of download_tasks
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And set field file_url of task_info to <value> and type to <type>
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should not add any task to PSPFC_PUSH_ID
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |

  @push_hub @download_tasks @pspfc @invalid
  Scenario Outline: push-hub should not add any task to PSPFC with invalid file_size (not int)
    Given prepare valid request body of download_tasks
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And set field file_size of task_info to <value> and type to <type>
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should not add any task to PSPFC_PUSH_ID
    Examples: not int type
        | value | type   |
        | ""    | object |
        | " "   | object |
        | 0     | str    |
        | 0.0   | float  |
        | 0.1   | float  |

  @push_hub @download_tasks @pspfc @invalid
  Scenario Outline: push-hub should not add any task to PSPFC with invalid file_type (not string)
    Given prepare valid request body of download_tasks
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And set field file_type of task_info to <value> and type to <type>
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should not add any task to PSPFC_PUSH_ID
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |

  @push_hub @download_tasks @pspfc @invalid
  Scenario Outline: push-hub should not add any task to PSPFC with invalid ppc (not int)
    Given prepare valid request body of download_tasks
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And set field ppc of task_info to <value> and type to <type>
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should not add any task to PSPFC_PUSH_ID
    Examples: not int type
        | value | type   |
        | ""    | object |
        | " "   | object |
        | 0     | str    |
        | 0.0   | float  |
        | 0.1   | float  |

  @push_hub @download_tasks @pspfc @invalid
  Scenario Outline: push-hub should not add any task to PSPFC with invalid cppc (not int)
    Given prepare valid request body of download_tasks
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And set field cppc of task_info to <value> and type to <type>
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should not add any task to PSPFC_PUSH_ID
    Examples: not int type
        | value | type   |
        | ""    | object |
        | " "   | object |
        | 0     | str    |
        | 0.0   | float  |
        | 0.1   | float  |

  @push_hub @download_tasks @pspfc @invalid
  Scenario Outline: push-hub should not add any task to PSPFC with invalid piece_size (not int)
    Given prepare valid request body of download_tasks
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And set field piece_size of task_info to <value> and type to <type>
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should not add any task to PSPFC_PUSH_ID
    Examples: not int type
        | value | type   |
        | ""    | object |
        | " "   | object |
        | 0     | str    |
        | 0.0   | float  |
        | 0.1   | float  |

  @push_hub @download_tasks @pspfc @invalid
  Scenario Outline: push-hub should not add any task to PSPFC with invalid priority (not int)
    Given prepare valid request body of download_tasks
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And set field priority of task_info to <value> and type to <type>
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should not add any task to PSPFC_PUSH_ID
    Examples: not int type
        | value | type   |
        | ""    | object |
        | " "   | object |
        | 0     | str    |
        | 0.0   | float  |
        | 0.1   | float  |

  @push_hub @download_tasks @pspfc @invalid
  Scenario Outline: push-hub should not add any task to PSPFC with invalid push_id (not string)
    Given prepare valid request body of download_tasks
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And set field push_id of task_info to <value> and type to <type>
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should not add any task to PSPFC_PUSH_ID
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |

  @push_hub @download_tasks @pspfc @invalid
  Scenario Outline: push-hub should not add any task to PSPFC with invalid push_ip
    Given prepare valid request body of download_tasks
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And set field push_ip of task_info to <value> and type to str
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should not add any task to PSPFC_PUSH_ID
    Examples: invalid ip
        | value           |
        | 0               |
        | ...             |
        | 1.1.1           |
        | 1.1.1.1.1       |
        | 1.1.1.          |
        | .1.1.1          |
        | 1...1           |
        | 255.255.255.256 |
        | *.*.*.*         |

  @push_hub @download_tasks @pspfc @invalid
  Scenario Outline: push-hub should not add any task to PSPFC with invalid push_ip (not string)
    Given prepare valid request body of download_tasks
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And set field push_ip of task_info to <value> and type to <type>
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should not add any task to PSPFC_PUSH_ID
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |



