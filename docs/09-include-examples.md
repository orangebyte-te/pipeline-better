# include 示例

后端服务
```yaml
include:
  - project: 'devops/pipeline-better'
    ref: 'release'
    file: 'variables/insgeek-platform-gateway.yml'
```

前端服务
```yaml
include:
  - project: 'devops/pipeline-better'
    ref: 'release'
    file: 'front/insgeek-front-h5.yml'
```

Maven 发布
```yaml
include:
  - project: 'devops/pipeline-better'
    ref: 'release'
    file: 'mvn-push/insgeek-components.yml'
```
