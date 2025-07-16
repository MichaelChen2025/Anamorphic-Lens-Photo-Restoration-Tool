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
