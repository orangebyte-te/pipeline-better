# pipeline-better 变量说明文档

这份文档专门说明 `pipeline-better` 里常见变量的来源、用途、是否必填，以及排查思路。

目标：
- 看清楚每个变量是谁赋值的
- 明白变量最终在哪个 job 里被使用
- 新项目接入时知道哪些必须配
- 出问题时知道先检查哪一层

---

# 一、变量来源总览

在 `pipeline-better` 里，变量主要有 5 个来源：

1. GitLab 内置变量
- 例如：
  - `CI_PROJECT_TITLE`
  - `CI_PROJECT_NAME`
  - `CI_COMMIT_BRANCH`
  - `CI_COMMIT_SHORT_SHA`
  - `CI_JOB_TOKEN`
  - `CI_SERVER_URL`
  - `CI_PIPELINE_ID`
  - `CI_PIPELINE_URL`

2. GitLab 项目/组级 CI 变量
- 例如：
  - `SONAR_TOKEN`
  - `SONAR_HOST_URL`
  - `DINGTALK_WEBHOOK`
  - `YAML_CONFIG_REPO_HTTP`
  - `YAML_CONFIG_REPO_TOKEN`
  - `REGISTRY`

3. workflow 注入的变量
- 例如：
  - `PIPELINE_MODE`
  - `image_env`
  - `image_source_env`
  - `deploy_targets`
  - `build_env`
  - `skip_mvn_test`
  - `dockerfile_name`
  - `RUNNER_TAG`

4. 项目入口文件里定义的变量
- 后端示例：`variables/insgeek-business-ka.yml`
- 前端示例：`front/insgeek-front-h5.yml`
- Maven 发布示例：`mvn-push/insgeek-protocols.yml`

5. job 运行时通过 shell 组装出来的变量
- 例如：
  - `SERVICE_NAME`
  - `DEPLOY_PATH`
  - `PROJECT_NAME`
  - `EXTRA_ARGS`

---

# 二、变量优先级怎么理解

从使用角度看，一般按下面顺序覆盖：

1. GitLab 系统变量
2. workflow 注入变量
3. 项目入口文件变量
4. job 内 `export` 出来的变量

你现在模板里一个典型例子：

```bash
export SERVICE_NAME="${service_name:-${DOCKER_IMAGE_NAME:-$CI_PROJECT_TITLE}}"
```

意思是：
- 先用 `service_name`
- 没有就用 `DOCKER_IMAGE_NAME`
- 再没有就退回 `CI_PROJECT_TITLE`

所以实际优先级是：
`service_name > DOCKER_IMAGE_NAME > CI_PROJECT_TITLE`

这在“项目名、镜像名、部署目录名不一致”的场景非常重要。

补充：
- `deploy_targets` 决定要更新哪些 yaml-config 目录
- `image_source_env` 决定这些目录最终指向哪套镜像环境
- 当前 release 分支的典型组合是：`image_env=uat`、`image_source_env=uat`、`deploy_targets="uat pro"`

---

# 三、按类别说明变量

## A. 分支/流程控制变量

### 1）PIPELINE_MODE
来源：
- `templates/backend.workflow.yml`
- `templates/frontend.workflow.yml`

常见值：
- `backend`
- `frontend`
- `mr`

作用：
- 决定当前 pipeline 是后端、前端还是 MR 场景
- 很多 job 都通过 `rules` 判断它

使用位置：
- `templates/backend.base.yml`
- `templates/frontend.base.yml`

是否必填：
- 不是手工配置变量
- 由 workflow 自动注入

排查建议：
- 如果某些 job 没执行，先看当前分支是否命中了对应 workflow rule
- 再看 `rules: if: '$PIPELINE_MODE == ...'` 是否匹配

### 2）image_env
来源：
- backend/frontend workflow

常见值：
- 后端：`dev`、`fat`、`uat`、`platform`、`vintage`
- 前端：`dev`、`fat`、`uat`、`platform`

作用：
- 决定镜像推送目录
- 决定 yaml-config 更新目录

使用位置：
- Kaniko 构建镜像地址
- `yaml-config/.../${image_env}`

是否必填：
- 自动注入

### 3）build_env
来源：
- `templates/frontend.workflow.yml`

常见值：
- `dev`
- `stage`
- `uat`
- `platform`

作用：
- 前端执行 `yarn build:${build_env}`

使用位置：
- `templates/frontend.base.yml`

是否必填：
- 仅前端需要，由 workflow 自动注入

