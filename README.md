# AxeChromium

[中文](#中文) · [English](#english)

## 中文

为小斧浏览器（AxeBrowser）提供独立的 AxeChromium 内核。完整内核压缩包通过 [GitHub Releases](https://github.com/axe-browser/axe-kernels/releases) 分发。

### 下载

| 内核版本 | macOS Apple Silicon（arm64） | 大小 | 发布说明 |
| --- | --- | --- | --- |
| **154.0.8037.17** | [TAR.GZ](https://github.com/axe-browser/axe-kernels/releases/download/kernel-154.0.8037.17-mac-arm64-preview-r1/chromium_154_mac_arm64.tar.gz) | 239.9 MiB | [Preview r1](https://github.com/axe-browser/axe-kernels/releases/tag/kernel-154.0.8037.17-mac-arm64-preview-r1) |
| **153.0.8010.55** | [TAR.GZ](https://github.com/axe-browser/axe-kernels/releases/download/kernel-153.0.8010.55-mac-arm64-preview-r1/chromium_153_mac_arm64.tar.gz) | 239.1 MiB | [Preview r1](https://github.com/axe-browser/axe-kernels/releases/tag/kernel-153.0.8010.55-mac-arm64-preview-r1) |

两版均为 **Prerelease 测试版**，采用 ad-hoc 签名，已通过本机下载安装、GUI、环境隔离、正常退出和桌面联动验收。尚未完成 Developer ID 签名、Apple 公证及另一台 Mac 的验收。

### 在 AxeBrowser 中安装

1. 打开 AxeBrowser 的“内核管理”。
2. 将[测试版下载目录](https://raw.githubusercontent.com/axe-browser/axe-kernels/main/catalog-prerelease.json)设置为下载源。
3. 选择 153 或 154 下载，客户端会校验并安装完整内核。

每个 Release 另附 SHA-256 校验清单、版本元数据与许可声明。`Source code (zip/tar.gz)` 是 GitHub 自动生成的分发仓库快照；需要运行包时，请下载表中的 **TAR.GZ**。

### 发布与维护

本仓库维护下载目录、发布元数据和工具。内核源码在各自的独立项目维护，编译产物作为 Release assets 上传。

详细流程见[发布说明](docs/publishing.md)。

## English

Independent AxeChromium kernels for AxeBrowser. Complete runtime archives are distributed through [GitHub Releases](https://github.com/axe-browser/axe-kernels/releases).

### Download

| Kernel version | macOS Apple Silicon (arm64) | Size | Release notes |
| --- | --- | --- | --- |
| **154.0.8037.17** | [TAR.GZ](https://github.com/axe-browser/axe-kernels/releases/download/kernel-154.0.8037.17-mac-arm64-preview-r1/chromium_154_mac_arm64.tar.gz) | 239.9 MiB | [Preview r1](https://github.com/axe-browser/axe-kernels/releases/tag/kernel-154.0.8037.17-mac-arm64-preview-r1) |
| **153.0.8010.55** | [TAR.GZ](https://github.com/axe-browser/axe-kernels/releases/download/kernel-153.0.8010.55-mac-arm64-preview-r1/chromium_153_mac_arm64.tar.gz) | 239.1 MiB | [Preview r1](https://github.com/axe-browser/axe-kernels/releases/tag/kernel-153.0.8010.55-mac-arm64-preview-r1) |

Both are **test prereleases** with ad-hoc signing. Local download and installation, GUI, environment isolation, normal shutdown, and desktop integration checks passed. Developer ID signing, Apple notarization, and validation on another Mac have not been completed.

### Install in AxeBrowser

1. Open Kernel Manager in AxeBrowser.
2. Set the [prerelease catalog](https://raw.githubusercontent.com/axe-browser/axe-kernels/main/catalog-prerelease.json) as the download source.
3. Select 153 or 154 to download. The client verifies and installs the complete kernel.

Each Release includes SHA-256 checksums, version metadata, and license notices. GitHub's automatic `Source code (zip/tar.gz)` downloads are snapshots of this distribution repository. Choose **TAR.GZ** in the table for the runtime package.

### Publishing and maintenance

This repository maintains download catalogs, release metadata, and tools. Kernel source is maintained in its own projects, and compiled packages are uploaded as Release assets.

See the [publishing guide](docs/publishing.md) for the detailed workflow.
