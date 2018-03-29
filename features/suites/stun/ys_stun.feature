Feature: stun server support nat type detect

  @stun2_udp
  Scenario: correct steps get correct response
    Given stun is ready
    When peer send step 1 to stun port 9000
    Then response step is 1 or 3
    And response port is 60000
    When peer send step 2 to stun port 9002
    Then response step is 2 or 4
    And response port is 60000

  @stun2_udp
  Scenario Outline: long step data get none response
    Given stun is ready
    When peer send step 0001 to stun port <port>
    Then response is None
    Examples:
        |port|
        |9000|
        |9002|

  @stun2_udp @debug
  Scenario Outline: short step data get none response
    Given stun is ready
    When peer send short step to stun port <port>
    Then response is None
    Examples:
        |port|
        |9000|
        |9002|





#    @stun_udp
#Scenario: wrong step get none response
#    Given stun is ready
#    When peer send step 3 to stun port 9002
#    Then port 9002 response is None