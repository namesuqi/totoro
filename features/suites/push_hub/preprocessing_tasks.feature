# Created by liwenxuan at 2017/10/17
Feature: vod-push send preprocessing_tasks request to push-hub
  # As push-hub,
  # when I receive a valid preprocessing_tasks request,
  # I will return valid tasks (ttl=3min) in PSPFC which belongs to request push_id to requester
  # Then I will delete the PSPFC

  @push_hub @preprocessing_tasks @pspfc @valid
  Scenario: push-hub should return the download_task to vod-push with one download_task in PSPFC
    Given prepare valid request body of preprocessing_tasks, push_id defaults to PUSH_ID
    Given prepare a valid download_task
    And add task_info to PSPFC_PUSH_ID and set score to localtime+0s
    When push-hub receive the preprocessing_tasks request
    Then response status_code should be 200
    And response error_code should be None
    And response data of preprocessing_tasks should be all valid tasks in PSPFC_PUSH_ID
    Then push-hub should delete PSPFC_PUSH_ID

  @push_hub @preprocessing_tasks @pspfc @valid
  Scenario: push-hub should return the delete_task to vod-push with one delete_task in PSPFC
    Given prepare valid request body of preprocessing_tasks, push_id defaults to PUSH_ID
    Given prepare a valid delete_task
    And add task_info to PSPFC_PUSH_ID and set score to localtime+0s
    When push-hub receive the preprocessing_tasks request
    Then response status_code should be 200
    And response error_code should be None
    And response data of preprocessing_tasks should be all valid tasks in PSPFC_PUSH_ID
    Then push-hub should delete PSPFC_PUSH_ID

  @push_hub @preprocessing_tasks @pspfc @valid
  Scenario: push-hub should return tasks to vod-push with both download_task and delete_task in PSPFC
    Given prepare valid request body of preprocessing_tasks, push_id defaults to PUSH_ID
    Given prepare a valid download_task
    And add task_info to PSPFC_PUSH_ID and set score to localtime+0s
    Given prepare a valid delete_task
    And add task_info to PSPFC_PUSH_ID and set score to localtime+0s
    When push-hub receive the preprocessing_tasks request
    Then response status_code should be 200
    And response error_code should be None
    And response data of preprocessing_tasks should be all valid tasks in PSPFC_PUSH_ID
    Then push-hub should delete PSPFC_PUSH_ID

  @push_hub @preprocessing_tasks @pspfc @valid
  Scenario: push-hub should return no task to vod-push with expired download_task in PSPFC
    Given prepare valid request body of preprocessing_tasks, push_id defaults to PUSH_ID
    Given prepare a valid download_task
    And add task_info to PSPFC_PUSH_ID and set score to localtime-180s
    When push-hub receive the preprocessing_tasks request
    Then response status_code should be 200
    And response error_code should be None
    And response data of preprocessing_tasks should be all valid tasks in PSPFC_PUSH_ID
    Then push-hub should delete PSPFC_PUSH_ID

  @push_hub @preprocessing_tasks @pspfc @valid
  Scenario: push-hub should return no task to vod-push with expired delete_task in PSPFC
    Given prepare valid request body of preprocessing_tasks, push_id defaults to PUSH_ID
    Given prepare a valid delete_task
    And add task_info to PSPFC_PUSH_ID and set score to localtime-180s
    When push-hub receive the preprocessing_tasks request
    Then response status_code should be 200
    And response error_code should be None
    And response data of preprocessing_tasks should be all valid tasks in PSPFC_PUSH_ID
    Then push-hub should delete PSPFC_PUSH_ID

  @push_hub @preprocessing_tasks @pspfc @valid
  Scenario: push-hub should return valid tasks to vod-push with both valid tasks and expired tasks in PSPFC
    Given prepare valid request body of preprocessing_tasks, push_id defaults to PUSH_ID
    And prepare a valid download_task
    And add task_info to PSPFC_PUSH_ID and set score to localtime-180s
    And create and change to new file_id
    And prepare a valid download_task
    And add task_info to PSPFC_PUSH_ID and set score to localtime-0s
    And create and change to new file_id
    And prepare a valid delete_task
    And add task_info to PSPFC_PUSH_ID and set score to localtime-0s
    And create and change to new file_id
    And prepare a valid delete_task
    And add task_info to PSPFC_PUSH_ID and set score to localtime-180s
    When push-hub receive the preprocessing_tasks request
    Then response status_code should be 200
    And response error_code should be None
    And response data of preprocessing_tasks should be all valid tasks in PSPFC_PUSH_ID
    And push-hub should delete PSPFC_PUSH_ID

  @push_hub @preprocessing_tasks @pspfc @invalid
  Scenario: push-hub should not return any task_info to vod-push when missing param id
    Given prepare valid request body of preprocessing_tasks, push_id defaults to PUSH_ID
    And delete field id of preprocessing_tasks
    And prepare a valid delete_task
    And add task_info to PSPFC_PUSH_ID and set score to localtime-0s
    When push-hub receive the preprocessing_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should do nothing to the PSPFC

  @push_hub @preprocessing_tasks @pspfc @invalid
  Scenario: push-hub should not return any task_info to vod-push when param id is ""
    Given prepare valid request body of preprocessing_tasks, push_id defaults to PUSH_ID
    And set field id of preprocessing_tasks to "" and type to object
    And prepare a valid delete_task
    And add task_info to PSPFC_PUSH_ID and set score to localtime-0s
    When push-hub receive the preprocessing_tasks request
    Then response status_code should be 400
    And response error_code should be None
    And response data should be None
    And push-hub should do nothing to the PSPFC

