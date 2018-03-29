Feature: SDK login to Tracker Server with field natType

  @ts @login @redis @nat_type @valid @etcd_user_p2p
  Scenario Outline: SDK can login to TS successfully with valid natType
    Given valid request body of login
    And set field natType of login to <value> and type to int
    When send login request to ts-server
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"p2p_enable":true}
    And ts-srv should add the peer_info to PNIC correctly
    Examples: all allowed natType
        | value  |
        | 0      |
        | 1      |
        | 2      |
        | 3      |
        | 4      |
        | 5      |
        | 6      |

  @ts @login @redis @nat_type @invalid
  Scenario Outline: SDK cannot login to TS with invalid natType
    Given valid request body of login
    And set field natType of login to <value> and type to int
    When send login request to ts-server
    Then ts-srv should not add the peer_info to PNIC
    And response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: invalid nat_type
        | value  |
        | -1     |
        | 7      |
        | 100    |

  @ts @login @redis @nat_type @invalid
  Scenario Outline: SDK cannot login to TS with natType (not int)
    Given valid request body of login
    And set field natType of login to <value> and type to <type>
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

