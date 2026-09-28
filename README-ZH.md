# AxeChromium

[English](README.md)

为小斧浏览器（AxeBrowser）提供定制 Chromium 内核。编译产物通过 [GitHub Releases](https://github.com/axe-browser/axe-kernels/releases) 分发。

## 下载

| 版本 | macOS Apple Silicon（arm64） | 发布说明 |
| --- | --- | --- |
| **154.0.8037.17** | [axe-chromium_154.0.8037.17_macos_arm64.dmg](https://github.com/axe-browser/axe-kernels/releases/download/kernel-154.0.8037.17-mac-arm64-preview-r1/axe-chromium_154.0.8037.17_macos_arm64.dmg) | [发布说明](https://github.com/axe-browser/axe-kernels/releases/tag/kernel-154.0.8037.17-mac-arm64-preview-r1) |
| **153.0.8010.55** | [axe-chromium_153.0.8010.55_macos_arm64.dmg](https://github.com/axe-browser/axe-kernels/releases/download/kernel-153.0.8010.55-mac-arm64-preview-r1/axe-chromium_153.0.8010.55_macos_arm64.dmg) | [发布说明](https://github.com/axe-browser/axe-kernels/releases/tag/kernel-153.0.8010.55-mac-arm64-preview-r1) |

两版均为 **Prerelease 测试版**，采用 ad-hoc 签名，已通过本机安装、GUI 启动和正常退出验收。尚未完成 Developer ID 签名、Apple 公证及另一台 Mac 的验收。目前尚未发布 Intel Mac、Windows 或 Linux 包。

## 安装

- **手动下载：**打开 DMG，将 `Chromium.app` 拖入 Applications。镜像还包含完整内核清单和许可声明。
- **通过 AxeBrowser 安装：**打开“内核管理”，将[测试版下载目录](https://github.com/axe-browser/axe-kernels/releases/download/kernel-catalog/catalog-prerelease.json)设为下载源，再选择 153 或 154。管理器会下载并校验 TAR.GZ 内核包。

每个版本的 Assets 提供 DMG 和 TAR.GZ 运行包。GitHub 自动生成的 `Source code (zip/tar.gz)` 是分发仓库快照，不是内核运行包。本仓库只保留英文 README、中文 README 和 LICENSE。

## 校验与许可证

[下载目录 Release](https://github.com/axe-browser/axe-kernels/releases/tag/kernel-catalog) 提供两版的下载目录、包元数据、SHA-256 校验清单及第三方声明。

Chromium 的许可条款见 [LICENSE](LICENSE)。第三方组件适用各自的许可条款，DMG 与下载目录 Release 中附有对应声明。
