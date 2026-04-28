# pipeline-better 巡检清单

这份文档用于日常巡检 `pipeline-better` 相关能力是否健康。

目标：
- 不是等 pipeline 挂了才排查
- 而是定期发现变量失效、权限漂移、模板分支不一致、runner 不可用等问题

建议巡检频率：
- 每周做一次轻巡检
- 每月做一次全量巡检
- 模板有较大改动或 GitLab 升级后，做一次专项巡检

---

# 一、轻巡检（建议每周）

## 1）模板引用是否统一
检查项：
- 业务仓库是否统一 include `devops/pipeline-better`
- include 的 `ref` 是否统一为 `release`
- 是否还有项目混用旧模板仓库 `devops/pipeline`

重点风险：
- 同一批项目混用旧模板和新模板
- include ref 与模板内 `TEMPLATE_REF` 不一致

建议处理：
- 做一个项目清单，标记：旧模板 / 新模板 / 待迁移

## 2）Runner 是否可用
检查项：
- `templates/backend.workflow.yml` / `templates/frontend.workflow.yml` 为目标分支注入的 `RUNNER_TAG` 是否仍正确
- 当前硬编码的 `dev-runner-k8s-ali` 对应 runner 是否在线
- 如果未来重新改回 CI 变量控制，文档与模板是否同步更新

重点风险：
- runner 离线
- tag 被改名
- 新 runner 上线但没继承原有 tag

## 3）关键 token 是否过期
检查项：
- `SONAR_TOKEN`
- `YAML_CONFIG_REPO_TOKEN`
- 钉钉 webhook 是否还能发
- 任何 project access token / deploy token 是否即将过期

重点风险：
- token 到期导致流水线批量失败

## 4）最近一周失败流水线是否有共性
检查项：
- 是否集中失败在同一个 job
- 是否集中失败在某一个环境
- 是否集中失败在某个 runner

建议看：
- 后端：`prepare_dockerfile`、`build_image`、`update_deploy_repo`
- 前端：`build_frontend_image`、`update_frontend_deploy_repo`
- 通用：通知类 job

---

# 二、全量巡检（建议每月）

## 1）模板仓库分支一致性巡检
检查项：
- `templates/backend.base.yml` 中 `TEMPLATE_REF` 是否仍为统一值
- `templates/frontend.base.yml` 中 `TEMPLATE_REF` 是否仍为统一值
- 文档中的 include 示例是否与真实模板一致

重点风险：
- 文档说 `release`，模板实际写 `main`
- 业务仓库 include 用 `release`，下载模板资产却走 `main`

## 2）模板资产完整性巡检
检查项：
- `dockerfile/` 中关键模板是否齐全
- `scripts/` 中通知脚本是否存在
- 前端 nginx 配置文件是否齐全

重点看：
- `Dockerfile.backend-jdk8-agent`
- `Dockerfile.backend-jdk8`
- `Dockerfile.frontend-nginx`
- `Dockerfile.frontend-subpath`
- `scripts/sonarqube_notify.py`
- `scripts/index.conf`
- `scripts/index-subpath.conf`

重点风险：
- 入口文件还在引用某个模板，但仓库里已删除或改名

## 3）入口文件规范性巡检
检查项：
- `variables/*.yml` 是否都只做少量变量覆盖
- `front/*.yml` 是否保持统一风格
- 是否有新接入项目没有显式写 `service_name`
- 是否有镜像名和部署目录名不一致但未显式写 `DOCKER_IMAGE_NAME` / `DEPLOY_CONFIG_PROJECT_PATH`

重点风险：
- 新项目靠默认推导，后期出现镜像名/路径错误

## 4）CI 变量完整性巡检
检查项：
- 后端项目组是否都有：
  - `DINGTALK_WEBHOOK`
  - `YAML_CONFIG_REPO_HTTP`
  - `YAML_CONFIG_REPO_TOKEN`
  - `YAML_CONFIG_REPO_BRANCH`
  - `SONAR_HOST_URL`
  - `SONAR_TOKEN`（develop 分支需要）
- 前端项目组是否都有：
  - `DINGTALK_WEBHOOK`（如果启用通知）
  - `YAML_CONFIG_REPO_HTTP`
  - `YAML_CONFIG_REPO_TOKEN`
  - `YAML_CONFIG_REPO_BRANCH`

重点风险：
- 新项目放到了新组里，但没继承原有 group variables

## 5）yaml-config 目标路径巡检
检查项：
- 后端项目的 `DEPLOY_CONFIG_PROJECT_PATH` 是否仍对应真实目录
- 前端目录结构是否仍符合 `front/${image_env}/${PROJECT_NAME}`
- 是否有人手工改了 yaml-config 目录结构而没同步模板

