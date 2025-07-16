# 📷 Anamorphic Lens Photo Restoration Tool  
> 变形镜头照片还原工具（支持 RAW/JPG/PNG，图形界面批量横向还原）  
> Produced by Michael Chen | Email: michaelchen2025@163.com

---

## 🧩 简介 | Introduction

该工具用于还原使用变形镜头（Anamorphic Lens）拍摄后横向拉伸的照片。  
支持 Sony ARW、Nikon NEF、Panasonic RW2 以及 JPG/PNG 等格式，适用于摄影后期。

This GUI-based tool batch processes horizontally stretched images taken with anamorphic lenses.  
It supports various RAW and standard image formats, customizable stretch ratios, and multi-threaded processing.

---

## 🆚 版本对比 | Version Comparison

| 功能 / 版本                | v1.0 初始版本                             | ✅ v1.1 最新稳定发行版                         |
|----------------------------|------------------------------------------|------------------------------------------|
| 图像格式支持               | ✅ ARW/NEF/RW2/JPG/PNG                    | ✅ 相同                                  |
| 输出格式                   | PNG / JPEG / TIFF                        | ✅ 相同                                  |
| 变形倍率选择               | 固定倍率（1.33 / 1.5 / 1.55 / 2.0）      | ✅ 支持自定义倍率 + 自动保存             |
| 比例检测建议               | ❌ 无                                     | ✅ 自动识别图像比例并弹窗建议倍率        |
| 多线程处理                 | ✅ 支持                                   | ✅ 加强稳定性，日志异步处理              |
| 取消按钮                   | ❌ 无                                     | ✅ 可随时终止批处理                      |
| 日志显示                   | 有，但较简洁                             | ✅ 增加时间戳，反馈更清晰                |
| 打赏码功能                 | ✅ 支持基本展示                           | ✅ 点击可放大预览，支持更多格式          |
| 安装方式                   | Inno Setup 安装包                        | ✅ 相同                                  |
| 推荐使用                   | ❌ 学习体验                               | ✅ 推荐安装使用                         |

---

## 🧠 开发背景与实现思路 | Background & Implementation

### 🎬 开发初衷

作为一名变形宽荧幕镜头（Anamorphic Lens）爱好者，我发现市面上缺乏简单、高效、支持 RAW 的图像还原工具。  
为了方便自己与社区使用，我用 Python 自主开发了这个免费工具，并计划将其逐步拓展到视频还原。

---

### 🧰 使用语言与核心库

- **语言**：Python 3.x
- **图像处理**：
  - `rawpy`：读取 RAW 格式（.arw/.nef/.rw2）
  - `Pillow`：图像打开、缩放、保存
- **界面构建**：
  - `tkinter` / `ttk`：图形界面组件
- **系统交互**：
  - `threading`：多线程处理图像防卡顿
  - `platform`：跨平台打开文件夹

---

### 🧩 实现逻辑简述（伪代码）

```python
GUI启动：
    等待用户选择输入文件夹
    提供倍率选择（可自定义）与输出格式
    点击开始处理后：
        遍历所有图像文件
        RAW 图像用 rawpy 解码，JPG/PNG 用 Pillow 打开
        横向拉伸并保存到 Output 文件夹
        实时更新进度与日志
```
## 🧭 安装方法 | Installation

### ✅ Windows 安装（推荐）

1. 前往 [Releases 页面](https://github.com/MichaelChen2025/Anamorphic-Lens-Photo-Restoration-Tool/releases/)下载最新版安装包；
2. 运行安装程序（如 `AnamorphicRestore_v1.1_Setup.exe`）；
3. 安装完成后可从桌面或开始菜单启动软件。

> ⚠️ 若安装受限，请右键选择“以管理员身份运行”。

---

## 🚀 使用说明 | Usage

1. 选择输入图像所在文件夹；
2. 设置横向拉伸还原倍率（可自定义）；
3. 选择输出格式（PNG / JPEG / TIFF）；
4. 点击“开始处理图像”，等待进度完成；
5. 点击“打开输出文件夹”查看结果。

---

## 📷 支持格式 | Supported Formats

- **输入格式**：`.arw`, `.nef`, `.rw2`, `.jpg`, `.jpeg`, `.png`
- **输出格式**：`.png`, `.jpeg`, `.tiff`

---

## 📦 Releases 下载 | Latest Versions

| 版本号 | 文件名 | 日期 | 下载链接 |
|--------|--------|------|-----------|
| v1.1   | `AnamorphicRestore_v1.1_Setup.exe` | 2025-07-17 | [📥 点此下载](https://github.com/MichaelChen2025/Anamorphic-Lens-Photo-Restoration-Tool/releases/tag/v1.1) |
| v1.0   | `AnamorphicRestore_v1.0_Setup.exe` | 2025-07-16 | [📥 点此下载](https://github.com/MichaelChen2025/Anamorphic-Lens-Photo-Restoration-Tool/releases/tag/v1.0) |

---

## ❤️ 打赏支持作者 | Support the Author

程序右侧展示了作者的收款二维码，点击可放大预览。  
如你觉得本工具对你有帮助，欢迎小额打赏支持我继续开发！

---

## 📄 License | 许可证

**MIT License (with Non-Commercial Clause)**  
Copyright (c) 2025 Michael Chen

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the “Software”), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, and distribute copies of the Software,  
subject to the following conditions:

⚠️ **The Software may NOT be used, distributed, or integrated for commercial purposes**  
**without the express written permission of the author (Michael Chen, michaelchen2025@163.com).**

The above copyright notice and this permission notice shall be included in all  
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
SOFTWARE.

MIT 许可证（仅限非商业用途）

版权所有 (c) 2025 Michael Chen

在遵守以下条件的前提下，特此免费授权任何人获得本软件及相关文档文件（以下简称“软件”）的副本，以无限制地使用本软件，包括但不限于使用、复制、修改、合并、发布、分发、再许可和/或出售软件的副本。

⚠️ 但本软件**不得用于商业目的**，除非事先获得原作者 Michael Chen 的**书面授权**。  
商业目的包括但不限于：
- 将本软件整合入任何商业产品；
- 用于付费服务、商业演示或销售；
- 修改后作为新软件用于盈利或销售。

如需商业授权，请联系作者：michaelchen2025@163.com

以上版权声明和本许可声明应包含在本软件的所有副本或主要部分中。

本软件按“原样”提供，不提供任何形式的明示或暗示的担保，包括但不限于对适销性、特定用途适用性及不侵权的担保。在任何情况下，作者或版权持有人均不对因软件或软件的使用或其他交易而产生的任何索赔、损害或其他责任负责，无论是在合同诉讼、侵权行为或其他方面。
