# Skills

《潮落之前》AI 影视化制作配套 Codex skills。

| Skill | 职责 |
|---|---|
| `character-quad-sheet` | 生成人物四宫格定妆图（2×2：左上正面特写、右上侧身全身、左下正面全身、右下背面全身），一人一张基准 |
| `scene-master-sheet` | 生成场景全景基准图，一景一张，锁定空间结构、固定道具、光源 |
| `shot-prompt-six-axis` | 按六维（主体/环境/光线/构图/色调/运镜）产出关键帧与视频提示词，并审核分镜 |
| `episode-pipeline` | 单集生产编排：审核分镜 → 补齐资产 → 批量出图 → 组装交付包（含返修指引） |

## 安装

复制到 `~/.claude/skills/` 或 `$CODEX_HOME/skills/` 即可被自动发现。

```bash
cp -r skills/character-quad-sheet ~/.claude/skills/
cp -r skills/scene-master-sheet ~/.claude/skills/
cp -r skills/shot-prompt-six-axis ~/.claude/skills/
cp -r skills/episode-pipeline ~/.claude/skills/
```

## 制作链路

```
剧本 → 分镜脚本 → 人物定妆图 + 场景基准图 → 关键帧图 → 视频
                   character-quad-sheet
                   scene-master-sheet
                                      shot-prompt-six-axis
         └──────────── episode-pipeline 编排全流程 ────────────┘
```

`episode-pipeline` 自带两个脚本：

- `scripts/batch_generate.py` — 批量出图，支持断点续跑、限流退避、失败重试清单
- `scripts/make_repair_guide.py` — 生成 `REPAIR.md` 返修指引，按症状指向对应 skill

## 已知限制

当前使用的 Ducky 网关 `gpt-image-2` 通道**仅支持文生图**，会静默忽略参考图：传入 `images` / `imageUrls` / 多模态 `chatMessage` 均返回 HTTP 200，但参考图不会到达模型（已用男女母版对照实验验证——换成女性参考图，输出仍为男性，构图几乎不变）。

因此人物身份完全依靠文字描述维持，跨镜头存在面部漂移。真正的图生图需要 `OPENAI_API_KEY`，走 `imagegen` skill 的 `scripts/image_gen.py edit` 路径。
