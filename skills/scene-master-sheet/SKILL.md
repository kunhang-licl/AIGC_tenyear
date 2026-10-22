---
name: scene-master-sheet
description: Create a single wide master reference image that locks a scene's spatial layout, fixed props, and light sources, so every shot filmed in that location stays consistent. Use when the user asks for 场景基准图, 场景定妆, 场景母版, scene master, location reference, or environment reference; when a storyboard scene needs an environment baseline before keyframes are generated; or when shots set in one location are drifting - furniture moving, props disappearing, light direction flipping between shots.
---

# Scene Master Sheet (场景基准图)

One scene, one wide master image. Characters have a定妆图; locations need the same anchor. Every shot set in that location derives its environment description from this single image.

## Core rule: one wide establishing image

Generate exactly **one** image per scene: a wide shot showing the full space, its spatial relationships, and its light sources. Do not produce multi-angle sets.

Reasons:

- The master's job is to fix layout, props, and lighting. One well-composed wide shot carries all three.
- Extra angles multiply drift instead of reducing it, since this pipeline carries continuity through text only.
- Individual shots restate the needed corner of the space in their own prompt; they do not need a pre-rendered view of every angle.

No characters in the master image. An empty room reads as a location; a room with a person reads as a scene and biases later shots toward that staging.

## What the master must lock

| Element | Requirement |
|---|---|
| 空间结构 | Room type, approximate area, ceiling height, where walls, doors, and windows sit relative to each other |
| 固定陈设 | Large furniture with stated positions, described as left/right/center/against-the-back-wall |
| 连续性道具 | 3–6 small props that recur across shots and prove the era |
| 光源 | Every practical light source, its position, and its color temperature |
| 年代质感 | Period-correct materials, wear, and clutter level |
| 色彩关系 | The 3–4 colors that dominate the space |

## Workflow

1. **Read the project's scene bible** if one exists. Match its structure: 类型 / 固定结构 / 年代变化 / 连续性道具. If the scene is not in the bible, draft an entry and add it after the user approves the image.
2. **Resolve the era.** A location that appears across multiple years needs the era stated. Generate the master at the earliest era in which it appears, then note what changes later rather than generating a second master.
3. **Write the prompt** using `references/master-prompt-template.md`.
4. **Generate** with `scripts/gen_scene_master.sh`.
5. **Inspect before delivering.** Verify the space reads as one coherent room, props are period-correct, light direction is unambiguous, and no people or text appear.
6. **Save** as `<scene_id>_master.png` in the project's scene asset directory, then record the locked facts in the scene bible so later sessions reuse them.

```bash
bash scripts/gen_scene_master.sh "<full prompt text>" <output-dir>
```

Use `python3`, not `python`.

## Deriving shots from the master

The master is the source of truth; shot prompts quote it rather than reinventing it.

For each shot in the scene, the environment axis should:

- Name the corner of the space the camera sees, using the master's own spatial vocabulary.
- Repeat the light source and direction verbatim from the master.
- Repeat the palette verbatim.
- Mention only the props actually in that framing, selected from the master's prop list.

Never introduce a prop in a shot that does not exist in the master. If a shot needs one, add it to the master record first so later shots stay consistent.

## Text-only continuity warning

This pipeline carries scene identity through words, not through image-to-image conditioning. The master image cannot be fed back into later generations. Therefore:

- Write the master's locked facts into the scene bible as text. That text, not the image, is what actually propagates.
- Expect generated shots to approximate rather than match the master. Treat the master as the art-direction target a human checks against.
- Keep the spatial description short enough to repeat verbatim in every shot prompt. A 200-word environment block will be paraphrased and will drift.

## Common failures

| Symptom | Fix |
|---|---|
| Room reads as a showroom | Add wear and clutter: `墙面略旧`, `桌面有使用痕迹`, `电线外露` |
| Era ambiguous | Replace generic furniture with 3+ dated objects; era comes from props, not captions |
| Light direction unclear | Name one dominant source and say where it is; demote others to `辅助` |
| Space feels flat | State foreground, mid-ground, and what is visible through doors or windows |
| Model adds people | Add `no people, empty room, unoccupied` to the prompt and to negatives |
| Looks like a different class of home | State the social register directly: `普通工薪家庭`, `九十年代末商品房`, not just `公寓` |

## References

- `references/master-prompt-template.md`: prompt skeleton plus a worked example and a scene-bible entry format.
