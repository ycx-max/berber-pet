# berber

一对牵手相伴的 Q 版情侣桌面宠物，适用于支持本地自定义宠物的 Codex 桌面应用。浅蓝衣男生与粉衣女生一起待机、挥手、跳跃，陪你完成每天的工作。

A hand-holding chibi couple companion for the Codex desktop app, with nine animation states and a transparent spritesheet.

![berber 动画预览](assets/preview.gif)

## 安装

1. 下载本仓库：点击 **Code → Download ZIP**，然后解压。
2. 打开应用的 **设置 → Mini 与虚拟宠物**（部分版本显示为 **Pets / 宠物**），使用自定义宠物的 **打开文件夹** 找到本地宠物目录。
3. 将仓库中的 **`berber` 文件夹**复制进去。最终目录应为 `pets/berber/pet.json` 和 `pets/berber/spritesheet.webp`。
4. 回到宠物设置，点击 **刷新**，选择 **berber**。如果当前隐藏了宠物，先显示宠物。

默认宠物目录是 Windows 的 `%USERPROFILE%\.codex\pets` 或 macOS / Linux 的 `~/.codex/pets`。如果设置过 `CODEX_HOME`，则使用该目录下的 `pets`。以应用“打开文件夹”显示的实际位置为准。

不要把整个仓库套在 `pets` 里；`pet.json` 必须直接位于 `pets/berber/` 下。刷新后未出现时，可重启应用再检查。

## 动画

| 状态 | 帧数 | 动作 |
| --- | ---: | --- |
| idle | 6 | 呼吸、眨眼 |
| running-right | 8 | 一起向右移动 |
| running-left | 8 | 一起向左移动 |
| waving | 4 | 挥手打招呼 |
| jumping | 5 | 一起跳跃 |
| failed | 8 | 失落与相互陪伴 |
| waiting | 6 | 等待输入或确认 |
| running | 6 | 专注工作与思考 |
| review | 6 | 查看结果 |

共 **9 组、57 帧**。图集为透明 WebP，尺寸 **1536 × 1872**，采用 **8 列 × 9 行**，每格 **192 × 208**。未使用的单元格保持完全透明。这是 8×9 的旧版图集格式，`pet.json` 未声明 v2；不要直接标记为 `spriteVersionNumber: 2`。

![动画总览](assets/contact-sheet.png)

## 修改与检查

使用 Python 3.10 或更高版本：

```text
python -m pip install -r requirements.txt
python tools/validate_pet.py
```

检查器验证配置文件、图集尺寸、57 个有效帧、15 个空白单元格，以及完全透明像素的颜色残留。它不代替对人物一致性、动作方向和循环效果的视觉检查。

修改图集后，可重新生成仓库中的演示动画：

```text
python tools/render_preview.py
```

如果制作自己的角色，建议同时修改文件夹名、`pet.json` 的 `id`、`displayName` 和描述，便于区分不同宠物。

## 制作来源

角色由作者提供的情侣合照转化为 Q 版形象，通过 hatch-pet 工作流和内置图片生成制作动画，再进行透明背景处理、尺寸统一和视觉检查。

仓库仅包含完成后的 Q 版素材和本仓库工具；原始照片、生成参考图、聊天记录及私人制作文件不在仓库中。其他宠物仓库的素材和 hatch-pet 的实现代码均未复制进来。

本项目为独立社区作品，与 OpenAI 无隶属关系。

## 许可证

本仓库的素材、文档和工具按 [MIT License](LICENSE) 发布。再分发时请保留版权和许可证声明。
