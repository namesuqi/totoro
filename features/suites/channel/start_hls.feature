Feature: channel server can return correct responses when received starthls requests from peers

  @channel @start_hls
  Scenario Outline: channel server should return 200 and error info when sdk sends starthls request of MasterPlaylist
    Given create and change to new peer_id
    When channel-srv receives starthls request with master playlist
    Then response status_code should be 200
    And response error_code should be <error_code>
    Examples:
        | error_code |
        | E_OK|

  @channel @start_hls
  Scenario: channel server should return 200 and file info when sdk sends starthls request of MediaPlaylist
    Given create and change to new peer_id
    When channel-srv receives starthls request with media playlist
    Then response status_code should be 200
    And response of starthls request should be correct

  @channel @start_hls
  Scenario Outline: channel server should return 400 when sdk sends starthls with invalid peer id
    Given peer id is <invalid>
    When channel-srv receives starthls request with <different> playlist
    Then response status_code should be 400
    And response error_code should be None
    Examples:
        | invalid | different |
        | 2222222 | master    |
        | 00010023AAAAAAAAAA| media |

  @channel @start_hls
  Scenario: channel server should return 400 when sdk sends starthls with void url
    Given create and change to new peer_id
    When channel-srv receives starthls request with void playlist
    Then response status_code should be 400
    And response error_code should be None

  @channel @start_hls
  Scenario Outline: channel server should return 200 and error info when sdk sends starthls request with invalid url_prefix
    Given create and change to new peer_id
    When channel-srv receives starthls request with invalid <url_prefix>
    Then response status_code should be 200
    And response error_code should be <error_code>
    Examples:
        | url_prefix | error_code |
        |yunshangss.cloutropy.com | E_AUTH_FAILED |


