# Created by liwenxuan at 2017/11/16
@upgrade @upgrade_get @robustness
Feature: upgrade-srv receive a upgrade_get request with unexpected data
  # As upgrade-srv,
  # when I receive a invalid upgrade_get request,
  # I will return 400 and empty data to requester

  @invalid
  Scenario Outline: missing required fields
    Given prepare a valid upgrade_get request
    And delete field <field> of upgrade_get
    When upgrade-srv receive the upgrade_get request
    Then response status_code should be 400
    And response data should be None
    Examples: required fields
        | field               |
        | targetversion       |
        | shellversion        |
        | os                  |
        | osversion           |
        | distribution        |
        | distributionversion |
        | envCPU              |
        | realCPU             |
        | toolchain           |

  @invalid
  Scenario Outline: the value of fields is None
    Given prepare a valid upgrade_get request
    And modify the value of field "<field>" of upgrade_get to "None" and type to "NoneType"
    When upgrade-srv receive the upgrade_get request
    Then response status_code should be 400
    And response data should be None
    Examples: all fields
        | field               |
        | targetversion       |
        | peerid              |
        | shellversion        |
        | os                  |
        | osversion           |
        | distribution        |
        | distributionversion |
        | envCPU              |
        | realCPU             |
        | toolchain           |

  @invalid
  Scenario Outline: the value of fields is ""
    Given prepare a valid upgrade_get request
    And modify the value of field "<field>" of upgrade_get to """" and type to "object"
    When upgrade-srv receive the upgrade_get request
    Then response status_code should be 400
    And response data should be None
    Examples: all fields
        | field               |
        | targetversion       |
        | peerid              |
        | shellversion        |
        | os                  |
        | osversion           |
        | distribution        |
        | distributionversion |
        | envCPU              |
        | realCPU             |
        | toolchain           |

  @invalid
  Scenario Outline: targetversion is not a valid version
    Given prepare a valid upgrade_get request
    And modify the value of field "targetversion" of upgrade_get to "<value>" and type to "str"
    When upgrade-srv receive the upgrade_get request
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
  Scenario Outline: targetversion is not a string
    Given prepare a valid upgrade_get request
    And modify the value of field "targetversion" of upgrade_get to "<value>" and type to "<type>"
    When upgrade-srv receive the upgrade_get request
    Then response status_code should be 400
    And response data should be None
    Examples: not type string
        | value     | type   |
        | -1        | int    |
        | 0         | int    |
        | 1         | int    |
        | 0.0       | float  |
        | 0.1       | float  |
        | ["4.1.0"] | list   |

  @invalid
  Scenario Outline: peerid is not hexadecimal 32 bytes
    Given prepare a valid upgrade_get request
    And modify the value of field "peerid" of upgrade_get to "<value>" and type to "str"
    When upgrade-srv receive the upgrade_get request
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
  Scenario Outline: peerid is not a string
    Given prepare a valid upgrade_get request
    And modify the value of field "peerid" of upgrade_get to "<value>" and type to "<type>"
    When upgrade-srv receive the upgrade_get request
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
  Scenario Outline: shellversion is not a valid version
    Given prepare a valid upgrade_get request
    And modify the value of field "shellversion" of upgrade_get to "<value>" and type to "str"
    When upgrade-srv receive the upgrade_get request
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
  Scenario Outline: shellversion is not a string
    Given prepare a valid upgrade_get request
    And modify the value of field "shellversion" of upgrade_get to "<value>" and type to "<type>"
    When upgrade-srv receive the upgrade_get request
    Then response status_code should be 400
    And response data should be None
    Examples: not type string
        | value     | type   |
        | -1        | int    |
        | 0         | int    |
        | 1         | int    |
        | 0.0       | float  |
        | 0.1       | float  |
        | ["1.1.1"] | list   |

  @invalid
  Scenario Outline: os is not a string
    Given prepare a valid upgrade_get request
    And modify the value of field "os" of upgrade_get to "<value>" and type to "<type>"
    When upgrade-srv receive the upgrade_get request
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
  Scenario Outline: osversion is not a string
    Given prepare a valid upgrade_get request
    And modify the value of field "osversion" of upgrade_get to "<value>" and type to "<type>"
    When upgrade-srv receive the upgrade_get request
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
  Scenario Outline: distribution is not a string
    Given prepare a valid upgrade_get request
    And modify the value of field "distribution" of upgrade_get to "<value>" and type to "<type>"
    When upgrade-srv receive the upgrade_get request
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
  Scenario Outline: distributionversion is not a string
    Given prepare a valid upgrade_get request
    And modify the value of field "distributionversion" of upgrade_get to "<value>" and type to "<type>"
    When upgrade-srv receive the upgrade_get request
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
  Scenario Outline: envCPU is not a string
    Given prepare a valid upgrade_get request
    And modify the value of field "envCPU" of upgrade_get to "<value>" and type to "<type>"
    When upgrade-srv receive the upgrade_get request
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
  Scenario Outline: realCPU is not a string
    Given prepare a valid upgrade_get request
    And modify the value of field "realCPU" of upgrade_get to "<value>" and type to "<type>"
    When upgrade-srv receive the upgrade_get request
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
  Scenario Outline: toolchain is not a string
    Given prepare a valid upgrade_get request
    And modify the value of field "toolchain" of upgrade_get to "<value>" and type to "<type>"
    When upgrade-srv receive the upgrade_get request
    Then response status_code should be 400
    And response data should be None
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |
