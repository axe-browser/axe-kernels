# AxeChromium

[中文文档](README-ZH.md)

Customized Chromium kernels for AxeBrowser. Download compiled packages from [GitHub Releases](https://github.com/axe-browser/axe-kernels/releases).

## Download

| Version | macOS Apple Silicon (arm64) | Release |
| --- | --- | --- |
| **154.0.8037.17** | [axe-chromium_154.0.8037.17_macos_arm64.dmg](https://github.com/axe-browser/axe-kernels/releases/download/154.0.8037.17/axe-chromium_154.0.8037.17_macos_arm64.dmg) | [Release notes](https://github.com/axe-browser/axe-kernels/releases/tag/154.0.8037.17) |
| **153.0.8010.55** | [axe-chromium_153.0.8010.55_macos_arm64.dmg](https://github.com/axe-browser/axe-kernels/releases/download/153.0.8010.55/axe-chromium_153.0.8010.55_macos_arm64.dmg) | [Release notes](https://github.com/axe-browser/axe-kernels/releases/tag/153.0.8010.55) |
| **152.0.7977.141** | [axe-chromium_152.0.7977.141_macos_arm64.dmg](https://github.com/axe-browser/axe-kernels/releases/download/152.0.7977.141/axe-chromium_152.0.7977.141_macos_arm64.dmg) | [Release notes](https://github.com/axe-browser/axe-kernels/releases/tag/152.0.7977.141) |
| **151.0.7922.226** | [axe-chromium_151.0.7922.226_macos_arm64.dmg](https://github.com/axe-browser/axe-kernels/releases/download/151.0.7922.226/axe-chromium_151.0.7922.226_macos_arm64.dmg) | [Release notes](https://github.com/axe-browser/axe-kernels/releases/tag/151.0.7922.226) |

All versions are **regular Releases** and use ad-hoc signing. Local installation, GUI and shutdown checks passed. Developer ID signing, Apple notarization and validation on another Mac have not been completed. Intel Mac, Windows and Linux packages have not been published.

## Installation

- **Install through AxeBrowser:** open Kernel Manager, select 151, 152, 153 or 154, and download. The manager reads this repository's [Releases](https://github.com/axe-browser/axe-kernels/releases) by default, then verifies and installs the TAR.GZ package.
- **Run as a standalone browser:** open the DMG and copy `Chromium.app` to Applications.
- **Register a local kernel in AxeBrowser:** keep `Chromium.app`, `args.gn` and both kernel manifests together in a permanent local directory, then select its `axe-chromium-kernel.json` in Kernel Manager.

Each version's Assets contains a DMG and a TAR.GZ runtime package. GitHub's automatic `Source code (zip/tar.gz)` downloads are repository snapshots, not runtime packages. The repository contains only this README, the Chinese README and LICENSE.

## Checksums and licenses

The SHA-256 checksums for each version's DMG and TAR.GZ packages are available in its Release Assets.

See [LICENSE](LICENSE) for Chromium's license. Third-party components retain their own licenses. The DMG includes the Chromium license and third-party credits files.
