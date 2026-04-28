# 原仓库 -> 新仓库 逐文件迁移清单

| 原文件 | 新文件 | 迁移说明 |
|---|---|---|
| `.gitlab-ci.yml` | `.gitlab-ci.yml` | 模板仓库自检流水线；原来只发 artifacts，现在增加 YAML lint/打包校验 |
| `README.md` | `README.md` | 新增更完整的仓库说明 |
| `Jenkinsfile` | `docs/05-legacy-jenkins-analysis.md` | 不再作为主执行链，转为历史分析文档 |
| `templates/default-pipline.yml` | `templates/backend.base.yml` | 后端主模板，拆分为后端主模板 |
| `templates/workflow.yml` | `templates/backend.workflow.yml` | 后端 workflow 单独拆出 |
| `front/pipeline.yml` | `templates/frontend.base.yml` | 前端主模板统一放到 templates |
| `front/workflow.yml` | `templates/frontend.workflow.yml` | 前端 workflow 单独拆出 |
| `mvn-push/pipeline.yml` | `templates/maven-publish.base.yml` | Maven 发布主模板抽到 templates |
| `variables/insgeek-business-claim-adjust.yml` | `variables/insgeek-business-claim-adjust.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-business-claim-ocr.yml` | `variables/insgeek-business-claim-ocr.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-business-claim-report.yml` | `variables/insgeek-business-claim-report.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-business-claim-vendor.yml` | `variables/insgeek-business-claim-vendor.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-business-claim.yml` | `variables/insgeek-business-claim.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-business-finance.yml` | `variables/insgeek-business-finance.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-business-group.yml` | `variables/insgeek-business-group.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-business-harbour.yml` | `variables/insgeek-business-harbour.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-business-insurance.yml` | `variables/insgeek-business-insurance.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-business-ka.yml` | `variables/insgeek-business-ka.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-business-policy.yml` | `variables/insgeek-business-policy.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-business-quote.yml` | `variables/insgeek-business-quote.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-business-routing.yml` | `variables/insgeek-business-routing.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-business-toc.yml` | `variables/insgeek-business-toc.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-business-vendor-docking.yml` | `variables/insgeek-business-vendor-docking.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-dataapp-ai.yml` | `variables/insgeek-dataapp-ai.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-dataapp-bi.yml` | `variables/insgeek-dataapp-bi.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-dataapp-lake.yml` | `variables/insgeek-dataapp-lake.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-platform-calculator.yml` | `variables/insgeek-platform-calculator.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-platform-common.yml` | `variables/insgeek-platform-common.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-platform-data.yml` | `variables/insgeek-platform-data.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-platform-fileservice.yml` | `variables/insgeek-platform-fileservice.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-platform-flow.yml` | `variables/insgeek-platform-flow.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-platform-gateway.yml` | `variables/insgeek-platform-gateway.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-platform-integration.yml` | `variables/insgeek-platform-integration.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-platform-message.yml` | `variables/insgeek-platform-message.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-platform-restapi.yml` | `variables/insgeek-platform-restapi.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-platform-rule.yml` | `variables/insgeek-platform-rule.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-platform-trade.yml` | `variables/insgeek-platform-trade.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-platform-user.yml` | `variables/insgeek-platform-user.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/insgeek-platfrom-company.yml` | `variables/insgeek-platfrom-company.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/k8s-project.yml` | `variables/k8s-project.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/xxl-job-admin.yml` | `variables/xxl-job-admin.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `front/insgeek-front-channel-h5.yml` | `front/insgeek-front-channel-h5.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-claims-forecasting.yml` | `front/insgeek-front-claims-forecasting.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-credit-library.yml` | `front/insgeek-front-credit-library.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-data-report.yml` | `front/insgeek-front-data-report.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-direct-sales-system.yml` | `front/insgeek-front-direct-sales-system.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-empower.yml` | `front/insgeek-front-empower.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-finance.yml` | `front/insgeek-front-finance.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-h5.yml` | `front/insgeek-front-h5.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-hr-saas-h5.yml` | `front/insgeek-front-hr-saas-h5.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-hr-saas.yml` | `front/insgeek-front-hr-saas.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-insgeek-login.yml` | `front/insgeek-front-insgeek-login.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-insgeek-website.yml` | `front/insgeek-front-insgeek-website.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-insgeek-xxsd.yml` | `front/insgeek-front-insgeek-xxsd.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-insgeeker-app-new.yml` | `front/insgeek-front-insgeeker-app-new.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-marketing-tools.yml` | `front/insgeek-front-marketing-tools.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-new-bi.yml` | `front/insgeek-front-new-bi.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-new-claim.yml` | `front/insgeek-front-new-claim.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-new-gide.yml` | `front/insgeek-front-new-gide.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-new-insurance.yml` | `front/insgeek-front-new-insurance.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-new-quote.yml` | `front/insgeek-front-new-quote.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-operation-manage.yml` | `front/insgeek-front-operation-manage.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-quotation.yml` | `front/insgeek-front-quotation.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/insgeek-front-rocket.yml` | `front/insgeek-front-rocket.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/pipeline.yml` | `front/pipeline.yml` | 保留兼容入口，内部转发到 templates 下新模板 |
| `front/workflow.yml` | `front/workflow.yml` | 保留兼容入口，内部转发到 templates 下新模板 |
| `mvn-push/insgeek-boot.yml` | `mvn-push/insgeek-boot.yml` | Maven 发布入口保留同名文件；内部改为 include templates/maven-publish.base.yml |
| `mvn-push/insgeek-business-claim-common.yml` | `mvn-push/insgeek-business-claim-common.yml` | Maven 发布入口保留同名文件；内部改为 include templates/maven-publish.base.yml |
| `mvn-push/insgeek-components.yml` | `mvn-push/insgeek-components.yml` | Maven 发布入口保留同名文件；内部改为 include templates/maven-publish.base.yml |
| `mvn-push/insgeek-protocols.yml` | `mvn-push/insgeek-protocols.yml` | Maven 发布入口保留同名文件；内部改为 include templates/maven-publish.base.yml |
| `mvn-push/insurance-meta.yml` | `mvn-push/insurance-meta.yml` | Maven 发布入口保留同名文件；内部改为 include templates/maven-publish.base.yml |
| `mvn-push/pipeline.yml` | `mvn-push/pipeline.yml` | 保留兼容入口，内部转发到 templates/maven-publish.base.yml |
| `dockerfile/Dockerfile` | `dockerfile/Dockerfile.backend-jdk8` | 后端基础 JDK8 版 |
| `dockerfile/Dockerfile-fat` | `dockerfile/Dockerfile.backend-jdk8-agent` | 旧 fat 逻辑统一到带 agent 的后端模板 |
| `dockerfile/Dockerfile-uat` | `dockerfile/Dockerfile.backend-jdk8-agent` | UAT 统一到带 agent 的后端模板 |
| `dockerfile/Dockerfile-ubuntu` | `dockerfile/Dockerfile.backend-jdk8-agent` | Ubuntu 基础能力保留到 agent 版模板 |
| `dockerfile/Dockerfile-front` | `dockerfile/Dockerfile.frontend-nginx` | 前端根路径部署模板 |
| `dockerfile/Dockerfile-front-new` | `dockerfile/Dockerfile.frontend-subpath` | 前端子路径部署模板 |
| `scripts/sonarqube.py` | `scripts/sonarqube_notify.py` | 去硬编码 token，改为环境变量驱动 |
| `scripts/codereview.py` | `scripts/gitlab_mr_review.py` | 去硬编码 PAT，改为环境变量驱动 |
| `scripts/index.conf` | `scripts/index.conf` | 保留 |
| `scripts/index-h5.conf` | `scripts/index-h5.conf` | 保留 |
| `scripts/index-new.conf` | `scripts/index-subpath.conf` | 子路径模板统一命名 |
