Feature: vod-push send register request to push-hub

  @push_hub @register @valid
  Scenario: push-hub should return request_ip with x-forwarded-for
    Given prepare valid request header of register, x-forwarded-for defaults to PUSH_IP
    When push-hub receive the register request
    Then response status_code should be 200
    And response error_code should be None
    And response data of register should be request_ip

  @push_hub @register @valid
  Scenario: push-hub should return source_ip without x-forwarded-for
    Given prepare valid request header of register, x-forwarded-for defaults to PUSH_IP
    And delete field x-forwarded-for of register_header
    When push-hub receive the register request
    Then response status_code should be 200
    And response error_code should be None
    And response data of register should be source_ip

