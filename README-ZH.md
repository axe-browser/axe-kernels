# AxeChromium

[English](README.md)

为斧头浏览器（AxeBrowser）提供定制 Chromium 内核。编译产物通过 [GitHub Releases](https://github.com/axe-browser/axe-kernels/releases) 分发。

## 下载

| 版本 | macOS Apple Silicon（arm64） | 发布说明 |
| --- | --- | --- |
| **154.0.8037.17** | [axe-chromium_154.0.8037.17_macos_arm64.dmg](https://github.com/axe-browser/axe-kernels/releases/download/154.0.8037.17/axe-chromium_154.0.8037.17_macos_arm64.dmg) | [发布说明](https://github.com/axe-browser/axe-kernels/releases/tag/154.0.8037.17) |
| **153.0.8010.55** | [axe-chromium_153.0.8010.55_macos_arm64.dmg](https://github.com/axe-browser/axe-kernels/releases/download/153.0.8010.55/axe-chromium_153.0.8010.55_macos_arm64.dmg) | [发布说明](https://github.com/axe-browser/axe-kernels/releases/tag/153.0.8010.55) |

两版均为 **正式 Release**，采用 ad-hoc 签名，已通过本机安装、GUI 启动和正常退出验收。尚未完成 Developer ID 签名、Apple 公证及另一台 Mac 的验收。目前尚未发布 Intel Mac、Windows 或 Linux 包。

## 安装

- **通过 AxeBrowser 安装：** 打开“内核管理”，选择 153 或 154 下载。管理器默认读取本仓库的 [Releases](https://github.com/axe-browser/axe-kernels/releases)，然后校验并安装 TAR.GZ 内核包。
- **独立运行浏览器：** 打开 DMG，将 `Chromium.app` 拖入 Applications。
- **在 AxeBrowser 注册本地内核：** 将 `Chromium.app`、`args.gn` 和两份内核清单一起保存到固定的本地目录，再在“内核管理”中选择其中的 `axe-chromium-kernel.json`。

每个版本的 Assets 提供 DMG 和 TAR.GZ 运行包。GitHub 自动生成的 `Source code (zip/tar.gz)` 是分发仓库快照，不是内核运行包。本仓库只保留英文 README、中文 README 和 LICENSE。

## 校验与许可证

各版本 DMG 和 TAR.GZ 包的 SHA-256 校验值可在对应的 Release Assets 中查看。

Chromium 的许可条款见 [LICENSE](LICENSE)。第三方组件适用各自的许可条款，DMG 中附有 Chromium 许可证与第三方声明文件。
