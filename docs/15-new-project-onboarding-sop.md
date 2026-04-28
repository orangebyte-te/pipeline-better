# pipeline-better 新项目接入 SOP

这份文档用于指导一个“新的业务项目”接入 `pipeline-better`。

目标：
- 不只是知道要 include 什么文件
- 而是从接入前检查、模板选择、变量配置、灰度验证到回滚，都给出一条可执行路径

适用范围：
- 后端 Java 项目
- 前端项目
- Maven 多模块发布项目

---

# 一、接入前先判断项目属于哪一类

在接入前，先判断你的项目属于哪种流水线：

## 1）后端项目
通常满足这些特征：
- 有 `pom.xml`
- 需要 `mvn clean package`
- 需要构建 jar
- 需要构建 Docker 镜像
- 需要更新 yaml-config

推荐入口目录：
- `variables/`

## 2）前端项目
通常满足这些特征：
- 有 `package.json`
- 需要 `yarn install`
- 需要 `yarn build:*`
- 需要 nginx Dockerfile
- 有普通站点或子路径站点两种模式

推荐入口目录：
- `front/`

## 3）Maven 发布项目
通常满足这些特征：
- 主要是把模块 publish 到 Maven 仓库
- 不一定构建 Docker 镜像
- 常见为多模块/协议仓库

推荐入口目录：
- `mvn-push/`

如果项目类型判断错了，后面的变量配置基本都会错。

---

# 二、接入前置检查

无论是哪类项目，先检查下面这些前置条件。

## 1）模板仓库是否可访问
业务仓库最终会引用：
- `project: "devops/pipeline-better"`
- `ref: main`

需要确认：
- 业务项目所在组有权限读取 `devops/pipeline-better`
- 业务仓库的 pipeline 可以 include 这个仓库

## 2）Job Token 跨项目读取权限是否已放开
当前模板会通过 GitLab API 下载：
- Dockerfile
- Sonar 通知脚本
- 前端 nginx 配置

所以要确认：
- `CI_JOB_TOKEN` 是否可以读取 `devops/pipeline-better` 的 raw file / repository file API

如果这一步没打通，`prepare_dockerfile`、前端配置下载、Sonar 通知脚本下载都会失败。

## 3）Runner 是否准备好
至少确认 workflow 当前注入的 runner tag 对应 runner 已经在线：
- 当前验证通过的值是 `RUNNER_TAG=dev-runner-k8s-ali`
- 如果未来改回变量化控制，再补 `RUNNER_TAG_*` 变量

## 4）外部依赖是否准备好
按项目类型检查：

后端建议确认：
- Harbor 可推送
- Sonar 可访问
- yaml-config 仓库可 clone / push
- 钉钉 webhook 可用

前端建议确认：
- Harbor 可推送
- yaml-config 仓库可 clone / push
- 如需通知，钉钉 webhook 可用

Maven 发布建议确认：
- Maven 私服可 deploy
- runner 网络能访问 Maven 私服

---

# 三、需要预先配置的 GitLab CI/CD Variables

## 1）后端项目至少建议有
- `DINGTALK_WEBHOOK`
- `YAML_CONFIG_REPO_HTTP`
- `YAML_CONFIG_REPO_TOKEN`
- `YAML_CONFIG_REPO_BRANCH`（建议显式配成 `release`）
- `REGISTRY`（可选，默认 harbor.insgeek.cn）
- `SONAR_HOST_URL` / `SONAR_TOKEN`（develop 分支需要）

## 2）前端项目至少建议有
- `DINGTALK_WEBHOOK`（如需要通知）
- `YAML_CONFIG_REPO_HTTP`
- `YAML_CONFIG_REPO_TOKEN`
- `YAML_CONFIG_REPO_BRANCH`（建议显式配置）
- `REGISTRY`（可选）

## 3）通用检查
- 变量值里不要有多余空格
- token 尽量设置为 masked / protected
- 如果 release 分支是 protected branch，注意变量作用范围也要匹配

