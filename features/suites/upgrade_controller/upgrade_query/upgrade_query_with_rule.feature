# Created by liwenxuan at 2017/11/14
@upgrade_controller @upgrade_query @functionality @with_rule
Feature: upgrade-controller received a valid upgrade_query request with rules in upgrade_controller
  # As upgrade_controller,
  # when I receive a valid upgrade_query request,
  # I should return the correct upgrade_version to requester

  Background: there is a rule valid for all in upgrade_controller
    Given make sure that there is a rule valid for all in upgrade_controller

  @valid
  Scenario: SDK do not have core and field "is_basic" is "true"
    Given prepare a valid upgrade_query request without core
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 200
    And response error_code should be None
    And upgrade_query response should be "{"target_version": TARGET_VERSION}"

  @invalid
  Scenario: SDK do not have core but field "is_basic" is "false"
    Given prepare a valid upgrade_query request without core
    And modify the value of field "is_basic" of upgrade_query to "false" and type to "str"
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None

  @valid
  Scenario: SDK have core and nat_detect successfully
    Given prepare a valid upgrade_query request with core and success of nat_detect
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 200
    And response error_code should be None
    And upgrade_query response should be "{"target_version": TARGET_VERSION}"

  @valid
  Scenario: SDK have core but fail to nat_detect
    Given prepare a valid upgrade_query request with core and failure of nat_detect
    When upgrade_controller receive the upgrade_query request
    Then response status_code should be 200
    And response error_code should be None
    And upgrade_query response should be "{"target_version": TARGET_VERSION}"

