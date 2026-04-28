# pipeline-better 故障排查手册

这份文档用于排查 `pipeline-better` 在真实使用中的常见问题。

适用范围：
- 后端流水线
- 前端流水线
- Maven 发布流水线

目标：
- 快速判断失败点在哪一层
- 按固定顺序排查，避免一上来就到处翻日志
- 总结当前模板最常见的故障模式

---

# 一、先按 4 层定位问题

遇到 pipeline 失败时，先不要急着看单个命令报错。
建议先判断故障属于哪一层：

1. 触发层
- pipeline 有没有生成
- 哪些 job 根本没出现

2. 调度层
- job 有没有 runner 执行
- 是 pending 还是 running 后失败

3. 执行层
- job 内命令是否报错
- 失败是构建、下载、推镜像、发通知还是更新配置

4. 外部依赖层
- Sonar、GitLab API、Harbor、deployment-config、钉钉、runner 权限是否正常

大多数排查，按这个顺序会更快。

---

# 二、先看 pipeline 是否生成正确

## 场景 1：提交后根本没有生成想要的 pipeline

重点检查：
1. 业务仓库 `.gitlab-ci.yml` 的 include 是否正确
2. include 的 `project/ref/file` 是否正确
3. `workflow.rules` 是否匹配当前分支

当前模板常见分支映射：
- 后端：feature / feature_test / develop / release / platform / vintage
- 前端：feature / develop / release / platform
- Maven 发布：develop

典型现象：
- 你提交了一个分支，但相关 job 没有出现

排查顺序：
1. 看当前分支名是不是模板支持的格式
2. 看 workflow 里有没有这条分支规则
3. 看 job 自己的 `rules` 是否额外过滤掉了它

典型原因：
- 分支名不匹配正则
- `PIPELINE_MODE` 没被注入
- job 的 `rules` 比 workflow 更严格

---

# 三、job 一直 pending，不执行

## 场景 2：job 卡在 pending

最常见原因：runner tag 不匹配。

当前模板直接在 workflow rules 里注入最终的 `RUNNER_TAG`。
当前已验证的后端/前端链路使用：
- `RUNNER_TAG=generic-runner-k8s`

排查顺序：
1. 看 job 页面显示的 tags 是什么
2. 看 `templates/backend.workflow.yml` / `templates/frontend.workflow.yml` 当前给匹配分支注入了哪个 `RUNNER_TAG`
3. 看 runner 实际是否在线
4. 看 runner 是否真的绑定了这个 tag
5. 看 runner 是否允许当前项目/分组使用

典型现象：
- pipeline 创建了
- job 不报错，但就是不跑

处理建议：
- 如果后续要改成变量化 runner tag，必须同步改 workflow 和文档
- 当前版本先以 workflow 中显式写死的 `RUNNER_TAG` 为准

---

# 四、模板仓库文件拉取失败

## 场景 3：prepare_dockerfile 或脚本下载失败

当前模板会通过 GitLab API 下载：
- Dockerfile
- Sonar 通知脚本
- 前端 nginx 配置

典型命令类似：
```bash
curl --fail --header "JOB-TOKEN: $CI_JOB_TOKEN" ... ref=${TEMPLATE_REF}
```

重点检查 4 个变量：
1. `CI_JOB_TOKEN`
2. `TEMPLATE_PROJECT_PATH_ENCODED`
3. `TEMPLATE_REF`
4. `dockerfile_name` / `index_conf`

常见原因：
1. `CI_JOB_TOKEN` 没有跨项目读取模板仓库权限
2. 模板仓库项目路径 URL 编码不对
3. `TEMPLATE_REF` 指到了不存在的分支
4. 指定文件名在模板仓库里不存在

排查顺序：
1. 看日志里 GitLab API 返回的是 404、403 还是 401
2. 403/401：优先怀疑权限
3. 404：优先怀疑路径、ref、文件名写错
4. 看业务仓库 include 的 `ref` 是否与 `TEMPLATE_REF` 一致

处理建议：
- 在 GitLab 上确认 Job Token allowlist
- 优先把 include ref 和 `TEMPLATE_REF` 统一
- 文件名尽量在入口文件中显式写清楚

---

# 五、Maven 构建失败

## 场景 4：build_backend 失败

