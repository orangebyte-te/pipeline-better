# 迁移示例

后端项目旧写法（示意）
```yaml
include:
  - project: "devops/pipeline"
    ref: release
    file: "variables/insgeek-platform-gateway.yml"
```

后端项目新写法
```yaml
include:
  - project: "devops/pipeline-better"
    ref: main
    file: "variables/insgeek-platform-gateway.yml"
```

前端项目新写法
```yaml
include:
  - project: "devops/pipeline-better"
    ref: main
    file: "front/insgeek-front-h5.yml"
```

Maven 发布项目新写法
```yaml
include:
  - project: "devops/pipeline-better"
    ref: main
    file: "mvn-push/insgeek-components.yml"
```

上线前要准备的 GitLab CI 变量
- DINGTALK_WEBHOOK
- SONAR_HOST_URL
- SONAR_TOKEN（develop 分支需要）
- YAML_CONFIG_REPO_HTTP
- YAML_CONFIG_REPO_BRANCH
- YAML_CONFIG_REPO_TOKEN
- REGISTRY（可选，不配时默认 harbor.insgeek.cn）
- REGISTRY_USER（可选）
- REGISTRY_PASSWORD（可选）

说明
- 当前 workflow 已直接注入 `RUNNER_TAG=dev-runner-k8s-ali`，不再依赖 `RUNNER_TAG_*` 变量
- 业务仓库 include 的 `ref` 应与模板内 `TEMPLATE_REF` 保持一致；当前验证通过的组合是 `main`
- release 分支会构建 `uat` 镜像，并同时更新 yaml-config 中的 `uat` / `pro` 目录
