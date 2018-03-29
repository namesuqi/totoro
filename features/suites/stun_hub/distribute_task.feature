@stun_hub @distribute_task @functionality
Feature: courier send distribute_task request to stun-hub
  # As stun-hub,
  # when I receive a valid distribute_task request,
  # I will get stun_ip from PNIC_<peer_id> in redis-cluster (if the PNIC is not exist, I will ignore the task)
  # and then add tasks converged by peer_id to RRPC_<stun_ip> in redis-single (each peer_id corresponds to one rrpc_command)

  @valid @rrpc @pnic
  Scenario Outline: stun-hub should add rrpc_command to RRPC in redis with peer_id in PNIC
    Given prepare valid request body of distribute_task
    And prepare a valid task for distribute_task
    And make sure that the peer_id is online, stun_ip is STUN_IP
    And set field op of task_info to <valid_op> and type to str
    And add task_info to distribute_task
    When stun-hub receive the distribute_task request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"succ_task_count":1}
    And there should be 1 rrpc_commands in RRPC_STUN_IP
    And rrpc_command in RRPC_STUN_IP should be correct
    Examples: valid op
    | valid_op |
    | download |
    | delete   |

  @valid @rrpc @pnic
  Scenario Outline: stun-hub should ignore the task without peer_id in PNIC
    Given prepare valid request body of distribute_task
    And prepare a valid task for distribute_task
    And make sure that the peer_id is offline
    And set field op of task_info to <valid_op> and type to str
    And add task_info to distribute_task
    When stun-hub receive the distribute_task request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"succ_task_count":0}
    And there should be 0 rrpc_commands in RRPC_STUN_IP
    Examples: valid op
    | valid_op |
    | download |
    | delete   |

  @valid @rrpc @pnic
  Scenario: stun-hub should do nothing and work normally without task
    Given prepare valid request body of distribute_task
    When stun-hub receive the distribute_task request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"succ_task_count":0}

  @valid @rrpc @pnic
  Scenario: stun-hub should add rrpc_command to RRPC in redis when part of peer_ids is in PNIC and part is not in PNIC
    Given prepare valid request body of distribute_task
    And prepare a valid task for distribute_task
    And make sure that the peer_id is online, stun_ip is STUN_IP
    And add task_info to distribute_task
    And create and change to new peer_id
    And prepare a valid task for distribute_task
    And make sure that the peer_id is offline
    And add task_info to distribute_task
    When stun-hub receive the distribute_task request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"succ_task_count":1}
    And there should be 1 rrpc_commands in RRPC_STUN_IP
    And rrpc_command in RRPC_STUN_IP should be correct

  @valid @rrpc @pnic
  Scenario: stun-hub should add one rrpc_command to RRPC in redis with the same peer_id
    Given prepare valid request body of distribute_task
    And prepare a valid task for distribute_task
    And make sure that the peer_id is online, stun_ip is STUN_IP
    And add task_info to distribute_task
    And create and change to new file_id
    And prepare a valid task for distribute_task
    And add task_info to distribute_task
    When stun-hub receive the distribute_task request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"succ_task_count":2}
    And there should be 1 rrpc_commands in RRPC_STUN_IP
    And rrpc_command in RRPC_STUN_IP should be correct

  @valid @rrpc @pnic
  Scenario: stun-hub should add different rrpc_commands to RRPC in redis with different peer_id but the same stun_ip
    Given prepare valid request body of distribute_task
    And prepare a valid task for distribute_task
    And make sure that the peer_id is online, stun_ip is STUN_IP
    And add task_info to distribute_task
    And create and change to new peer_id
    And prepare a valid task for distribute_task
    And make sure that the peer_id is online, stun_ip is STUN_IP
    And add task_info to distribute_task
    When stun-hub receive the distribute_task request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"succ_task_count":2}
    And there should be 2 rrpc_commands in RRPC_STUN_IP
    And rrpc_command in RRPC_STUN_IP should be correct

  @valid @rrpc @pnic @clear_rrpc
  Scenario Outline: stun-hub should add rrpc_commands to different RRPC in redis with different peer_id and different stun_ip
    Given clear RRPC_<another_stun_ip>
    And prepare valid request body of distribute_task
    And prepare a valid task for distribute_task
    And make sure that the peer_id is online, stun_ip is STUN_IP
    And add task_info to distribute_task
    And create and change to new peer_id
    And prepare a valid task for distribute_task
    And make sure that the peer_id is online, stun_ip is <another_stun_ip>
    And add task_info to distribute_task
    When stun-hub receive the distribute_task request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"succ_task_count":2}
    And there should be 1 rrpc_commands in RRPC_STUN_IP
    And rrpc_command in RRPC_STUN_IP should be correct
    And there should be 1 rrpc_commands in RRPC_<another_stun_ip>
    And rrpc_command in RRPC_<another_stun_ip> should be correct
    Examples: another_stun_ip
    | another_stun_ip |
    | 192.168.9.9     |



#  @stun_hub @distribute_task
#  Scenario Outline: valid seed task
#    Given load defaults of peer_info
#    And there is <num> seed task
#    When send login request to ts-server
#    And send the task to stun-hub
#    Then response status_code should be 200
#    And the response task count is <num>
#    Examples:
#      | num |
#      | 1   |
#      | 2   |
#
#  @stun_hub @distribute_task
#  Scenario Outline: invalid seed task
#    Given load defaults of peer_info
#    And there is <num> invalid seed task
#    When send login request to ts-server
#    And send the task to stun-hub
#    Then response status_code should be 200
#    And the response task count is 0
#    Examples:
#      | num |
#      | 1   |
#      | 2   |
#
#  @stun_hub @distribute_task
#  Scenario Outline: valid and invalid seed task
#    Given load defaults of peer_info
#    And there is <num1> valid seed task <num2> invalid seed task
#    When send login request to ts-server
#    And send the task to stun-hub
#    Then response status_code should be 200
#    And the response task count is <num1>
#    Examples:
#      | num1 | num2 |
#      | 1    | 2    |
#      | 2    | 1    |


