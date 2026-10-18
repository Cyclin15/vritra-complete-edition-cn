# VRITRA COMPLETE EDITION 简体中文汉化（非官方）

Steam 版《VRITRA COMPLETE EDITION》（Neotro Inc. 出品，Solar2D/Corona 引擎，
Steam appid 892830，游戏版本 1.2.0 rev.560）的完整简体中文本地化工程。

## 下载使用

从本仓库 **Releases** 页面下载 `VRITRA_COMPLETE_EDITION_CN_v1.2.0.zip`，
解压得到 `VritraCompleteEdition` 文件夹，运行其中的 `VritraCompleteEdition.exe` 即可。

- 需要 Steam 客户端在线，且当前 Steam 账户已拥有本作（游戏经 steam_api 校验启动）。
- 也可以用解压出的文件夹直接覆盖 Steam 安装目录下的同名文件夹：
  `.../steamapps/common/VRITRA COMPLETE EDITION/windows_content/VritraCompleteEdition/`

## 汉化范围

| 类别 | 内容 |
|---|---|
| 文本数据 | resource.car 内 Lua 字节码字符串常量（菜单、对话框、提示、成就等全部游戏内文本） |
| 字体 | `Resources/MatryoshkaXS.ttf` 替换为支持中日韩的 zpix 像素字体，风格与原作一致 |
| UI 图片 | 130+ 张 asset_ui 图片重绘（菜单按钮、各窗口标题、武器/难度按钮、排行榜标题等） |
| 精灵图表 | sp_ui_1.png 70 帧（按键提示、关卡标题、难度说明、44 行剧情、7 个 Boss 名）、sp_ending.png 12 帧（双结局文本、最终留言） |

按汉化决定保留原文的内容：STAFF 分类（7 项）与制作人员名单（22 人）、
日文版资源帧。专有名词沿用剧情文本译法（因陀罗、金刚杵；VRITRA / GOLIATH 保留原词）。

## 工程文件说明

使用方法：把本仓库内容整个复制到 `<游戏根目录>/_cn_work/` 下即可运行各脚本
（脚本按 `游戏根目录/_cn_work/xxx.py` 的相对路径定位游戏文件）。

- `translations.py` — 全部译文总表（car 字符串、坐标映射）
- `patch_car.py` + `cartool.py` + `Rtt_Archive.cpp` / `Rtt_Car.cpp` / `lundump_swap.c`
  — resource.car（Lua 字节码）解析与字符串常量替换工具链（替换前校验原文，可重复执行）
- `patch_sprites.py` — 精灵图帧重绘（sp_ui_1 / sp_ending，含全部译文与帧号）
- `render_ui.py` / `render_inplace.py` / `render_howto.py` — asset_ui 图片重绘
- `zpix.ttf` — 替换所用像素字体
- `ui_backup/` — 被修改图片的英文原件（还原用）
- `resource.car.orig` — 原始 resource.car
- `MatryoshkaXS.orig.ttf` — 原始字体
- `all_strings.json` / `corona_tree.json` / `story_ocr2.json` / `ui_dump*.txt` / `story_dump.txt` 等
  — 逆向与 OCR 过程的数据转储
- 其余 `*.py` 为逆向、OCR、点阵转储与验证脚本

## 还原英文原版

1. `resource.car.orig` → 覆盖 `Resources/resource.car`
2. `MatryoshkaXS.orig.ttf` → 覆盖 `Resources/MatryoshkaXS.ttf`
3. `ui_backup/` 内同名文件 → 覆盖回 `Resources/asset_ui/` 与 `Resources/asset/sprites/`

## 声明

本仓库为个人学习与备份用途的民间汉化工程，游戏全部资源版权归
Neotro Inc. 所有。仓库与 Release 附件请勿公开再分发；喜欢本作请购买正版支持开发者。
