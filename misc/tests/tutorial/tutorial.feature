Feature: showing off behave

  Scenario: run a simple test
    Given we have behave installed
  when we implement a test
  then behave will test it for us!

  @test
  Scenario Outline: test2
    Given test params type <number>, <number2>
    Then assert int <number>, and string <number2>

    Examples:
      | number | number2 |
      | 10     | 30      |
      | 20     | 40      |
