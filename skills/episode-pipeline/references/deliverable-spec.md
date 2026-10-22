# Deliverable file formats

## shots.json

Machine input for `batch_generate.py`. A list, one object per shot.

```json
[
  {
    "shot": "01",
    "prompt": "<complete keyframe prompt: subject, environment, lighting, framing, color>",
    "note": "场景1 镜01 空镜"
  }
]
```

- `shot` becomes the filename: `<prefix>_shot<id>.png`. Keep ids zero-padded and identical to the storyboard.
- `prompt` must be the full keyframe prompt. No camera movement — a still cannot move.
- `note` is copied into `manifest.json` for traceability.

## shot_index.md

The human entry point. One row per shot, linking everything together.

```markdown
| 镜号 | 首帧图 | 时长 | 景别 | 运镜 | 场景 | 备注 |
|---|---|---:|---|---|---|---|
| 00 | `keyframes/ep01_shot00.png` | 4秒 | 中景（闪回） | 固定 | 周父母家客厅 | 字幕：2013年秋 |
| 01 | `keyframes/ep01_shot01.png` | 6秒 | 特写 | 固定 | 周父母家客厅 | 空镜 |
```

Mark post-composite shots in 备注 so nobody expects the model to have rendered the text.

## video_prompts.md

One block per shot, ready to paste into a video platform.

```markdown
### 镜01 | 6秒 | 特写

**首帧**：`keyframes/ep01_shot01.png`

**运镜**：固定机位，不移动。

**主体运动**：无人物。桌面静止，仅环境轻微变化。

**时间控制**：6秒内保持静止，不引入额外动作。

**负面**：人物入画、镜头移动、乱码文字、水印。
```

Keep video prompts short. Long descriptions dilute the motion instruction and the model stops following it.

## manifest.json

Written automatically by `batch_generate.py`. Records the exact prompt used for each generated file, so a later regeneration starts from what actually ran rather than from what was intended.

```json
{
  "01": {
    "file": "ep01_shot01.png",
    "prompt": "<the exact prompt used>",
    "note": "场景1 镜01 空镜",
    "generated_at": "2026-10-22T10:52:36"
  }
}
```

Never hand-edit this file. To change a prompt, edit `shots.json` and rerun with `--only <id> --force`.