### 4）skip_mvn_test
来源：
- `templates/backend.workflow.yml`
- 也可被项目变量文件覆盖

常见值：
- `true`
- `false`

作用：
- 控制 Maven 是否跳过测试

使用位置：
- `mvn clean package -Dmaven.test.skip=${skip_mvn_test}`

是否必填：
- 后端建议有，通常由 workflow 注入

---

## B. Runner 相关变量

### 5）RUNNER_TAG
来源：
- workflow 注入

作用：
- 让 job 匹配指定 runner

使用位置：
- `default.tags`

当前默认值：
- `dev-runner-k8s-ali`（由 workflow rules 直接注入）

是否必填：
- 必须最终有值，否则 job 会卡在无 runner 可用

排查建议：
- 先看匹配分支对应的 workflow rule 注入了什么 `RUNNER_TAG`
- 再确认 runner 实际是否打了该 tag

---

## C. 模板仓库定位变量

### 6）TEMPLATE_PROJECT_PATH_ENCODED
来源：
- `templates/backend.base.yml`
- `templates/frontend.base.yml`

当前默认值：
- `devops%2Fpipeline-better`

作用：
- 通过 GitLab API 下载模板仓库中的 Dockerfile、脚本、nginx 配置

使用位置：
- `prepare_dockerfile`
- 前端 Dockerfile/index.conf 下载
- Sonar 通知脚本下载

是否必填：
- 模板里已有默认值
- 如果 GitLab 实际项目路径不同，必须改

排查建议：
- 下载模板资产失败时，先检查它
- 注意这里是 URL 编码后的项目路径，`/` 要写成 `%2F`

### 7）TEMPLATE_REF
来源：
- `templates/backend.base.yml`
- `templates/frontend.base.yml`

当前默认值：
- `main`

作用：
- 指定通过 GitLab API 拉取模板文件时使用哪个分支

是否必填：
- 模板里已有默认值

重要说明：
- 它最好与业务仓库 `include` 使用的 `ref` 保持一致
- 当前验证通过的组合是 `include ref=main` + `TEMPLATE_REF=main`

排查建议：
- 如果 include 用的是 `release`，但下载资产拉的是 `main`，就会出现版本漂移

---

## D. 构建与镜像相关变量

### 8）dockerfile_name
来源：
- workflow 默认注入
- 项目入口文件可覆盖

后端常见值：
- `Dockerfile.backend-jdk8-agent`
- `Dockerfile.backend-jdk8`

前端常见值：
- `Dockerfile.frontend-nginx`
- `Dockerfile.frontend-subpath`

作用：
- 指定使用哪个 Dockerfile 模板

使用位置：
- 后端/前端的 Dockerfile 下载逻辑

是否必填：
- 建议每个项目入口文件都明确写

### 9）REGISTRY / IMAGE_REGISTRY
来源：
- `REGISTRY`：GitLab CI variable
- `IMAGE_REGISTRY`：模板里根据 `REGISTRY` 组装，未配置时回退 `harbor.insgeek.cn`

作用：
- 作为镜像仓库地址

使用位置：
- Kaniko 推送镜像
- kustomize 设置镜像名

是否必填：
- `REGISTRY` 可选，模板有默认值
- 如果环境不是默认 Harbor，必须配

### 10）service_name
来源：
- 项目入口文件

示例：
- `insgeek-business-ka`
- `insgeek-front-h5`

作用：
- 作为服务名的显式定义
- 用于服务名推导

使用位置：
- 后端 `SERVICE_NAME` 推导
- 前端入口文件也会定义，但前端模板当前主要还是直接用项目名/镜像名规则

是否必填：
- 强烈建议填

### 11）DOCKER_IMAGE_NAME
来源：
- 模板默认值
- 项目入口文件可显式覆盖

默认值：
- 后端：`${CI_PROJECT_TITLE}`
- 前端：`${CI_PROJECT_TITLE,,}`

作用：
- 控制镜像名

使用位置：
- Kaniko 推镜像
- kustomize 替换镜像

是否必填：
- 模板有默认值
- 但当项目名与镜像名不一致时，必须显式配置

### 12）DEPLOY_CONFIG_PROJECT_PATH
来源：
- 模板默认值
- 项目入口文件可显式覆盖

默认值：
- 后端：`${CI_PROJECT_TITLE}`
- 前端：`front/${CI_PROJECT_TITLE,,}`

作用：
- 控制 yaml-config 仓库里的项目目录路径

