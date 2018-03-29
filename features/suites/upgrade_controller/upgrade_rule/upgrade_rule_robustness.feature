# Created by liwenxuan at 2017/11/14
@upgrade_controller @upgrade_rule @robustness
Feature: upgrade-controller received a upgrade_rule request with unexpected data
  # As upgrade_controller,
  # when I receive a invalid upgrade_rule request,
  # I should return 400 and empty data to requester

  @valid
  Scenario: there are duplicate rule_group in request body
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And add the rule_group to upgrade_rule
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 200
    And response error_code should be None
    And upgrade_rule response should be "{"result": "OK"}"

  @invalid
  Scenario Outline: there is an overlap between the rules in the same rule_group
    Given prepare an empty upgrade_rule request
    And prepare a rule_group without rules
    Given prepare a rule
    And modify the value of field "core_version" of rule to "<version_range_1>" and type to "list"
    And add the rule to rule_group
    Given prepare a rule
    And modify the value of field "core_version" of rule to "<version_range_2>" and type to "list"
    And add the rule to rule_group
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
    Examples: overlap between core_version
        | version_range_1    | version_range_2    |
        | ["1.1.1", "2.2.2"] | ["2.2.2", "3.3.3"] |
        | ["1.1.1", "3.3.3"] | ["2.2.2", "4.4.4"] |
        | ["1.1.1", "3.3.3"] | ["2.2.2", "3.3.3"] |
        | ["1.1.1", "3.3.3"] | ["1.1.1", "2.2.2"] |
        | ["1.1.1", "4.4.4"] | ["2.2.2", "3.3.3"] |

  @invalid
  Scenario: there is no rule in rule_group (upgrade_paths)
    Given prepare an empty upgrade_rule request
    And prepare a rule_group without rules
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None

  @valid
  Scenario: there are duplicate rules in rule_group (upgrade_paths)
    Given prepare an empty upgrade_rule request
    And prepare a rule_group without rules
    And prepare a rule
    And add the rule to rule_group
    And add the rule to rule_group
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None

  # about rule_group
  @invalid
  Scenario Outline: missing required field
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And delete field <field> of rule_group
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
	Examples: required field of rule_group
        | field          |
        | user_ids       |
        | province_ids   |
        | isp_ids        |
        | percent        |
        | upgrade_paths  |

  @invalid
  Scenario Outline: the value of required field is None
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "<field>" of rule_group to "None" and type to "NoneType"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
	Examples: required field of rule_group
        | field          |
        | user_ids       |
        | province_ids   |
        | isp_ids        |
        | percent        |
        | upgrade_paths  |

  @invalid
  Scenario Outline: user_ids is not an array
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "user_ids" of rule_group to "<value>" and type to "<type>"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
	Examples: not array type
        | value  | type    |
        | ""     | object  |
        | " "    | object  |
        | 0      | int     |
        | 0.0    | float   |
        | {}     | dict    |

  @invalid
  Scenario Outline: user_id in user_ids is not a string
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "user_ids" of rule_group to "[<value>]" and type to "list"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
    Examples: not type string
        | value |
        | -1    |
        | 0     |
        | 1     |
        | 0.0   |
        | 0.1   |
        | None  |

  @invalid
  Scenario Outline: the value of user_id in user_ids is incorrect
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "user_ids" of rule_group to "["<value>"]" and type to "list"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
	Examples: user_id is not hexadecimal 8 bytes
        | value        |
        | a            |
        | 1234567      |
        | 123456789    |
        | 1234567G     |
        | 01234567890  |
        | ********     |

  @invalid
  Scenario: the value of user_id in user_ids is ""
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "user_ids" of rule_group to "[""]" and type to "list"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None

  @valid
  Scenario: there are duplicate user_id in user_ids
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "user_ids" of rule_group to "["FFFFFFFF", "FFFFFFFF"]" and type to "list"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 200
    And response error_code should be None
    And upgrade_rule response should be "{"result": "OK"}"

  @invalid
  Scenario Outline: province_ids is not an array
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "province_ids" of rule_group to "<value>" and type to "<type>"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
	Examples: not array type
        | value  | type    |
        | ""     | object  |
        | " "    | object  |
        | 0      | int     |
        | 0.0    | float   |
        | {}     | dict    |

  @invalid
  Scenario Outline: province_id in province_ids is not a string
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "province_ids" of rule_group to "[<value>]" and type to "list"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
    Examples: not type string
        | value  |
        | -1     |
        | 0      |
        | 1      |
        | 0.0    |
        | 0.1    |
        | 123456 |

  @invalid
  Scenario Outline: the value of province_id in province_ids is incorrect
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "province_ids" of rule_group to "["<value>"]" and type to "list"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
	Examples: not 6 bits number
        | value        |
        | 0            |
        | -1           |
        | 12345        |
        | 1234567      |
        | 1234567890   |

  @invalid
  Scenario Outline: isp_ids is not an array
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "isp_ids" of rule_group to "<value>" and type to "<type>"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
	Examples: not array type
        | value  | type    |
        | ""     | object  |
        | " "    | object  |
        | 0      | int     |
        | 0.0    | float   |
        | {}     | dict    |

  @invalid
  Scenario Outline: isp_id in isp_ids is not a string
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "isp_ids" of rule_group to "[<value>]" and type to "list"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
    Examples: not type string
        | value     |
        | -1        |
        | 0         |
        | 1         |
        | 0.0       |
        | 0.1       |
        | 123456    |
        | 123456789 |

  @invalid
  Scenario Outline: the value of isp_id in isp_ids is incorrect
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "isp_ids" of rule_group to "["<value>"]" and type to "list"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
	Examples: not 6~9 bits number
        | value        |
        | 0            |
        | -1           |
        | 12345        |
        | 1234567890   |
        | 123456789000 |

  @invalid
  Scenario Outline: the value of percent is not between 0 and 1
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "percent" of rule_group to "<value>" and type to "float"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
    Examples: invalid value of "percent"
        | value  |
        | -1     |
        | -0.01  |
        | 1.01   |
        | 2      |

  @invalid
  Scenario Outline: percent is not a float
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "percent" of rule_group to "<value>" and type to "<type>"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
    Examples: not float type
        | value | type   |
        | ""    | object |
        | " "   | object |
        | 0     | str    |
        | [1]   | list   |

  @invalid
  Scenario Outline: upgrade_paths is not an array
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "upgrade_paths" of rule_group to "<value>" and type to "<type>"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
	Examples: not array type
        | value  | type    |
        | ""     | object  |
        | " "    | object  |
        | 0      | int     |
        | 0.0    | float   |
        | {}     | dict    |

  # about rule
  @invalid
  Scenario Outline: missing required field of rule
    Given prepare an empty upgrade_rule request
    And prepare a rule_group without rules
    And prepare a rule
    And delete field <field> of rule
    And add the rule to rule_group
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
	Examples: required field of rule
        | field          |
        | core_version   |
        | target_version |

  @invalid
  Scenario Outline: the value of required field is None
    Given prepare an empty upgrade_rule request
    And prepare a rule_group without rules
    And prepare a rule
    And modify the value of field "<field>" of rule to "None" and type to "NoneType"
    And add the rule to rule_group
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
	Examples: required field of rule
        | field          |
        | core_version   |
        | target_version |

  @invalid
  Scenario Outline: core_version of rule is not an array
    Given prepare an empty upgrade_rule request
    And prepare a rule_group without rules
    And prepare a rule
    And modify the value of field "core_version" of rule to "<value>" and type to "<type>"
    And add the rule to rule_group
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
	Examples: not array type
        | value  | type    |
        | ""     | object  |
        | " "    | object  |
        | 0      | int     |
        | 0.0    | float   |
        | {}     | dict    |

  @invalid
  Scenario Outline: core_version of rule is not a valid version range
    Given prepare an empty upgrade_rule request
    And prepare a rule_group without rules
    And prepare a rule
    And modify the value of field "core_version" of rule to "<value>" and type to "list"
    And add the rule to rule_group
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
    Examples: invalid version range
        | value                       |
        | []                          |
        | ["1.1.1"]                   |
        | ["1.1.1", "2.2.2", "3.3.3"] |
    Examples: [v1, v2] & v1 > v2
        | value                       |
        | ["2.2.2", "1.3.3"]          |
        | ["2.2.2", "2.1.3"]          |
        | ["2.2.2", "2.2.1"]          |

  @invalid
  Scenario Outline: version in core_version of rule is not a valid version
    Given prepare an empty upgrade_rule request
    And prepare a rule_group without rules
    And prepare a rule
    And modify the value of field "core_version" of rule to "["0.0.0", "<value>"]" and type to "list"
    And add the rule to rule_group
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
    Examples: invalid version
        | value     |
        | 4         |
        | 4.0       |
        | 4.0.0.0   |
        | .0.0      |
        | 4..0      |
        | 4.0.      |
        | 4.0.0.    |
        | A.B.C     |

  @invalid
  Scenario Outline: version in core_version of rule is not a string
    Given prepare an empty upgrade_rule request
    And prepare a rule_group without rules
    And prepare a rule
    And modify the value of field "core_version" of rule to "["0.0.0", <value>]" and type to "list"
    And add the rule to rule_group
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
    Examples: not type string
        | value |
        | -1    |
        | 0     |
        | 1     |
        | 0.0   |
        | 0.1   |

  @invalid
  Scenario Outline: target_version of rule is not a valid version
    Given prepare an empty upgrade_rule request
    And prepare a rule_group without rules
    And prepare a rule
    And modify the value of field "target_version" of rule to "<value>" and type to "str"
    And add the rule to rule_group
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
    Examples: invalid version
        | value     |
        | 4         |
        | 4.0       |
        | 4.0.0.0   |
        | .0.0      |
        | 4..0      |
        | 4.0.      |
        | 4.0.0.    |
        | A.B.C     |

  @invalid
  Scenario Outline: target_version of rule is not a string
    Given prepare an empty upgrade_rule request
    And prepare a rule_group without rules
    And prepare a rule
    And modify the value of field "target_version" of rule to "<value>" and type to "<type>"
    And add the rule to rule_group
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 400
    And response data should be None
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |

