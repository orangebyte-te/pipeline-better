# GitLab CI 与 Dockerfile 语法讲解（结合 pipeline-better）

这份文档是给当前 `pipeline-better` 仓库配套使用的。
目标不是讲全所有官方语法，而是：
- 先解释你现在项目里已经用到的写法
- 再补充一些虽然当前没大量使用，但在实际 CI/CD 中很常用、很重要的写法
- 尽量用你现在仓库里的真实例子来说明

---

# 一、先建立整体认识

你现在这套流水线可以简单理解为：

1. 业务仓库 `.gitlab-ci.yml`
2. `include` 外部模板仓库里的某个入口文件
3. 入口文件再 `include` 基础模板
4. 基础模板定义真正的 jobs
5. `workflow` / `rules` 决定哪些分支跑、带什么变量跑
6. job 按 `stages` 顺序执行

例如你现在推荐的业务仓库写法：

```yaml
include:
  - project: "ci-templates/pipeline-better"
    ref: main
    file: "variables/example-business-ka.yml"
```

它的意思是：
- 当前业务仓库不自己写完整流水线
- 而是直接复用 `ci-templates/pipeline-better` 仓库里 `main` 分支下的 `variables/example-business-ka.yml`

这个变量文件里又会再引入：

```yaml
include:
  - local: 'templates/backend.base.yml'
```

这里的意思是：
- 在模板仓库内部继续加载 `templates/backend.base.yml`
- `local` 是“当前仓库根目录下的文件”，不是业务仓库的本地文件

---

# 二、GitLab CI 最核心的几种语法

## 1）include

作用：引入其他 YAML 文件。

当前仓库里你已经在用两种：

### 写法 A：引入其他仓库文件
```yaml
include:
  - project: "ci-templates/pipeline-better"
    ref: main
    file: "variables/example-business-ka.yml"
```

含义：
- `project`：模板来自哪个 GitLab 项目
- `ref`：用哪个分支、tag、commit
- `file`：取这个仓库里的哪个 YAML 文件

适用场景：
- 统一管理模板
- 多个业务项目共用一套 CI/CD

### 写法 B：引入当前仓库内文件
```yaml
include:
  - local: 'templates/backend.base.yml'
```

含义：
- 从当前 YAML 所属仓库继续加载文件
- 常用于模板拆分

注意：
- `include: local:` 是相对“仓库根目录”，不是相对当前文件目录

---

## 2）stages

作用：定义流水线阶段顺序。

示例：
```yaml
stages:
  - build
  - quality
  - package
  - notify
  - deploy_meta
```

含义：
- `build`：编译打包
- `quality`：质量检查，例如 Sonar
- `package`：产物处理、构建镜像
- `notify`：通知
- `deploy_meta`：更新部署配置仓库

规则：
- job 默认按 stage 顺序执行
- 同一个 stage 下多个 job 可以并行

---

## 3）job

GitLab CI 里，真正执行的任务就叫 job。

例如：
```yaml
build_backend:
  stage: build
  image: ${MAVEN_IMAGE}
  script:
    - mvn clean package -Dmaven.test.skip=${skip_mvn_test}
```

这里：
- `build_backend`：job 名称
- `stage: build`：属于 build 阶段
- `image`：用哪个容器镜像执行
- `script`：执行的 shell 命令

你可以把一个 job 理解成“流水线里的一个步骤”。

---

## 4）image

作用：指定 job 运行时使用的容器镜像。

示例：
```yaml
image: harbor.example.internal/base/mvn:3.6.3
```

含义：
- 这个 job 会在一个带 Maven 的容器里跑
- 所以 job 内可以直接执行 `mvn`

你当前模板里常见 image：
- Maven 镜像：构建 Java
- Kaniko 镜像：构建 Docker 镜像
- curl 镜像：下载文件、调 webhook
- Python 镜像：跑脚本
- kustomize 镜像：改部署配置

这是容器化流水线的核心思想：
不同 job 用不同工具镜像，互不污染。

---

## 5）script

作用：定义 job 要执行的命令。

示例：
```yaml
script:
  - test -f target/Dockerfile
  - /kaniko/executor --context "$CI_PROJECT_DIR" --dockerfile target/Dockerfile --destination ${IMAGE_REGISTRY}/${image_env}/${SERVICE_NAME}:$CI_COMMIT_SHORT_SHA
```

含义：
- 每一行本质上都是 shell 命令
- 前一行检查文件是否存在
- 后一行执行镜像构建

### script 的两种常见写法

写法 A：一行一条命令
```yaml
script:
  - pwd
  - ls
  - mvn clean package
```

写法 B：多行脚本块
```yaml
script:
  - |
      if [ -n "$VAR" ]; then
        echo "ok"
      else
        echo "empty"
      fi
```

`|` 的意思是：
把下面这一整段当成一个多行 shell 脚本来执行。

---

## 6）variables

作用：定义变量。

示例：
```yaml
variables:
  skip_sonarqube_err: 'false'
  dockerfile_name: 'Dockerfile.backend-jdk8-agent'
  service_name: 'example-business-ka'
  DOCKER_IMAGE_NAME: 'example-business-ka'
  DEPLOY_CONFIG_PROJECT_PATH: 'example-business-ka'
```

含义：
- `dockerfile_name`：指定本项目要用哪个 Dockerfile 模板
- `service_name`：服务名
- `DOCKER_IMAGE_NAME`：镜像名
- `DEPLOY_CONFIG_PROJECT_PATH`：deployment-config 中的目录路径

### 变量来源一般有几层
1. GitLab 系统内置变量
   - 例如 `CI_PROJECT_TITLE`、`CI_COMMIT_BRANCH`、`CI_JOB_TOKEN`
2. 项目/组级 CI 变量
   - 例如 `SONAR_TOKEN`、`DINGTALK_WEBHOOK`
3. YAML 里自己定义的变量
4. job 内 `export` 出来的变量

### 变量引用
```yaml
${CI_PROJECT_TITLE}
${image_env}
${SERVICE_NAME}
```

这和 shell 变量展开是同一套思路。

---

## 7）default

作用：给所有 job 设置默认配置。

示例：
```yaml
default:
  tags:
    - ${RUNNER_TAG}
  interruptible: true
  retry: 1
```

含义：
- `tags`：默认都去匹配这个 runner
- `interruptible: true`：新的提交来了，旧任务可以被取消
- `retry: 1`：失败后自动重试一次

这样可以减少重复配置。

---

## 8）cache

作用：缓存依赖或中间产物，加快后续流水线。

示例：
```yaml
cache:
  key: '$CI_PROJECT_TITLE-$CI_COMMIT_REF_SLUG'
  paths:
    - .m2/repository
```

含义：
- `key`：缓存键，决定“谁和谁共用同一份缓存”
- `paths`：哪些目录需要缓存

当前意义：
- `.m2/repository`：缓存 Maven 依赖

关于 `key`，你当前这套模板里：
- `CI_PROJECT_TITLE` 负责区分项目
- `CI_COMMIT_REF_SLUG` 负责区分分支/tag
- 所以当前 key 表示“同项目同分支共享一份缓存”

这意味着：
- 不同项目之间 cache 会隔离
- 同一项目不同分支之间 cache 会隔离
- 但同一项目、同一分支上并发跑多条流水线时，它们可能会共用同一份 cache

所以当前 key 很适合：
- `.m2/repository`
- node_modules
- pip 缓存
这类“丢了最多重下，主要目标是加速”的内容

但不适合拿来强保证本次构建产物传递，比如：
- `target/`
- 本次流水线生成的 jar
- 本次流水线生成的编译结果

注意：
- cache 不是“跨 job 必然传文件”的强保证
- cache 更偏“加速”和“复用”
- 真正要给后续 job 可靠传文件，优先考虑 `artifacts`
- 如果一个文件需要保证只属于当前 pipeline，应该用 artifacts，而不是只靠 cache

---

## 9）artifacts

作用：把 job 产出的文件保存下来，并给后续 job 使用或下载。

当前你旧版里就用过，例如把 `dockerfile/`、`scripts/` 作为产物保存。

典型写法：
```yaml
artifacts:
  paths:
    - target/
  expire_in: 1 day
```

含义：
- 这个 job 执行后，`target/` 会作为当前 pipeline 的产物保留
- 下游 job 可以可靠拿到“本条 pipeline 这一轮构建出来的结果”

适用场景：
- 编译结果传给后续 job
- 供人工下载查看
- 跨 stage 传文件
- 需要避免同分支并发流水线之间相互污染时

---

## 10）needs

作用：显式指定 job 依赖谁，从而加快执行。

示例：
```yaml
build_image:
  needs: ['build_backend', 'prepare_dockerfile']
```

