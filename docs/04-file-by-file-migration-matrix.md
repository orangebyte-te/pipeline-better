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
| `variables/example-business-claim-adjust.yml` | `variables/example-business-claim-adjust.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-business-claim-ocr.yml` | `variables/example-business-claim-ocr.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-business-claim-report.yml` | `variables/example-business-claim-report.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-business-claim-vendor.yml` | `variables/example-business-claim-vendor.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-business-claim.yml` | `variables/example-business-claim.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-business-finance.yml` | `variables/example-business-finance.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-business-group.yml` | `variables/example-business-group.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-business-harbour.yml` | `variables/example-business-harbour.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-business-insurance.yml` | `variables/example-business-insurance.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-business-ka.yml` | `variables/example-business-ka.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-business-policy.yml` | `variables/example-business-policy.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-business-quote.yml` | `variables/example-business-quote.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-business-routing.yml` | `variables/example-business-routing.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-business-toc.yml` | `variables/example-business-toc.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-business-vendor-docking.yml` | `variables/example-business-vendor-docking.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-dataapp-ai.yml` | `variables/example-dataapp-ai.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-dataapp-bi.yml` | `variables/example-dataapp-bi.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-dataapp-lake.yml` | `variables/example-dataapp-lake.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-platform-calculator.yml` | `variables/example-platform-calculator.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-platform-common.yml` | `variables/example-platform-common.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-platform-data.yml` | `variables/example-platform-data.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-platform-fileservice.yml` | `variables/example-platform-fileservice.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-platform-flow.yml` | `variables/example-platform-flow.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-platform-gateway.yml` | `variables/example-platform-gateway.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-platform-integration.yml` | `variables/example-platform-integration.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-platform-message.yml` | `variables/example-platform-message.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-platform-restapi.yml` | `variables/example-platform-restapi.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-platform-rule.yml` | `variables/example-platform-rule.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-platform-trade.yml` | `variables/example-platform-trade.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-platform-user.yml` | `variables/example-platform-user.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/example-platfrom-company.yml` | `variables/example-platfrom-company.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/k8s-project.yml` | `variables/k8s-project.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `variables/xxl-job-admin.yml` | `variables/xxl-job-admin.yml` | 后端项目入口保留同名文件；内部改为极简变量 + include templates/backend.base.yml |
| `front/example-front-channel-h5.yml` | `front/example-front-channel-h5.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-claims-forecasting.yml` | `front/example-front-claims-forecasting.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-credit-library.yml` | `front/example-front-credit-library.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-data-report.yml` | `front/example-front-data-report.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-direct-sales-system.yml` | `front/example-front-direct-sales-system.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-empower.yml` | `front/example-front-empower.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-finance.yml` | `front/example-front-finance.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-h5.yml` | `front/example-front-h5.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-hr-saas-h5.yml` | `front/example-front-hr-saas-h5.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-hr-saas.yml` | `front/example-front-hr-saas.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-example-login.yml` | `front/example-front-example-login.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-example-website.yml` | `front/example-front-example-website.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-example-xxsd.yml` | `front/example-front-example-xxsd.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-customerapp-app-new.yml` | `front/example-front-customerapp-app-new.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-marketing-tools.yml` | `front/example-front-marketing-tools.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-new-bi.yml` | `front/example-front-new-bi.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-new-claim.yml` | `front/example-front-new-claim.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-new-gide.yml` | `front/example-front-new-gide.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-new-insurance.yml` | `front/example-front-new-insurance.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-new-quote.yml` | `front/example-front-new-quote.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-operation-manage.yml` | `front/example-front-operation-manage.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-quotation.yml` | `front/example-front-quotation.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/example-front-rocket.yml` | `front/example-front-rocket.yml` | 前端项目入口保留同名文件；内部改为极简变量 + include templates/frontend.base.yml |
| `front/pipeline.yml` | `front/pipeline.yml` | 保留兼容入口，内部转发到 templates 下新模板 |
| `front/workflow.yml` | `front/workflow.yml` | 保留兼容入口，内部转发到 templates 下新模板 |
| `mvn-push/example-boot.yml` | `mvn-push/example-boot.yml` | Maven 发布入口保留同名文件；内部改为 include templates/maven-publish.base.yml |
| `mvn-push/example-business-claim-common.yml` | `mvn-push/example-business-claim-common.yml` | Maven 发布入口保留同名文件；内部改为 include templates/maven-publish.base.yml |
| `mvn-push/example-components.yml` | `mvn-push/example-components.yml` | Maven 发布入口保留同名文件；内部改为 include templates/maven-publish.base.yml |
| `mvn-push/example-protocols.yml` | `mvn-push/example-protocols.yml` | Maven 发布入口保留同名文件；内部改为 include templates/maven-publish.base.yml |
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
