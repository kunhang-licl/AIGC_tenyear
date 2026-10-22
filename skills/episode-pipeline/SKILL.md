---
name: episode-pipeline
description: Run the full production pipeline for one episode of an AI-generated film or series, from a finished storyboard to a delivery folder containing keyframe images, video prompts, character and scene reference images, a shot index, and a repair guide. Use when the user asks to 跑一集, 出一集的素材, produce an episode, generate all keyframes for an episode, or batch-produce shot assets; also use when assembling a deliverable package to hand to a video-generation platform such as Sora, Kling, Jimeng, Runway, or Veo.
---

# Episode Pipeline (单集生产流水线)

Takes a finished storyboard and produces everything needed to generate video on an external platform.

## Prerequisite

The storyboard must be final: shot ids, durations, shot sizes, action, and dialogue all settled. This pipeline does not write or revise story content. If the storyboard is still changing, stop and finish it first.

## Skills are read, not called

Skills cannot invoke each other. This file is a sequence the agent follows, reading each referenced skill at the step where it is needed:

- `character-quad-sheet` — at step 2, once per new character
- `scene-master-sheet` — at step 2, once per new location
- `shot-prompt-six-axis` — at steps 1 and 3
- `scripts/batch_generate.py` — at step 4

## Steps

### 1. Audit the storyboard

Read `shot-prompt-six-axis` and run its audit mode over the full shot list. Report a table of 镜号 / 问题 / 建议. Fix blocking issues before generating anything, since every defect here multiplies across every shot that follows.

Also flag every element that must be composited in post: on-screen Chinese text, readable documents, ID cards, phone messages, precise numerals.

### 2. Close the asset gap

Count what the episode needs against what already exists:

```bash
grep -oE "^- [^（:：]+" <storyboard> | sed 's/^- //'   # characters
grep -E "^地点：" <storyboard>                          # locations
ls <project>/assets/characters/quad_sheets/            # existing
ls <project>/assets/scenes/
```

For each missing character, read `character-quad-sheet` and produce one baseline sheet. For each missing location, read `scene-master-sheet` and produce one master.

Then write the locked traits back into the project's character bible and scene bible as text. **This is the step most often skipped and it is the one that matters most**: the pipeline carries continuity through words, not through images. Un-recorded traits do not propagate.

Characters appearing only as body parts (hands, a swaddled infant) need no sheet.

### 3. Write shot prompts

Read `shot-prompt-six-axis`. For every shot produce a keyframe prompt and a video prompt, quoting the character bible and scene bible verbatim for subject and environment.

Emit two artifacts:

- `shots.json` — machine input: `[{"shot":"01","prompt":"<keyframe prompt>","note":"<scene, intent>"}]`
- `video_prompts.md` — human-facing: one block per shot with duration, shot size, camera move, subject motion, and timing

### 4. Generate keyframes

```bash
python3 scripts/batch_generate.py shots.json --out-dir <deliverable>/keyframes --prefix ep01
```

Resumable: existing outputs are skipped, so a failed run can simply be rerun. Rate limits are retried with escalating backoff. Failed shots are listed at the end with a ready-to-paste `--only` retry command.

Shots that are pure environment inserts with no people can be cropped from the scene master instead of generated.

### 5. Review every frame

Open each image. Do not deliver unreviewed frames. Check:

- Face matches the character's baseline sheet
- Wardrobe and accessory side match the bible
- Framing matches the stated shot size and camera height
- Lighting direction consistent with other shots in the same scene
- No text rendered where post-compositing was planned
- Hands, fingers, and mirrors are not malformed

Regenerate failures with `--only <ids> --force`. Record which shots were regenerated and why.

### 6. Assemble the deliverable

```
<episode>_delivery/
├── README.md              起点：怎么用这个包
├── keyframes/             首帧图 + manifest.json
├── video_prompts.md       每镜视频提示词
├── shot_index.md          镜号 → 首帧图 → 时长 → 景别 → 运镜 总表
├── reference/
│   ├── characters/        本集人物定妆图
│   └── scenes/            本集场景基准图
└── REPAIR.md              返修指引
```

Generate `REPAIR.md` with `scripts/make_repair_guide.py`. It maps each failure symptom to the skill and command that fixes it, so a problem found weeks later does not require re-deriving the workflow.

## Delivery README

Include: what the package contains, which platform the prompts target, that on-screen text is composited in post, and a pointer to `REPAIR.md`.

## Realistic expectations

- Reviewing is human work. Expect to regenerate roughly 1 shot in 4 on the first pass.
- Faces drift between shots because this pipeline is text-only. The baseline sheet is the target, not a guarantee.
- A 25-shot episode takes roughly 15–25 minutes of generation wall time plus review.
- Rate limits are frequent. The batch script handles them; do not run parallel batches.

## References

- `references/deliverable-spec.md`: file formats for `shots.json`, `shot_index.md`, and `video_prompts.md`.