含义：
- `build_image` 必须等 `build_backend` 和 `prepare_dockerfile` 完成
- 同时 GitLab 会更清楚依赖关系
- 当上游 job 定义了 artifacts 时，下游通常会结合 `needs` 获取当前 pipeline 的上游产物

和 stage 的区别：
- `stage` 决定大顺序
- `needs` 决定更细粒度的依赖关系

---

## 11）rules

作用：决定 job 在什么条件下执行。

这是你现在模板里最重要的语法之一。

示例：
```yaml
rules:
  - if: '$CI_COMMIT_BRANCH =~ /^develop.*/'
    when: on_success
```

含义：
- 如果当前分支匹配 `develop` 开头
- 就在上游成功后执行这个 job

### 你当前常见的 `when`
- `on_success`：前面成功后自动执行
- `manual`：手动点击执行
- `on_failure`：前面失败时执行
- `never`：不执行

### 正则判断示例
```yaml
if: '$CI_COMMIT_BRANCH =~ /^feature.*/'
```
含义：
- 分支名以 `feature` 开头时匹配

### 精确判断示例
```yaml
if: '$CI_COMMIT_BRANCH == "release"'
```
含义：
- 只在 release 分支生效

---

## 12）workflow

作用：控制“整个 pipeline 怎么生成”。

示例：
```yaml
workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH == "release"'
      variables:
        PIPELINE_MODE: 'backend'
        image_env: 'uat'
        RUNNER_TAG: 'generic-runner-k8s'
```

含义：
- 不是只控制某个 job
- 而是决定整个 pipeline 在什么情况下创建，以及给整条流水线注入哪些变量

你现在 `backend.workflow.yml` 的主要作用就是：
- 根据分支决定环境
- 决定 runner tag
- 决定是否跳过测试
- 决定 Dockerfile 名称

可以把它理解成：
“分支 -> 环境变量映射表”。

---

## 13）extends

作用：继承一个模板 job。

你旧版 default-pipline.yml 大量使用过这个写法。

示例：
```yaml
deploy-sonarqueb:
  extends: .sonarqube
```

含义：
- `deploy-sonarqueb` 继承隐藏模板 `.sonarqube`
- 再叠加自己的 `rules` 或其他配置

### 为什么模板 job 经常以 `.` 开头？
例如：
```yaml
.sonarqube:
  stage: sonarqube
  script:
    - sonar-scanner
```

`.` 开头表示“隐藏 job / 模板 job”，默认不直接执行，主要用于被继承。

当前 `pipeline-better` 主要使用“拆文件 + 直接 job”的方式，
而旧版更偏向“隐藏 job + extends”。

两种都能用，只是组织方式不同。

---

## 14）allow_failure

作用：允许 job 失败但不把整条流水线打红。

示例：
```yaml
allow_failure: true
```

当前场景：
- Sonar 扫描失败，可能只做提醒，不阻断主流程
- 通知脚本失败，不应该让构建整体失败

注意：
- 适合“辅助型步骤”
- 不适合核心步骤，例如 build、image build、deploy meta

---

## 15）when

`when` 常和 `rules` 配合用。

常见值：
- `on_success`
- `on_failure`
- `manual`
- `always`
- `never`

示例：
```yaml
rules:
  - if: '$CI_COMMIT_BRANCH == "feature_test"'
    when: manual
```

含义：
- feature_test 分支下，这个 job 不自动跑，需要手工点

---

# 三、结合你当前模板，逐段解释常见写法

## 1）backend.workflow.yml 的本质

典型片段：
```yaml
- if: '$CI_COMMIT_BRANCH == "release"'
  variables:
    PIPELINE_MODE: 'backend'
    image_env: 'uat'
    image_source_env: 'uat'
    deploy_targets: 'uat pro'
    skip_mvn_test: 'true'
    dockerfile_name: 'Dockerfile.backend-jdk8-agent'
    RUNNER_TAG: 'generic-runner-k8s'
```

意思是：
- 当分支是 `release`
- 这条流水线被认定为后端流水线
- 镜像环境是 `uat`
- 用 workflow 里直接注入的 `RUNNER_TAG`
- 用指定 Dockerfile
- Maven 测试默认跳过

这就是“分支控制行为”的核心。

---

## 2）backend.base.yml 中 prepare_dockerfile 的语法

