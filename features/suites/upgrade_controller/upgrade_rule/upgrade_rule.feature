# Created by liwenxuan at 2017/11/13
@upgrade_controller @upgrade_rule @functionality
Feature: upgrade-controller received a valid upgrade_rule request
  # As upgrade_controller,
  # when I receive a valid upgrade_rule request,
  # I will cache the rule locally, (if there is a rule in the cache, new rule will cover the rule)

  Background: rule_group and rule defaults to be valid for all and target_version defaults to TARGET_VERSION

  @valid
  Scenario: do not configure any rules
    Given prepare an empty upgrade_rule request
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 200
    And response error_code should be None
    And upgrade_rule response should be "{"result": "OK"}"

  @valid
  Scenario: configure a rule valid for all
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 200
    And response error_code should be None
    And upgrade_rule response should be "{"result": "OK"}"

  @valid
  Scenario: configure a rule valid for one version
    Given prepare an empty upgrade_rule request
    And prepare a rule_group without rules
    And prepare a rule
    And modify the value of field "core_version" of rule to "["1.1.1", "1.1.1"]" and type to "list"
    And add the rule to rule_group
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 200
    And response error_code should be None
    And upgrade_rule response should be "{"result": "OK"}"

  @valid
  Scenario Outline: configure independent rules in one rule_group
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
    Then response status_code should be 200
    And response error_code should be None
    And upgrade_rule response should be "{"result": "OK"}"
    Examples: independent version_range_1 and version_range_2
        | version_range_1    | version_range_2    |
        | ["1.1.1", "2.2.2"] | ["2.2.3", "3.3.3"] |
        | ["1.1.1", "2.2.2"] | ["2.3.1", "3.3.3"] |
        | ["1.1.1", "2.2.2"] | ["3.1.1", "3.3.3"] |

  @valid
  Scenario Outline: configure rules with multi rule_group
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "<field>" of rule_group to "<value_1>" and type to "<type>"
    And add the rule_group to upgrade_rule
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "<field>" of rule_group to "<value_2>" and type to "<type>"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 200
    And response error_code should be None
    And upgrade_rule response should be "{"result": "OK"}"
    Examples:
        | field        | value_1        | value_2       | type   |
        | user_ids     | ["AAAAAAAA"]   | ["BBBBBBBB"]  | list   |
        | province_ids | ["310000"]     | ["110000"]    | list   |
        | isp_ids      | ["100017"]     | ["1000103"]   | list   |
        | percent      | 0.2            | 0.5           | float  |

  # valid_field_value
  @valid
  Scenario Outline: the value of user_ids is valid
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "user_ids" of rule_group to "<value>" and type to "list"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 200
    And response error_code should be None
    And upgrade_rule response should be "{"result": "OK"}"
    Examples: valid value of "user_ids"
    | value                    |
    | []                       |
    | ["12345678"]             |
    | ["90ABCDEF"]             |
    | ["12345678", "90ABCDEF"] |

  @valid
  Scenario Outline: the value of province_ids is valid
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "province_ids" of rule_group to "<value>" and type to "list"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 200
    And response error_code should be None
    And upgrade_rule response should be "{"result": "OK"}"
    Examples: valid value of "province_ids"
    | value                |
    | []                   |
    | ["310000"]           |
    | ["110000"]           |
    | ["310000", "110000"] |

  @valid
  Scenario Outline: the value of isp_ids is valid
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "isp_ids" of rule_group to "<value>" and type to "list"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 200
    And response error_code should be None
    And upgrade_rule response should be "{"result": "OK"}"
    Examples: valid value of "isp_ids"
    | value                 |
    | []                    |
    | ["100017"]            |
    | ["1000103"]           |
    | ["123456789"]         |
    | ["100017", "1000103"] |

  @valid
  Scenario Outline: the value of percent is between 0 and 1
    Given prepare an empty upgrade_rule request
    And prepare a rule_group with a rule valid for all versions
    And modify the value of field "percent" of rule_group to "<value>" and type to "float"
    And add the rule_group to upgrade_rule
    When upgrade_controller receive the upgrade_rule request
    Then response status_code should be 200
    And response error_code should be None
    And upgrade_rule response should be "{"result": "OK"}"
    Examples: valid value of "percent"
    | value  |
    | 0      |
    | 0.01   |
    | 0.5    |
    | 0.99   |
    | 1      |


