# AxeChromium 发布说明 / Publishing guide

[中文](#中文) · [English](#english)

## 中文

`axe-kernels` 是编译产物的独立分发仓库。各 `axe-chromium-N` 项目负责源码、补丁、编译和验收；本仓库维护版本清单、校验信息和 GitHub Releases 下载目录。`axe-desktop` 根据目录中的固定版本地址按需下载、验证和安装内核。

### 目录

```text
axe-kernels/
  catalog.json           正式版下载目录
  catalog-prerelease.json 测试预发布下载目录
  releases/              各候选或已发布版本的元数据
  tools/build_catalog.py 独立目录生成器
  tests/                 发布目录验证
  artifacts/             本地编译归档，Git 忽略
```

Git 跟踪文档、目录、发布元数据和工具。完整 `.tar.gz` 浏览器运行包及其 `.tar.gz.json` 校验清单作为 GitHub Release assets 上传。不要直接提交 Chromium.app、源码 checkout、编译对象或浏览器用户数据。

GitHub 普通 Git 文件上限为 100 MiB，Release 单资产应小于 2 GiB。见 [大文件说明](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) 和 [Release 限额](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)。

### 准备候选包

在相应内核项目运行已有导出器，将输出指向本仓库 `artifacts/` 下的新路径：

```sh
python3 tools/export_kernel.py \
  --source-output /absolute/verified-build-output \
  --output /absolute/axe-kernels/artifacts/chromium_154/154.0.8037.17_r1/AxeChromium-154.0.8037.17-mac-arm64-r1.tar.gz \
  --archive --sign-local
```

此命令属于独立内核项目；本发布仓库不导入其 Python 源码。归档包含完整运行文件、`axe-chromium-kernel.json` 和构建清单，保留 Framework 软链接与可执行权限。生成器拒绝覆盖既有输出。`--sign-local` 生成 ad-hoc 签名的本机验收候选包；完成完整性、安装、GUI 与退出验收后，可按下述测试预发布流程分发。正式发布前还需实现并验收 Developer ID 签名、公证及客户端对最终包的验证流程，再为最终归档重新生成校验清单。

将 sidecar 元数据复制至 `releases/`，增加 `release_tag` 和 `status`。候选状态必须为 `not_published`；完成资产上传和对应下载验收后，才改成 `published`。固定 tag 要包含完整版本、平台和构建修订，例如 `kernel-154.0.8037.17-mac-arm64-r1`；新修订使用新 tag，保留旧资产。

### 正式发布流程

1. 使用公开仓库 [`axe-browser/axe-kernels`](https://github.com/axe-browser/axe-kernels)；本地候选包不会自动上传。
2. 仅对完成正式签名、公证和异机验收的最终归档继续发布；验证最终归档与 sidecar 的 SHA-256、大小、解压布局、实际启动与退出行为，以及许可声明。
3. 在固定 tag 下创建 GitHub Release，上传 `.tar.gz` 和 `.tar.gz.json`。GitHub 自动提供的 Source code ZIP 不是内核运行包。
4. 核对实际下载地址、大小与摘要后，将该 release 元数据标记 `published`。
5. 在本仓库生成新的目录文件，审阅后替换 `catalog.json`，再提交并推送目录更新：

```sh
python3 tools/build_catalog.py \
  --repo axe-browser/axe-kernels \
  --release releases/kernel-154.0.8037.17-mac-arm64-r1.json \
  --output dist/catalog-next.json
```

`--release` 可重复，为不同内核使用不同的固定 Release tag。生成器检查协议、版本、平台、摘要、大小、重复主版本和地址格式，不覆盖已有输出。`not_published` 候选仍可列出，但不会暴露可下载字段。

首次提交并推送 `catalog.json` 后，客户端下载目录可使用稳定的 `https://raw.githubusercontent.com/axe-browser/axe-kernels/main/catalog.json`，每项 `download_url` 则固定指向 `https://github.com/axe-browser/axe-kernels/releases/download/<tag>/<archive>`。不要为内核本身使用 `releases/latest`，它可能切换到其他 Chromium 主版本。

将真实目录地址配置到 AxeBrowser 后，用户点击下载即可获取所选内核，不需要 Git、GitHub CLI 或自己的 GitHub token。当前客户端可手工设置这个目录；默认自动读取远程目录的接入需要在仓库地址和首个实际 Release 确定后完成。

### 当前状态

| 测试版 | 平台 | 下载 |
| --- | --- | --- |
| 153.0.8010.55 · Preview r1 | macOS arm64 | [Release](https://github.com/axe-browser/axe-kernels/releases/tag/kernel-153.0.8010.55-mac-arm64-preview-r1) |
| 154.0.8037.17 · Preview r1 | macOS arm64 | [Release](https://github.com/axe-browser/axe-kernels/releases/tag/kernel-154.0.8037.17-mac-arm64-preview-r1) |

两版已完成现行命名的编译与本机完整包验收，包括真实下载器安装、双环境 GUI 与持久化、正常退出、文件下载和桌面包联动。归档与校验清单作为 Release assets 分发，另附 Chromium 许可证、第三方声明和 SHA-256 清单。

在 AxeBrowser 的内核管理中手动填写[测试版目录](https://raw.githubusercontent.com/axe-browser/axe-kernels/main/catalog-prerelease.json)，即可选择 153 或 154 下载。两版均标记为 **Prerelease**，使用 ad-hoc 签名，尚未完成 Developer ID 签名、Apple 公证或异机验收。`catalog.json` 的正式版目录保持为空。

测试预发布仍需验证归档、签名与运行行为，上传资产并回下载核对后才将元数据改为 `published`，生成 `catalog-prerelease.json`。此状态表示资产已公开可下载；不表示已经完成正式 macOS 签名和公证。每个 Release 同时附上仅包含该版本的 `catalog.json`。正式发布流程的 Developer ID、公证与异机验收要求继续适用。

当前客户端支持 mac-arm64、每个 Chromium 主版本一个下载条目。内核能力统一使用 `AxeChromium*`，构建清单为 `axe-chromium-build.json`，不提供旧名称兼容。内核必须按新命名重新编译后才可发布；公网正式 macOS 分发还需完成 Developer ID 签名、公证、异机验收，并核对 Chromium 与第三方组件的许可声明。

验证工具：`python3 -m unittest discover -s tests -q`。本项目无需相邻源码仓库即可运行目录工具和测试。

## English

`axe-kernels` distributes compiled AxeChromium kernels. Each `axe-chromium-N` project owns its source, patches, builds, and validation. This repository holds release metadata, a download catalog, and publishing tools. AxeBrowser downloads, verifies, and installs a selected kernel from a fixed release URL.

### Repository layout

```text
axe-kernels/
  catalog.json           Stable download catalog
  catalog-prerelease.json Test prerelease download catalog
  releases/              Candidate and published release metadata
  tools/build_catalog.py Catalog generator
  tests/                 Catalog tests
  artifacts/             Local archives; ignored by Git
```

Git tracks documentation, metadata, the catalog, and tools. Upload each complete `.tar.gz` runtime archive and its `.tar.gz.json` checksum sidecar as **GitHub Release assets**. Do not commit the archives, `Chromium.app`, Chromium source, build objects, or browser user data to this repository. GitHub blocks ordinary Git files over 100 MiB, while each Release asset must be smaller than 2 GiB ([large files](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), [Release limits](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)).

### Prepare a candidate

After rebuilding and validating a kernel in its own project, export a complete archive to a new path under this repository's ignored `artifacts/` directory. For example, from the kernel project:

```sh
python3 tools/export_kernel.py \
  --source-output /absolute/verified-build-output \
  --output /absolute/axe-kernels/artifacts/chromium_154/154.0.8037.17_r1/AxeChromium-154.0.8037.17-mac-arm64-r1.tar.gz \
  --archive --sign-local
```

The exporter preserves the complete runtime layout, Framework symlinks, executable permissions, `axe-chromium-kernel.json`, and the build manifest. `--sign-local` creates an ad-hoc signed candidate for local validation. After integrity, installation, GUI, and shutdown validation, it can be distributed through the test prerelease process below. A stable release requires an implemented and validated Developer ID signing and notarization flow, client verification of the final package, and a newly generated checksum sidecar for the final archive. Copy the final sidecar metadata into `releases/`, add `release_tag`, and set `status` to `not_published`. Use a unique, fixed tag containing the full version, platform, and build revision, such as `kernel-154.0.8037.17-mac-arm64-r1`. Never reuse a tag for a changed archive.

### Publish a stable release

1. Publish only the final archive after Developer ID signing, notarization, and validation on another Mac. Verify its sidecar SHA-256, compressed and unpacked sizes, layout, kernel identity, launch and exit behavior, code signature, and applicable Chromium and third-party license notices.
2. Create a GitHub Release in [`axe-browser/axe-kernels`](https://github.com/axe-browser/axe-kernels) under its fixed tag. Upload the `.tar.gz` archive and `.tar.gz.json` sidecar as assets. GitHub's automatically generated “Source code” downloads are not kernel runtime packages.
3. Download the uploaded assets and verify their checksums. Only then change the matching metadata to `published`.
4. Generate and review the next catalog, then replace `catalog.json` and publish that Git change:

```sh
python3 tools/build_catalog.py \
  --repo axe-browser/axe-kernels \
  --release releases/kernel-154.0.8037.17-mac-arm64-r1.json \
  --output dist/catalog-next.json
```

Repeat `--release` for multiple kernel versions. The generator checks protocol, version, platform, hashes, sizes, duplicate major versions, and URL format. It does not overwrite an existing output. A candidate marked `not_published` can appear in the catalog but does not expose a download URL.

After the initial commit containing `catalog.json` is pushed, the stable client catalog URL is `https://raw.githubusercontent.com/axe-browser/axe-kernels/main/catalog.json`. Each published kernel URL points to its own fixed `https://github.com/axe-browser/axe-kernels/releases/download/<tag>/<archive>` asset. Avoid `releases/latest`, which can move to a different Chromium major version. Users can enter the catalog URL in AxeBrowser's Kernel Manager; downloads from a public Release need no GitHub account or token.

### Current status and checks

| Test version | Platform | Download |
| --- | --- | --- |
| 153.0.8010.55 · Preview r1 | macOS arm64 | [Release](https://github.com/axe-browser/axe-kernels/releases/tag/kernel-153.0.8010.55-mac-arm64-preview-r1) |
| 154.0.8037.17 · Preview r1 | macOS arm64 | [Release](https://github.com/axe-browser/axe-kernels/releases/tag/kernel-154.0.8037.17-mac-arm64-preview-r1) |

Both versions were rebuilt with the current naming and passed local package validation, real downloader installation, dual-environment GUI and persistence checks, normal shutdown, file downloads, and packaged desktop integration. Runtime archives and checksum sidecars are Release assets, accompanied by the Chromium license, third-party notices, and SHA-256 checksums.

Manually enter the [prerelease catalog](https://raw.githubusercontent.com/axe-browser/axe-kernels/main/catalog-prerelease.json) in AxeBrowser's Kernel Manager to download either version. Both are marked **Prerelease** and use ad-hoc signing. Developer ID signing, Apple notarization, and validation on another Mac have not been completed. The stable `catalog.json` remains empty.

Test prereleases require archive, signature, and runtime validation. Upload and download-check the assets before setting metadata to `published` and generating `catalog-prerelease.json`. This status means the assets are publicly downloadable; it does not assert completion of formal macOS signing or notarization. Each Release also includes a `catalog.json` containing only its own version. The stable release requirements for Developer ID signing, notarization, and validation on another Mac still apply.

The current client supports macOS arm64 and one catalog entry per Chromium major version. Kernels use `AxeChromium*` capabilities and the `axe-chromium-build.json` manifest.

Run the catalog tests with `python3 -m unittest discover -s tests -q`. They do not require a neighboring source checkout.

[返回下载首页 / Back to downloads](../README.md)