使用位置：
- `cd yaml-config/${DEPLOY_PATH}/${image_env}`
- 前端 `cd yaml-config/front/${image_env}/${PROJECT_NAME}`

是否必填：
- 模板有默认值
- 但项目目录名和仓库名不一致时，必须显式配置

---

## E. Sonar 与通知相关变量

### 13）SONAR_HOST_URL
来源：
- GitLab CI variable

作用：
- SonarQube 地址

使用位置：
- `sonar_scan`

是否必填：
- 如果要跑 Sonar，必填

### 14）SONAR_TOKEN
来源：
- GitLab CI variable

作用：
- SonarQube 认证 token

使用位置：
- `sonar_scan`

是否必填：
- 如果要跑 Sonar，必填

### 15）skip_sonarqube_err
来源：
- 项目入口文件

常见值：
- `false`
- `true`

作用：
- 传给 Sonar 通知脚本，用于控制质量门禁处理逻辑

使用位置：
- `notify_quality_gate`

### 16）DINGTALK_WEBHOOK
来源：
- GitLab CI variable

作用：
- 钉钉通知地址

使用位置：
- `notify_failure`
- `notify_success`

是否必填：
- 如果要发通知，必填

---

## F. 部署配置仓库相关变量

### 17）YAML_CONFIG_REPO_HTTP
来源：
- GitLab CI variable

作用：
- yaml-config 仓库地址，不带协议头外的路径也要与你 clone 方式匹配

使用位置：
- `git clone --branch ... "http://project_bot:${YAML_CONFIG_REPO_TOKEN}@${YAML_CONFIG_REPO_HTTP}"`

是否必填：
- 如果要更新部署配置，必填

### 18）YAML_CONFIG_REPO_TOKEN
来源：
- GitLab CI variable

作用：
- 访问 yaml-config 仓库的 token

是否必填：
- 如果要更新部署配置，必填

### 19）YAML_CONFIG_REPO_BRANCH
来源：
- GitLab CI variable，可选

默认值：
- `release`

作用：
- 指定克隆 yaml-config 的分支

是否必填：
- 非必填，有默认值

---

## G. 前端专有变量

### 20）index_conf
来源：
- 前端入口文件

常见值：
- `index.conf`
- `index-subpath.conf`

作用：
- 指定下载哪个 nginx 配置模板

使用位置：
- 前端镜像构建前准备 nginx 配置

### 21）SUBPATH_ENABLED
来源：
- `templates/frontend.base.yml` 默认值
- 项目入口文件可覆盖

常见值：
- `false`
- `true`

作用：
- 是否启用子路径部署模式

使用位置：
- `if [ "$SUBPATH_ENABLED" = 'true' ] && [ -n "$Dir" ]; then ...`

### 22）Dir
来源：
- 前端入口文件可配置

作用：
- 子路径部署时，作为 Docker build arg 传入

使用位置：
- `--build-arg dir=${Dir}`

### 23）NPM_REGISTRY
来源：
- `templates/frontend.base.yml`

默认值：
- `https://registry.npmmirror.com`

作用：
- 指定 yarn/npm 安装依赖的源

---

## H. Maven 发布专有变量

### 24）path
来源：
- `mvn-push/*.yml` 中的 `parallel.matrix`

作用：
- 指定要进入哪个模块目录执行 `mvn deploy`

使用位置：
- `cd "$path"`

是否必填：
- Maven 发布场景必填

---

# 四、当前仓库接入时最常用的变量组合

## 1）后端项目最小推荐变量

```yaml
variables:
  skip_sonarqube_err: 'false'
  dockerfile_name: 'Dockerfile.backend-jdk8-agent'
  service_name: 'insgeek-business-ka'
  DOCKER_IMAGE_NAME: 'insgeek-business-ka'
  DEPLOY_CONFIG_PROJECT_PATH: 'insgeek-business-ka'
```

适用场景：
- 项目名、镜像名、部署目录名不完全一致时
- 希望配置明确，不依赖默认推导

## 2）前端项目常见变量

```yaml
variables:
  dockerfile_name: 'Dockerfile.frontend-nginx'
  index_conf: 'index.conf'
  service_name: 'insgeek-front-h5'
```

如果是子路径项目，常见会是：

```yaml
variables:
  dockerfile_name: 'Dockerfile.frontend-subpath'
  index_conf: 'index-subpath.conf'
  service_name: 'insgeek-front-channel-h5'
  SUBPATH_ENABLED: 'true'
  Dir: 'channel'
```

## 3）GitLab 项目/组级建议配置的 CI 变量

