# Created by liwenxuan at 2017/10/20
Feature: SDK send get_host request to httpdns
#  As httpdns,
#  when I receive a get_host request,
#  I will get ips and ttl of the required host from ETCD and return host_info to requester

  @httpdns @get_host @valid
  Scenario Outline: httpdns should return correct host_info to SDK
    Given prepare valid request body of get_host, host defaults to ts
    And set field host of get_host to <value> and type to str
    When httpdns receive get_host request
    Then response status_code should be 200
    And response error_code should be None
    And response data of get_host should be not defined
    Examples: valid host
        | value                  |
        | ts.crazycdn.com        |
        | seeds.crazycdn.com     |
        | report.crazycdn.com    |
        | errlogs.crazycdn.com   |
        | stats.crazycdn.com     |
        | live-ch.crazycdn.com   |
        | upgradev2.crazycdn.com |
        | channel.crazycdn.com   |
        | stun2.crazycdn.com     |
        | opt.crazycdn.com       |

  @httpdns @get_host @valid
  Scenario Outline: httpdns should return empty ips to SDK when host is not in ETCD
    Given prepare valid request body of get_host, host defaults to ts
    And set field host of get_host to <value> and type to str
    When httpdns receive get_host request
    Then response status_code should be 200
    And response error_code should be None
    And response data of get_host should be not defined
    Examples: host not in ETCD
        | value        |
        | crazycdn.com |
        | upgrade      |
        | .com         |

  @httpdns @get_host @invalid
  Scenario: httpdns should not return any host_info to SDK when host is ""
    Given prepare valid request body of get_host, host defaults to ts
    And set field host of get_host to "" and type to object
    When httpdns receive get_host request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None

  @httpdns @get_host @invalid
  Scenario: httpdns should not return any host_info to SDK when missing host
    Given prepare valid request body of get_host, host defaults to ts
    And delete field host of get_host
    When httpdns receive get_host request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None

  @httpdns @get_host @valid
  Scenario: httpdns should return correct host_info to SDK when missing ip
    Given prepare valid request body of get_host, host defaults to ts
    And delete field ip of get_host
    When httpdns receive get_host request
    Then response status_code should be 200
    And response error_code should be None
    And response data of get_host should be not defined

  @httpdns @get_host @valid
  Scenario: httpdns should return correct host_info to SDK when ip is ""
    Given prepare valid request body of get_host, host defaults to ts
    And set field ip of get_host to "" and type to object
    When httpdns receive get_host request
    Then response status_code should be 200
    And response error_code should be None
    And response data of get_host should be not defined

  @httpdns @get_host @valid
  Scenario Outline: httpdns should return correct host_info to SDK with valid ip
    Given prepare valid request body of get_host, host defaults to ts
    And set field ip of get_host to <value> and type to str
    When httpdns receive get_host request
    Then response status_code should be 200
    And response error_code should be None
    And response data of get_host should be not defined
    Examples: valid ip
        | value           |
        | 0.0.0.0         |
        | 1.1.1.1         |
        | 254.254.254.254 |
        | 255.255.255.255 |

  @httpdns @get_host @invalid
  Scenario Outline: httpdns should not return any host_info to SDK with invalid ip
    Given prepare valid request body of get_host, host defaults to ts
    And set field ip of get_host to <value> and type to str
    When httpdns receive get_host request
    Then response status_code should be 400
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
        | *.*.*.*         |

  @httpdns @etcd_httpdns_user_domain @valid
  Scenario Outline: httpdns should return matched host_info to SDK when its peerid's prefix is in ETCD
    Given httpdns has been configured ok with the <user_id> of <user_name> and <host_ip> of <host>
    Given prepare a url with <peer_id> and <host>
    When httpdns receive get_host request
    Then response status_code should be 200
    And response error_code should be None
    And response host info should be correct
    Examples:
        | user_id | user_name | host_ip | host | peer_id |
        | 00002222|t_test |192.168.1.222|ts.crazycdn.com|00002222123456781234567812345611|
#    | 00002222|t_test |192.168.1.222|report.crazycdn.com|00002222123456781234567812345611|
#    | 00003333|t_test |192.168.1.222|seeds.crazycdn.com|00003333123456781234567812345611|

  @httpdns @etcd_httpdns_user_domain @invalid
  Scenario Outline: httpdns should return 400 when SDK's peerid is invalid
    Given httpdns has been configured ok with the <user_id> of <user_name> and <host_ip> of <host>
    Given prepare a url with <peer_id> and <host>
    When httpdns receive get_host request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples:
        | user_id | user_name | host_ip | host | peer_id |
        | 00002222|t_test |192.168.1.222|ts.crazycdn.com|00002222123456781234567|
  #      | 00002222|t_test |192.168.1.333|report.crazycdn.com|00002222AAAAAAAAAAAAAAA|
  #      | 00004444|t_test |192.168.1.444|seeds.crazycdn.com|00004444|

  @httpdns @etcd_httpdns_user_domain @valid
  Scenario Outline: httpdns should return 200 and default ip when SDK's peerid is null
    Given httpdns has been configured ok with the <user_id> of <user_name> and <host_ip> of <host>
    Given prepare a url with empty peer_id but with <host>
    When httpdns receive get_host request
    Then response status_code should be 200
    And response error_code should be None
    And response host info should be default
    Examples:
        | user_id | user_name | host_ip | host |
        | 00002222|t_test |192.168.1.222|ts.crazycdn.com|
  #      | 00003333|t_test |192.168.1.333|ts.crazycdn.com|

  @httpdns @etcd_httpdns_user_domain @valid
  Scenario Outline: httpdns should return 200 and default ip when the user is not configured in ETCD
    Given httpdns is not configured with the <user_id> of <user_name> and <host>
    Given prepare a url with <peer_id> and <host>
    When httpdns receive get_host request
    Then response status_code should be 200
    And response error_code should be None
    And response host info should be default
    Examples:
        | user_id | user_name | host | peer_id |
        |00002222 |t_test     |ts.crazycdn.com|00002222123456781234567812345622|
  #      |00003333 |h_test     |ts.crazycdn.com|00002222123456781234567812345622|

  @httpdns @etcd_httpdns_user_domain @valid
  Scenario Outline: httpdns should return 200 and default ip when its user info is in ETCD but host is not configured
    Given httpdns has been configured ok with the <user_id> of <user_name> and <host_ip> of <host>
    Given prepare a url with <peer_id> and <expected_host>
    When httpdns receive get_host request
    Then response status_code should be 200
    And response error_code should be None
    And response host info should be default
    Examples:
        | user_id | user_name | host_ip | host | peer_id | expected_host |
        |00002222 |t_test     |192.168.1.222|ts.crazycdn.com|00002222123456781234567812345622|seeds.crazycdn.com|

  @httpdns @etcd_httpdns_user_domain @valid
  Scenario Outline: httpdns should return 200 and default ip without peer_id
    Given httpdns has been configured ok with the <user_id> of <user_name> and <host_ip> of <host>
    Given prepare a url without peer_id but with <host>
    When httpdns receive get_host request
    Then response status_code should be 200
    And response error_code should be None
    And response host info should be default
    Examples:
        | user_id | user_name | host_ip | host |
        | 00002222|t_test |192.168.1.222|ts.crazycdn.com|
