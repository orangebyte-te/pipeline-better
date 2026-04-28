# 重构方案

一、重构原则
1. 入口文件极简：每个项目只声明差异变量
2. 模板集中：真正的逻辑只在 templates/ 维护
3. 敏感配置外置：全部改为 GitLab CI Variables
4. 分支策略收口：后端/前端分别维护一份 workflow 模板
5. 命名统一：修复拼写错误、规范 stage/job 名称
6. 迁移友好：保留原目录结构，方便逐个项目替换

二、新结构
- templates/backend.base.yml
- templates/backend.workflow.yml
- templates/frontend.base.yml
- templates/frontend.workflow.yml
- templates/maven-publish.base.yml
- variables/*.yml           后端项目入口
- front/*.yml               前端项目入口
- mvn-push/*.yml            Maven 发布入口

三、优化点
1. 把 secrets 从仓库中删除，改为以下变量注入：
   - SONAR_HOST_URL
   - SONAR_TOKEN
   - DINGTALK_WEBHOOK
   - YAML_CONFIG_REPO_HTTP
   - YAML_CONFIG_REPO_BRANCH
   - YAML_CONFIG_REPO_TOKEN
   - GITLAB_API_TOKEN

2. 把“分支 -> 环境”的逻辑放入 workflow 模板，不再分散在每个项目文件中

3. 统一 job 命名：
   - build_backend
   - sonar_scan
   - notify_quality_gate
   - build_image
   - update_deploy_repo

4. 更新 Dockerfile 写法：
   - 使用 `LABEL` 代替 `MAINTAINER`
   - 参数化 JAR 文件名和 JVM 参数
   - 前端区分根路径部署和子路径部署

5. 对模板仓库本身增加建议：
   - CI lint 校验 YAML
   - 对 scripts 做 basic lint
   - 给每次模板改动打 tag

四、迁移建议
1. 先挑 3 个项目灰度
2. 将旧入口文件切换到新入口文件
3. 验证以下链路：
   - develop 构建是否正常
   - release 镜像是否正确写入配置仓库
   - Sonar 通知是否正常
   - 钉钉通知是否正常
4. 全量替换
