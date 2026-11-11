# Windows 安装与构建

[简体中文教程](TUTORIAL.zh-CN.md) · [English tutorial](TUTORIAL.en.md) · [历史 Windows 验收](WINDOWS_ACCEPTANCE.md)

## 安装使用

从 [SynthBO Releases](https://github.com/wei-rui499/SynthBO/releases) 下载 `SynthBO-0.2.5-windows-x64-setup-unsigned.exe`，按向导完成安装。安装向导可选择中英文；应用内右上角的 **English / 中文** 按钮单独切换界面语言。

便携版须完整解压 `SynthBO-0.2.5-windows-x64-portable-unsigned.zip`，运行 `SynthBO/SynthBO.exe`，保留旁边的 `_internal` 文件夹。不要单独复制 EXE。应用自带 Python、CPU 科学库、三个预设引擎、离线双语教程及练习数据，无需 WSL、Conda、编译器或 API 账户。实验项目保存在自己选择的文件夹。

## 本次 Windows 包的依据

使用者已确认 GitHub 上的 0.2.4 Windows 包可以运行。本次以该已发布便携包为固定基线，不重新解析或升级科学计算依赖：

- 基线：`NanoBO-0.2.4-windows-x64-portable-unsigned.zip`，SHA-256 `07905f83af0ff4c8586dba1be83e363fb4a70bc61073cc083bf4a91ce3ee8be5`。
- 保留：原生 DLL / PYD、经典科学库、全部非界面冻结模块，以及完整的独立现代 worker。
- 更新：应用版本、主界面、配方对话框、分析图表、语言模块、分发自检代码，以及教程和致谢资源。
- 核对：未修改的冻结模块压缩数据和运行环境文件逐项与基线比对；科学引擎源码与基线源码按统一换行符比对。
- 封装：在原生 Windows x64 上以 CPython 3.10 编译界面，再由固定校验和的 Inno Setup 7.1.1 生成安装器；安装器 AppId 保持稳定。

`WINDOWS_BUILD-0.2.5.json` 内的 `interface_update` 记录基线、修改清单、保留文件计数与摘要。**基线由使用者确认运行成功；新增双语界面和新安装器没有在 Windows 启动或安装测试。** 按使用者安排，Windows 运行验证由其在 Windows 电脑进行。macOS 测试不代替这一步。

安装包未签名，首次安装仍可能出现系统信誉提示。历史 Hotfix1 的 Windows 11 软件验收另见上方链接；这些软件检查使用合成数据，不构成湿实验或算法普遍性能的证据。

## 维护者复现当前发布

原生 Windows x64 安装 CPython 3.10、PyInstaller 6.16.0、Inno Setup 7.1.1。按工作流下载并校验固定的 0.2.4 便携包、Windows 源码和对应库源，执行：

```powershell
python scripts/repack_windows_ui.py --base baseline/NanoBO-0.2.4-windows-x64-portable-unsigned.zip --base-source baseline/NanoBO-0.2.4-windows-source.zip --output dist
# 解压并校验基线 windows-library-sources.zip 到 release/library-sources
python scripts/package_windows.py --compiler 'C:/Program Files/Inno Setup 7/ISCC.exe'
```

完整下载、校验和、封装和草稿上传步骤见 [windows-release.yml](../.github/workflows/windows-release.yml)。该工作流不运行应用、模型或安装器，也不会把构建成功标记为 Windows 运行验收通过。历史兼容性修复工具 `repack_windows_hotfix.py` 的默认行为保留。

需要完整源码重建科学运行库时，另按[开发说明](DEVELOPMENT.md)建立隔离的 Python 3.10 / 3.13 环境、编译依赖与 worker；那会产生新的运行环境，需要单独验收，不能自动沿用本次基线的运行结论。

## 来源与许可

科研模型与算法原作者保留全部归属，见[公开致谢](../ACKNOWLEDGMENTS.md)、[引用指南](HOW_TO_CITE.md)、[第三方说明](../THIRD_PARTY_NOTICES.md)和[上游修改记录](UPSTREAM_MODIFICATIONS.md)。包内许可证及对应 Windows 库源沿用已发布版本；新增界面代码随本次源码发布。
