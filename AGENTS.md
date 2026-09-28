# 内核分发仓库约定

- 本项目只维护已编译内核的发布目录、归档、校验清单和发布工具，不保存或编译 Chromium 源码。
- 内核归档与本地候选包存于 artifacts/，必须被 Git 忽略；编译后的大文件作为 GitHub Release assets 分发。
- 不导入相邻桌面或内核项目源码；输入为各独立内核项目导出的完整归档和校验清单。
- 未确认上传成功的文件不得写成公开已发布条目；下载地址使用固定版本 Release tag。
- 本机验收的测试包使用 GitHub Prerelease 和 catalog-prerelease.json；发布说明明确 ad-hoc 签名、公证与异机验收状态，正式目录不混入测试包。
- 保留每个 Chromium 主版本一个当前下载条目，不自动替换已有用户环境的版本。
- 保留 SHA-256、下载/解压大小、平台、版本和 axe-chromium-features-v1 协议检查。
- 不覆盖已有归档或用户改动，不记录凭证；未经明确要求不 commit、push、创建分支或发布 Release。
- 修改后运行相关单测，说明本机签名、公证与异机验收状态。
- 项目源码、元数据和文档统一使用 AxeBrowser/AxeChromium 命名，不提供旧名称兼容；构建清单必须为 axe-chromium-build.json，能力前缀必须为 AxeChromium。
- 自定义编译和打包输出目录使用小写 snake_case，不加产品名称前缀；平台标准路径按运行格式保持。
