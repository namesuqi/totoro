@stun_hub @get_lf_rrpc
Feature: stun-srv send get_lf_rrpc request to stun-hub
  # As stun-hub,
  # when I receive a valid get_lf_rrpc request,
  # I will return tasks_info in RRPC_<stun_ip> to requester (stun_ip equals to request_ip)
  # If there is no task in RRPC_<stun_ip>, I will wait for some time and then return empty tasks_info to requester

  @functionality @valid
  Scenario: stun-hub should return correct rrpc_command with one download_task in RRPC
    Given prepare an empty tasks_info
    And prepare a valid download_task for get_lf_rrpc
    And add the task to tasks_info
    Given add tasks_info to RRPC_STUN_IP converged by peer_id
    When stun-hub receive the get_lf_rrpc request
    Then response status_code should be 200
    And response error_code should be None
    And stun-hub should return correct rrpc_command
    Then stun-hub should delete the RRPC_STUN_IP

  @functionality @valid
  Scenario: stun-hub should return correct rrpc_command with one delete_task in RRPC
    Given prepare an empty tasks_info
    Given prepare a valid delete_task for get_lf_rrpc
    And add the task to tasks_info
    Given add tasks_info to RRPC_STUN_IP converged by peer_id
    When stun-hub receive the get_lf_rrpc request
    Then response status_code should be 200
    And response error_code should be None
    And stun-hub should return correct rrpc_command
    Then stun-hub should delete the RRPC_STUN_IP

  @functionality @valid
  Scenario: stun-hub should return correct rrpc_command with one rrpc_command in RRPC (both download_task and delete_task)
    Given prepare an empty tasks_info
    Given prepare a valid delete_task for get_lf_rrpc
    And add the task to tasks_info
    And prepare a valid download_task for get_lf_rrpc
    And add the task to tasks_info
    Given add tasks_info to RRPC_STUN_IP converged by peer_id
    When stun-hub receive the get_lf_rrpc request
    Then response status_code should be 200
    And response error_code should be None
    And stun-hub should return correct rrpc_command
    Then stun-hub should delete the RRPC_STUN_IP

  @functionality @valid
  Scenario: stun-hub should return correct rrpc_command with many rrpc_commands in RRPC
    Given prepare an empty tasks_info
    And prepare a valid delete_task for get_lf_rrpc
    And add the task to tasks_info
    And create and change to new peer_id
    And prepare a valid download_task for get_lf_rrpc
    And add the task to tasks_info
    And add tasks_info to RRPC_STUN_IP converged by peer_id
    When stun-hub receive the get_lf_rrpc request
    Then response status_code should be 200
    And response error_code should be None
    And stun-hub should return correct rrpc_command
    And stun-hub should delete the RRPC_STUN_IP



