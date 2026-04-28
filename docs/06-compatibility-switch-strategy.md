# 兼容性与切换策略

目标：尽量让业务仓库只改 include 路径，不改太多项目内逻辑。

一、最小改动切换方式
1. 后端项目
   - 原 include: `devops/pipeline:variables/<service>.yml`
   - 新 include: `devops/pipeline-better:variables/<service>.yml`

2. 前端项目
   - 原 include: `devops/pipeline:front/<service>.yml`
   - 新 include: `devops/pipeline-better:front/<service>.yml`

3. Maven 发布项目
   - 原 include: `devops/pipeline:mvn-push/<service>.yml`
   - 新 include: `devops/pipeline-better:mvn-push/<service>.yml`

二、切换前必须准备的变量
- DINGTALK_WEBHOOK
- SONAR_HOST_URL
- SONAR_TOKEN（develop 分支需要）
- YAML_CONFIG_REPO_HTTP
- YAML_CONFIG_REPO_BRANCH
- YAML_CONFIG_REPO_TOKEN
- REGISTRY

补充说明
- 当前 workflow 已直接注入 `RUNNER_TAG=dev-runner-k8s-ali`
- 如未来改回变量化 runner，请同步更新模板和文档

三、灰度顺序
- 先后端 1 个
- 再前端 1 个
- 再 maven-publish 1 个
- 验证无误后批量切换