典型失败点：
- 依赖下载失败
- Java/Maven 环境问题
- 单元测试失败
- 代码编译失败

排查顺序：
1. 看 Maven 最后一段报错，不要只看 job 标题
2. 判断是依赖问题、测试问题还是编译问题
3. 看 `skip_mvn_test` 当前值是什么
4. 看 runner 网络是否能访问依赖仓库

常见原因：
- 私服不可达
- pom 变更后依赖冲突
- 分支规则让 `skip_mvn_test=false`，导致测试失败

处理建议：
- 先区分“测试失败”和“编译失败”
- 如果只是临时验证链路，可以先在测试分支用 `skip_mvn_test: 'true'`
- 但不要长期绕过真正的编译/测试问题

---

# 六、Sonar 相关失败

## 场景 5：sonar_scan 失败

重点检查：
- `SONAR_HOST_URL`
- `SONAR_TOKEN`
- runner 到 Sonar 的网络连通性

模板行为：
- `sonar_scan` 当前是 `allow_failure: true`
- 所以它失败不一定会让整条 pipeline 红掉

常见原因：
1. Token 没配置
2. Token 失效
3. Sonar 服务不可达
4. 项目 key 冲突或策略问题

排查顺序：
1. 日志里先看是否有 `test -n "$SONAR_HOST_URL"` 或 `test -n "$SONAR_TOKEN"` 失败
2. 如果变量存在，再看 `sonar-scanner` 具体错误
3. 区分是认证失败、网络失败还是质量门禁失败

## 场景 6：notify_quality_gate 失败

重点检查：
- `CI_JOB_TOKEN` 是否能拉到 `sonarqube_notify.py`
- Python 镜像是否可用
- `skip_sonarqube_err` 是否配置符合预期

常见原因：
- 下载脚本失败
- Sonar 项目名与脚本查询参数不一致
- 脚本运行异常

---

# 七、Kaniko 构建镜像失败

## 场景 7：build_image / build_frontend_image 失败

重点检查：
1. `target/Dockerfile` 是否真的准备好了
2. 构建上下文中所需文件是否存在
3. Harbor 地址、权限、命名空间是否正确
4. Dockerfile 本身是否引用了不存在的文件

后端常见检查点：
- `target/APP.jar` 是否存在
- `build_backend` 的 artifacts 是否产出了完整 `target/`
- Dockerfile 中 `COPY ${APP_JAR} /data/target/APP.jar` 对应文件是否真的在构建上下文中

前端常见检查点：
- `dist` 是否生成成功
- `index.conf` 是否下载成功
- 子路径参数 `Dir` 是否正确

常见原因：
1. 前置 job 没产出构建文件或 artifacts 不完整
2. Dockerfile 路径错
3. Harbor 权限问题
4. 镜像仓库路径不对
5. 把 `target/` 这类本次构建产物错误地当成 cache 共享，导致并发流水线下内容不符合预期

排查顺序：
1. 先看 `prepare_dockerfile` 是否成功
2. 再看构建上下文里的文件是否齐全
3. 再看 Kaniko 最后的 push 错误
4. 若是权限问题，重点看 Harbor 认证

---

# 八、通知失败

## 场景 8：notify_failure / notify_success 失败

重点检查：
- `DINGTALK_WEBHOOK`
- runner 网络是否能访问钉钉

模板行为：
- 通知不是主流程的核心业务逻辑
- 但失败会影响你对状态的感知

常见原因：
1. webhook 未配置
2. webhook 已失效
3. 钉钉关键词或安全策略拦截
4. runner 外网访问受限

排查顺序：
1. 看 `test -n "$DINGTALK_WEBHOOK"` 是否失败
2. 看 curl 返回值和响应体
3. 如果有钉钉安全策略，确认消息内容是否命中限制

---

# 九、deployment-config 更新失败

## 场景 9：update_deploy_repo / update_frontend_deploy_repo 失败

重点检查：
- `YAML_CONFIG_REPO_HTTP`
- `YAML_CONFIG_REPO_TOKEN`
- `YAML_CONFIG_REPO_BRANCH`
- `DEPLOY_CONFIG_PROJECT_PATH`
- `image_env`

常见原因：
1. clone 仓库失败
2. token 权限不足
3. 目标路径不存在
4. `kustomize edit set image` 执行失败
5. git push 被保护分支策略拦截

