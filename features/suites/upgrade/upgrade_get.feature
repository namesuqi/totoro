# Created by liwenxuan at 2017/11/16
@upgrade @upgrade_get @functionality
Feature: upgrade-srv receive a valid upgrade_get request
  # As upgrade-srv,
  # when I receive a valid upgrade_get request,
  # I will return the correct version_url to requester if target_version in mongo_db

  @valid
  Scenario: get correct version_url from upgrade-srv with target_version in mongo_db
    # setup: target_verison 4.1.0 in mongo_db
    Given prepare a valid upgrade_get request
    When upgrade-srv receive the upgrade_get request
    Then response status_code should be 200
    And response error_code should be None
    And response data of upgrade_get should be correct

  @valid
  Scenario: missing optional fields
    Given prepare a valid upgrade_get request
    And delete field peerid of upgrade_get
    When upgrade-srv receive the upgrade_get request
    Then response status_code should be 200
    And response error_code should be None
    And response data of upgrade_get should be correct

  @invalid
  Scenario: get correct version_url from upgrade-srv without target_version in mongo_db
    # setup: target_verison 4.2.10 not in mongo_db
    Given prepare a valid upgrade_get request
    And modify the value of field "targetversion" of upgrade_get to "4.2.10" and type to "str"
    When upgrade-srv receive the upgrade_get request
    Then response status_code should be 200
    And response error_type of upgrade_get should be E_NO_APPLICATION_PACKET

