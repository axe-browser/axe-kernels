# AxeChromium

[中文文档](README-ZH.md)

Customized Chromium kernels for AxeBrowser. Download compiled packages from [GitHub Releases](https://github.com/axe-browser/axe-kernels/releases).

## Download

| Version | macOS Apple Silicon (arm64) | Release |
| --- | --- | --- |
| **154.0.8037.17** | [axe-chromium_154.0.8037.17_macos_arm64.dmg](https://github.com/axe-browser/axe-kernels/releases/download/kernel-154.0.8037.17-mac-arm64-preview-r1/axe-chromium_154.0.8037.17_macos_arm64.dmg) | [Release notes](https://github.com/axe-browser/axe-kernels/releases/tag/kernel-154.0.8037.17-mac-arm64-preview-r1) |
| **153.0.8010.55** | [axe-chromium_153.0.8010.55_macos_arm64.dmg](https://github.com/axe-browser/axe-kernels/releases/download/kernel-153.0.8010.55-mac-arm64-preview-r1/axe-chromium_153.0.8010.55_macos_arm64.dmg) | [Release notes](https://github.com/axe-browser/axe-kernels/releases/tag/kernel-153.0.8010.55-mac-arm64-preview-r1) |

Both versions are **test prereleases** with ad-hoc signing. Local installation, GUI and shutdown checks passed. Developer ID signing, Apple notarization and validation on another Mac have not been completed. Intel Mac, Windows and Linux packages have not been published.

## Installation

- **Manual download:** open the DMG and copy `Chromium.app` to Applications. The image also includes the complete kernel manifests and license notices.
- **Install through AxeBrowser:** open Kernel Manager, set the [prerelease catalog](https://github.com/axe-browser/axe-kernels/releases/download/kernel-catalog/catalog-prerelease.json) as the download source, then select 153 or 154. The manager downloads and verifies the TAR.GZ package.

Each version's Assets contains a DMG and a TAR.GZ runtime package. GitHub's automatic `Source code (zip/tar.gz)` downloads are repository snapshots, not runtime packages. The repository contains only this README, the Chinese README and LICENSE.

## Checksums and licenses

The [download catalog Release](https://github.com/axe-browser/axe-kernels/releases/tag/kernel-catalog) provides catalogs, package metadata, SHA-256 checksums and third-party notices for both versions.

See [LICENSE](LICENSE) for Chromium's license. Third-party components retain their own licenses; the DMG and catalog Release include the corresponding notices.