典型片段：
```yaml
prepare_dockerfile:
  stage: package
  image: ${CURL_IMAGE}
  script:
    - mkdir -p target
    - curl --fail --header "JOB-TOKEN: $CI_JOB_TOKEN" -o target/Dockerfile "$CI_SERVER_URL/api/v4/projects/${TEMPLATE_PROJECT_PATH_ENCODED}/repository/files/dockerfile%2F${dockerfile_name}/raw?ref=${TEMPLATE_REF}" || cp dockerfile/${dockerfile_name} target/Dockerfile
```

意思是：
- 用 curl 镜像跑这个 job
- 先建 `target` 目录
- 优先从模板仓库通过 GitLab API 拉 Dockerfile
- 如果拉取失败，再尝试从本地仓库 `dockerfile/` 目录复制

这里的关键知识点：
- `||`：前一个命令失败时，执行后一个命令
- `CI_JOB_TOKEN`：GitLab 自动注入的 job token
- `ref=${TEMPLATE_REF}`：从指定分支拉文件

---

## 3）backend.base.yml 中 build_image 的语法

典型片段：
```yaml
script:
  - test -f target/Dockerfile
  - export SERVICE_NAME="${service_name:-${DOCKER_IMAGE_NAME:-$CI_PROJECT_TITLE}}"
  - /kaniko/executor --context "$CI_PROJECT_DIR" --dockerfile target/Dockerfile --destination ${IMAGE_REGISTRY}/${image_env}/${SERVICE_NAME}:$CI_COMMIT_SHORT_SHA --cache=true --cache-repo=${IMAGE_REGISTRY}/kaniko-cache
```

这里最容易看不懂的是这句：
```bash
${service_name:-${DOCKER_IMAGE_NAME:-$CI_PROJECT_TITLE}}
```

它是 shell 的“默认值链式回退”写法，意思是：
- 如果 `service_name` 有值，就用它
- 否则看 `DOCKER_IMAGE_NAME`
- 如果它也没值，就用 `CI_PROJECT_TITLE`

也就是：
优先级 = `service_name > DOCKER_IMAGE_NAME > CI_PROJECT_TITLE`

---

## 4）update_deploy_repo 的语法

典型片段：
```yaml
- export DEPLOY_PATH="${DEPLOY_CONFIG_PROJECT_PATH:-$SERVICE_NAME}"
- cd deployment-config/${DEPLOY_PATH}/${image_env}
- kustomize edit set image ${IMAGE_REGISTRY}/${image_env}/${SERVICE_NAME}=${IMAGE_REGISTRY}/${image_env}/${SERVICE_NAME}:$CI_COMMIT_SHORT_SHA
```

含义：
- `DEPLOY_PATH` 优先使用显式配置的部署目录
- 没配就退回服务名
- 进入 deployment-config 对应目录
- 用 `kustomize edit set image` 改镜像 tag

这个设计的价值是：
项目名、镜像名、部署目录名不一致时，也能明确控制。

---

# 四、Dockerfile 语法讲解（结合你当前项目）

Dockerfile 可以理解为：
“怎么把应用打成镜像的一份构建说明书”。

你当前仓库里有后端和前端两类 Dockerfile。

---

## 1）FROM

示例：
```dockerfile
FROM harbor.example.internal/ci-tools/ubuntu-24.04:v5
```

含义：
- 以这个基础镜像为起点继续构建

可以理解成：
“先有一台装好基础环境的机器，然后在上面继续加工。”

---

## 2）LABEL

示例：
```dockerfile
LABEL maintainer="maintainer@example.internal"
```

含义：
- 给镜像增加元数据
- 常用于标记维护人、项目说明、版本信息

---

## 3）ARG

示例：
```dockerfile
ARG APP_JAR=target/APP.jar
```

含义：
- 定义“构建时变量”
- 主要在 `docker build` / Kaniko build 时使用

特点：
- 构建阶段有效
- 容器运行后不一定还能拿到

当前例子里：
- `APP_JAR` 默认表示要拷贝的 jar 包路径

---

## 4）ENV

示例：
```dockerfile
ENV JAVA_HOME=/opt/jdk1.8.0_251
ENV PATH=$PATH:/opt/jdk1.8.0_251/bin
```

含义：
- 定义环境变量
- 构建阶段和容器运行阶段通常都可用

和 `ARG` 的区别：
- `ARG` 更偏构建参数
- `ENV` 更偏镜像内运行环境配置

---

## 5）RUN

