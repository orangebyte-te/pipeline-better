# 原仓库分析

一、原仓库是什么
原仓库本质上是一个“GitLab CI 模板与入口文件仓库”，用于给多个业务仓库提供统一流水线能力，主要覆盖三类场景：
1. Java 后端构建、SonarQube 扫描、Kaniko 镜像构建、Kustomize 更新镜像标签
2. 前端项目 yarn build、Docker 构建、更新前端 kustomize 配置
3. Maven 组件/协议仓库的 deploy 发布

二、原仓库主要目录职责
1. templates/
   - `default-pipline.yml`: 后端主模板，是真正的流水线核心
   - `workflow.yml`: 分支到环境变量的映射规则

2. variables/
   - 这里不是“通用变量定义”，而是“各个后端项目的入口文件”
   - 大部分文件只做两件事：
     a) 覆盖少量变量，如 `runner_tags`、`dockerfile_name`、`ci_result_dingding_url`
     b) include `templates/workflow.yml`
   - 所以 variables 目录实际承担的是“后端项目适配层”

3. front/
   - `pipeline.yml`: 前端主模板
   - `workflow.yml`: 前端分支到环境的变量映射
   - 其他 `example-front-*.yml`: 前端项目入口文件

4. mvn-push/
   - `pipeline.yml`: Maven 发布模板
   - `example-*.yml`: 通过 `parallel.matrix` 定义多模块发布路径

5. dockerfile/
   - 提供后端、前端、UAT、Ubuntu 等不同 Dockerfile 模板
   - 流水线通过 artifact/curl 把这些 Dockerfile 下发到业务仓库构建时使用

6. scripts/
   - `sonarqube.py`: SonarQube 查询 + 钉钉通知
   - `codereview.py`: 读取 GitLab MR diff，原意是做自动 code review，但目前半成品/关闭状态
   - `index*.conf`: 前端 nginx 配置模板

7. 根目录 `.gitlab-ci.yml`
   - 仅负责把 `dockerfile/` 和 `scripts/` 作为 artifacts 暴露出来
   - 业务仓库在运行流水线时再通过 GitLab artifact URL 把 Dockerfile/脚本下载过去

8. 根目录 `Jenkinsfile`
   - 历史遗留的 Jenkins 流水线，和 GitLab CI 是两套体系
   - 说明仓库有过 Jenkins -> GitLab 的迁移过程

三、原仓库的核心
核心不是变量文件，而是这三层：
1. `templates/default-pipline.yml`：定义后端流水线阶段与 job
2. `templates/workflow.yml` / `front/workflow.yml`：决定不同分支对应哪个环境变量
3. 各业务入口文件：只做少量差异化覆盖，然后 include 模板

四、原仓库调用链
1. 后端项目调用链
   业务仓库 `.gitlab-ci.yml`
   -> include `legacy-templates/pipeline:variables/某个服务.yml`
   -> 该入口文件 include `templates/workflow.yml`
   -> workflow rules 根据分支设置 `image_env`、`dockerfile_name`、`runner_tags` 等变量
   -> `templates/default-pipline.yml` 中各 job 执行构建、扫描、构镜像、通知、更新 deployment-config

   注意：原仓库中很多 variables 文件只 include 了 workflow.yml，而不是明确 include default-pipline.yml。说明它依赖外部项目可能还会再 include 主模板，或仓库历史上做过合并/裁剪，结构表达不够清晰。

2. 前端项目调用链
   业务仓库 `.gitlab-ci.yml`
   -> include `front/某个项目.yml`
   -> include `front/workflow.yml`
   -> 通过 `front/pipeline.yml` 中的 job 执行 yarn build / docker build / 更新配置仓库

3. Maven 发布调用链
   业务仓库 `.gitlab-ci.yml`
   -> include `mvn-push/某个组件定义.yml`
   -> 使用 `mvn-push/pipeline.yml`
   -> 根据 `parallel.matrix` 下的 `path` 循环发布多个模块

五、当前暴露出来的明显问题
1. 重复文件非常多
   - variables 目录大量文件内容几乎一样
   - front 目录大量项目入口文件完全一样

2. 敏感信息硬编码
   - Sonar token
   - GitLab token
   - 钉钉 access_token
   - 这些都不应该出现在仓库里

3. 命名不统一/存在拼写问题
   - `default-pipline.yml` 少了 e
   - `depoly-build` / `deploy-sonarqueb`
   - `example-platfrom-company.yml` 平台 platform 拼错
   - `yaml-conflg` 看起来也像拼写问题

4. 结构表达不够直观
   - 调用链分散在多个文件
   - 业务入口文件和主模板之间关系不够显式

5. 历史包袱较重
   - Jenkinsfile 仍在仓库
   - code review 脚本未完整接入
   - 注释掉的大量逻辑没有整理

6. 可维护性差
   - 改一个共性参数可能要改几十个文件
   - 分支策略和环境策略散落多处

7. 安全风险高
   - token 泄露风险
   - 外部 HTTP 地址和机器人地址硬编码

8. 可观测性和验证不足
   - 模板仓库本身没有 lint / validate
   - 缺少迁移说明和使用说明
