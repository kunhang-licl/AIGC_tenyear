#!/usr/bin/env python3
"""Write REPAIR.md into a delivery folder.

The guide maps a visible defect to the skill that owns it and the exact command
that fixes it, so a problem noticed long after production does not require
re-deriving the workflow.

Usage:
    make_repair_guide.py --out-dir ep01_delivery --prefix ep01 [--project /path/to/project]
"""
import argparse
import os
from datetime import date

TEMPLATE = """# 返修指引

生成日期：{today}
交付包：`{prefix}`

出问题时先定位**属于哪一层**，再用对应的 skill 修。改错层会白做。

## 快速定位

| 你看到的问题 | 属于哪一层 | 用哪个 skill | 跳到 |
|---|---|---|---|
| 某张首帧的脸不像定妆图 | 单镜偶发漂移 | `shot-prompt-six-axis` | [A](#a-单张脸漂了) |
| 这个角色**每张**都不像 | 人物基准不牢 | `character-quad-sheet` | [B](#b-整个角色都不像) |
| 构图歪了、景别不对、人物位置不对 | 构图轴写得不够死 | `shot-prompt-six-axis` | [C](#c-构图歪了) |
| 同场戏里房间结构变了、道具跑了 | 场景基准没传下去 | `scene-master-sheet` | [D](#d-场景不一致) |
| 同场戏里光线方向或色调跳了 | 光线/色调轴跨镜不一致 | `shot-prompt-six-axis` | [E](#e-光线或色调跳了) |
| 服装、配饰左右手变了 | 主体轴没逐字复用 | `shot-prompt-six-axis` | [F](#f-服装配饰不一致) |
| 画面里出现乱码中文 | 该后期合成却去生成了 | `shot-prompt-six-axis` | [G](#g-出现乱码文字) |
| 手指数量不对、手掌融合 | 缺针对性负面词 | `shot-prompt-six-axis` | [H](#h-手部畸形) |
| 视频生成出来动作不对 | 视频提示词问题 | `shot-prompt-six-axis` | [I](#i-视频动作不对) |
| 整批图风格不统一 | 色调轴未锁定 | `shot-prompt-six-axis` | [J](#j-整批风格不统一) |

---

## A. 单张脸漂了

只有个别镜头不像，其他镜头正常。属于文生图的随机漂移，不用动基准。

1. 打开 `keyframes/manifest.json`，找到该镜的 `prompt`
2. 把主体描述的**前三项特征**（脸型、眼型、鼻梁）提到最前面，关键特征用大写强调
3. 重跑该镜：

```bash
python3 {script_dir}/batch_generate.py shots.json \\
  --out-dir keyframes --prefix {prefix} --only <镜号> --force
```

漂移是这条管道的固有特性（纯文生图，参考图传不进去）。同一镜重试 2–3 次挑最好的一张是正常做法。

## B. 整个角色都不像

该角色**所有**镜头都偏离，说明问题在基准层，不在单镜。

1. 读 `character-quad-sheet`，重新生成该角色的定妆图
2. 把新的特征描述**逐字**写回项目的角色设定文档
3. 用新描述更新 `shots.json` 里**所有**涉及该角色的镜头
4. 批量重跑这些镜头

顺序不能颠倒。先改设定文档，再改提示词，最后出图。

## C. 构图歪了

景别、机位高度、人物位置不对。

读 `shot-prompt-six-axis` 的构图轴规则。最常见的遗漏是**没写机位高度**——只写"中景"而不写平视还是俯拍，模型会随机给。

构图轴必须同时包含：景别 + 机位高度 + 角度 + 人物在画面中的位置 + 画幅比例。

## D. 场景不一致

同一场戏里房间结构变了、家具位置跑了、道具消失了。

**不要**重新生成场景基准图。问题在于基准图的文字没有被逐字复制到每个镜头。

1. 打开项目设定表里该场景的条目
2. 确认条目足够短——超过 200 字会被模型自行概括，然后就开始漂
3. 把固定结构、固定陈设、光源三项**逐字**复制进每个镜头的环境轴
4. 镜头里不得出现基准图里没有的道具。确需新增，先加进设定表条目

场景基准图本身只在空间布局要改时才重出，读 `scene-master-sheet`。

## E. 光线或色调跳了

同场戏内光线方向或色调在镜头间变化。除非剧情发生了时间推移，否则这是穿帮。

光线轴必须跨镜逐字一致，包含：光源 + 方位 + 软硬 + 色温。
色调轴同理：主色关系 + 饱和度 + 对比度 + 质感。

写法参考 `shot-prompt-six-axis/references/axis-checklist.md` 的术语表。

## F. 服装配饰不一致

服装变了，或者手表从左手跑到右手。

- 服装必须单独成块，前缀写明"四格/全场相同"
- 配饰的左右必须**大写**：`LEFT wrist`。小写的 left/right 会被模型忽略
- 主体描述在同一角色的所有镜头间逐字复用，只改年代状态修饰词

## G. 出现乱码文字

画面里出现看不懂的中文字符。

当前模型**无法**渲染可靠的中文。以下内容一律不要让模型生成，改为后期合成：

- 手机屏幕上的消息
- 文件、审批表、合同上的文字
- 工牌、证件上的姓名单位
- 任何需要观众读懂的数字

提示词里只描述物理载体，并明确要求表面留白或不可辨识，负面词加 `no text, no readable characters, blank screen`。

## H. 手部畸形

手指数量不对、手掌融合。手部特写镜头高发。

在该镜负面词里追加：`额外手指、融合手掌、畸形手部、extra fingers, fused hands, malformed hands`。

手部特写本身就是高失败率题材，重试 3–4 次挑一张是常态。

## I. 视频动作不对

首帧图没问题，但生成的视频动作不对。

这是**视频提示词**的问题，不是首帧的问题。查 `video_prompts.md` 里该镜：

- 运镜是否只给了一个？复合运镜（又推又摇）现在的模型失败率很高
- 主体运动是否写了起止状态？只写"走过去"模型不知道从哪到哪
- 动作量是否塞得进时长？8 秒镜头做不完"推镜头 + 坐下 + 一轮对话"
- 视频提示词是否太长？长描述会稀释运动指令

## J. 整批风格不统一

不同镜头之间质感、色彩、胶片感不一致。

色调轴必须在**一场戏内逐字相同**。建议把色调轴写成一个固定字符串，在该场所有镜头间复制粘贴，不要每镜重写。

---

## 重跑命令速查

```bash
# 重跑指定镜头
python3 {script_dir}/batch_generate.py shots.json \\
  --out-dir keyframes --prefix {prefix} --only 03,07,12 --force

# 续跑未完成的（已存在的自动跳过）
python3 {script_dir}/batch_generate.py shots.json \\
  --out-dir keyframes --prefix {prefix}

# 放慢节奏避免限流
python3 {script_dir}/batch_generate.py shots.json \\
  --out-dir keyframes --prefix {prefix} --delay 20
```

## Skill 位置

| Skill | 路径 |
|---|---|
| `character-quad-sheet` | `{skills_root}/character-quad-sheet` |
| `scene-master-sheet` | `{skills_root}/scene-master-sheet` |
| `shot-prompt-six-axis` | `{skills_root}/shot-prompt-six-axis` |
| `episode-pipeline` | `{skills_root}/episode-pipeline` |

## 已知限制

当前生图通道仅支持**文生图**，会静默忽略参考图输入。人物身份完全依靠文字描述维持，跨镜头必然存在一定漂移。

真正的图生图需要 `OPENAI_API_KEY`，走 `imagegen` skill 的 `scripts/image_gen.py edit` 路径。接上之后 A 类和 B 类问题会大幅减少。
"""


def main():
    ap = argparse.ArgumentParser(description="Write REPAIR.md into a delivery folder.")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--prefix", default="ep01")
    ap.add_argument("--skills-root", default=os.path.expanduser("~/.claude/skills"))
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    script_dir = os.path.join(args.skills_root, "episode-pipeline", "scripts")
    text = TEMPLATE.format(
        today=date.today().isoformat(),
        prefix=args.prefix,
        script_dir=script_dir,
        skills_root=args.skills_root,
    )
    path = os.path.join(args.out_dir, "REPAIR.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(path)


if __name__ == "__main__":
    main()