后端建议至少有：
- `DINGTALK_WEBHOOK`
- `YAML_CONFIG_REPO_HTTP`
- `YAML_CONFIG_REPO_TOKEN`
- `YAML_CONFIG_REPO_BRANCH`（建议显式配成 `release`）
- `REGISTRY`（可选）
- `SONAR_HOST_URL` / `SONAR_TOKEN`（develop 分支需要）

前端建议至少有：
- `DINGTALK_WEBHOOK`（如果要通知）
- `YAML_CONFIG_REPO_HTTP`
- `YAML_CONFIG_REPO_TOKEN`
- `YAML_CONFIG_REPO_BRANCH`
- `REGISTRY`（可选）

---

# 五、变量和 job 的对应关系速查

后端：
- `PIPELINE_MODE` -> 控制后端 job 是否执行
- `skip_mvn_test` -> `build_backend`
- `SONAR_HOST_URL` / `SONAR_TOKEN` -> `sonar_scan`
- `skip_sonarqube_err` -> `notify_quality_gate`
- `dockerfile_name` -> `prepare_dockerfile`
- `service_name` / `DOCKER_IMAGE_NAME` -> `build_image`
- `DEPLOY_CONFIG_PROJECT_PATH` -> `update_deploy_repo`
- `DINGTALK_WEBHOOK` -> `notify_failure` / `notify_success`
- `YAML_CONFIG_REPO_HTTP` / `YAML_CONFIG_REPO_TOKEN` -> `update_deploy_repo`
- `CI_PROJECT_TITLE` / `CI_COMMIT_REF_SLUG` -> backend cache key，仅用于 Maven 依赖缓存隔离

前端：
- `PIPELINE_MODE` -> 控制前端 job 是否执行
- `build_env` -> `yarn_build`
- `dockerfile_name` -> `build_frontend_image`
- `index_conf` -> `build_frontend_image`
- `SUBPATH_ENABLED` / `Dir` -> `build_frontend_image`
- `YAML_CONFIG_REPO_HTTP` / `YAML_CONFIG_REPO_TOKEN` -> `update_frontend_deploy_repo`

Maven 发布：
- `path` -> `.publish_maven`
- `RUNNER_TAG` -> `default.tags`

---

# 六、接入新项目时，推荐检查顺序

1. 先确认 include 入口文件是否选对
- 后端：`variables/*.yml`
- 前端：`front/*.yml`
- Maven：`mvn-push/*.yml`

2. 再确认 workflow 能否匹配你的分支
- feature / develop / release / platform / vintage

3. 再确认项目入口文件变量是否完整
- `dockerfile_name`
- `service_name`
- 必要时显式加 `DOCKER_IMAGE_NAME`
- 必要时显式加 `DEPLOY_CONFIG_PROJECT_PATH`

4. 最后确认 GitLab CI variables 是否已配
- token
- webhook
- registry
- 如需 develop 分支质量检查，再补 Sonar 变量

---

# 七、最容易出问题的 8 个变量

1. `RUNNER_TAG`
- 问题：job 一直 pending
- 原因：workflow 注入的 runner tag 与真实 runner 不匹配

2. `TEMPLATE_PROJECT_PATH_ENCODED`
- 问题：下载 Dockerfile/脚本失败
- 原因：项目路径 URL 编码不对

3. `TEMPLATE_REF`
- 问题：include 的模板和实际下载到的脚本版本不一致
- 原因：ref 混用

4. `dockerfile_name`
- 问题：prepare_dockerfile 失败
- 原因：模板仓库里没有这个文件

5. `service_name`
- 问题：镜像名或配置更新路径不符合预期
- 原因：未显式配置，回退到了项目名

6. `DOCKER_IMAGE_NAME`
- 问题：推送到了错误镜像名
- 原因：项目名和镜像名不一致却没覆盖

7. `DEPLOY_CONFIG_PROJECT_PATH`
- 问题：更新 yaml-config 目录失败
- 原因：部署目录和仓库名不一致

8. `YAML_CONFIG_REPO_TOKEN`
- 问题：clone yaml-config 失败
- 原因：token 权限不足或过期

---

# 八、结论

维护 `pipeline-better` 时，变量不用一次性全记住。
最关键的是先分清三层：

1. workflow 决定“当前是什么流程、什么环境”
2. 项目入口文件决定“这个项目叫什么、用哪个 Dockerfile”
3. GitLab CI variables 决定“有没有权限、有哪种 runner、发到哪里”

如果这三层想清楚了，大多数问题都会变得容易排查。