#@stun_hub @get_lf_rrpc @join_lf @redis
#Scenario Outline:reverse join LF request with legal peer ids
#    Given peer ids list is correct
#    And peer ids are <all> listed
#    And file url is correct
#    And file id is correct
#    When send join LF request
#    Then the response status code is 200
#    And the response error code is None
#    And the response data is <data>
#    Examples: if peer has login
#    |all    |data   |
#    |all    |{"useable_peer_count":3}|
#    |part   |{"useable_peer_count":2}|
#    |not    |{"useable_peer_count":0}|
#
#
#@stun_hub @get_lf_rrpc @join_lf @redis
#Scenario Outline:reverse join LF request with mixed illegal peer id or legal peer id
#    Given peer ids list is <mixed invalid peer id>
#    And file url is correct
#    And file id is correct
#    When send join Lf request
#    Then the response status code is 400
#    And the response error code is None
#    And the response data is None
#    Examples: invalid peer id
#    |mixed invalid peer id  |
#    |HAVECHARS                      |
#    |000000001234512345123451234    |
#    |1234567890123456789012345678931|
#    |1234567890123456789012345678932G|
#    |123456789012345678901234567890133|
#    |000000001234512345123451234AADBCFDABCDDADDD|
#
#
#@stun_hub @get_lf_rrpc @join_lf @redis
#Scenario Outline: reverse join LF request with correct peer id
#    Given peer id list is correct
#    And peer ids are <all> listed
#    And file id is correct
#    And file url is correct
#    When send join LF request
#    Then the response status code is 200
#    And the response error code is None
#    And the response data is <data>
#    Examples: if peer has login
#    |all    |data   |
#    |all    |{"useable_peer_count":1}|
#    |not    |{"useable_peer_count":0}|
#
#
#@stun_hub @get_lf_rrpc @join_lf @redis
#Scenario Outline: reverse join LF request with invalid peer id
#    Given peer id list is <invalid>
#    And file id is correct
#    And file url is correct
#    When send join LF request
#    Then the response status code is 400
#    And the response error code is None
#    And the response data is None
#    Examples: invalid peer id
#    |invalid    |
#    |missing    |
#    |HAVECHARS                      |
#    |000000001234512345123451234    |
#    |1234567890123456789012345678931|
#    |1234567890123456789012345678932G|
#    |123456789012345678901234567890133|
#    |000000001234512345123451234AADBCFDABCDDADDD|
#
#
#@stun_hub @get_lf_rrpc @join_lf @redis
#Scenario Outline: reverse join LF request with invalid file id
#    Given peer ids list is correct
#    And file id is <invalid>
#    And file url is correct
#    When send join LF request
#    Then the response status code is 400
#    And the response error code is None
#    And the response data is None
#    Examples: invalid file id
#    |invalid|
#    |missing|
#    |23DA046BD3E2F06367C159534CE88A4|
#    |23DA046BD3E2F06367C159534CE88A423|
#    |23DA046BD3E2F06367C159534CE88A4G|
#    |@$%!@#!@#%#@%@#$^#^@#$!@#@!#%!@#|
#
#
#@stun_hub @get_lf_rrpc @join_lf @redis
#Scenario Outline: reverse join LF request with file url which does not exist
#    Given peer ids list is correct
#    And file id is correct
#    And file url is <invalid>
#    When send join LF request
#    Then the response status code is <status code>
#    And the response error code is None
#    And the response data is <data>
#    Examples: invalid file url
#    |invalid|status code|data|
#    |http://flv.srs.cloutropy123.com/wasu/test.flv|200|{"useable_peer_count":0}|
#    |http://flv.srs.cloutropy123.com/wasu/test1234.flv|200|{"useable_peer_count":0}|
#    |  !@##$$# qsd @!@#$QWR |200|{"useable_peer_count":0}|
#    |missing|400|None|
#
#
#@stun_hub @get_lf_rrpc @leave_lf @redis
#Scenario Outline:reverse leave LF request with legal peer ids
#    Given peer ids list is correct
#    And peer ids are <all> listed
#    And file id is correct
#    When send leave LF request
#    Then the response status code is 200
#    And the response error code is None
#    And the response data is <data>
#    Examples: if peer has login
#    |all    |data   |
#    |all    |{"useable_peer_count":3}|
#    |part   |{"useable_peer_count":2}|
#    |not    |{"useable_peer_count":0}|
#
#
#@stun_hub @get_lf_rrpc @leave_lf @redis
#Scenario Outline:reverse leave LF request with mixed illegal peer id or legal peer id
#    Given peer ids list is <mixed invalid peer id>
#    And file id is correct
#    When send leave Lf request
#    Then the response status code is 400
#    And the response error code is None
#    And the response data is None
#    Examples: invalid peer id
#    |mixed invalid peer id          |
#    |HAVECHARS                      |
#    |000000001234512345123451234    |
#    |1234567890123456789012345678931|
#    |1234567890123456789012345678932G|
#    |123456789012345678901234567890133|
#    |000000001234512345123451234AADBCFDABCDDADDD|
#
#
#@stun_hub @get_lf_rrpc @leave_lf @redis
#Scenario Outline: reverse leave LF request with correct peer id
#    Given peer id list is correct
#    And peer ids are <all> listed
#    And file id is correct
#    When send leave LF request
#    Then the response status code is 200
#    And the response error code is None
#    And the response data is <data>
#    Examples: if peer has login
#    |all    |data   |
#    |all    |{"useable_peer_count":1}|
#    |not    |{"useable_peer_count":0}|
#
#
#@stun_hub @get_lf_rrpc @leave_lf @redis
#Scenario Outline: reverse leave LF request with invalid peer id
#    Given peer id list is <invalid>
#    And file id is correct
#    When send leave LF request
#    Then the response status code is 400
#    And the response error code is None
#    And the response data is None
#    Examples: invalid peer id
#    |invalid    |
#    |missing    |
#    |HAVECHARS                      |
#    |000000001234512345123451234    |
#    |1234567890123456789012345678931|
#    |1234567890123456789012345678932G|
#    |123456789012345678901234567890133|
#    |000000001234512345123451234AADBCFDABCDDADDD|
#
#
#@stun_hub @get_lf_rrpc @leave_lf @redis
#Scenario Outline: reverse leave LF request with invalid file id
#    Given peer ids list is correct
#    And file id is <invalid>
#    When send leave LF request
#    Then the response status code is 400
#    And the response error code is None
#    And the response data is None
#    Examples: invalid file id
#    |invalid|
#    |missing|
#    |23DA046BD3E2F06367C159534CE88A4|
#    |23DA046BD3E2F06367C159534CE88A423|
#    |23DA046BD3E2F06367C159534CE88A4G|
#    |@$%!@#!@#%#@%@#$^#^@#$!@#@!#%!@#|
#
#
#@stun_hub @get_lf_rrpc @rrpc @redis
#Scenario: stun hub return 200 and {} when rrpc_[stun ip] list is null
#    Given the rrpc list contains nothing
#    When send hub lf rrpc request
#    Then the response status code is 200
#    And the response error code is None
#    And the response data is empty json
#
#
#@stun_hub @get_lf_rrpc @rrpc @redis @draft
#Scenario Outline: stun hub return 200 and data when the rrpc list contains one oder and the oder contains one peer id
#    Given the oder contains <peer>
#    And the rrpc list contains <oder>
#    When send hub lf rrpc request
#    Then the response status code is 200
#    And the response error code is None
#    And the response data is <data>
#    Examples: rrpc list contains single oder
#    |   peer    |   oder            |   data    |
#    |single peer|one join LF oder   |empty json |
#    |multi peer |one join LF oder   |empty json |
#    |single peer|one leave LF oder  |empty json |
#    |multi peer |one leave LF oder  |empty json |
#
#    Examples: rrpc list contains multi oder
#    |   peer    |   oder                                |   data    |
#    |single peer|two join LF oder and one leave LF oder |empty json |
#    |multi peer |two join LF oder and one leave LF oder |empty json |
#
#
#@stun_hub @get_lf_rrpc @rrpc @redis @long_time
#Scenario: the timeout oder should not be received
#    Given the oder contains single peer
#    And the rrpc list contains one join LF oder
#    And wait 60 seconds
#    When send hub lf rrpc request
#    Then the response status code is 200
#    And the response error code is None
#    And the response data is empty json

