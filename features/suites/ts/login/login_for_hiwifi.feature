Feature: SDK for hiwifi login to Tracker Server

  @ts @login @redis @hiwifi @valid @etcd_user_p2p
  Scenario: SDK for hiwifi login with nat3 but PNIC in redis should be nat4
    Given load defaults of peer_info for hiwifi
    When send login request to ts-server
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"p2p_enable":true}
    And ts-srv should add the peer_info for hiwifi to PNIC correctly




