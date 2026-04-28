# Jenkins 历史链路说明

原仓库中的 `Jenkinsfile` 属于历史遗留发布链路，不建议继续作为主链维护。

保留它的原因：
- 便于追溯 Jenkins -> GitLab CI 的演进历史
- 便于对照某些早期部署步骤

不建议继续使用它的原因：
- 凭据、环境和部署方式已偏老
- 与当前 GitLab CI 模板体系并存会增加理解成本
- 生产迁移应统一落到 GitLab CI 模板仓库

建议：
- 仅作为参考，不再在新仓库中恢复 Jenkinsfile 执行
- 如果必须保留，建议单独移到 `legacy/jenkins/` 目录并加 README
