Feature: SDK login to Tracker Server with field macs

  @ts @login @redis @macs @valid @etcd_user_p2p
  Scenario Outline: SDK can login to TS successfully when masc has more than 1000 elements
    Given valid request body of login
    And set macs of login have <length> elements
    When send login request to ts-server
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"p2p_enable":true}
    And ts-srv should add the peer_info to PNIC correctly
    Examples: macs length
        | length  |
        | 1000    |
        | 1001    |
        | 3000    |

  @ts @login @redis @macs @valid @etcd_user_p2p
  Scenario: SDK can login to TS successfully with empty masc
    Given valid request body of login
    And set field macs of login to {} and type to dict
    When send login request to ts-server
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"p2p_enable":true}
    And ts-srv should add the peer_info to PNIC correctly

  @ts @login @redis @macs @valid
  Scenario Outline: SDK can login to TS successfully with invalid masc (not dict)
    Given valid request body of login
    And set field macs of login to <value> and type to <type>
    When send login request to ts-server
    Then ts-srv should not add the peer_info to PNIC
    And response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: not dict type
        | value  | type    |
        | ""     | object  |
        | " "    | object  |
        | 0      | int     |
        | 0.0    | float   |
        | []     | list    |
        | ()     | tuple   |

