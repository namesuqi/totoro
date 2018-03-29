Feature: SDK log out from Tracker Server
    SDK send get request to TS for keeping alive

  @ts @heartbeat @redis
  Scenario: listed peer can report heartbeat succeed
    Given peer id isn't invalid
    And sdk has login
    When sdk send heartbeat report
    Then response status_code should be 200
    And response data should be empty json
    And peer id is in database


  @ts @heartbeat @redis
  Scenario: the peer that haven't login can't report heartbeat
    Given peer id isn't invalid
    And sdk has not login
    When sdk send heartbeat report
    Then response status_code should be 200
    And response error_code should be E_TS_NOT_LOGIN
    And peer id isn't in database


  @ts @heartbeat @redis
  Scenario Outline: the invalid peer id can't report heartbeat
    Given peer id is <invalid>
    When sdk send heartbeat report
    Then response status_code should be 400
    And response data should be None
    And peer id isn't in database
    Examples: Invalid Peer ids
        |invalid                        |
        |HAVECHARS                      |
        |000000001234512345123451234    |
        |1234567890123456789012345678931|
        |1234567890123456789012345678932G|
        |123456789012345678901234567890133|
        |000000001234512345123451234AADBCFDABCDDADDD|