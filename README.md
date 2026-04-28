# pipeline-better

A structured, maintainable, and auditable GitLab CI template repository for multi-project delivery scenarios.

这个仓库是对原始 `the legacy pipeline repository` 的结构化重构版。目标不是“局部修补”，而是沉淀成一个可长期维护、可审计、可扩展、可逐步迁移落地的 GitLab CI 模板仓库。

## 1. 项目目标

本仓库重点解决以下问题：

- 去掉大量重复 YAML，减少维护成本
- 去掉硬编码 token / access_token / PAT，降低安全风险
- 把“分支 -> 环境”的规则收口到少量模板
- 将前端、后端、Maven 发布场景拆分治理
- 优化 Dockerfile 与通用脚本，提升复用性
- 增加迁移文档、排障文档、巡检文档和变量说明

## 2. 适用场景

适用于以下 GitLab CI/CD 治理场景：

- 多后端服务共享一套 Pipeline 模板
- 多前端项目共享构建、镜像、部署流程
- Maven 多模块或公共组件统一发布
- 希望逐步从“项目内堆叠脚本”迁移到“模板化、变量化、标准化”管理
- 需要提升可维护性、审计性与团队协作效率

## 3. 仓库结构

```text
pipeline-better/
├── docs/         # 原仓库分析、迁移说明、巡检清单、排障手册、变量说明
├── templates/    # 前端 / 后端 / Maven 发布的共享模板
├── variables/    # 后端服务入口文件，每个服务只保留少量项目变量
├── front/        # 前端服务入口文件
├── mvn-push/     # Maven 多模块或组件发布入口文件
├── dockerfile/   # 优化后的构建镜像模板
├── scripts/      # 可复用脚本，敏感配置通过 CI 变量注入
├── env.template  # 环境变量模板示例
└── .gitlab-ci.yml
```

## 4. 推荐使用方式

推荐按以下方式落地：

1. 业务仓库自己的 `.gitlab-ci.yml` 只负责 include 对应入口文件
2. 入口文件只负责项目级变量覆盖
3. 公共逻辑全部在 `templates/` 中统一维护
4. 敏感信息全部放 GitLab CI/CD Variables 或外部 Secret Manager
5. 先灰度验证，再批量迁移，避免一次性切换风险

## 5. 目录说明

### docs/
沉淀原始分析、迁移计划、迁移步骤、变量参考、排障手册、巡检清单、上线清单等文档。

### templates/
放公共模板逻辑，是整个仓库的核心复用层。

### variables/
后端项目入口文件。每个服务只保留必要变量，尽量避免重复流水线逻辑。

### front/
前端服务的入口文件，适合统一治理前端项目的构建、镜像、发布流程。

### mvn-push/
适用于 Maven 多模块或组件型项目的统一发布场景。

### dockerfile/
维护标准化构建镜像模板，减少业务仓库内重复 Dockerfile。

### scripts/
维护可复用脚本，例如校验、通知、Review 辅助等脚本。

## 6. 已验证场景

当前已验证场景：`example-business-test`

验证要点：

- 业务仓库 `.gitlab-ci.yml` 使用：`project: "ci-templates/pipeline-better"` + `ref: main` + `file: "variables/example-business-insurance.yml"`
- 模板入口显式指定：`service_name`、`DOCKER_IMAGE_NAME`、`DEPLOY_CONFIG_PROJECT_PATH`
- 当前 workflow 直接注入 `RUNNER_TAG=generic-runner-k8s`，因此不依赖 `RUNNER_TAG_*` CI 变量
- release 分支会构建 `uat` 镜像，并同步更新 deployment-config 中的 `uat` / `pro` 目录到同一个镜像 tag
- 最小必备变量：`DINGTALK_WEBHOOK`、`YAML_CONFIG_REPO_HTTP`、`YAML_CONFIG_REPO_TOKEN`、`YAML_CONFIG_REPO_BRANCH`
- `SONAR_HOST_URL` / `SONAR_TOKEN` 仅 develop 分支必需

## 7. 迁移建议

强烈建议迁移时不要一步切全量，建议按下面顺序推进：

1. 先选择 1 个后端项目做灰度验证
2. 再选择 1 个前端项目验证模板兼容性
3. 再选择 1 个 Maven 发布项目验证制品发布链路
4. 验证通过后再批量迁移其它项目
5. 迁移过程中同步完善 `docs/` 中的 SOP、回滚、排障和巡检文档

## 8. 文档导航

建议重点阅读：

- `docs/03-migration-guide.md`
- `docs/08-production-rollout-checklist.md`
- `docs/12-gitlab-ci-and-dockerfile-syntax-guide.md`
- `docs/13-pipeline-better-variable-reference.md`
- `docs/14-pipeline-better-troubleshooting-guide.md`
- `docs/15-new-project-onboarding-sop.md`
- `docs/16-pipeline-better-inspection-checklist.md`

## 9. 后续可继续优化方向

- 增加更多标准化服务入口模板
- 增加更细粒度的变量约束与校验机制
- 增加 CI 配置自动校验与预览能力
- 增加回滚演练与发布审计说明
- 增加更多真实业务接入示例

## 10. License

MIT
