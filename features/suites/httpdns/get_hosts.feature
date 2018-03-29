# Created by liwenxuan at 2017/10/23
Feature: SDK send get_hosts request to httpdns
#  As httpdns,
#  when I receive a get_hosts request,
#  I will get all hosts of the required group from ETCD and host_info of each host
#  and then return all host_info to requester

  @httpdns @get_hosts @valid
  Scenario: httpdns should return all correct host_info to SDK
    Given prepare valid request body of get_hosts, group defaults to crazycdn
    When httpdns receive get_hosts request
    Then response status_code should be 200
    And response error_code should be None
    And response data of get_hosts should be not defined

  @httpdns @get_host @valid
  Scenario Outline: httpdns should return empty list to SDK when group is not in ETCD
    Given prepare valid request body of get_hosts, group defaults to crazycdn
    And set field groupName of get_hosts to <value> and type to str
    When httpdns receive get_hosts request
    Then response status_code should be 200
    And response error_code should be None
    And response data of get_hosts should be not defined
    Examples: group not in ETCD
        | value           |
        | ts.crazycdn.com |
        | upgrade         |
        | crazycdn        |

  @httpdns @get_host @invalid
  Scenario: httpdns should not return any host_info to SDK when group is ""
    Given prepare valid request body of get_hosts, group defaults to crazycdn
    And set field groupName of get_hosts to "" and type to object
    When httpdns receive get_hosts request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None

  @httpdns @get_host @invalid
  Scenario: httpdns should not return any host_info to SDK when missing groupName
    Given prepare valid request body of get_hosts, group defaults to crazycdn
    And delete field groupName of get_hosts
    When httpdns receive get_hosts request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None

  @httpdns @get_hosts @valid
  Scenario: httpdns should return all correct host_info to SDK when missing ip
    Given prepare valid request body of get_hosts, group defaults to crazycdn
    And delete field ip of get_hosts
    When httpdns receive get_hosts request
    Then response status_code should be 200
    And response error_code should be None
    And response data of get_hosts should be not defined

  @httpdns @get_hosts @valid
  Scenario: httpdns should return all correct host_info to SDK when ip is ""
    Given prepare valid request body of get_hosts, group defaults to crazycdn
    And set field ip of get_hosts to "" and type to object
    When httpdns receive get_hosts request
    Then response status_code should be 200
    And response error_code should be None
    And response data of get_hosts should be not defined


  @httpdns @get_hosts @valid
  Scenario Outline: httpdns should return all correct host_info to SDK with valid ip
    Given prepare valid request body of get_hosts, group defaults to crazycdn
    And set field ip of get_hosts to <value> and type to str
    When httpdns receive get_hosts request
    Then response status_code should be 200
    And response error_code should be None
    And response data of get_hosts should be not defined
    Examples: valid ip
        | value           |
        | 0.0.0.0         |
        | 1.1.1.1         |
        | 254.254.254.254 |
        | 255.255.255.255 |

  @httpdns @get_hosts @invalid
  Scenario Outline: httpdns should not return any host_info to SDK with invalid ip
    Given prepare valid request body of get_hosts, group defaults to crazycdn
    And set field ip of get_hosts to <value> and type to str
    When httpdns receive get_hosts request
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
    Given httpdns user domain info has been configured ok with the <user_id> of <user_name> and <host_ip> of <host>
    Given prepare a url about groupName with <peer_id>
    When httpdns receive get_hosts request
    Then response status_code should be 200
    And response error_code should be None
    And response hosts info should be correct
    Examples: matched peer_id
        |user_id|user_name|host_ip|host|peer_id|
        | 00002222|t_test |192.168.1.222|ts.crazycdn.com|00002222123456781234567812345611|
    #    | 00002222|t_test |192.168.1.222|report.crazycdn.com|00002222123456781234567812345622|
    #    | 00004444|t_test |192.168.1.222|seeds.crazycdn.com|00004444123456781234567812345622|

  @httpdns @etcd_httpdns_user_domain @invalid
  Scenario Outline: httpdns should return 400 when SDK's peerid is invalid
    Given httpdns user domain info has been configured ok with the <user_id> of <user_name> and <host_ip> of <host>
    Given prepare a url about groupName with <peer_id>
    When httpdns receive get_hosts request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples:
        | user_id | user_name | host_ip | host | peer_id |
        | 00002222|t_test |192.168.1.222|ts.crazycdn.com|00002222123456781234567|
  #      | 00002222|t_test |192.168.1.222|report.crazycdn.com|00002222AAAAAAAAAAAAAAA|

  @httpdns @etcd_httpdns_user_domain @invalid
  Scenario Outline: httpdns should return 200 and default ips when SDK's peerid is null
    Given httpdns user domain info has been configured ok with the <user_id> of <user_name> and <host_ip> of <host>
    Given prepare a url about groupName but with empty peer_id
    When httpdns receive get_hosts request
    Then response status_code should be 200
    And response error_code should be None
    And response hosts info should be default
    Examples:
        | user_id | user_name | host_ip | host |
        | 00002222|t_test |192.168.1.222|ts.crazycdn.com|

  @httpdns @etcd_httpdns_user_domain @valid
  Scenario Outline: httpdns should return 200 and default ips when the user is not configured in ETCD
    Given httpdns user domain info is not configured with the <user_id> of <user_name> and <host>
    Given prepare a url about groupName with <peer_id>
    When httpdns receive get_hosts request
    Then response status_code should be 200
    And response error_code should be None
    And response hosts info should be default
    Examples:
        | user_id | user_name | host | peer_id |
        |00002222 |t_test     |ts.crazycdn.com|00002222123456781234567812345622|

  @httpdns @etcd_httpdns_user_domain @valid
  Scenario Outline: httpdns should return 200 and default ips when its user info is in ETCD but host is ""
    Given httpdns has been just configured ok with the <user_id> of <user_name>
    Given prepare a url about groupName with <peer_id>
    When httpdns receive get_hosts request
    Then response status_code should be 200
    And response error_code should be None
    And response hosts info should be default
    Examples:
        | user_id | user_name | peer_id |
        |00002222 |t_test   |00002222123456781234567812345622|

  @httpdns @etcd_httpdns_user_domain @valid
  Scenario Outline: httpdns should return 200 and default ips without peer_id
    Given httpdns user domain info has been configured ok with the <user_id> of <user_name> and <host_ip> of <host>
    Given prepare a url about groupName without peer_id
    When httpdns receive get_hosts request
    Then response status_code should be 200
    And response error_code should be None
    And response hosts info should be default
    Examples:
        | user_id | user_name | host_ip | host |
        | 00002222|t_test |192.168.1.222|ts.crazycdn.com|