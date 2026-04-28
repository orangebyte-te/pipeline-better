# example-business-ka 接入示例

推荐业务仓库 `.gitlab-ci.yml`：

```yaml
include:
  - project: "ci-templates/pipeline-better"
    ref: main
    file: "variables/example-business-ka.yml"
```

推荐模板入口 `variables/example-business-ka.yml`：

```yaml
include:
  - local: 'templates/backend.base.yml'

variables:
  skip_sonarqube_err: 'false'
  dockerfile_name: 'Dockerfile.backend-jdk8-agent'
  service_name: 'example-business-ka'
  DOCKER_IMAGE_NAME: 'example-business-ka'
  DEPLOY_CONFIG_PROJECT_PATH: 'example-business-ka'
```

说明：
- `ref` 与模板内默认 `TEMPLATE_REF` 统一为 `main`
- `service_name` 用于兼容模板中的服务名推导
- `DOCKER_IMAGE_NAME` 明确控制镜像名
- `DEPLOY_CONFIG_PROJECT_PATH` 明确控制 deployment-config 中的目录路径
- 当前 workflow 已直接注入 `RUNNER_TAG=generic-runner-k8s`，入口文件不需要再写 `runner_tags`
- 当项目名、镜像名、部署目录名不一致时，优先以上述显式变量为准
