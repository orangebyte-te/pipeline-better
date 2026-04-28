# include 示例

后端服务
```yaml
include:
  - project: 'ci-templates/pipeline-better'
    ref: 'release'
    file: 'variables/example-platform-gateway.yml'
```

前端服务
```yaml
include:
  - project: 'ci-templates/pipeline-better'
    ref: 'release'
    file: 'front/example-front-h5.yml'
```

Maven 发布
```yaml
include:
  - project: 'ci-templates/pipeline-better'
    ref: 'release'
    file: 'mvn-push/example-components.yml'
```