重点风险：
- pipeline 没问题，但 push 更新时找不到目录

---

# 三、专项巡检：模板改动后必须检查什么

当你改了 `templates/`、`dockerfile/`、`scripts/` 后，建议做专项巡检。

## 1）改了 workflow 后
必须确认：
- feature / develop / release / platform / vintage 的分支映射没被破坏
- runner tag 仍能正确注入
- 前后端的 `PIPELINE_MODE` 没串

## 2）改了 Dockerfile 模板后
必须确认：
- 入口文件里引用的 `dockerfile_name` 仍存在
- 后端 jar 路径仍匹配
- 前端构建产物路径仍匹配
- Kaniko 仍能正常推镜像

## 3）改了脚本下载逻辑后
必须确认：
- `CI_JOB_TOKEN` 权限仍可用
- `TEMPLATE_PROJECT_PATH_ENCODED` 仍正确
- `TEMPLATE_REF` 与 include ref 仍一致

## 4）改了部署更新逻辑后
必须确认：
- yaml-config clone 正常
- 目录路径正确
- `deploy_targets` 与 `image_source_env` 语义仍一致
- release 分支是否仍同时更新 `uat` / `pro`
- `kustomize edit set image` 正常
- git push 不受保护分支限制影响

---

# 四、建议固定维护的项目清单

建议你额外维护一份表，最少包含这些列：
- 项目名
- 项目类型（backend/frontend/mvn-push）
- 当前 include 路径
- include ref
- 是否已切到 pipeline-better
- 是否已验证 develop
- 是否已验证 release
- 镜像名是否与项目名一致
- 部署目录是否与项目名一致
- 特殊变量说明

这份表的作用很大：
- 批量迁移时不会乱
- 巡检时能快速发现特殊项目
- 模板升级时知道哪些项目要重点回归

---

# 五、巡检时最容易忽略的 10 个点

1. 文档和模板代码不一致
2. include ref 和 TEMPLATE_REF 不一致
3. runner 在线，但 tag 被改了
4. token 没过期，但权限范围变了
5. 新项目用了默认镜像名，实际不符合要求
6. yaml-config 目录被人手工改过
7. 子路径前端项目漏了 `Dir`
8. Sonar 项目名规则变了，但通知脚本没跟上
9. Maven 模块目录改名了，但 `parallel.matrix.path` 没同步
10. GitLab 升级后 Job Token 跨项目策略变化

---

# 六、建议的巡检动作模板

## 每周动作
1. 看最近一周失败流水线分布
2. 看 runner 在线状态
3. 检查关键 token 是否临近过期
4. 抽样验证 1 个后端、1 个前端项目最近流水线是否健康

## 每月动作
1. 对照文档检查模板分支/ref 一致性
2. 抽查入口文件变量规范性
3. 抽查 yaml-config 路径是否仍匹配
4. 抽查模板资产文件是否齐全
5. 抽查 1 条 release 分支流水线是否完整跑通

## 模板改动后动作
1. 至少回归 1 个后端项目
2. 至少回归 1 个前端项目
3. 如涉及 Maven 模板，再回归 1 个 Maven 发布项目
4. 回归 develop 和 release 两类关键分支

---

# 七、发现问题后的处理优先级

巡检发现问题后，建议按优先级处理：

## P0：立即处理
- runner 全挂
- token 全失效
- 模板 ref 漂移导致批量失败
- Harbor / yaml-config / Sonar 权限整体失效

## P1：本周处理
- 单类项目接入规范不统一
- 文档与模板不一致
- 个别项目镜像名/部署目录变量未显式配置

## P2：持续优化
- 文档补全
- 示例补全
- 特殊项目变量收口
- 调试日志增强

---

# 八、推荐巡检结论模板

你以后做完巡检，可以按这个格式记录：

1. 本次巡检时间
2. 巡检范围
- 后端项目数
- 前端项目数
- Maven 发布项目数

3. 巡检结论
- 正常项
- 风险项
- 已处理项
- 待处理项

4. 本次发现的主要问题
- 例如：2 个项目 include ref 不一致
- 例如：1 个前端项目子路径变量缺失
- 例如：release runner 离线

5. 建议动作
- 立即修复
- 本周修复
- 下次模板升级时统一处理

---

# 九、结论

`pipeline-better` 的巡检重点，不在于把所有项目流水线都点开看一遍，
而是抓住 5 类最容易漂移的东西：

1. ref
2. runner
3. token
4. 入口变量
5. yaml-config 路径

把这 5 类盯住，模板仓库会稳定很多。
