# Created by liwenxuan at 2017/9/29
@ts @seeds @get_seeds
Feature: SDK send get_seeds request to seeds-srv
  # As seeds-srv,
  # when I receive a valid get_seeds request,
  # I will return seeds_info to requester if request peer_id is online

  @functionality @valid @pnic
  Scenario: seeds-srv should return correct seeds_info with online peer_id
    Given prepare valid request body of get_seeds
    And make sure that the peer_id is online, stun_ip is STUN_IP
#    And add 1 seeds to the FOSC in redis
    When seeds-srv receive the get_seeds request
    Then response status_code should be 200
    And response error_code should be None
    And seeds-srv should return seeds in FOSC correctly

  @functionality @invalid @pnic
  Scenario: seeds-srv should not return seeds_info with offline peer_id
    Given prepare valid request body of get_seeds
    And make sure that the peer_id is offline
    When seeds-srv receive the get_seeds request
    Then response status_code should be 200
    And response error_code should be E_TS_NOT_LOGIN

  @robustness @invalid
  Scenario Outline: seeds-srv should not return seeds_info with incorrect peer_id
    Given prepare valid request body of get_seeds
    And set field pid of get_seeds to <value> and type to str
    When seeds-srv receive the get_seeds request
    Then response status_code should be 400
    And response error_code should be None
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

  @robustness @invalid
  Scenario Outline: seeds-srv should not return seeds_info with incorrect file_id
    Given prepare valid request body of get_seeds
    And set field fid of get_seeds to <value> and type to str
    When seeds-srv receive the get_seeds request
    Then response status_code should be 400
    And response error_code should be None
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

  @robustness @invalid
  Scenario Outline: seeds-srv should not return seeds_info with empty required params
    Given prepare valid request body of get_seeds
    And set field <param> of get_seeds to "" and type to object
    When seeds-srv receive the get_seeds request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: invalid peer_id
        | param  |
        | pid    |
        | fid    |

  @robustness @invalid
  Scenario Outline: seeds-srv should not return seeds_info without required params
    Given prepare valid request body of get_seeds
    And delete field <param> of get_seeds
    When seeds-srv receive the get_seeds request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: url params
        | param  |
        | pid    |
        | fid    |



# the treatment (server or strategy) and format of FOSC is not definite

#  @valid @pnic
#  Scenario: SDK can get seeds from seeds-srv with FOSC not existed
#    Given add peer_info to PNIC_STUN_IP
#    And prepare valid request body of get_seeds
#    And delete the FOSC in redis
#    When seeds-srv receive the get_seeds request
#    Then response status_code should be 200
#    And response error_code should be None
#    And seeds-srv should return seeds in FOSC correctly
#    And delete the FOSC in redis

#  @valid @pnic
#  Scenario: SDK can get at most 500 seeds from seeds-srv
#    Given add peer_info to PNIC_STUN_IP
#    And prepare valid request body of get_seeds
#    And delete the FOSC in redis
#    And add 510 seeds to the FOSC in redis
#    When seeds-srv receive the get_seeds request
#    Then response status_code should be 200
#    And response error_code should be None
#    And seeds-srv should return at most 500 seeds
#    And delete the FOSC in redis





