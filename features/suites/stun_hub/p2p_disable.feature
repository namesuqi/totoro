@stun_hub @p2p_disable @functionality
Feature: ops send p2p_disable request to stun-hub
  # As stun-hub,
  # when I receive a valid p2p_disable request,
  # I will get stun_ip from PNIC_<peer_id> in redis-cluster (if the PNIC is not exist, I will ignore the task)
  # and then add tasks converged by peer_id to RRPC_<stun_ip> in redis-single (each peer_id corresponds to one rrpc_command)

  @valid @pnic @rrpc
  Scenario: stun-hub should add rrpc_command to RRPC in redis with peer_id in PNIC
    Given prepare valid request body of p2p_disable
    And make sure that the peer_id is online, stun_ip is STUN_IP
    And add a valid peer_id to p2p_disable
    When stun-hub receive the p2p_disable request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}
    And there should be 1 p2p_disable in RRPC_STUN_IP
    And rrpc_command about p2p_disable in RRPC_STUN_IP should be correct

  @valid @rrpc @pnic
  Scenario: stun-hub should add rrpc_command to RRPC in redis with peer_id in PNIC
    Given prepare valid request body of p2p_disable
    And make sure that the peer_id is online, stun_ip is STUN_IP
    And add a valid peer_id to p2p_disable
    And create and change to new peer_id
    And make sure that the peer_id is online, stun_ip is STUN_IP
    And add a valid peer_id to p2p_disable
    When stun-hub receive the p2p_disable request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}
    And there should be 1 p2p_disable in RRPC_STUN_IP
    And rrpc_command about p2p_disable in RRPC_STUN_IP should be correct

  @valid @rrpc @pnic @clear_rrpc
  Scenario Outline: stun-hub should add p2p_disable to different RRPC in redis with different peer_id and different stun_ip
    Given clear RRPC_<another_stun_ip>
    And prepare valid request body of p2p_disable
    And make sure that the peer_id is online, stun_ip is STUN_IP
    And add a valid peer_id to p2p_disable
    And create and change to new peer_id
    And make sure that the peer_id is online, stun_ip is <another_stun_ip>
    And add a valid peer_id to p2p_disable
    When stun-hub receive the p2p_disable request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {}
    And there should be 1 p2p_disable in RRPC_STUN_IP
    And rrpc_command about p2p_disable in RRPC_STUN_IP should be correct
    And there should be 1 p2p_disable in RRPC_<another_stun_ip>
    And rrpc_command about p2p_disable in RRPC_<another_stun_ip> should be correct
    Examples: another_stun_ip
        | another_stun_ip |
        | 192.168.9.9     |