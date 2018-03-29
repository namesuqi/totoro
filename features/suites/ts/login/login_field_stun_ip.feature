Feature: SDK login to Tracker Server with field stunIP

  @ts @login @redis @stun_ip @valid @etcd_user_p2p
  Scenario Outline: SDK can login to TS successfully with valid stunIP
    Given valid request body of login
    And set field stunIP of login to <value> and type to str
    When send login request to ts-server
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"p2p_enable":true}
    And ts-srv should add the peer_info to PNIC correctly
    Examples: valid ip
        | value           |
        | 0.0.0.0         |
        | 1.1.1.1         |
        | 254.254.254.254 |
        | 255.255.255.255 |

  @ts @login @redis @stun_ip @invalid
  Scenario Outline: SDK cannot login to TS with invalid stunIP
    Given valid request body of login
    And set field stunIP of login to <value> and type to str
    When send login request to ts-server
    Then ts-srv should not add the peer_info to PNIC
    And response status_code should be 400
    And response error_code should be None
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

  @ts @login @redis @stun_ip @invalid
  Scenario Outline: SDK cannot login to TS with stunIP (not string)
    Given valid request body of login
    And set field stunIP of login to <value> and type to <type>
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

  @ts @login @redis @stun_ip @invalid
  Scenario: SDK cannot login to TS when stunIP values ""
    Given valid request body of login
    And set field stunIP of login to "" and type to object
    When send login request to ts-server
    Then ts-srv should not add the peer_info to PNIC
    And response status_code should be 400
    And response error_code should be None
    And response data should be None




