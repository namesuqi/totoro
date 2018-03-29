Feature: channel server can return correct responses when received refreshchannel requests from peers

  @channel @refresh_channel
  Scenario Outline: channel server should return 200 and {} when sdk sends refreshchannel request after logining
    Given create and change to new peer_id
    When channel-srv receives refreshchannel request <without> channel_url
    Then response status_code should be 200
    And response data should be {}
    Examples:
        | without |
        | without |

  @channel @refresh_channel
  # 暂不考虑channel_url是否存在与redis
  Scenario Outline: channel server should return 200 and {} when sdk sends refreshchannel request with channel url
    Given create and change to new peer_id
    When channel-srv receives refreshchannel request <with> <channel_url>
    Then response status_code should be 200
    And response data should be {}
    Examples:
        | with | channel_url |
        | with |  http://c23.myccdn.info/e1edddbc239c069d8a2378d9bcd598d6/5b14e012/mp4/Avatar_20Mbps.mp4 |

  @channel @refresh_channel
  Scenario Outline: channel server should return 400 and error code when sdk sends refreshchannel request with invalid peer id
    Given peer id is <invalid>
    When channel-srv receives refreshchannel request <with> <channel_url>
    Then response status_code should be 400
    Then response error_code should be <error_code>
    Examples:
        | invalid | with | channel_url | error_code |
        | 2222222 | with | http://c23.myccdn.info/e1edddbc239c069d8a2378d9bcd598d6/5b14e012/mp4/Avatar_20Mbps.mp4| E_INVALID_PARAMS |
