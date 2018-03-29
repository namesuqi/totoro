Feature: SDK login to Tracker Server with field version

  @ts @login @redis @version @invalid
  Scenario Outline: SDK cannot login to TS with invalid version
    Given valid request body of login
    And set field version of login to <value> and type to <type>
    When send login request to ts-server
    Then ts-srv should not add the peer_info to PNIC
    And response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: invalid version
        | value     | type   |
        | ""        | object |
        | " "       | object |
        | 3         | str    |
        | 3.12      | str    |
        | 3.12.0.0  | str    |
        | .12.9     | str    |
        | 3..9      | str    |
        | 3.12.     | str    |
        | A.B.C     | str    |

  @ts @login @redis @version @invalid
  Scenario Outline: SDK cannot login to TS with version (not string)
    Given valid request body of login
    And set field version of login to <value> and type to <type>
    When send login request to ts-server
    Then ts-srv should not add the peer_info to PNIC
    And response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not type string
        | value | type   |
        | -1    | int    |
        | 0     | int    |
        | 1     | int    |
        | 0.0   | float  |
        | 0.1   | float  |
