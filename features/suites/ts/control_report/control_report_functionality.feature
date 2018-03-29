# Created by liwenxuan at 2017/10/11
@ts @report @control_report @functionality
Feature: report-srv received a valid control_report request
  # As report-srv,
  # when I receive a valid control_report request,
  # I will record control_msg in business.log (topic: vod_sdk_flow)

  @valid @pnic
  Scenario: control_report with seeds and channels
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid seed_info of control_report
    And add seed_info to control_report
    And prepare a valid channel_info of control_report
    And add channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}

  @valid @pnic
  Scenario: control_report with empty seeds
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid channel_info of control_report
    And add channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}

  @valid @pnic
  Scenario: control_report with empty channels
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid seed_info of control_report
    And add seed_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}

  @valid @pnic
  Scenario: control_report with empty seeds and empty channels
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of control_report with empty seeds and empty channels
    When report-srv receive the control_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}

  @invalid @pnic
  Scenario: control_report without login
    Given make sure that the peer_id is offline
    And prepare valid request body of control_report with empty seeds and empty channels
    When report-srv receive the control_report request
    Then response status_code should be 200
    And response error_code should be E_TS_NOT_LOGIN

  @valid @pnic
  Scenario: there are many records in channels
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid channel_info of control_report
    And add channel_info to control_report
    And create and change to new file_id
    And prepare a valid channel_info of control_report
    And add channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}

  @valid @pnic
  Scenario: there are many records in seeds
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid seed_info of control_report
    And add seed_info to control_report
    And create and change to new file_id
    And prepare a valid seed_info of control_report
    And add seed_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}

  @valid @pnic @large_number
  Scenario: there are over 3000 bytes in seeds
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid seed_info of control_report
    And add 100 seed_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}

  @valid @pnic @large_number
  Scenario: there are over 3000 bytes in channels
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid channel_info of control_report
    And add 100 channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}

  # valid value
  @valid @pnic
  Scenario Outline: the value of "type" in channels is valid
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid channel_info of control_report
    And modify the value of field "type" of channel_info to "<value>" and type to "str"
    And add channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}
    Examples: valid type
        | value      |
        | vod        |
        | download   |
        | hls        |
        | live_flv   |
        | live_m3u8  |
        | live_ts    |
        | push       |
        | vhls       |
        | xmtp       |

  @valid @pnic
  Scenario Outline: the value of "op" in channels is valid
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid channel_info of control_report
    And modify the value of field "op" of channel_info to "<value>" and type to "str"
    And add channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}
    Examples: valid op
        | value    |
        | add      |
        | del      |
        | playing  |

  @valid @pnic
  Scenario Outline: the value of "err_type" in channels is valid
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid channel_info of control_report
    And modify the value of field "err_type" of channel_info to "<value>" and type to "<type>"
    And add channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}
    Examples: valid err_type
        | value         | type   |
        | ""            | object |
        | E_DECODE_FAIL | str    |

  @valid @pnic
  Scenario Outline: the value of "p2penable" in channels is valid
    Given make sure that the peer_id is online, stun_ip is STUN_IP
    And prepare valid request body of control_report with empty seeds and empty channels
    And prepare a valid channel_info of control_report
    And modify the value of field "p2penable" of channel_info to "<value>" and type to "bool"
    And add channel_info to control_report
    When report-srv receive the control_report request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}
    Examples: valid err_type
        | value |
        | True  |
        | False |


