# Created by liwenxuan at 2017/10/9
@ts @report @lsm_report @functionality
Feature: report-srv received a valid lsm_report request
  #  As report-srv,
  #  When I receive a valid lsm_report request,
  #  I will record the lsm_msg in business.log (topic: vod_sdk_lsm & vod_sdk_file_status)

  @valid @pnic
  Scenario: lsm_report with files
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of lsm_report with empty files
    And prepare a valid file_info of lsm_report
    And add file_info to lsm_report
    When report-srv receive the lsm_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}

  @valid @pnic
  Scenario: lsm_report with empty files
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of lsm_report with empty files
    When report-srv receive the lsm_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}

  @invalid @pnic
  Scenario: lsm_report without login
    Given make sure that the peer_id is offline
    And prepare valid request body of lsm_report with empty files
    When report-srv receive the lsm_report request
    Then response status_code should be 200
    And response error_code should be E_TS_NOT_LOGIN

  @valid @pnic
  Scenario: there are many records in files
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of lsm_report with empty files
    And prepare a valid file_info of lsm_report
    And add file_info to lsm_report
    And create and change to new file_id
    And prepare a valid file_info of lsm_report
    And add file_info to lsm_report
    When report-srv receive the lsm_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}

  @valid @pnic
  Scenario Outline: the value of "universe" is valid
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of lsm_report with empty files
    And modify the value of field "universe" of lsm_report to "<value>" and type to "bool"
    When report-srv receive the lsm_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}
    Examples: valid stat
    | value   |
    | True    |
    | False   |

  @valid @pnic
  Scenario Outline: the value of "stat" in files is valid
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of lsm_report with empty files
    And prepare a valid file_info of lsm_report
    And modify the value of field "stat" of file_info to "<value>" and type to "str"
    And add file_info to lsm_report
    When report-srv receive the lsm_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}
    Examples: valid stat
        | value       |
        | downloading |
        | done        |
        | waiting     |
        | interrupt   |
        | deleted     |