排查顺序：
1. 先看是 clone 失败、cd 失败还是 push 失败
2. 如果是 `cd deployment-config/...` 失败，优先怀疑目录路径变量错了
3. 如果是 push 失败，优先怀疑 token 权限或保护分支策略
4. 如果日志显示 `no diff, skip push`，说明不是失败，而是没有实际变更

典型变量关系：
- 后端：`DEPLOY_CONFIG_PROJECT_PATH` 决定服务目录
- 前端：当前主要用 `front/${image_env}/${PROJECT_NAME}`

处理建议：
- 项目目录名不规则时，显式配置 `DEPLOY_CONFIG_PROJECT_PATH`
- 首次接入项目时，先人工确认 deployment-config 中真实路径

---

# 十、前端子路径项目失败

## 场景 10：前端子路径部署构建异常

重点检查：
- `SUBPATH_ENABLED`
- `Dir`
- `dockerfile_name`
- `index_conf`

常见原因：
1. 应该用 `Dockerfile.frontend-subpath` 却用了普通 nginx Dockerfile
2. `index-subpath.conf` 没配置
3. `Dir` 没传，导致 build arg 不完整

排查顺序：
1. 看入口文件是不是子路径模板
2. 看日志里是否生成了 `EXTRA_ARGS="--build-arg dir=..."`
3. 看最终构建命令是否真的带上了 `--build-arg dir=...`

---

# 十一、Maven 多模块发布失败

## 场景 11：mvn-push 并行发布失败

当前做法：
- `parallel.matrix`
- 每个 `path` 代表一个模块目录

重点检查：
- `path` 是否真实存在
- 模块 pom 是否能独立 deploy
- develop 分支规则是否命中

常见原因：
1. 某个模块目录名写错
2. 模块本身 deploy 需要的配置缺失
3. 不是 develop 分支，job 根本没执行

排查顺序：
1. 看失败的是哪个 matrix 子任务
2. 看对应 `path` 是哪个模块
3. 进入该模块看是否能单独执行 `mvn clean deploy`

---

# 十二、最推荐的排查顺序

当你以后看到一条 pipeline 失败，建议固定按这个顺序看：

1. 看失败的是哪个 job
2. 看这个 job 属于哪一层：
   - 触发
   - runner
   - 执行命令
   - 外部依赖
3. 看这个 job 依赖哪些变量
4. 看这个 job 的前置 job 是否成功
5. 最后再看具体命令最后 20~50 行日志

不要一上来从头翻完整日志。
优先看：
- 最后报错
- 当前 job 的输入变量
- 前置 job 是否产出成功

---

# 十三、建议长期补充的排查能力

后续如果你继续维护这套模板，建议逐步补这些能力：

1. 在关键 job 开头打印关键变量
- 例如：
  - `echo $CI_COMMIT_BRANCH`
  - `echo $image_env`
  - `echo $dockerfile_name`
  - `echo $SERVICE_NAME`

2. 在下载模板资产前打印最终下载 URL
- 方便定位是路径问题还是权限问题

3. 在更新 deployment-config 前打印目标目录
- 方便定位 `DEPLOY_CONFIG_PROJECT_PATH` 是否有问题

4. 在失败通知中补关键上下文
- 比如失败 job 名称、环境名

---

# 十四、当前模板最容易出现的 10 个故障模式

1. runner tag 不匹配 -> job pending
2. Job Token 无跨项目权限 -> 下载模板文件失败
3. include ref 与 TEMPLATE_REF 不一致 -> 版本漂移
4. dockerfile_name 写错 -> prepare_dockerfile 失败
5. dist / jar 未生成 -> Kaniko build 失败
6. Harbor 权限或地址异常 -> 镜像 push 失败
7. Sonar token 缺失 -> sonar_scan 失败
8. deployment-config token 无权限 -> clone/push 失败
9. 部署目录变量不对 -> `cd deployment-config/...` 失败
10. 子路径前端没传 `Dir` -> 前端镜像构建不符合预期

---

# 十五、结论

这套模板的排查核心，不是记住所有命令，
而是先判断失败点到底属于哪一层：

1. 没触发
2. 没 runner
3. 命令失败
4. 外部系统失败

把层次分清楚后，再回头看变量，就能快很多。
