---
name: shot-prompt-six-axis
description: >-
  Write and audit shot prompts for image-to-video production using a six-axis
  structure - subject appearance, environment, lighting, camera framing,
  color/style, and motion. Use when producing or reviewing 分镜 storyboards, 关键帧
  keyframe image prompts, 运镜 camera-movement descriptions, or video-generation
  prompts for platforms like Sora, Kling, Jimeng, Runway, or Veo. Also use when
  auditing existing shot lists for missing visual specification, inconsistent
  lighting or wardrobe continuity, or prompts too vague to
---

# Six-Axis Shot Prompts (分镜六维提示词)

For image-to-video pipelines, the keyframe image carries the look and the video prompt carries the change. Both are written from the same six axes so they stay consistent.

## The six axes

Every shot must specify all six. A missing axis is a defect, not a stylistic choice.

| # | Axis | Must answer | Common failure |
|---|---|---|---|
| 1 | 主体 Subject | Who, exact wardrobe, accessories with body side, physical state, expression | "周启航站着" with no clothing named |
| 2 | 环境 Environment | Place, era, specific props in frame, spatial depth, what is behind the subject | Treating background as scenery instead of a generated image needing its own spec |
| 3 | 光线 Lighting | Source, direction, hardness, color temperature, resulting time-of-day and mood | "光线自然" |
| 4 | 构图 Framing | Shot size, camera height, angle, subject placement, aspect ratio | Shot size named but camera height left undefined |
| 5 | 色调 Color/Style | Palette, saturation, contrast, film or stock reference, era texture | Style drifting between shots in one scene |
| 6 | 运镜 Motion | Camera move AND subject move, with speed and completion within shot duration | Camera move named, subject left static |

## Two prompts per shot

Image-to-video needs two distinct artifacts. Do not merge them.

**Keyframe prompt** — a still. Uses axes 1–5. Written in present-tense static description. No camera movement, because a still cannot move. This generates the first frame.

**Video prompt** — the change. Uses axis 6 plus the minimum of 1–5 needed to hold continuity. Describes only what moves and how far it gets within the shot's duration. Keep it short: long video prompts dilute motion instructions.

## Output format

Produce one block per shot:

```
【镜XX】时长X秒 | 景别

■ 关键帧提示词
主体：...
环境：...
光线：...
构图：...
色调：...

■ 视频提示词
运镜：...
主体运动：...
时间控制：...

■ 负面提示词
...
```

Write prompts in the language the target platform handles best. Chinese platforms (即梦, 可灵) take Chinese well. Sora, Veo, and Runway perform better in English. When unsure, write Chinese and note that an English version is available.

## Writing rules by axis

### 1. Subject
- Name every garment and its color; never write 便装, 常服, or 普通衣服.
- State accessory body side in caps: `LEFT wrist`, `RIGHT hand`.
- Carry fixed character traits verbatim from the project's character bible every time.
- Describe state as observable detail, not adjectives: `袖口有少量油渍` beats `显得辛苦`.

### 2. Environment
- The background is also a generated image. Spec it as deliberately as the subject.
- Name 3–5 concrete props actually visible in frame, not a general vibe.
- State spatial depth: what is immediately behind the subject, what is in the mid-ground, what is visible through windows or doors.
- Anchor the era with period-accurate objects. A 2013 interior is established by a CRT-era flat TV, paper documents, and a plastic thermos, not by a caption.
- Respect project-level environment bans (for example no rural elements in a provincial-capital setting).

### 3. Lighting
- Name the source: window daylight, ceiling fluorescent, warm table lamp, screen glow, street light.
- Name direction and hardness: `侧前方45度柔光`, `顶部硬光`.
- Name color temperature in words: 暖黄, 冷白, 日光中性.
- Keep lighting consistent across all shots in one scene unless time passes in-story. Changing it mid-scene reads as a continuity error.

### 4. Framing
- Shot size: 特写 / 近景 / 中景 / 全景 / 远景.
- Camera height: 平视 / 俯拍 / 仰拍 / 齐腰 / 地面. Always state it; defaulting to eye level silently is a frequent miss.
- Angle: 正面 / 侧面 / 过肩 / 背面.
- Subject placement and aspect ratio. For vertical short-form, keep the subject and key props inside the central safe area.

### 5. Color and style
- Palette as named colors, not moods: `暖黄灯光 + 暗红针织衫 + 米白墙面`.
- Saturation and contrast direction: `低饱和、中对比`.
- Era texture: light film grain, slight halation, soft highlight rolloff.
- Lock one style per scene and repeat it verbatim in every shot of that scene.

### 6. Motion
- Camera: 固定 / 推 / 拉 / 摇 / 移 / 跟拍 / 手持轻微晃动 / FPV穿越.
- Subject: what the body actually does, with a start and an end state.
- Both must complete inside the stated duration. An 8-second shot cannot hold a camera push, a sit-down, and a conversation turn.
- Prefer one camera move per shot. Compound moves fail frequently in current models.
- Emotional beats read better through subject motion than camera motion. Reserve camera moves for shifts in attention.

## Audit mode

When reviewing an existing storyboard or prompt set, check in this order and report findings as a table of 镜号 / 缺失轴 / 具体问题 / 建议补充:

1. **Axis completeness** — any of the six unspecified.
2. **Intra-scene continuity** — wardrobe, accessory side, lighting direction, and palette identical across shots in one scene.
3. **Duration feasibility** — total described action fits the shot length.
4. **Generatability** — anything the model cannot render: on-screen Chinese text, precise numerals, readable documents, brand logos. These must be composited in post; mark them.
5. **Project constraints** — negative-prompt list and era or location bans.
6. **Keyframe/video separation** — camera movement must not appear in keyframe prompts.

Report problems concretely. `镜03缺光线轴` is useful; `提示词不够详细` is not.

## Negative prompts

Carry the project's standing negative list into every shot. Add per-shot negatives for the specific failure that shot invites: hand close-ups invite `额外手指、融合手掌`; mirrors invite `错误镜面`; multi-character shots invite `人物变脸`.

## References

- `references/axis-checklist.md`: per-axis vocabulary tables and a filled example derived from a real storyboard shot.