示例：
```dockerfile
RUN mkdir -pv /data/logs /data/target /oss
```

含义：
- 在镜像构建时执行命令
- 常用于安装软件、建目录、改权限

注意：
- `RUN` 是构建时执行
- 不是容器启动后执行

---

## 6）COPY

示例：
```dockerfile
COPY ${APP_JAR} /data/target/APP.jar
```

含义：
- 把构建上下文中的文件复制进镜像

这里的意思是：
- 把 `target/APP.jar` 复制到镜像内 `/data/target/APP.jar`

前端 Dockerfile 里也有：
```dockerfile
COPY dist /opt/dist
COPY index.conf /etc/nginx/conf.d/default.conf
```

意思是：
- 把前端构建好的 dist 目录复制进去
- 把 nginx 配置复制进去

---

## 7）WORKDIR

示例：
```dockerfile
WORKDIR /data
```

含义：
- 设置后续命令默认工作目录

相当于 shell 里的 `cd /data`，但它是 Dockerfile 层面的。

---

## 8）ENTRYPOINT

示例：
```dockerfile
ENTRYPOINT ["nginx", "-g", "daemon off;"]
```

含义：
- 容器启动时执行的主命令
- 通常一个容器最终就靠这个进程活着

后端 Dockerfile 里：
```dockerfile
ENTRYPOINT ["/bin/bash","-lc","java ... -jar /data/target/APP.jar ..."]
```

意思是：
- 容器启动后，用 bash 启动 Java 进程
- 这是最终业务进程

为什么要用数组形式：
- 结构更清晰
- 避免部分 shell 转义问题

---

# 五、你当前没有大量使用，但非常常见/重要的 GitLab CI 写法

## 1）before_script / after_script

作用：
- `before_script`：job 开始前先执行
- `after_script`：job 执行完后收尾

示例：
```yaml
before_script:
  - echo "start"

after_script:
  - echo "cleanup"
```

适用场景：
- 统一打印环境信息
- 收集日志
- 清理临时文件

---

## 2）artifacts:expire_in

作用：设置产物保留时间。

示例：
```yaml
artifacts:
  paths:
    - target/
  expire_in: 7 days
```

适用场景：
- 避免 artifacts 永久堆积

---

## 3）rules:changes

作用：只有某些文件变化时才执行 job。

示例：
```yaml
rules:
  - changes:
      - Dockerfile
      - src/**/*
```

含义：
- 只有这些文件有变化时，才跑这个 job

适用场景：
- 减少无意义流水线
- 配置变更时单独触发检查

---

## 4）rules:exists

作用：当某些文件存在时才执行 job。

示例：
```yaml
rules:
  - exists:
      - pom.xml
```

含义：
- 只有仓库里有 `pom.xml` 才跑 Maven 构建

适用场景：
- 一套模板适配多种项目

---

## 5）trigger

作用：触发下游流水线或子项目流水线。

示例：
```yaml
trigger_other_project:
  trigger:
    project: ci-templates/deploy-jobs
    branch: release
```

适用场景：
- 把“构建”和“部署”拆到不同仓库/不同流水线

---

## 6）parallel / matrix

作用：并行跑多个相似 job。

示例：
```yaml
parallel:
  matrix:
    - MODULE: [api, web, admin]
```

适用场景：
- 多模块并行构建
- 多环境并行发布

---

## 7）environment

作用：定义这个 job 对应哪个部署环境。

示例：
```yaml
environment:
  name: uat
  url: https://uat.example.com
```

适用场景：
- GitLab 环境页可视化
- 部署记录管理

---

## 8）only / except

这是旧语法，现在更推荐 `rules`。

旧写法示例：
```yaml
only:
  - release
```

虽然还能用，但建议新模板统一用 `rules`，因为：
- 表达力更强
- 逻辑更清楚
- 更方便组合条件

---

# 六、你当前没有大量使用，但非常常见/重要的 Dockerfile 写法

## 1）CMD

作用：给容器默认参数或默认命令。

示例：
```dockerfile
CMD ["--server.port=8080"]
```

区别：
- `ENTRYPOINT` 更像主程序
- `CMD` 更像默认参数

两者可以组合。

---

## 2）EXPOSE

作用：声明容器对外暴露的端口。

示例：
```dockerfile
EXPOSE 8080
```

注意：
- 它更多是说明性信息
- 不等于自动开放端口

---

## 3）ADD

和 `COPY` 类似，但能力更多。

