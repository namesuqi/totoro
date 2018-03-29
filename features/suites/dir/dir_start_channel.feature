# Created by liwenxuan at 2017/10/26
@dir @dir_start_channel @functionality @mysql_config_for_dir
Feature: vod-channel send dir_start_channel request to dir
  # As dir,
  # when I receive a valid dir_start_channel request,
  # I will return file_info such as file_id to requester.
  # If request url is in MySQL, I will return file_info directly.
  # If request url is not in MySQL but exist and domain in request url matches request user, I will create new file_info for the url and then return file_info

  @valid
  Scenario Outline: dir should return correct file_info to vod-channel with url in MySQL
    Given make sure that url '<url>' is in table_files in MySQL
    And prepare valid request body of dir_start_channel
    And set field user of dir_start_channel to <user> and type to str
    And set field url of dir_start_channel to <url> and type to str
    When dir receive dir_start_channel request
    Then response status_code should be 200
    And response error_code should be None
    And response data of dir_start_channel should be consistent with file_info in MySQL
    Examples: matched (user, url)
        | user      | url                                                    |
        | cloutropy | http://yunshang.cloutropy.com/demo/low/Ocean_2mbps.ts  |

  @valid
  Scenario Outline: dir should return correct file_info to vod-channel when url is in MySQL but doesn't match request user
    Given make sure that url '<url>' is in table_files in MySQL
    And prepare valid request body of dir_start_channel
    And set field user of dir_start_channel to <user> and type to str
    And set field url of dir_start_channel to <url> and type to str
    When dir receive dir_start_channel request
    Then response status_code should be 200
    And response error_code should be None
    And response data of dir_start_channel should be consistent with file_info in MySQL
    Examples: mismatched (user, url)
        | user      | url                                                    |
        | crazycdn  | http://yunshang.cloutropy.com/demo/low/Ocean_2mbps.ts  |

  @valid
  Scenario Outline: dir should register file_info to MySQL when url is not in MySQL but exist and domain in request url matches request user
    Given make sure that url '<url>' is not in table_files in MySQL
    And prepare valid request body of dir_start_channel
    And set field user of dir_start_channel to <user> and type to str
    And set field url of dir_start_channel to <url> and type to str
    When dir receive dir_start_channel request
    Then response status_code should be 200
    And response error_type of dir_start_channel should be None, sometimes E_REGISTERING
    And response data of dir_start_channel should be consistent with file_info in MySQL
    Then dir should add the file_info to table_files in MySQL
    Examples: matched (user, url)
        | user      | url                                                    |
        | cloutropy | http://yunshang.cloutropy.com/demo/low/Ocean_2mbps.ts  |

  @invalid
  Scenario Outline: dir should not add file_info to MySQL when url is not in MySQL but exist and domain in request url doesn't match request user
    Given make sure that url '<url>' is not in table_files in MySQL
    And prepare valid request body of dir_start_channel
    And set field user of dir_start_channel to <user> and type to str
    And set field url of dir_start_channel to <url> and type to str
    When dir receive dir_start_channel request
    Then response status_code should be 200
    And response error_type of dir_start_channel should be E_INVALID_URL_PREFIX, sometimes E_REGISTERING
    Then dir should not add the file_info to table_files in MySQL
    Examples: mismatched (user, url)
        | user      | url                                                    |
        | crazycdn  | http://yunshang.cloutropy.com/demo/low/Ocean_2mbps.ts  |

  @invalid
  Scenario Outline: dir should not add file_info to MySQL when domain in request url is not in MySQL
    Given make sure that url '<url>' is not in table_files in MySQL
    And prepare valid request body of dir_start_channel
    And set field user of dir_start_channel to <user> and type to str
    And set field url of dir_start_channel to <url> and type to str
    When dir receive dir_start_channel request
    Then response status_code should be 200
    And response error_code should be E_UNREGISTERED_URL_PREFIX
#    And response error_type of dir_start_channel should be E_UNREGISTERED_URL_PREFIX, sometimes E_REGISTERING
    Then dir should not add the file_info to table_files in MySQL
    Examples: invalid domain
        | user      | url                                                    |
        | cloutropy | http://test.test.test/auto/test                        |

  @invalid
  Scenario Outline: dir should not add file_info to MySQL when url is not exist
    Given make sure that url '<url>' is not in table_files in MySQL
    And prepare valid request body of dir_start_channel
    And set field user of dir_start_channel to <user> and type to str
    And set field url of dir_start_channel to <url> and type to str
    When dir receive dir_start_channel request
    Then response status_code should be 200
    And response error_code should be E_INVALID_URL
    Then dir should not add the file_info to table_files in MySQL
    Examples: invalid url
        | user      | url                                                    |
        | cloutropy | http://yunshang.cloutropy.com/auto/test/test.ts        |

  @invalid
  Scenario Outline: dir should not add file_info to MySQL when both user and url are not in MySQL
    Given make sure that url '<url>' is not in table_files in MySQL
    And make sure that user '<user>' is not in table_users in MySQL
    And prepare valid request body of dir_start_channel
    And set field user of dir_start_channel to <user> and type to str
    And set field url of dir_start_channel to <url> and type to str
    When dir receive dir_start_channel request
    Then response status_code should be 200
    And response error_type of dir_start_channel should be E_INVALID_USERNAME, sometimes E_REGISTERING
    Then dir should not add the file_info to table_files in MySQL
    Examples: invalid user
        | user      | url                                                    |
        | auto_test | http://yunshang.cloutropy.com/demo/low/Ocean_2mbps.ts  |

