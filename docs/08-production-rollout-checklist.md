# 生产迁移执行清单

一、切换前
- [ ] 在测试组或沙箱组创建 pipeline-better 仓库
- [ ] 导入 templates / variables / front / mvn-push / dockerfile / scripts
- [ ] 在 GitLab 配置必需 CI 变量
- [ ] 确认 runner tag 存在
- [ ] 确认 Harbor、Sonar、deployment-config 仓库权限正常

二、灰度验证
- [ ] 选择 1 个后端项目切换 include
- [ ] develop 分支验证 build -> sonar -> image -> update_deploy_repo
- [ ] release 分支验证 image_env=uat
- [ ] 失败通知和成功通知验证
- [ ] 选择 1 个前端项目验证根路径部署
- [ ] 选择 1 个前端项目验证子路径部署
- [ ] 选择 1 个 maven-publish 项目验证 parallel 发布

三、批量切换
- [ ] 按业务域分批替换 include 路径
- [ ] 每批控制在 3~5 个项目
- [ ] 每批切换后观察 1~2 天

四、回滚策略
- [ ] 如遇问题，业务仓库 include 直接切回旧仓库路径
- [ ] 保留旧模板仓库直到全部项目稳定运行两周以上