---

# 四、后端项目接入步骤

## 步骤 1：选择一个现成入口文件还是新建一个入口文件

如果 `variables/` 目录里已经有非常接近的服务，可以参考它。
如果没有，就新建一个服务入口文件，例如：

`variables/insgeek-business-demo.yml`

推荐内容：

```yaml
include:
  - local: 'templates/backend.base.yml'

variables:
  skip_sonarqube_err: 'false'
  dockerfile_name: 'Dockerfile.backend-jdk8-agent'
  service_name: 'insgeek-business-demo'
  DOCKER_IMAGE_NAME: 'insgeek-business-demo'
  DEPLOY_CONFIG_PROJECT_PATH: 'insgeek-business-demo'
```

### 这几个变量怎么判断
- `dockerfile_name`
  - 看项目需要 agent 版还是普通版
  - 常见：
    - `Dockerfile.backend-jdk8-agent`
    - `Dockerfile.backend-jdk8`
- `service_name`
  - 建议写成服务真实名
- `DOCKER_IMAGE_NAME`
  - 如果镜像名与项目名一致，也建议显式写清楚
- `DEPLOY_CONFIG_PROJECT_PATH`
  - 对应 yaml-config 仓库里的服务目录
- `image_source_env`
  - 只有在“多个部署目录共用同一套镜像”时才需要额外理解
  - 当前 release 分支默认用 `uat` 镜像同时更新 `uat` / `pro`

## 步骤 2：修改业务仓库 `.gitlab-ci.yml`

推荐只保留一个 include：

```yaml
include:
  - project: "devops/pipeline-better"
    ref: main
    file: "variables/insgeek-business-demo.yml"
```

注意：
- 不要再同时 include 老模板和新模板
- 避免双模板混跑

## 步骤 3：确认分支映射

当前后端 workflow 大致是：
- `feature*` / `feature_test*` -> `image_env=dev`
- `develop*` -> `image_env=fat`
- `release` -> `image_env=uat`
- `platform*` -> `image_env=platform`
- `vintage*` -> `image_env=vintage`

如果你的项目分支策略不在这个范围内，接入前要先补 workflow 规则。

## 步骤 4：验证 develop 分支链路

建议先验证一条 develop 或 feature 分支链路，观察：
- `build_backend`
- `prepare_dockerfile`
- `build_image`
- `update_deploy_repo`
- 如启用 Sonar，再看 `sonar_scan` / `notify_quality_gate`

## 步骤 5：验证 release 分支链路

重点看：
- 是否走到 `image_env=uat`
- 是否用了正确 runner
- 是否能更新 yaml-config 中对应 `uat` 目录

---

# 五、前端项目接入步骤

## 步骤 1：区分普通站点还是子路径站点

### 普通站点常见入口文件
```yaml
include:
  - local: 'templates/frontend.base.yml'

variables:
  dockerfile_name: 'Dockerfile.frontend-nginx'
  index_conf: 'index.conf'
  service_name: 'insgeek-front-demo'
```

### 子路径站点常见入口文件
```yaml
include:
  - local: 'templates/frontend.base.yml'

variables:
  dockerfile_name: 'Dockerfile.frontend-subpath'
  index_conf: 'index-subpath.conf'
  service_name: 'insgeek-front-demo-subpath'
  SUBPATH_ENABLED: 'true'
  Dir: 'demo'
```

### 这几个变量怎么判断
- `dockerfile_name`
  - 普通站点用 `Dockerfile.frontend-nginx`
  - 子路径站点用 `Dockerfile.frontend-subpath`
- `index_conf`
  - 普通站点 `index.conf`
  - 子路径站点 `index-subpath.conf`
- `Dir`
  - 子路径部署时对应站点挂载子目录

## 步骤 2：修改业务仓库 `.gitlab-ci.yml`

```yaml
include:
  - project: "devops/pipeline-better"
    ref: main
    file: "front/insgeek-front-demo.yml"
```

