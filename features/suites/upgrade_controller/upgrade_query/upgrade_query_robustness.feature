# Created by liwenxuan at 2017/11/13
@upgrade_controller @upgrade_query @robustness
Feature: upgrade-controller received a upgrade_query request with unexpected data
  # As upgrade_controller,
  # when I receive a invalid upgrade_query request,
  # I should return 400 and empty data to requester

  @valid
  Scenario Outline: SDK have core but there is unexpected field in request body
    Given prepare a valid upgrade_query request with core and failure of nat_detect
    And add field "<field>" to upgrade_query, value to "<value>" and type to "str"
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 200
    And response error_code should be None
    And upgrade_query response should be "{"target_version": ""}"
    Examples: unexpected field-value
        | field    | value   |
        | is_basic | true    |
        | is_basic | false   |
        | test     | test    |

  # SDK do not have core
  @invalid
  Scenario Outline: upgrade_query request with invalid field "is_basic"
    Given prepare a valid upgrade_query request without core
    And modify the value of field "is_basic" of upgrade_query to "<value>" and type to "str"
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None
    Examples: invalid value of "is_basic"
        | value  |
        | 0      |
        | 1      |
        | *      |
        | True   |
        | False  |

  @invalid
  Scenario Outline: upgrade_query request with invalid field "is_basic" (not string)
    Given prepare a valid upgrade_query request without core
    And modify the value of field "is_basic" of upgrade_query to "<value>" and type to "<type>"
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |
        | True  | bool   |
        | False | bool   |

  @invalid
  Scenario: upgrade_query request when field "is_basic" is ""
    Given prepare a valid upgrade_query request without core
    And modify the value of field "is_basic" of upgrade_query to """" and type to "object"
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None

  @invalid
  Scenario: upgrade_query request when field "is_basic" is None
    Given prepare a valid upgrade_query request without core
    And modify the value of field "is_basic" of upgrade_query to "None" and type to "NoneType"
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None

  @invalid
  Scenario: upgrade_query request without field "is_basic"
    Given prepare a valid upgrade_query request without core
    And delete field is_basic of upgrade_query
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None

  # SDK have core
  @invalid
  Scenario Outline: upgrade_query request with invalid field "peer_id"
    Given prepare a valid upgrade_query request with core and success of nat_detect
    And modify the value of field "peer_id" of upgrade_query to "<value>" and type to "str"
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
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
  Scenario Outline: upgrade_query request with invalid field "peer_id" (not string)
    Given prepare a valid upgrade_query request with core and success of nat_detect
    And modify the value of field "peer_id" of upgrade_query to "<value>" and type to "<type>"
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |

  @invalid
  Scenario: upgrade_query request when field "peer_id" is ""
    Given prepare a valid upgrade_query request with core and success of nat_detect
    And modify the value of field "peer_id" of upgrade_query to """" and type to "object"
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None

  @invalid
  Scenario: upgrade_query request when field "peer_id" is None
    Given prepare a valid upgrade_query request with core and success of nat_detect
    And modify the value of field "peer_id" of upgrade_query to "None" and type to "NoneType"
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None

  @invalid
  Scenario: upgrade_query request without field "peer_id"
    Given prepare a valid upgrade_query request with core and success of nat_detect
    And delete field peer_id of upgrade_query
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None

  @invalid
  Scenario Outline: upgrade_query request with invalid field "version"
    Given prepare a valid upgrade_query request with core and success of nat_detect
    And modify the value of field "version" of upgrade_query to "<value>" and type to "str"
    When upgrade_controller receive the upgrade_query request
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
  Scenario Outline: upgrade_query request with invalid field "version" (not string)
    Given prepare a valid upgrade_query request with core and success of nat_detect
    And modify the value of field "version" of upgrade_query to "<value>" and type to "<type>"
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |

  @invalid
  Scenario: upgrade_query request when field "version" is ""
    Given prepare a valid upgrade_query request with core and success of nat_detect
    And modify the value of field "version" of upgrade_query to """" and type to "object"
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None

  @invalid
  Scenario: upgrade_query request when field "version" is None
    Given prepare a valid upgrade_query request with core and success of nat_detect
    And modify the value of field "version" of upgrade_query to "None" and type to "NoneType"
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None

  @invalid
  Scenario: upgrade_query request without field "version"
    Given prepare a valid upgrade_query request with core and success of nat_detect
    And delete field version of upgrade_query
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None

  @invalid
  Scenario Outline: upgrade_query request with invalid field "public_ip"
    Given prepare a valid upgrade_query request with core and success of nat_detect
    And modify the value of field "public_ip" of upgrade_query to "<value>" and type to "str"
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None
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

  @invalid
  Scenario Outline: upgrade_query request with invalid field "public_ip" (not string)
    Given prepare a valid upgrade_query request with core and success of nat_detect
    And modify the value of field "public_ip" of upgrade_query to "<value>" and type to "<type>"
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |

  @invalid
  Scenario: upgrade_query request when field "public_ip" is None
    Given prepare a valid upgrade_query request with core and success of nat_detect
    And modify the value of field "public_ip" of upgrade_query to "None" and type to "NoneType"
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None

  @invalid
  Scenario: upgrade_query request without field "public_ip"
    Given prepare a valid upgrade_query request with core and success of nat_detect
    And delete field public_ip of upgrade_query
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response data should be None

