# Created by liwenxuan at 2017/10/17
Feature: courier send download_tasks request to push-hub
  # As push-hub,
  # when I receive a valid download_tasks request,
  # I will add tasks to PSPFC_<push_id> in redis-single

  @push_hub @download_tasks @pspfc @valid
  Scenario: push-hub can add tasks to PSPFC in redis successfully
    Given prepare valid request body of download_tasks
    Given prepare a valid task for download_tasks, push_id is PUSH_ID
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"task_count":1,"success_count":1}
    Then there should be 1 tasks in PSPFC_PUSH_ID
    Then download_task in PSPFC_PUSH_ID should be correct

  @push_hub @download_tasks @pspfc @valid
  Scenario: push-hub should add tasks to the same PSPFC with different tasks belong to the same push_id
    Given prepare valid request body of download_tasks
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And add the task to download_tasks
    And create and change to new file_id
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"task_count":2,"success_count":2}
    And there should be 2 tasks in PSPFC_PUSH_ID
    And download_task in PSPFC_PUSH_ID should be correct

  @push_hub @download_tasks @pspfc @valid @clear_pspfc
  Scenario Outline: push-hub should add tasks to different PSPFC with tasks belong to different push_id
    Given clear PSPFC_<push_id>
    Given prepare valid request body of download_tasks
    Given prepare a valid task for download_tasks, push_id is PUSH_ID
    And add the task to download_tasks
    Given prepare a valid task for download_tasks, push_id is <push_id>
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"task_count":2,"success_count":2}
    Then there should be 1 tasks in PSPFC_PUSH_ID
    And there should be 1 tasks in PSPFC_<push_id>
    Then download_task in PSPFC_PUSH_ID should be correct
    And download_task in PSPFC_<push_id> should be correct
    Examples: another push_id
        | push_id           |
        | AA:AA:AA:AA:AA:AA |

  @push_hub @download_tasks @pspfc @valid
  Scenario: push-hub should add tasks to PSPFC with the same tasks (but redis will delete duplication)
    Given prepare valid request body of download_tasks
    Given prepare a valid task for download_tasks, push_id is PUSH_ID
    And add the task to download_tasks
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"task_count":2,"success_count":2}
    And there should be 1 tasks in PSPFC_PUSH_ID
    And download_task in PSPFC_PUSH_ID should be correct

  @push_hub @download_tasks @pspfc @valid
  Scenario: push-hub should add all tasks to PSPFC with many valid tasks
    Given prepare valid request body of download_tasks
    Given prepare a valid task for download_tasks, push_id is PUSH_ID
    And add 100 tasks to download_tasks with different file_id
    When push-hub receive the download_tasks request
    Then response status_code should be 200
    And response error_code should be None
    And response data should be {"task_count":100,"success_count":100}
    And there should be 100 tasks in PSPFC_PUSH_ID

  @push_hub @download_tasks @pspfc @invalid
  Scenario Outline: push-hub should not add any task to PSPFC with one valid task and one invalid task
    Given prepare valid request body of download_tasks
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And add the task to download_tasks
    And create and change to new file_id
    And prepare a valid task for download_tasks, push_id is PUSH_ID
    And set field <field> of task_info to <value> and type to <type>
    And add the task to download_tasks
    When push-hub receive the download_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should not add any task to PSPFC_PUSH_ID
    Examples: invalid field-value
        | field      | value | type   |
        | file_id    | 0     | int    |
        | file_url   | 0     | int    |
        | file_size  | ""    | object |
        | file_type  | ""    | object |
        | ppc        | ""    | object |
        | cppc       | ""    | object |
        | piece_size | ""    | object |
        | priority   | ""    | object |
        | push_id    | 0     | int    |
        | push_ip    | 0     | int    |



