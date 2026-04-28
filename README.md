# pipeline-better

这是对原始 `/Users/yangdong/work/pipeline` 的结构化重构版，目标不是“改一点点”，而是把它整理成可长期维护、可审计、可扩展的 GitLab CI 模板仓库。

优化目标
- 去掉大量重复 YAML
- 去掉硬编码 token / access_token / PAT
- 把“分支 -> 环境”的规则收口到少量模板
- 前端 / 后端 / Maven 发布分离
- Dockerfile 和脚本现代化
- 增加文档，明确调用链和迁移方式

目录说明
- docs/: 原仓库分析、调用关系、优化建议、迁移说明
- templates/: 后端、前端、Maven 发布的共享模板
- variables/: 后端服务入口文件，每个服务只保留少量变量
- front/: 前端服务入口文件
- mvn-push/: Maven 多模块或组件发布入口文件
- dockerfile/: 优化后的构建镜像模板
- scripts/: 可复用脚本，敏感配置改为 CI 变量注入

推荐使用方式
1. 业务仓库自己的 `.gitlab-ci.yml` 只 include 对应入口文件
2. 入口文件只负责“项目级变量覆盖”
3. 公共逻辑全部在 templates/ 中维护
4. 敏感信息全部放 GitLab CI/CD Variables 或外部 secret manager

强烈建议迁移时先从一个后端项目、一个前端项目、一个 mvn-push 项目做灰度验证，再批量切换。


已验证场景（insgeek-business-test）
- 业务仓库 `.gitlab-ci.yml` 使用：`project: "devops/pipeline-better"` + `ref: main` + `file: "variables/insgeek-business-insurance.yml"`
- 模板入口显式指定：`service_name`、`DOCKER_IMAGE_NAME`、`DEPLOY_CONFIG_PROJECT_PATH`
- 当前 workflow 直接注入 `RUNNER_TAG=dev-runner-k8s-ali`，因此不依赖 `RUNNER_TAG_*` CI 变量
- release 分支会构建 `uat` 镜像，并同步更新 yaml-config 中的 `uat` / `pro` 目录到同一个镜像 tag
- 最小必备变量：`DINGTALK_WEBHOOK`、`YAML_CONFIG_REPO_HTTP`、`YAML_CONFIG_REPO_TOKEN`、`YAML_CONFIG_REPO_BRANCH`；`SONAR_HOST_URL` / `SONAR_TOKEN` 仅 develop 分支必需
