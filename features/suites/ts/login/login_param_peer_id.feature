Feature: SDK login to Tracker Server with param peer_id

  @ts @login @redis @peer_id @invalid
  Scenario Outline: SDK cannot login to TS with invalid peer_id
    Given valid request body of login
    And set param peer_id to <value> and type to str
    When send login request to ts-server
    Then ts-srv should not add the peer_info to PNIC
    And response status_code should be 400
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

  @ts @login @redis @peer_id @invalid
  Scenario: SDK cannot login to TS without peer_id
    Given valid request body of login
    And set param peer_id to "" and type to object
    When send login request to ts-server
    Then ts-srv should not add the peer_info to PNIC
    And response status_code should be 404
    And response error_code should be None
    And response data should be None

