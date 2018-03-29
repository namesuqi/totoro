@ts2 @login
Feature: SDK login to Tracker Server with fields
  # As ts-srv,
  # when I receive a valid login request,
  # I will add peer_info to PNIC_<peer-id> in redis-cluster

  @functionality @valid @login @pnic @fields @etcd_user_p2p
  Scenario: SDK can login to TS successfully
    Given valid request body of login
    When send login request to ts-server
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"p2p_enable":true}
    And ts-srv should add the peer_info to PNIC correctly

  @robustness @invalid @login @pnic @fields
  Scenario Outline: SDK cannot login to TS without required field
    Given valid request body of login
    And delete field <field> of login
    When send login request to ts-server
    Then ts-srv should not add the peer_info to PNIC
    And response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: required fields
        | field      |
        | version    |
        | natType    |
        | publicIP   |
        | publicPort |
        | privateIP  |
        | privatePort|
        | stunIP     |
        | macs       |

  @robustness @invalid @login @pnic @fields
  Scenario Outline: SDK cannot login to TS when required field values None
    Given valid request body of login
    And set field <field> of login to None and type to NoneType
    When send login request to ts-server
    Then ts-srv should not add the peer_info to PNIC
    And response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: required fields
        | field       |
        | version     |
        | natType     |
        | publicIP    |
        | publicPort  |
        | privateIP   |
        | privatePort |
        | stunIP      |
        | macs        |

  @ts @valid @login @pnic @fields @etcd_user_p2p
  Scenario Outline: SDK get login response with p2p false when p2p_enable percent is 0
    Given valid request body of login
    And set user 66666666 p2p_enable percent 0%
    And set param peer_id to <value> and type to str
    When send login request to ts-server
    Then response status_code should be 200
    And response data should be {"p2p_enable":false}
    And ts-srv should add the peer_info to PNIC correctly
    Examples:
        | value                                 |
        | 66666666ABCDEF1234567890ABCDEF00 |
        | 66666666ABCDEF1234567890ABCDEFFF |

  @ts @valid @login @pnic @fields @etcd_user_p2p
  Scenario Outline: SDK get login response with p2p true when p2p_enable percent is 100
    Given valid request body of login
    And set user 66666666 p2p_enable percent 100%
    And set param peer_id to <value> and type to str
    When send login request to ts-server
    Then response status_code should be 200
    And response data should be {"p2p_enable":true}
    And ts-srv should add the peer_info to PNIC correctly
    Examples:
        | value                                 |
        | 66666666ABCDEF1234567890ABCDEF00 |
        | 66666666ABCDEF1234567890ABCDEFFF |

  @ts @valid @login @pnic @fields @etcd_user_p2p
  Scenario Outline: SDK get login response with p2p true when p2p_enable percent is 50
    Given valid request body of login
    And set user 66666666 p2p_enable percent 50%
    And set param peer_id to <value> and type to str
    When send login request to ts-server
    Then response status_code should be 200
    And response data should be {"p2p_enable":true}
    And ts-srv should add the peer_info to PNIC correctly
    Examples:
        | value                                 |
        | 66666666ABCDEF1234567890ABCDEF00 |
        | 66666666ABCDEF1234567890ABCDEF7F |

  @ts @valid @login @pnic @fields @etcd_user_p2p
  Scenario Outline: SDK get login response with p2p false when p2p_enable percent is 50
    Given valid request body of login
    And set user 66666666 p2p_enable percent 50%
    And set param peer_id to <value> and type to str
    When send login request to ts-server
    Then response status_code should be 200
    And response data should be {"p2p_enable":false}
    And ts-srv should add the peer_info to PNIC correctly
    Examples:
        | value                                 |
        | 66666666ABCDEF1234567890ABCDEF80 |
        | 66666666ABCDEF1234567890ABCDEFFF |