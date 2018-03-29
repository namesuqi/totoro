Feature: SDK login to Tracker Server with field publicPort

  @ts @login @redis @public_port @valid @etcd_user_p2p
  Scenario Outline: SDK can login to TS successfully with valid publicPort
    Given valid request body of login
    And set field publicPort of login to <value> and type to int
    When send login request to ts-server
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"p2p_enable":true}
    And ts-srv should add the peer_info to PNIC correctly
    Examples: valid port
        | value |
        | 0     |
        | 1     |
        | 65534 |
        | 65535 |

  @ts @login @redis @public_port @invalid
  Scenario Outline: SDK cannot login to TS with invalid publicPort
    Given valid request body of login
    And set field publicPort of login to <value> and type to int
    When send login request to ts-server
    Then ts-srv should not add the peer_info to PNIC
    And response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: invalid port
        | value  |
        | -1     |
        | 65536  |
        | 70000  |

  @ts @login @redis @public_port @invalid
  Scenario Outline: SDK cannot login to TS with publicPort (not int)
    Given valid request body of login
    And set field publicPort of login to <value> and type to <type>
    When send login request to ts-server
    Then ts-srv should not add the peer_info to PNIC
    And response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not int type
        | value | type   |
        | ""    | object |
        | " "   | object |
        | 0     | str    |
        | 0.0   | float  |
        | 0.1   | float  |




