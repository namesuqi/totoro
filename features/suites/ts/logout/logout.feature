Feature: SDK log out from Tracker Server
    SDK send delete request to TS for logout


  @ts @logout @redis
  Scenario Outline: TS logout with listed/not login peer id
    Given peer id isn't invalid
    And sdk <has> login
    When sdk send logout request to ts
    Then response status_code should be 200
    And response error_code should be None
    And response data should be empty json
    And peer id isn't in database
    Examples: has or hasn't login
        |has    |
        |has    |
        |has not|


  @ts @logout @redis
  Scenario Outline: TS logout with invalid peer id
    Given peer id is <invalid>
    When sdk send logout request to ts
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    Examples: Invalid Peer ids
        |invalid                        |
        |HAVECHARS                      |
        |000000001234512345123451234    |
        |1234567890123456789012345678931|
        |1234567890123456789012345678932G|
        |123456789012345678901234567890133|
        |000000001234512345123451234AADBCFDABCDDADDD|

