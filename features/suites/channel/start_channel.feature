Feature: SDK start channel from Channel Server
    SDK send get request to Channel server for file information

  @channel @start_channel
  Scenario Outline: the peer can start channel with correct user and available file url
    Given peer id <belongs> to <user>
    And sdk <has> login
    And play user is <user>
    And file url <belongs> to <user>
    When sdk send start channel request
    Then response status_code should be 200
    Then response should be correct
#    And  the file info of response is equal to the file info of database
    Examples: has login
        |belongs|user|has|
        |belongs|demo|has|
        |belongs|demo|has not|


  @channel @start_channel
  Scenario Outline: the peer start channel with unmatched file url
    Given peer id <belongs> to <user>
    And sdk <has> login
    And play user is <user>
    And file url <doesn't belongs> to <user>
    When sdk send start channel request
    Then response status_code should be 200
    And response error_code should be E_AUTH_FAILED
    Examples: belongs to user
        |belongs|user|doesn't belongs|has|
        |belongs|demo|doesn't belongs|has|
        |belongs|demo|doesn't belongs|has not|

  @channel @start_channel
  Scenario Outline: SDK start channel with invalid peer id
    Given peer id is <invalid>
    And play user is demo
    And file url belongs to demo
    When sdk send start channel request
    Then response status_code should be 400
    And response error_code should be None
#    And the response data is None
    Examples: Invalid Peer ids
        |invalid|
        |HAVECHARS|
        |000000001234512345123451234|
        |1234567890123456789012345678931|
        |1234567890123456789012345678932G|
        |123456789012345678901234567890133|
        |000000001234512345123451234AADBCFDABCDDADDD|


  @channel @start_channel
  Scenario Outline: the peer start channel with unmatched user
    Given peer id <doesn't belongs> to <user>
    And sdk <has> login
    And play user is <user>
    And file url <belongs> to <user>
    When sdk send start channel request
    Then response status_code should be 200
#    And the response error code is E_AUTH_FAILED
    Examples: belongs to user
        |doesn't belongs|user|belongs|has|
        |doesn't belongs|demo|belongs|has|
        |doesn't belongs|demo|belongs|has not|



