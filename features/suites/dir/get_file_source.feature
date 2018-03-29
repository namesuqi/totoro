# Created by liwenxuan at 2017/10/31
@dir @get_file_source @mysql_config_for_dir
Feature: vod-channel send get_file_source request to dir
  # As dir,
  # when I receive a valid get_file_source request,
  # I will return file_info such as file_url to requester if request file_id is in MySQL

  @functionality @valid
  Scenario: dir should return correct file_info to vod-channel with file_id in MySQL
    Given make sure that the file_id is in table_files in MySQL
    Given prepare valid request body of get_file_source
    When dir receive get_file_source request
    Then response status_code should be 200
    And response error_code should be None
    And response data of get_file_source should be consistent with file_info in MySQL
    And make sure that the file_id is in table_files in MySQL

  @functionality @invalid @tang_test
  Scenario: dir should not return file_info to vod-channel without file_id in MySQL
    Given make sure that the file_id is not in table_files in MySQL
    Given prepare valid request body of get_file_source
    When dir receive get_file_source request
    Then response status_code should be 200
    And response error_code should be E_FILE_NON_EXISTS

  @robustness @invalid
  Scenario: dir should not return file_info to vod-channel with empty file_id
    Given prepare valid request body of get_file_source
    And set field file_id of get_file_source to "" and type to object
    When dir receive get_file_source request
    Then response status_code should be 200
    And response error_code should be E_PARAM_MISSING

  @robustness @invalid
  Scenario: dir should not return file_info to vod-channel when missing param file_id
    Given prepare valid request body of get_file_source
    And delete field file_id of get_file_source
    When dir receive get_file_source request
    Then response status_code should be 200
    And response error_code should be E_PARAM_MISSING

  @robustness @invalid
  Scenario Outline: dir should not return file_info to vod-channel with invalid file_id
    Given prepare valid request body of get_file_source
    And set field file_id of get_file_source to <value> and type to str
    When dir receive get_file_source request
    Then response status_code should be 200
    And response error_code should be E_PARAM_FORMAT_INCORRECT
    Examples: not hexadecimal 32 bytes
        | value                                       |
        | a                                           |
        | 00000000123451234512345                     |
        | 1234567890123456789012345678931             |
        | 1234567890123456789012345678932G            |
        | 123456789012345678901234567890133           |
        | 000000001234512345123451234AADBCFDABCDDADDD |
        | ********************************            |