## 步骤 3：验证分支构建环境

当前前端 workflow 大致是：
- `feature*` -> `build_env=dev`, `image_env=dev`
- `develop*` -> `build_env=stage`, `image_env=fat`
- `release` -> `build_env=uat`, `image_env=uat`
- `platform*` -> `build_env=platform`, `image_env=platform`

重点确认：
- `yarn build:${build_env}` 对应脚本在 `package.json` 中真实存在

## 步骤 4：验证构建产物

重点看：
- `dist` 是否生成
- `index.conf` 是否下载成功
- Kaniko 是否能成功推镜像
- yaml-config 前端目录是否更新正确

---

# 六、Maven 发布项目接入步骤

## 步骤 1：定义入口文件

典型写法：

```yaml
include:
  - local: 'templates/maven-publish.base.yml'

publish_maven_modules:
  extends: .publish_maven
  parallel:
    matrix:
      - path:
          - module-a
          - module-b
          - module-c
```

## 步骤 2：修改业务仓库 `.gitlab-ci.yml`

```yaml
include:
  - project: "devops/pipeline-better"
    ref: main
    file: "mvn-push/demo-components.yml"
```

## 步骤 3：只在 develop 验证

当前 `maven-publish.base.yml` 只在 develop 分支自动执行。
所以测试时优先用 develop 分支。

## 步骤 4：检查每个模块 path

重点确认：
- path 是真实存在的模块目录
- 每个模块都能独立执行 `mvn deploy`

---

# 七、首条流水线验证清单

推荐按下面顺序验证。

## 1）先验证“能触发”
- pipeline 成功创建
- 目标 job 出现在页面中

## 2）再验证“能调度”
- job 不会一直 pending
- runner tag 匹配正确

## 3）再验证“能拉模板资产”
- Dockerfile 下载成功
- 前端 index.conf 下载成功
- Sonar 通知脚本下载成功

## 4）再验证“能构建”
- 后端 jar 成功
- 前端 dist 成功
- Maven deploy 成功

## 5）再验证“能发产物”
- 镜像推送成功
- Maven 包上传成功

## 6）再验证“能更新部署元数据”
- yaml-config clone 成功
- 目录正确
- image tag 更新成功
- git push 成功

## 7）最后验证“附属能力”
- Sonar 正常
- 钉钉通知正常

---

# 八、建议的灰度接入顺序

不要一上来全量切换。

建议顺序：
1. 先选 1 个后端项目
2. 再选 1 个前端项目
3. 再选 1 个 Maven 发布项目
4. 每类先跑通 develop
5. 再验证 release
6. 每批次控制在 3~5 个项目内

这样即使有问题，也能快速止损。

---

# 九、回滚方案

如果新模板接入后出问题，最简单的回滚方式是：
- 直接把业务仓库 `.gitlab-ci.yml` 的 include 切回旧模板仓库
- 不要边修边让线上项目持续漂在不稳定模板上

推荐做法：
1. 保留旧模板仓库一段时间
2. 接入项目分批灰度
3. 一类项目稳定后再扩大范围

---

# 十、接入后建议补充的内容

新项目接入成功后，建议补 3 件事：

1. 在 `pipeline-better/docs/` 补一个该项目示例文档
- 说明为什么选这个 Dockerfile
- 镜像名和部署目录有没有特殊性

2. 如果项目有特殊变量，写清楚变量用途
- 比如前端 `Dir`
- 比如后端自定义镜像名

3. 记录首条成功 pipeline 的验证结果
- develop 是否通过
- release 是否通过
- Sonar / 钉钉 / yaml-config 是否都正常

---

# 十一、最实用的接入口诀

你以后接一个新项目，优先记住这 6 步：

1. 先判断项目类型
2. 再选对入口目录
3. 明确项目变量
4. 配齐 CI variables
5. 先跑 develop 灰度
6. 最后再切 release

这样大多数接入问题都能提前避免。
