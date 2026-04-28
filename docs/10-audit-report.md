# pipeline-better 体检报告

体检时间：本次会话

结论：
- 当前仓库未发现占位脏文本残留
- 未发现空文件
- YAML 可解析：70/70 通过
- Python 语法检查：3/3 通过
- 发现并已修复一个关键设计问题：模板仓库被业务仓库 include 后，job 在业务仓库工作区执行，因此不能直接依赖模板仓库内的 `dockerfile/` 和 `scripts/` 本地文件

已修复项：
1. 修复 `templates/backend.base.yml` 被误写成占位文本的问题
2. 修复 `templates/frontend.base.yml` 被误写成占位文本的问题
3. 修复模板资产获取方式：
   - 后端 Dockerfile 改为优先通过 GitLab API 从模板仓库拉取
   - Sonar 通知脚本改为优先通过 GitLab API 从模板仓库拉取
   - 前端 Dockerfile 和 nginx conf 改为优先通过 GitLab API 从模板仓库拉取
4. 补充模板仓库定位变量，并统一默认引用版本为 `release`：
   - `TEMPLATE_PROJECT_PATH_ENCODED`
   - `TEMPLATE_REF`

说明：
- `include: local:` 在 GitLab CI 中是“相对仓库根目录”而不是“相对当前文件路径”。
- 因此 `include: local: 'templates/backend.base.yml'` 这种写法本身没有问题。
- 体检程序若按文件相对路径去推断 include，会产生假阳性，这不属于真实缺陷。

仍需你在真实环境确认的运行条件：
1. `CI_JOB_TOKEN` 是否有权限读取 `ci-templates/pipeline-better` 仓库 raw 文件/API 文件内容
2. `TEMPLATE_PROJECT_PATH_ENCODED` 是否与你 GitLab 上真实项目路径一致
3. 业务仓库 include 的 `ref` 是否与模板内 `TEMPLATE_REF` 保持一致（当前验证通过的是 `main`）
4. `YAML_CONFIG_REPO_HTTP`、`YAML_CONFIG_REPO_TOKEN`、`SONAR_TOKEN`、`DINGTALK_WEBHOOK` 是否已配置
5. workflow 注入的 `RUNNER_TAG` 是否与真实环境一致

建议：
- 首批灰度前，先用一个测试项目验证模板仓库文件拉取是否成功
- 如果 `CI_JOB_TOKEN` 跨项目读模板仓库受限，则需要在 GitLab 上放开 Job Token allowlist，或改成 deploy token / project access token 方案
