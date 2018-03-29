Feature: channel server can return correct responses when received stopchannel requests from peers

  @channel @stop_channel
  # 暂不考虑channel_url是否存在与redis
  Scenario Outline: channel server should return 200 and {} when sdk sends stopchannel request with channel url
    Given create and change to new peer_id
    When channel-srv receives stopchannel request <with> <channel_url>
    Then response status_code should be 200
    And response data should be {}
    Examples:
        | with | channel_url |
        | with |  http://c23.myccdn.info/076c9b0081204412b0346d9beb486923/5abc4f25/mp4/Ocean_2mbps.ts |