一般建议：
- 能用 `COPY` 就优先用 `COPY`
- 因为语义更清晰，行为更可控

---

## 4）多阶段构建（非常常用）

这是现代 Dockerfile 很重要的写法。

示例：
```dockerfile
FROM maven:3.9-eclipse-temurin-8 AS builder
WORKDIR /app
COPY . .
RUN mvn clean package -DskipTests

FROM eclipse-temurin:8-jre
COPY --from=builder /app/target/app.jar /app/app.jar
ENTRYPOINT ["java","-jar","/app/app.jar"]
```

含义：
- 第一阶段负责编译
- 第二阶段只保留运行所需文件

优点：
- 镜像更小
- 更安全
- 构建过程更清晰

你现在的流水线是“在 CI 里先编译，再用 Dockerfile 只负责打包运行环境”，
所以暂时没有强依赖多阶段构建。
但如果以后想让 Dockerfile 自己承担编译逻辑，多阶段构建会非常重要。

---

# 七、你现在最值得优先记住的 10 个语法

如果你现在不想一下子记太多，优先记这 10 个就够用了：

GitLab CI：
1. `include`：引模板
2. `stages`：定阶段顺序
3. `job`：具体执行步骤
4. `image`：这个步骤用什么容器跑
5. `script`：执行什么命令
6. `variables`：变量定义
7. `workflow`：整条流水线的分支/变量控制
8. `rules`：某个 job 在什么条件下执行
9. `needs`：依赖哪个 job
10. `artifacts` / `cache`：保存产物 / 加速缓存

Dockerfile：
1. `FROM`
2. `ARG`
3. `ENV`
4. `RUN`
5. `COPY`
6. `WORKDIR`
7. `ENTRYPOINT`

---

# 八、结合你当前项目，怎么看一段 pipeline

以后你看到一段 `.gitlab-ci.yml`，建议按这个顺序看：

1. 先看有没有 `include`
   - 判断真正逻辑在哪个文件
2. 再看 `workflow`
   - 哪些分支跑
   - 注入哪些变量
3. 再看 `stages`
   - 流程顺序是什么
4. 再看每个 job 的：
   - `stage`
   - `image`
   - `script`
   - `rules`
   - `needs`
5. 最后看它依赖哪些外部变量
   - token
   - webhook
   - runner tag
   - registry

看 Dockerfile 时建议顺序：

1. `FROM`：基于什么镜像
2. `ARG/ENV`：有哪些参数和环境变量
3. `RUN`：构建时做了什么
4. `COPY`：哪些文件被打进镜像
5. `WORKDIR`：工作目录在哪
6. `ENTRYPOINT/CMD`：容器启动后跑什么

---

# 九、结合你当前 pipeline-better，容易混淆的几个点

## 1）include 进来的模板，不代表模板仓库文件会出现在业务仓库工作目录

这是最容易误解的点。

你现在已经修过这个问题。
正确理解是：
- YAML 可以从模板仓库 include 进来
- 但 job 执行目录仍然是业务仓库
- 所以 `dockerfile/`、`scripts/` 这些文件不能想当然地认为就在本地
- 需要通过 GitLab API 下载，或者业务仓库自己带一份

---

## 2）cache 和 artifacts 不是一回事

- `cache`：偏加速
- `artifacts`：偏可靠传递产物

如果是关键文件，例如：
- 构建后的 jar
- 生成的 Dockerfile
- 测试报告

建议优先考虑 `artifacts`。

---

## 3）workflow 和 rules 不是一回事

- `workflow`：更偏整条 pipeline 层面
- `rules`：更偏单个 job 层面

你现在 `workflow` 主要负责“根据分支注入变量”，
`rules` 负责“这个 job 该不该执行”。

---

# 十、后续建议

如果你准备继续维护这套模板，我建议你把后续文档继续拆成这几类：

1. `GitLab CI 语法速查表`
   - 专门列关键词和解释
2. `Dockerfile 语法速查表`
   - 专门列指令和例子
3. `pipeline-better 调试手册`
   - 某个 job 失败时怎么排查
4. `常见变量说明`
   - 每个变量从哪来、用于哪里
5. `分支 -> 环境映射表`
   - feature / develop / release 对应什么行为

如果你愿意，我下一步可以继续直接帮你补两份：
- 一份 `GitLab CI 语法速查表`
- 一份 `pipeline-better 变量说明文档`

这样你以后回来看模板时会更容易。