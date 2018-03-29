### BDD in behave 规范文档:
- feature:描述一个需求/功能
- scenario:将feature拆分成多个story，scenario描述单个story
- examples:说明了一个feature是如何工作的
- environment.py:设置执行feature/step/scenario的前置条件与后置条件

### 一个不带examples的.feature文件格式如下：
```
@tag_1
Feature: illustrate the functionality/requirement,show the business goals

  Background:
    Given do before each scenario

  @tag_2@tag_3(tag_2,tag_3继承tag_1)
  Scenario: buy a Iphone
    Given i prepare $100
    When i give it to the salesman
    Then he gives me the iphone
```
### 一个带examples的.feature文件格式如下：
```
@tag_1
Feature: illustrate the functionality/requirement,show the business goals

  Background:
    Given do before each scenario

  @tag_2@tag_3(tag_2,tag_3继承tag_1)
  Scenario Outline: buy a Iphone
    Given i prepare $<money>
    When i give it to the salesman
    Then he gives me <thing>
    Examples:
        | money | thing |
        | 100 | phone |
```
### 格式要求
- 1.首行为tag_1,缩进为0
- 2.Feature紧接tag_1换行，缩进为0
- 3.Background必须在Feature之后且在Scenario之前
- 4.一个feature文件最多只能有一个Background
- 5.Scenario与Background皆为2个空格缩进
- 6.Given,When,Then,And,But皆为4个空格缩进

### Scenario 与Scenario Outline
- 1.若使用Examples，使用Scenario Outline
- 2.若无Examples，使用Scenario

### Background编写原则
- 1.单个feature文件中各个scenario都需要的number
- 2.单个feature文件中各个scenario都需要执行的step

### 重复Given/When/Then使用原则
- 1.当有重复的Given，When，Then，可用And及But代替后续Given，When，Then
- 2.若仅为多个并列条件/执行/结果，用And
- 3.若存在“强调”“但是”“只是”等含义，用But

### test fixture(即指定测试执行所需要的固定环境)
- 通过tag指定要运行的Scenarios
- 通过tag指定测试执行所需要的固定环境(environment.py为具体实现)
-   1.在每个step执行前/后执行：before_step(context, step)/after_step(context, step)
-   2.在每个Scenario执行前/后执行：before_scenario(context, scenario)/after_scenario(context, scenario)
-   3.在每个feature执行前/后执行：before_feature(context, feature)/after_feature(context, feature)
-   4.在指定tag的Scenario执行前/后执行：before_tag(context, tag)/after_tag(context, tag)

### tag标记原则
- 1.多个feature共同使用的tag名放在feature文件的首行(即tag_1位置)
- 2.每个feature根据具体接口使用tag_2(即tag_2位置)
- 3.若单个scenario需要setup/cleanup或tearup/teardown使用tag3（即tag_3位置)
- 4.environment.py用来存放tag指定环境的实现方法

### 不同Scenarios或者feature重复调用相同函数解决办法
- 现象一：同个server目录下多个feature出现相同函数
- 方案：每个feature/suites/<server_name>目录下存放一个common.py
- 现象二：多个steps为同一个方法且关键字相同<br />
        @Given('a is b')<br />
        @Given('we know a is the same with b')
- 方案：加强业务需求描述能力，且可以通过表格传参或使用examples等形式使scenario能够明确表达需求
- 现象三：一个step即是when又是then<br />
        @Given('a is b')<br />
        @When('a is b')
- 方案：
- 1.与server相关的step尽量写入对应server下的common.py
- 2.引入background的使用，避免重复的steps
- 3.类似的scenario可合并为一个通用模板
- 4.明确业务目标，scenario拆分合理

### 接口用例编码规范
- 1.response的状态码及错误码写在/totoro/features/steps/common.py目录下
- 2.scenario中的状态码及错误码的step标题不省略<>
- 3.在每个.feature文件的background中准备合法与非法的两组数据，如用户信息/peer_id/url
- 4.如果存在多个given，若皆为合法及正确的条件，用and连接
- 5.如果存在多个given且存在合法与非法的条件，用but连接
- 6.steps标题的主语应一致，不应出现无主语或一个scenario存在多个主语的情况
- 7.when应该表述接口主要的行为（如发登录请求、起播请求），而不是表述人们（测试人员）自己做的操作
- 8.一个scenario的tag数不宜超过3个
- 9.scenario的step操作不应含数据库操作（添加数据及清除数据等）
- 10.总common.Py函数范围：1.url参数设置 2.公用数据准备 3.待完善......

### start_channel接口示例
```
@channel_srv
Feature: channel server should response correct info when user starts channel

  @start_channel@url_register
  Scenario Outline: channel-srv should register the url info when user play the video the first time
    Given user is valid
    And peer_id belongs to the user
    And channel_url is valid
    When he plays the video firstly
    Then response status_code should be <number>
    And response error_code should be <error_code>
    Examples:
        | number | error_code |
        | 200 | ok |
```